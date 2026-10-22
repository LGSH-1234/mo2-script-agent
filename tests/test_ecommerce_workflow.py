"""本地电商工具链集成测试：真实存储/排版/导出，不调用模型或网络。"""

from pathlib import Path

from PIL import Image

from aigc_agent.capabilities.skill_hub import SkillHub
from aigc_agent.capabilities.skill_hub.functions import SkillFunctions
from aigc_agent.domain.assets.store import AssetStore, AssetType
from aigc_agent.domain.compliance import ComplianceChecker, ComplianceRules
from aigc_agent.domain.functions.compliance import ComplianceFunctions
from aigc_agent.domain.functions.content import ContentFunctions
from aigc_agent.domain.functions.files import FileFunctions
from aigc_agent.domain.functions.poster import PosterFunctions
from aigc_agent.domain.lines import get_line, line_providers
from aigc_agent.harness.events.bus import EventBus
from aigc_agent.harness.tools.registry import ToolRegistry

ROOT = Path(__file__).resolve().parents[1]


async def test_local_ecommerce_workflow_preserves_versions_and_exports(tmp_path):
    output = tmp_path / "product"
    output.mkdir()
    store = AssetStore(tmp_path / "assets")
    hub = SkillHub(ROOT / "skills")
    hub.load()
    bus = EventBus()
    reg = ToolRegistry(bus)
    reg.register(SkillFunctions(hub))
    reg.register(ContentFunctions(store))
    reg.register(FileFunctions(store, tmp_path / "ws", output_root=output))
    reg.register(PosterFunctions(store))
    rules = ComplianceRules.load(ROOT / "config/compliance.yaml")
    reg.register(ComplianceFunctions(ComplianceChecker(rules), store, bus))
    await reg.refresh()
    reg.set_focus(line_providers(get_line("ecommerce")))

    async def call(tool, **args):
        result = await reg.invoke(tool, args)
        assert result.ok, f"{tool}: {result.error}"
        return result

    await call("load_skill", names=["ecommerce-pdp-production"])
    await call(
        "load_skill_reference", skill="ecommerce-pdp-production",
        name="cards/hero__single-product-hero",
    )

    # 纯色测试夹具仅验证本地图片流转，不冒充商品实拍或模型生图。
    original = output / "fixture.png"
    Image.new("RGB", (800, 800), (40, 70, 65)).save(original)
    original_bytes = original.read_bytes()
    imported = await call("fs_import", path="fixture.png", summary="电商测试底图")
    assert store.get(imported.asset_ref).type is AssetType.IMAGE

    bad_text = "本内容由 AI 生成。\n测试杯：全网最低价，永久耐用。"
    draft = await call(
        "save_draft", content=bad_text, kind="copy", summary="测试杯·第1屏·测试稿",
    )
    blocked = await call(
        "check_compliance", asset_id=draft.asset_ref, media_asset_ids=[imported.asset_ref],
    )
    report = store.get(blocked.asset_ref)
    assert not report.gen_params["passed"]
    assert report.gen_params["counts"]["block"] > 0
    assert store.content(draft.asset_ref) == bad_text, "机审不能悄悄改文案"

    revised_text = "本内容由 AI 生成。\n测试杯：为通勤准备。\n材质与容量待商品资料核验。"
    revised = await call(
        "save_draft", content=revised_text, kind="copy", parent_id=draft.asset_ref,
        summary="测试杯·第1屏·修订稿",
    )
    revision = store.get(revised.asset_ref)
    assert revision.type is AssetType.TEXT
    assert revision.version == 2 and draft.asset_ref in revision.parent_ids
    assert "episode" not in revision.gen_params, "电商屏号不能进入短剧流水线"
    assert store.content(draft.asset_ref) == bad_text
    readback = await call("read_asset", asset_id=revised.asset_ref)
    assert revised_text in readback.content
    checked = await call(
        "check_compliance", asset_id=revised.asset_ref, media_asset_ids=[imported.asset_ref],
    )
    assert store.get(checked.asset_ref).gen_params["passed"]

    poster = await call(
        "make_poster", title="通勤随行", subtitle="本地链路测试，不用于上架",
        template="clean", aspect_ratio="1:1", background_asset_id=imported.asset_ref,
        parent_id=revised.asset_ref, summary="测试杯·第1屏·预览",
    )
    image_asset = store.get(poster.asset_ref)
    assert image_asset.parent_ids == [imported.asset_ref, revised.asset_ref]
    await call("fs_export", asset_id=poster.asset_ref, path="preview.png")
    await call("fs_export", asset_id=revised.asset_ref, path="copy.md")
    assert (output / "copy.md").read_text(encoding="utf-8") == revised_text
    with Image.open(output / "preview.png") as exported:
        assert exported.format == "PNG"
        assert exported.size == (1080, 1080), "固定模板不会自动变成源资料的 800px"
    assert original.read_bytes() == original_bytes
    duplicate = await reg.invoke(
        "fs_export", {"asset_id": poster.asset_ref, "path": "preview.png"}
    )
    assert not duplicate.ok and "已存在" in duplicate.error
