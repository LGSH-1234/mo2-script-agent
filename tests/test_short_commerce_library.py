"""来源完整性、领域隔离及大型参考库的按需读取。"""

import hashlib
import json
import re
from pathlib import Path

import pytest

from aigc_agent.capabilities.skill_hub import SkillHub, load_skills
from aigc_agent.capabilities.skill_hub.functions import MAX_REF_CHARS, SkillFunctions
from aigc_agent.domain.lines import get_line

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME = "short-commerce-library"
BUNDLE = SKILLS / NAME


@pytest.fixture
def library():
    hub = SkillHub(SKILLS)
    hub.load()
    skill = next(s for s in hub.available if s.name == NAME)
    return hub, skill, SkillFunctions(hub)


def test_import_matches_full_manifest_and_keeps_source_skills_inactive(library):
    _, skill, _ = library
    manifest = json.loads((BUNDLE / "source-manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_skill_count"] == len(manifest["skills"]) == 80
    assert manifest["source_file_count"] == len(manifest["files"]) == 575
    source = BUNDLE / "references/source"
    actual = {p.relative_to(source).as_posix() for p in source.rglob("*") if p.is_file()}
    assert actual == {f["path"] for f in manifest["files"]}
    for entry in manifest["files"]:
        data = (source / entry["path"]).read_bytes()
        assert len(data) == entry["bytes"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"], entry["path"]
    registered = {s.name for s in load_skills(SKILLS)}
    for original in manifest["skills"]:
        assert original["directory"] not in registered
        assert skill.reference(original["reference"]) is not None
        assert skill.reference(original["guide"]) is not None


def test_guides_point_to_real_readable_sources_and_catalog_is_bounded(library):
    _, skill, _ = library
    assert len(skill.references) == 503
    assert skill.tokens <= 5000
    assert len(skill.reference_index()) < 1500
    for ref in skill.references:
        assert ref.read(), ref.name
        if "/" not in ref.name:
            for path in re.findall(r"`(source/[^`]+)`", ref.read()):
                if path.endswith("/SKILL"):
                    assert skill.reference(path) is not None, (ref.name, path)


@pytest.mark.parametrize("line,expected", [
    ("douyin", True), ("ecommerce", True), ("ad", True),
    ("drama", False), ("design", False),
])
def test_library_only_appears_on_relevant_lines(library, line, expected):
    hub, _, _ = library
    assert (NAME in {s.name for s in hub.candidates(get_line(line).content_type)}) is expected


async def test_list_references_pages_without_duplicates_and_filters_by_directory(library):
    _, skill, fns = library
    seen = []
    offset = 0
    while True:
        result = await fns.invoke(
            "list_skill_references", {"skill": NAME, "offset": offset, "limit": 30}
        )
        assert result.ok, result.error
        page = [line[2:].split("：", 1)[0] for line in result.content.splitlines()
                if line.startswith("- ")]
        seen.extend(page)
        if "下一页" not in result.content:
            break
        offset += len(page)
    assert seen == [r.name for r in skill.references]
    assert len(seen) == len(set(seen))
    directory = "source/generate-ecommerce-hook-videos"
    filtered = await fns.invoke(
        "list_skill_references", {"skill": NAME, "prefix": directory + "/", "limit": 30}
    )
    assert filtered.ok
    listed = [line[2:] for line in filtered.content.splitlines() if line.startswith("- ")]
    assert listed and all(name.startswith(directory + "/") for name in listed)
    query = await fns.invoke(
        "list_skill_references", {"skill": NAME, "prefix": directory, "query": "SEMANTIC"}
    )
    assert query.ok and "semantic-hooks" in query.content
    empty = await fns.invoke("list_skill_references", {"skill": NAME, "prefix": "../../"})
    assert empty.ok and "匹配 0 篇" in empty.content


async def test_source_boundaries_repeat_on_each_page_without_changing_raw_text(library):
    _, skill, fns = library
    name = "source/fashion-ecommerce-creator/SKILL"
    raw = skill.reference(name).read()
    assert len(raw) > MAX_REF_CHARS
    for offset in (0, MAX_REF_CHARS):
        result = await fns.invoke(
            "load_skill_reference", {"skill": NAME, "name": name, "offset": offset}
        )
        assert result.ok and "[来源资料：" in result.content
        assert raw[offset:offset + MAX_REF_CHARS] in result.content
        assert f"offset={offset + MAX_REF_CHARS}" in result.content
        assert len(result.content) <= MAX_REF_CHARS + 1600
    guide = await fns.invoke("load_skill_reference", {"skill": NAME, "name": "hooks-and-copy"})
    assert guide.ok and "[来源资料：" not in guide.content
    missing = await fns.invoke("load_skill_reference", {"skill": NAME, "name": "no-such-file"})
    assert not missing.ok and "list_skill_references" in missing.error
    assert len(missing.error) < 1500


async def test_list_reference_refresh_discovers_added_and_deleted_files(tmp_path):
    directory = tmp_path / "test"
    refs = directory / "references"
    refs.mkdir(parents=True)
    (directory / "SKILL.md").write_text(
        "---\nname: test\nstatus: active\n---\nTest", encoding="utf-8"
    )
    hub = SkillHub(tmp_path)
    hub.load()
    fns = SkillFunctions(hub)
    path = refs / "new.md"
    path.write_text("new reference", encoding="utf-8")
    listed = await fns.invoke("list_skill_references", {"skill": "test"})
    assert listed.ok and "- new" in listed.content
    path.unlink()
    loaded = await fns.invoke("load_skill_reference", {"skill": "test", "name": "new"})
    assert not loaded.ok
