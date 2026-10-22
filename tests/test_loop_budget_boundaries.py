"""文本预算在请求前、纯文本完成、续跑和子代理之间保持一致。"""

from __future__ import annotations

import json

import pytest

from aigc_agent.capabilities.memory.session import SessionSnapshot
from aigc_agent.capabilities.subagents import SubAgentDef, SubAgentRunner
from aigc_agent.domain.assets.store import AssetStore
from aigc_agent.domain.functions.content import ContentFunctions
from aigc_agent.harness.context.assembler import ContextAssembler
from aigc_agent.harness.context.window import ShortTermMemory
from aigc_agent.harness.events.bus import EventBus, EventType
from aigc_agent.harness.execution.loop import LoopRuntime, StopReason
from aigc_agent.harness.model.budget import CostGuard
from aigc_agent.harness.model.gateway import ModelResponse, ToolCall, Usage
from aigc_agent.harness.permission.gate import PermissionGate
from aigc_agent.harness.tools.builtin import builtin
from aigc_agent.harness.tools.dispatcher import ToolDispatcher
from aigc_agent.harness.tools.registry import ToolRegistry


class _Gateway:
    def __init__(self, bus, responses):
        self.bus = bus
        self.responses = list(responses)
        self.calls = 0

    async def chat(self, role, messages, tools=None):
        self.calls += 1
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            # 模拟并行任务在当前请求失败期间花掉了剩余额度。
            await self.bus.emit(EventType.COST, modality="text", cost=1.0)
            raise response
        await self.bus.emit(
            EventType.COST, modality="text", cost=response.usage.cost,
            est_cost=response.usage.est_cost,
        )
        return response


def _response(cost=0.4, *, tool=None, estimated=False):
    usage = Usage(cost=None, est_cost=cost) if estimated else Usage(cost=cost)
    calls = [ToolCall(id="call", name=tool, arguments="{}")] if tool else []
    return ModelResponse(text="已完成的回答", tool_calls=calls, usage=usage)


async def _loop(responses, *, guard=None, memory=None, **kwargs):
    bus = EventBus()
    if guard is not None:
        guard.attach(bus)
    registry = ToolRegistry(bus)
    registry.register(builtin)
    registry.register(ContentFunctions(AssetStore()))
    await registry.refresh()
    gateway = _Gateway(bus, responses)
    loop = LoopRuntime(
        gateway=gateway, registry=registry,
        dispatcher=ToolDispatcher(registry, PermissionGate(bus, guard=guard), bus),
        assembler=ContextAssembler(bus), memory=memory or ShortTermMemory(),
        bus=bus, guard=guard, **kwargs,
    )
    return loop, gateway


async def test_text_over_budget_preserves_answer_and_blocks_following_turns():
    loop, gateway = await _loop([_response(1.0)], guard=CostGuard(money_limit=0.5))

    first = await loop.run_turn("回答")
    second = await loop.run_turn("再回答")

    assert first.stop_reason is second.stop_reason is StopReason.BUDGET_EXCEEDED
    assert "已完成的回答" in first.text and "预算护栏" in first.text
    assert first.turn.assistant_text == "已完成的回答"
    assert second.iterations == 0 and gateway.calls == 1
    assert loop.guard.usage.money == 1.0


@pytest.mark.parametrize("limits", [
    {"max_cost": 0.0},
    {"guard": CostGuard(money_limit=0.0)},
    {"guard": CostGuard(call_limits={"text": 0})},
])
async def test_no_model_request_when_budget_is_already_exhausted(limits):
    loop, gateway = await _loop([], **limits)
    result = await loop.run_turn("回答")
    assert result.stop_reason is StopReason.BUDGET_EXCEEDED
    assert result.iterations == gateway.calls == 0


@pytest.mark.parametrize("estimated", [False, True])
async def test_single_text_response_obeys_max_cost(estimated):
    loop, gateway = await _loop([_response(1.0, estimated=estimated)], max_cost=0.5)
    result = await loop.run_turn("回答")
    assert result.stop_reason is StopReason.BUDGET_EXCEEDED
    assert result.turn.text_cost == 1.0 and gateway.calls == 1
    assert ("含估算" in result.text) is estimated
    assert result.cost == (None if estimated else 1.0), "展示仍只汇总本段真实成本"


async def test_real_zero_cost_does_not_fall_back_to_estimate():
    response = ModelResponse(text="免费回答", usage=Usage(cost=0.0, est_cost=1.0))
    loop, _ = await _loop([response], max_cost=0.5)
    result = await loop.run_turn("回答")
    assert result.stop_reason is StopReason.NO_TOOL_CALLS
    assert result.turn.text_cost == 0.0 and not result.turn.text_cost_estimated


async def test_continue_keeps_turn_cost_but_result_cost_is_per_segment():
    loop, gateway = await _loop(
        [_response(tool="now"), _response(tool="now")], max_cost=0.7, max_iterations=1,
    )
    first = await loop.run_turn("查时间")
    assert first.stop_reason is StopReason.MAX_ITERATIONS
    second = await loop.continue_turn(first.turn)
    third = await loop.continue_turn(first.turn)
    assert second.stop_reason is third.stop_reason is StopReason.BUDGET_EXCEEDED
    assert first.cost == second.cost == 0.4 and third.cost is None
    assert second.turn.text_cost == pytest.approx(0.8) and gateway.calls == 2


@pytest.mark.parametrize("restart", [False, True])
async def test_review_resume_keeps_turn_budget_including_snapshot(tmp_path, restart):
    review = _response()
    review.tool_calls = [ToolCall(
        id="review", name="request_review",
        arguments=json.dumps({"asset_ids": [], "question": "继续吗"}),
    )]
    loop, _ = await _loop([review, _response()], max_cost=0.7)
    first = await loop.run_turn("先审核")
    assert first.stop_reason is StopReason.AWAITING_REVIEW

    if restart:
        snapshot = SessionSnapshot(tmp_path, "budget")
        snapshot.save(loop.memory, pending_review=loop.pending_review)
        loaded = SessionSnapshot(tmp_path, "budget")
        memory = ShortTermMemory()
        assert loaded.load_into(memory) == 1
        loop, _ = await _loop([_response()], max_cost=0.7, memory=memory)
        loop.pending_review = loaded.pending_review

    resumed = await loop.resume_turn("adopt")
    assert resumed.stop_reason is StopReason.BUDGET_EXCEEDED
    assert resumed.cost == 0.4 and resumed.turn.text_cost == pytest.approx(0.8)
    assert loop.pending_review is None


def test_old_snapshot_defaults_to_zero_text_cost(tmp_path):
    snapshot = SessionSnapshot(tmp_path, "old")
    snapshot.path.write_text(json.dumps({
        "turns": [{"index": 0, "messages": [{"role": "user", "content": "旧对话"}]}],
    }), encoding="utf-8")
    memory = ShortTermMemory()
    assert snapshot.load_into(memory) == 1
    assert memory.turns[0].text_cost == 0.0
    assert not memory.turns[0].text_cost_estimated


@pytest.mark.parametrize("extra,expected_calls", [(0.2, 0), (2.0, 1)])
async def test_budget_top_up_is_rechecked_before_request(extra, expected_calls):
    asked = []

    async def ask(reason):
        asked.append(reason)
        return extra

    guard = CostGuard(money_limit=0.5)
    guard.record("text", 1.0)
    loop, gateway = await _loop([_response(0.1)], guard=guard, budget_asker=ask)
    result = await loop.run_turn("继续")
    assert len(asked) == 1 and gateway.calls == expected_calls
    assert (result.stop_reason is StopReason.NO_TOOL_CALLS) is bool(expected_calls)


async def test_completed_answer_does_not_ask_for_retroactive_top_up():
    async def ask(reason):
        pytest.fail("已完成的回答无需追问追加，下一次请求前再问")

    loop, _ = await _loop(
        [_response(1.0)], guard=CostGuard(money_limit=0.5), budget_asker=ask,
    )
    result = await loop.run_turn("回答")
    assert result.stop_reason is StopReason.BUDGET_EXCEEDED


async def test_context_retry_rechecks_budget_before_second_request():
    loop, gateway = await _loop(
        [RuntimeError("maximum context length exceeded")], guard=CostGuard(money_limit=0.5),
    )
    result = await loop.run_turn("回答")
    assert gateway.calls == 1 and loop.assembler.shrink
    assert result.stop_reason is StopReason.BUDGET_EXCEEDED


async def test_subagent_single_response_over_max_cost_is_not_success():
    loop, gateway = await _loop([_response(1.0)])
    result = await SubAgentRunner(gateway, loop.registry, loop.bus).run(
        SubAgentDef(name="writer", system_prompt="写作", max_cost=0.5), "写一段",
    )
    assert not result.ok and result.stop_reason == "budget_exceeded"
    assert gateway.calls == 1


async def test_queued_subagents_stop_when_shared_budget_is_exhausted():
    guard = CostGuard(money_limit=0.5)
    loop, gateway = await _loop([_response(1.0)], guard=guard)
    results = await SubAgentRunner(gateway, loop.registry, loop.bus, guard=guard).run_many(
        SubAgentDef(name="writer", system_prompt="写作"), ["一", "二", "三"], concurrency=1,
    )
    assert results.ok == 0 and gateway.calls == 1
    assert all(r.stop_reason == "budget_exceeded" for r in results.results)
