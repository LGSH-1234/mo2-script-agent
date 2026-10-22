"""成功产物也必须匹配当前输入；旧视频重渲需要单独的人确认。"""

from __future__ import annotations

import asyncio
import json

import pytest

from aigc_agent.domain.assets.store import AssetStore
from aigc_agent.harness.events.bus import EventBus

from .test_episode_pipeline import FakeRegistry, _build, _episode, _settle


class LineageRegistry(FakeRegistry):
    """保留真实 drama 工具的血缘和参考图签名，所有调用都在本地模拟。"""

    async def invoke(self, name, args):
        result = await super().invoke(name, args)
        if not result.ok:
            return result
        asset = self.store.get(result.asset_ref)
        if name == "drama_storyboard":
            asset.parent_ids = [args["script_id"]]
        elif name == "drama_assets":
            asset.parent_ids = args["script_ids"]
        elif name == "drama_render_assets":
            asset.parent_ids = [args["assets_id"]]
            asset.inline = json.dumps({"hero": {"asset": "image-original", "url": "old-url"}})
        elif name == "drama_shots":
            asset.parent_ids = [args["storyboard_id"], args["assets_id"]]
        elif name == "drama_render_shots":
            asset.parent_ids = [args["shots_id"], args["rendered_id"]]
            asset.gen_params["complete"] = True
        self.store.put(asset)
        return result


async def _ready(root, registry_class=LineageRegistry):
    store, bus = AssetStore(), EventBus()
    store.project = "test-project"
    registry = registry_class(store)
    pipe = _build(store, bus, registry, root, total=1)
    await _episode(store, 1)
    await _settle(pipe)
    assert registry.count("drama_render_shots") == 1
    return store, registry, pipe


async def test_revised_script_rebuilds_text_and_holds_paid_render(tmp_path):
    store, registry, pipe = await _ready(tmp_path)
    try:
        before = pipe._scan()
        revised = store.revise(before["scripts"][1], "第1集 改稿后的剧本")
        await _settle(pipe)
        current = pipe._scan()
        assert registry.count("drama_storyboard") == 2
        assert store.get(current["storyboards"][1]).parent_ids == [revised.id]
        assert current["shots"][1] != before["shots"][1]
        assert current["rendered"] == {}
        assert registry.count("drama_render_shots") == 1
        assert "旧视频已过期" in pipe.notices() and "重新付费" in pipe.holding

        assert pipe.pass_gate() == "开始重新渲第 1 集"
        await _settle(pipe)
        assert registry.count("drama_render_shots") == 2
        assert set(pipe._scan()["rendered"]) == {1}
    finally:
        await pipe.aclose()


async def test_each_new_storyboard_invalidates_text_and_requires_new_confirmation(tmp_path):
    store, registry, pipe = await _ready(tmp_path)
    try:
        for count in (2, 3):
            view = pipe._scan()
            board = store.get(view["storyboards"][1])
            updated = store.create(
                store.content(board.id), creator=board.creator, parents=board.parent_ids,
                type_=board.type, summary=f"分镜重拆 {count}",
            )
            await _settle(pipe)
            current = pipe._scan()
            assert registry.count("drama_shots") == count
            assert store.get(current["shots"][1]).parent_ids[0] == updated.id
            assert current["rendered"] == {}
            assert registry.count("drama_render_shots") == count - 1
            assert pipe.pass_gate() == "开始重新渲第 1 集"
            await _settle(pipe)
            assert registry.count("drama_render_shots") == count
    finally:
        await pipe.aclose()


async def test_latest_partial_render_protects_reuse_keys_despite_historical_complete(tmp_path):
    store, registry, pipe = await _ready(tmp_path)
    try:
        view = pipe._scan()
        shots = store.get(view["shots"][1])
        second_shots = store.create(
            "[]", creator=shots.creator, parents=shots.parent_ids, gen_params=shots.gen_params,
        )
        store.create(
            "[]", creator="tool:drama_render_shots",
            parents=[second_shots.id, view["refs"]],
            gen_params={"episode": 1, "complete": False, "failed": 1, "count": 39},
        )
        board = store.get(view["storyboards"][1])
        store.create(
            store.content(board.id), creator=board.creator, parents=board.parent_ids,
            type_=board.type, summary="又重拆了分镜",
        )
        await _settle(pipe)
        current = pipe._scan()
        assert current["rendered"] == {}
        assert current["completed_latest"] == set()
        assert current["shots"][1] == second_shots.id, "保留 39 段的复用键"
        assert registry.count("drama_shots") == 1
        assert registry.count("drama_render_shots") == 1
        assert any("已经渲过一部分" in note for note in pipe.notes)
    finally:
        await pipe.aclose()


@pytest.mark.parametrize("change", ["shots", "face"])
async def test_changed_paid_output_requires_confirmation_without_initial_gates(tmp_path, change):
    store, registry, pipe = await _ready(tmp_path)
    try:
        assert pipe.gates is False
        view = pipe._scan()
        if change == "shots":
            old = store.get(view["shots"][1])
            store.create(
                "[]", creator=old.creator, parents=old.parent_ids, gen_params=old.gen_params,
            )
        else:
            store.create(
                json.dumps({"hero": {"asset": "image-new-face", "url": "new-url"}}),
                creator="tool:drama_render_assets", parents=[view["assets_lib"]],
            )
        await _settle(pipe)
        assert pipe._scan()["rendered"] == {}
        assert "旧视频已过期" in pipe.holding
        pipe.retry()  # 重试失败环节不等于同意对新输入重付。
        await _settle(pipe)
        assert registry.count("drama_render_shots") == 1
        assert registry.count("drama_shots") == 1
        pipe.pass_gate()
        await _settle(pipe)
        assert registry.count("drama_render_shots") == 2
        assert set(pipe._scan()["rendered"]) == {1}
    finally:
        await pipe.aclose()


async def test_rehosting_same_images_keeps_successful_video(tmp_path):
    store, registry, pipe = await _ready(tmp_path)
    try:
        view = pipe._scan()
        original_render = view["rendered"][1]
        store.create(
            json.dumps({"hero": {"asset": "image-original", "url": "refreshed-url"}}),
            creator="tool:drama_render_assets", parents=[view["refs"]],
        )
        await _settle(pipe)
        assert pipe._scan()["rendered"] == {1: original_render}
        assert registry.count("drama_render_shots") == 1
        assert pipe.holding == ""
    finally:
        await pipe.aclose()


async def test_unknown_old_reference_pack_cannot_prove_video_matches_new_faces(tmp_path):
    store, registry, pipe = await _ready(tmp_path)
    try:
        view = pipe._scan()
        old_render = store.get(view["rendered"][1])
        old_render.parent_ids = [view["shots"][1]]  # 旧版索引漏记参考图包。
        store.put(old_render)
        store.set_status(view["refs"], "void")  # 历史包不再参与当前项目视图。
        store.create(
            json.dumps({"hero": {"asset": "image-new-face", "url": "new-url"}}),
            creator="tool:drama_render_assets", parents=[view["assets_lib"]],
        )
        await _settle(pipe)
        assert pipe._scan()["rendered"] == {}
        assert "参考图已更新" in pipe.holding
        assert registry.count("drama_render_shots") == 1
    finally:
        await pipe.aclose()


async def test_legacy_outputs_without_parents_are_invalidated_when_sources_change(tmp_path):
    store, registry, pipe = await _ready(tmp_path, FakeRegistry)
    try:
        source = pipe._scan()["scripts"][1]
        store.revise(source, "第1集 修订剧本")
        await _settle(pipe)
        assert registry.count("drama_storyboard") == 2
        assert registry.count("drama_shots") == 2
        assert registry.count("drama_render_shots") == 1
        assert pipe._scan()["rendered"] == {}
        assert "旧视频已过期" in pipe.holding
    finally:
        await pipe.aclose()


async def test_restart_cannot_treat_old_video_as_current_or_approve_new_inputs(tmp_path):
    store, registry, pipe = await _ready(tmp_path)
    gates_path = tmp_path / "gates.json"
    pipe.gates_path = gates_path
    view = pipe._scan()
    old_shots = store.get(view["shots"][1])
    store.create(
        "[]", creator=old_shots.creator, parents=old_shots.parent_ids,
        gen_params=old_shots.gen_params,
    )
    await _settle(pipe)
    pipe.pass_gate()
    await _settle(pipe)
    assert registry.count("drama_render_shots") == 2
    await pipe.aclose()

    # 再改一次提示词后重启：上一次重渲的授权只属于当时的输入。
    store.create(
        "[]", creator=old_shots.creator, parents=old_shots.parent_ids,
        gen_params=old_shots.gen_params,
    )
    restarted_registry = LineageRegistry(store)
    restarted = _build(store, EventBus(), restarted_registry, tmp_path, total=1)
    restarted.gates_path = gates_path
    try:
        restarted.kick()
        await _settle(restarted)
        assert restarted._scan()["rendered"] == {}
        assert restarted_registry.count("drama_render_shots") == 0
        assert "旧视频已过期" in restarted.holding
        restarted.pass_gate()
        await _settle(restarted)
        assert restarted_registry.count("drama_render_shots") == 1
    finally:
        await restarted.aclose()


async def test_queued_render_rechecks_inputs_before_submitting(tmp_path):
    store, registry, pipe = await _ready(tmp_path)
    blocker = pipe._render_sem
    try:
        # 占满渲染槽位，模拟两集正在渲、下一次已派发的渲染仍在排队。
        await blocker.acquire()
        await blocker.acquire()
        view = pipe._scan()
        shots = store.get(view["shots"][1])
        first = store.create(
            "[]", creator=shots.creator, parents=shots.parent_ids, gen_params=shots.gen_params,
        )
        await _settle(pipe)
        pipe.pass_gate()
        await asyncio.sleep(0.05)
        assert "render:1" in pipe._inflight
        second = store.create(
            "[]", creator=shots.creator, parents=shots.parent_ids, gen_params=shots.gen_params,
        )
        blocker.release()
        blocker.release()
        await _settle(pipe)
        assert pipe._scan()["shots"][1] == second.id != first.id
        assert registry.count("drama_render_shots") == 1
        assert "旧视频已过期" in pipe.holding
    finally:
        await pipe.aclose()


async def test_queued_render_uses_latest_urls_after_same_image_rehosting(tmp_path):
    store, registry, pipe = await _ready(tmp_path)
    blocker = pipe._render_sem
    try:
        await blocker.acquire()
        await blocker.acquire()
        view = pipe._scan()
        shots = store.get(view["shots"][1])
        store.create(
            "[]", creator=shots.creator, parents=shots.parent_ids, gen_params=shots.gen_params,
        )
        await _settle(pipe)
        pipe.pass_gate()
        await asyncio.sleep(0.05)
        assert "render:1" in pipe._inflight
        refreshed = store.create(
            json.dumps({"hero": {"asset": "image-original", "url": "refreshed-url"}}),
            creator="tool:drama_render_assets", parents=[view["refs"]],
        )
        blocker.release()
        blocker.release()
        await _settle(pipe)
        assert registry.count("drama_render_shots") == 2
        assert registry.args_of("drama_render_shots")[-1]["rendered_id"] == refreshed.id
        assert pipe._scan()["obsolete_renders"] == {}
        assert pipe.holding == ""
    finally:
        await pipe.aclose()
