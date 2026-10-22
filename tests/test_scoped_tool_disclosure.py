"""子代理按需展开工具：下一次请求刷新定义，展开也受工具作用域限制。"""

from __future__ import annotations

import json
from typing import Any

import pytest

from aigc_agent.capabilities.subagents import SubAgentDef, SubAgentRunner
from aigc_agent.harness.events.bus import EventBus
from aigc_agent.harness.model.gateway import ModelResponse, ToolCall
from aigc_agent.harness.tools.disclosure import DisclosureProvider
from aigc_agent.harness.tools.provider import PermissionLevel, ToolResult, ToolSpec
from aigc_agent.harness.tools.registry import ToolRegistry


class _LookupProvider:
    name = "lookup"
    namespaced = False
    disclosure = "digest"

    def __init__(self) -> None:
        self.calls: list[str] = []
        self.specs = {
            name: ToolSpec(name=name, summary=name, permission=PermissionLevel.READ)
            for name in ("allowed_lookup", "private_lookup")
        }

    async def list_tools(self):
        return [s.meta(self.name) for s in self.specs.values()]

    async def get_schema(self, name):
        return self.specs[name].to_openai(name)

    async def invoke(self, name, args):
        self.calls.append(name)
        return ToolResult(content="lookup result")


class _Gateway:
    def __init__(self, script: list[ModelResponse]) -> None:
        self.script = list(script)
        self.calls: list[dict[str, Any]] = []

    async def chat(self, role, messages, tools=None, **kwargs):
        self.calls.append({
            "messages": messages,
            "tools": {t["function"]["name"] for t in tools or []},
        })
        return self.script.pop(0)


async def _registry():
    bus = EventBus()
    reg = ToolRegistry(bus)
    provider = _LookupProvider()
    reg.register(provider)
    reg.register(DisclosureProvider(reg))
    await reg.refresh()
    return reg, provider, bus


def _expand(names: Any) -> ModelResponse:
    return ModelResponse(tool_calls=[ToolCall(
        id="expand",
        name="load_tool_schema",
        arguments=json.dumps({"names": names}),
    )])


DEF = SubAgentDef(
    name="lookup_agent",
    system_prompt="按需展开工具并查询。",
    tools=["load_tool_schema", "allowed_lookup"],
)


def _assert_private_hidden(gateway: _Gateway) -> None:
    for call in gateway.calls:
        assert "private_lookup" not in call["tools"]
        system = call["messages"][0]["content"]
        assert "private_lookup" not in system


async def test_subagent_receives_expanded_schema_on_next_request():
    reg, provider, bus = await _registry()
    # 父上下文已展开的无权工具也不能进入子代理请求。
    reg.expand("private_lookup")
    gateway = _Gateway([
        _expand(["allowed_lookup"]),
        ModelResponse(tool_calls=[ToolCall(
            id="lookup", name="allowed_lookup", arguments="{}",
        )]),
        ModelResponse(text="done"),
    ])

    result = await SubAgentRunner(gateway, reg, bus).run(DEF, "查询")

    assert result.ok, result.error
    assert gateway.calls[0]["tools"] == {"load_tool_schema"}
    assert gateway.calls[1]["tools"] == {"load_tool_schema", "allowed_lookup"}
    assert provider.calls == ["allowed_lookup"]
    _assert_private_hidden(gateway)


@pytest.mark.parametrize("names", [
    "private_lookup",
    ["private_lookup"],
    ["allowed_lookup", "private_lookup"],
])
async def test_subagent_cannot_expand_tools_outside_its_scope(names):
    reg, provider, bus = await _registry()
    gateway = _Gateway([_expand(names), ModelResponse(text="done")])

    result = await SubAgentRunner(gateway, reg, bus).run(DEF, "查询")

    assert result.ok, result.error
    assert reg.expanded == [], "被拒的元工具调用不能改变父注册表的展开状态"
    assert provider.calls == []
    assert all(c["tools"] == {"load_tool_schema"} for c in gateway.calls)
    tool_messages = [
        m for m in gateway.calls[1]["messages"] if m.get("role") == "tool"
    ]
    assert "无权展开" in tool_messages[-1]["content"]
    _assert_private_hidden(gateway)


async def test_scoped_direct_invoke_also_enforces_expansion_scope():
    reg, _, _ = await _registry()
    scoped = reg.scoped(DEF.tools)

    result = await scoped.invoke("load_tool_schema", {"names": ["private_lookup"]})

    assert not result.ok
    assert "无权展开" in result.error
    assert reg.expanded == []
