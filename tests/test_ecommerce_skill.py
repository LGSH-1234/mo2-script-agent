"""电商入口、资料按需读取与嵌套技法卡热加载。"""

from pathlib import Path

import pytest

from aigc_agent.capabilities.skill_hub import SkillHub
from aigc_agent.capabilities.skill_hub.functions import SkillFunctions
from aigc_agent.domain.lines import get_line, parse_line

SKILLS = Path(__file__).resolve().parents[1] / "skills"
NAME = "ecommerce-pdp-production"


@pytest.mark.parametrize("user_text", [
    "5", "电商", "ECOMMERCE", "e-commerce", "PDP", "主图", "卖点文案",
    "做抖音商品详情页", "电商图文", "SKU 上新", "产品广告的详情页",
])
def test_ecommerce_routes_by_deliverable(user_text):
    assert parse_line(user_text).key == "ecommerce"
    assert parse_line("抖音短视频").key == "douyin"
    assert parse_line("产品广告").key == "ad"


def test_ecommerce_skill_is_discoverable_only_on_its_line():
    hub = SkillHub(SKILLS)
    hub.load()
    names = {s.name for s in hub.candidates(get_line("ecommerce").content_type)}
    assert NAME in names and "compliance-redlines" in names
    assert not {"drama-script", "douyin-short", "seedance-prompting"} & names
    for line in ("drama", "douyin", "ad", "design"):
        assert NAME not in {s.name for s in hub.candidates(get_line(line).content_type)}


async def test_all_imported_references_can_be_loaded_individually():
    hub = SkillHub(SKILLS)
    hub.load()
    sk = next(s for s in hub.available if s.name == NAME)
    paths = {p.relative_to(SKILLS / NAME / "references").with_suffix("").as_posix()
             for p in (SKILLS / NAME / "references").rglob("*.md")}
    assert {r.name for r in sk.references} == paths
    assert len(paths) == 12
    assert all(r.purpose for r in sk.references)
    fns = SkillFunctions(hub)
    for ref in sk.references:
        result = await fns.invoke("load_skill_reference", {"skill": NAME, "name": ref.name})
        assert result.ok, result.error
        assert ref.read() in result.content
    bad = await fns.invoke("load_skill_reference", {"skill": NAME, "name": "../../README"})
    assert not bad.ok


async def test_nested_reference_names_do_not_collide_and_reload(tmp_path):
    skill_dir = tmp_path / "example"
    refs = skill_dir / "references"
    (refs / "cards").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: example\nstatus: active\n---\nExample", encoding="utf-8"
    )
    (refs / "same.md").write_text("top-level reference", encoding="utf-8")
    nested = refs / "cards" / "same.md"
    nested.write_text("nested reference", encoding="utf-8")
    hub = SkillHub(tmp_path)
    hub.load()
    fns = SkillFunctions(hub)
    top = await fns.invoke("load_skill_reference", {"skill": "example", "name": "same"})
    card = await fns.invoke(
        "load_skill_reference", {"skill": "example", "name": "cards/same.md"}
    )
    assert top.ok and "top-level reference" in top.content
    assert card.ok and "nested reference" in card.content
    nested.write_text("updated nested reference", encoding="utf-8")
    hub.refresh_if_changed()
    updated = await fns.invoke(
        "load_skill_reference", {"skill": "example", "name": "cards/same"}
    )
    assert updated.ok and "updated nested reference" in updated.content
    nested.unlink()
    hub.refresh_if_changed()
    removed = await fns.invoke(
        "load_skill_reference", {"skill": "example", "name": "cards/same"}
    )
    assert not removed.ok
