
#!/usr/bin/env python3
"""营销视频 Skill 的轻量结构与契约回归测试。

设计说明（与当前 Bootloader + 瘦身校验器保持一致）：
- **正文位置无关**：核心契约正文在这一轮已从 SKILL.md 逐字切到 `contract-*.md` /
  `references/**`。因此“某条契约是否存在”的检查一律扫描整个 .md 目录树
  （`all_md()`），不再钉死在 SKILL.md，避免正文搬家就误报。
- **只对内核钉死内核该有的东西**：frontmatter、恢复内核、契约指针等
  仍然直接读 SKILL.md。
- **校验器行为按项目内验收实现断言**：`validate_final_prompt.py` /
  `validate_story_script.py` 保留确定性结构、禁止项与自相矛盾，并只对当次用户
  所选 Hook 派生的 `hook_acceptance_contract` 做字面证据、开场时间窗与顺序回看；
  不恢复全局关键词表或其他泛化语义裁决。
  相应地，本文件断言的是中文错误文案子串，而不是已删除的英文错误码。
"""

from __future__ import annotations

import json
import re
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from functools import lru_cache
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent


def load_validator():
    path = SKILL_ROOT / "scripts/validate_creative_contract.py"
    spec = importlib.util.spec_from_file_location("creative_contract_validator", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_prompt_validator():
    path = SKILL_ROOT / "scripts/validate_final_prompt.py"
    spec = importlib.util.spec_from_file_location("final_prompt_validator", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_story_validator():
    path = SKILL_ROOT / "scripts/validate_story_script.py"
    spec = importlib.util.spec_from_file_location("story_script_validator", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_count_chars():
    path = SKILL_ROOT / "scripts/count_chars.py"
    spec = importlib.util.spec_from_file_location("count_chars", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_merge_images():
    path = SKILL_ROOT / "scripts/merge_images_grid.py"
    spec = importlib.util.spec_from_file_location("merge_images_grid", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ModuleNotFoundError:  # 环境缺 Pillow 时跳过该组用例
        return None
    return module


def read(relative_path: str) -> str:
    return (SKILL_ROOT / relative_path).read_text(encoding="utf-8")


def split_screen_hook_contract() -> dict:
    return {
        "selected": True,
        "hook_id": "hook-split-screen",
        "hook_name": "左右分屏对照",
        "selection_source": "user_selected",
        "original_prompt": "开场用左右分屏同时展示使用前后状态",
        "opening_deadline_seconds": 3.0,
        "core_mechanism": "同时分屏建立前后反差",
        "product_binding": "右屏由商品实际动作产生结果",
        "bridge_to_proof": "分屏右侧直接进入商品证明",
        "signature_requirements": [
            {
                "id": "split-composition",
                "source_text": "左右分屏同时展示",
                "kind": "composition",
                "critical": True,
                "opening_required": True,
                "deadline_seconds": 3.0,
                "evidence": {
                    "fields": ["画面描述", "运镜"],
                    "all_of": ["左右分屏"],
                    "any_of": ["同时对照", "同屏对照"],
                },
            }
        ],
        "sequence_policy": "adaptable",
        "ordered_requirement_ids": [],
        "conflict_resolution": {
            "status": "compatible",
            "default_override_applied": False,
            "user_confirmation": "",
        },
    }


def persuasion_quality_fields() -> dict:
    """一份可通过质量门的最小完整样例，供回归测试复用。"""
    return {
        "persuasion_quality_contract": {
            "brief_integrity": {
                "required_elements": [
                    {
                        "requirement": "商品必须在真实任务中使用",
                        "status": "covered",
                        "planned_shot": "shot_2",
                    }
                ],
                "unresolved_conflicts": [],
                "unreadable_critical_assets": [],
                "unsupported_high_risk_claims": [],
            },
            "product_exclusivity": {
                "irreplaceable_product_fact": "当前商品的具体使用动作会直接改变任务状态",
                "fact_source": "用户提供的商品信息与可观察素材",
                "replacement_test_passed": True,
                "story_elements_requiring_rewrite_if_replaced": ["主证明", "结局选择"],
            },
            "proof_chain": {
                "claim": "商品能改变当前任务结果",
                "buyer_doubt": "不确定是否真的有用",
                "baseline_state": "任务受阻",
                "product_action": "对目标区域执行商品专属动作",
                "observable_change": "目标区域状态变化",
                "result_or_task_consequence": "任务得以完成",
                "evidence_basis": "同场景前后状态和动作连续性",
                "observable_result_before_judgment": True,
                "voiceover_only": False,
                "package_text_only": False,
                "unearned_reaction_only": False,
                "fantasy_only": False,
            },
            "functional_durable_goods_guard": {
                "applicable": False,
                "not_applicable_reason": "该回归样例是清洁耗材证明，不以耐用品硬件功能为主要购买理由",
            },
            "emotional_causality": {
                "required": False,
                "not_applicable_reason": "这是任务证明型视频，由任务状态承担回报",
            },
            "novelty_mechanism": {
                "product_specific_mechanism": "当前商品的使用机制直接触发状态变化",
                "noncosmetic_state_change": "受阻任务变为可完成任务",
                "generic_sequence_only": False,
                "surface_swap_only": False,
            },
            "conversion_closure": {
                "required": True,
                "witnessed_evidence": "观众已看到商品动作与结果",
                "choice_reason": "商品解决了本场景的具体问题",
                "action": "点击商品卡",
                "evidence_to_cta_connected": True,
            },
        },
        "quality_acceptance_contract": {
            "requirements": [
                {
                    "id": "proof-action",
                    "role": "product_action",
                    "fields": ["画面描述"],
                    "all_of": ["按压喷头"],
                    "any_of": [],
                    "source_text": "商品实际动作",
                },
                {
                    "id": "proof-result",
                    "role": "observable_result",
                    "fields": ["画面描述"],
                    "all_of": ["污渍脱离"],
                    "any_of": [],
                    "source_text": "可观察结果",
                },
                {
                    "id": "changed-outcome",
                    "role": "changed_outcome",
                    "fields": ["画面描述", "对白·旁白"],
                    "all_of": [],
                    "any_of": ["决定带走"],
                    "source_text": "结果改变选择",
                },
                {
                    "id": "conversion-cta",
                    "role": "cta",
                    "fields": ["对白·旁白"],
                    "all_of": ["点击商品卡"],
                    "any_of": [],
                    "source_text": "明确转化动作",
                },
            ],
            "ordered_requirement_ids": [
                "proof-action",
                "proof-result",
                "changed-outcome",
                "conversion-cta",
            ],
        },
    }


@lru_cache(maxsize=1)
def all_md() -> str:
    """整个 skill 的 .md 正文拼接（跳过 __pycache__ 等无关目录）。

    契约正文可能位于 SKILL.md、contract-*.md 或 references/** 任意文件；
    “这条契约还在不在”应对整个语料库判定，才不会因为正文搬家而误报。
    """
    chunks: list[str] = []
    for markdown in sorted(SKILL_ROOT.rglob("*.md")):
        if "__pycache__" in markdown.parts:
            continue
        chunks.append(markdown.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def assert_all_present(test: unittest.TestCase, corpus: str, phrases) -> None:
    missing = [phrase for phrase in phrases if phrase not in corpus]
    test.assertEqual(missing, [], f"缺失契约正文：{missing}")


class PackageContractTest(unittest.TestCase):
    # ------------------------------------------------------------------ #
    # 内核 / 打包层面（钉死 SKILL.md 本体）
    # ------------------------------------------------------------------ #
    def test_frontmatter_and_name(self):
        content = read("SKILL.md")
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        self.assertIn("name: marketing-video-creator", frontmatter)
        self.assertIn("revision: bootloader-v100-functional-durable-proof-gate", frontmatter)
        self.assertIn("带货、促销、团购", frontmatter)
        self.assertNotIn("commerce-marketing-video-tool-guide", frontmatter)
        self.assertIn("allowed-tools:", frontmatter)
        self.assertNotRegex(frontmatter, r"(?m)^tools:")

    def test_skill_md_body_under_8k(self):
        # 8000 字符上限只计正文（frontmatter 之后），不含 YAML frontmatter；
        # 正文超限会被运行时摘要压成占位、导致中后段规则整体丢失。
        content = read("SKILL.md")
        parts = content.split("---", 2)
        self.assertEqual(len(parts), 3, "SKILL.md 缺少成对的 YAML frontmatter 分隔符")
        frontmatter, body = parts[1], parts[2]
        self.assertLessEqual(
            len(body), 8000,
            f"SKILL.md 正文 {len(body)} 字符已超 8000 上限，请把新增内容外置到 "
            f"contract-*.md / references/，内核只留指针。",
        )
        # 上限约定必须写进 frontmatter metadata，供后续编辑者知情。
        self.assertIn("size_budget", frontmatter)
        self.assertIn("8000", frontmatter)

    def test_skill_md_is_bootloader_kernel(self):
        main = read("SKILL.md")
        # 内核自我声明 + 契约/参考正文靠指针，而不是把正文全塞在内核里
        self.assertIn("恢复与调度内核", main)
        self.assertIn("contract-", main)

    def test_relative_markdown_links_resolve(self):
        missing: list[str] = []
        for markdown in SKILL_ROOT.rglob("*.md"):
            content = markdown.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)#]+\.md)(?:#[^)]+)?\)", content):
                if target.startswith(("http://", "https://", "/")):
                    continue
                resolved = (markdown.parent / target).resolve()
                if not resolved.is_file():
                    missing.append(f"{markdown.relative_to(SKILL_ROOT)} -> {target}")
        self.assertEqual(missing, [])

    # ------------------------------------------------------------------ #
    # 契约正文存在性（位置无关，扫整棵 .md 树）
    # ------------------------------------------------------------------ #
    def test_template_fusion_compiler_is_mandatory(self):
        assert_all_present(
            self,
            all_md(),
            [
                "禁止把用户 Prompt、Hook Prompt、Play Prompt、Style Prompt 依次拼接",
                "融合创意规格",
                "Hook 的最后一个动作必须同时是 Play/证明链的第一个动作",
                "事实与安全 > 用户明确硬约束/锁定文案 > 主证明可成立性",
                "总分低于 15/18",
            ],
        )

    def test_selected_modules_have_observable_coverage(self):
        assert_all_present(
            self,
            all_md(),
            [
                "因果机制",
                "可观察落点",
                "移除该模板后",
                "模块覆盖",
                "不静默换模板或丢模板",
            ],
        )

    def test_scene_topology_contract(self):
        assert_all_present(
            self,
            all_md(),
            [
                "A→B→C→D",
                "information_job",
                "A→B→A",
                "重复职责的换景必须合并",
            ],
        )

    def test_scope_routing_gate_precedes_ideation(self):
        # 创意库已删除;此处只钉死与库无关的交付范围路由与 Seedance 读取时机门。
        assert_all_present(
            self,
            all_md(),
            [
                "script_only / creative_only",
                "不得读取 Seedance 编译指导",
            ],
        )
        # 内部库编号(UUID)不得泄漏在任何正文里
        self.assertNotRegex(
            all_md(),
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        )

    def test_creative_direction_is_behaviorally_enforced(self):
        assert_all_present(
            self,
            all_md(),
            [
                "至少三个候选内容程序",
                "hook_question",
                "proof_answer_shot",
                "validate_creative_contract.py",
                "每条 `痛点或欲望 → 主证明 → Hook` 因果链都绑定当前商品事实",
            ],
        )

    def test_program_lock_and_actual_prompt_scan_are_mandatory(self):
        assert_all_present(
            self,
            all_md(),
            [
                "current_sku_lock",
                "selected_content_program",
                "program_lock",
                "动作密度 ≠ 卖点密度",
                "source_coverage",
                "style_native_adapter",
                "validate_final_prompt.py",
                "直接扫描实际要投喂的文本",
            ],
        )

    def test_scene_revisit_requires_causal_job(self):
        assert_all_present(
            self,
            all_md(),
            [
                "`A→B→A` 也不自动失败",
                "因果回报、主证明或关系改变",
                "仅重复背景、静态定格或“高级感呼应”",
            ],
        )

    def test_duration_speech_and_entity_contracts(self):
        assert_all_present(
            self,
            all_md(),
            [
                "时长—卖点—信息节拍预算",
                "9–15s",
                "douyin_native",
                "5.5–6.5",
                "商品实例与交互连续性合同",
                "shot_entity_ledger",
                "有限技术完整性审查",
            ],
        )
        self.assertNotIn("全片总共 3-5 条", all_md())
        self.assertNotIn("全片核心卖点总数控制在 3-5 条", all_md())

    def test_user_visible_language_boundary(self):
        assert_all_present(
            self,
            all_md(),
            [
                "用户可见语言隔离合同",
                "conversation_language",
                "content_language",
                "所有用户可见链路",
                "工具调用之间的过渡句",
                "不改变工作链路语言",
                "内部结构不得泄漏",
                "commentary/进度链路",
            ],
        )

    def test_first_second_information_contract(self):
        assert_all_present(
            self,
            all_md(),
            [
                "首秒信息可读合同",
                "0.5 秒内必须出现可理解信息",
                "无信息留白最多 0.4 秒",
                "无口播开场必须自证",
                "证明处让声",
                "对白栏为空时",
            ],
        )

    def test_story_script_actual_file_gate_is_mandatory(self):
        assert_all_present(
            self,
            all_md(),
            [
                "validate_story_script.py",
                "实际故事脚本是本步唯一真相源",
                "Hook Scope、Bridge、Body takeover",
                "不得用第 3 步创意合同的自报通过代替实际脚本通过",
            ],
        )

    def test_validators_describe_project_scoped_hook_acceptance(self):
        """产物校验只回看当次 Hook 合同，不恢复全局魔法关键词。"""
        corpus = all_md()
        assert_all_present(
            self,
            corpus,
            [
                "hook_acceptance_contract",
                "原始选择 → 验收合同 → 实际产物",
                "不使用全局关键词表",
                "UI 默认值永远不能静默覆盖用户明选 Hook",
            ],
        )

    def test_market_casting_and_template_leakage_contracts(self):
        assert_all_present(
            self,
            all_md(),
            [
                "泰语-only + TikTok/TikTok Shop",
                "locked_by_user",
                "未锁定的西方人物用于泰国本地广告属于不通过",
            ],
        )
        self.assertNotIn("约 75 BPM，柔和电钢琴主旋律", all_md())

    def test_claims_are_graded_not_blanket_blocked(self):
        assert_all_present(
            self,
            all_md(),
            [
                "证据门不等于功效词禁用门",
                "可直接表达的商品功能与即时物理结果",
                "体验、感受或外观改善",
                "用户明确提供的主张不自动删除",
                "不显示 `[USP] / P00 / 卖点#N` 等内部标签",
            ],
        )

    def test_multi_request_keeps_master_creative(self):
        assert_all_present(
            self,
            all_md(),
            [
                "后续片段只推进状态，不重启注意力债务",
                "商品真相 / 主 USP / 主专项说服机制 / Hook 职责与机制 / Play 机制 / Style 语法",
            ],
        )

    def test_persuasion_quality_gate_is_mandatory(self):
        assert_all_present(
            self,
            all_md(),
            [
                "商品替换测试",
                "前态 → 商品动作 → 可观察变化 → 结果",
                "quality_acceptance_contract",
                "只靠口播",
                "表层换皮",
                "功能型硬件与耐用品专项证明门",
                "外观、配色、透明材质、旋转、悬浮、液态特效、走秀或包装陈列只能承担 Hook",
                "sku_variant_coverage",
            ],
        )

    def test_validator_rejects_functional_durable_goods_without_functional_proof(self):
        validator = load_validator()
        contract = persuasion_quality_fields()
        quality = contract["persuasion_quality_contract"]
        quality["functional_durable_goods_guard"] = {
            "applicable": True,
            "applicability_reason": "无线鼠标依赖功能完成办公任务",
            "appearance_is_only_proof": True,
            "functional_action": "",
            "user_task_result": "",
            "user_benefit": "",
            "user_requested_variant_count": 8,
            "planned_distinct_variant_count": 3,
            "sku_variant_coverage_plan": "",
        }
        errors = validator.validate_contract(contract)
        joined = "\n".join(errors)
        self.assertIn("不能只靠外观", joined)
        self.assertIn("功能动作、用户任务结果和具体利益点", joined)
        self.assertIn("明确要求展示 8 个 SKU/款式", joined)
        self.assertIn("role=functional_action", joined)
        self.assertIn("role=sku_coverage", joined)

    # ------------------------------------------------------------------ #
    # 规划期创意契约校验器（自填 JSON,断言中文错误文案子串）
    # ------------------------------------------------------------------ #
    def test_validator_rejects_observed_failure_modes(self):
        validator = load_validator()
        bad_contract = {
            "current_sku_lock": {"unresolved_conflicts": ["material"]},
            "selected_content_program": "wet_use_loop",
            "program_lock": {
                "selected_content_program": "wrong_loop",
                "source_coverage": {},
                "main_proof_loop": "",
                "minimum_main_proof_seconds": 8,
                "auxiliary_seconds": 2,
                "ending_in_task": False,
            },
            "product_forms": ["short_handle"],
            "hook_claims": ["back_reach"],
            "proof_answer_shot": None,
            "sku_eligibility": False,
            "asset_eligibility": False,
            "eligibility_conflicts": ["hook task does not match current SKU form"],
            "platform": "TikTok Shop",
            "duration_seconds": 15,
            "content_budget": {
                "main_selling_points": 1,
                "supporting_selling_points": 1,
                "auxiliary_information_beats": 2,
                "active_selling_point_ids": ["usp", "support"],
            },
            "product_entity_contract": {
                "instance_budget": 1,
                "multi_instance_authority": "none",
                "immutable_signature": ["short handle", "synthetic soft bristles"],
                "shot_entity_ledger": [
                    {
                        "shot_id": "shot_1",
                        "instance_count": 1,
                        "left_hand_job": "holds the handle",
                        "right_hand_job": "keeps target surface stable",
                        "other_similar_objects": [],
                        "high_risk_interactions": [],
                        "occlusion_ratio": 0.1,
                    }
                ],
            },
            "speech_rhythm_contract": {
                "language": "Thai",
                "profile": "douyin_native",
                "target_rate": 0,
                "max_rate": 0,
                "line_budgets": [],
            },
            "opening_hook_contract": {
                "hook_question": "why is coverage uneven",
                "hook_carrier": "self_evident_visual",
                "first_information_at_seconds": 1.2,
                "viewer_can_name_problem_or_desire_by_seconds": 2.5,
                "spoken_hook": "",
                "on_screen_hook": "",
                "visible_contrast_or_consequence": "",
                "distinctive_sound_and_causal_result": "",
                "unframed_silence_seconds": 2.5,
                "silent_opening_authority": "none",
                "product_answer_at_seconds": 2.5,
            },
            "short_form_execution": {
                "first_event_at_seconds": 1.0,
                "product_in_real_task_at_seconds": 5.0,
                "static_product_intro": True,
                "effective_visual_beats": 4,
                "native_scores": [2, 2, 2, 2, 2, 2, 2, 0],
                "platform_execution_floor_preserved": False,
                "style_native_adapter": "",
                "main_proof_seconds": 2,
                "scene_sequence": ["a", "b", "a"],
            },
            "localization": {
                "target_market": "Thailand",
                "spoken_language": "Thai",
                "cast_localization": "western_generic",
                "character_reference_authority": "agent_generated",
            },
            "adaptive_fusion": {
                "selected_modules": {"hook": True, "play": True, "style": True},
                "module_observable_effects": {"hook": "", "play": "", "style": ""},
                "generic_template_skin_only": True,
            },
            "human_performance": {
                "required": True,
                "emotion_labels_only": True,
            },
            "spectacle_causality": {"required": True},
        }
        errors = "\n".join(validator.validate_contract(bad_contract))
        for fragment in (
            "current_sku_lock 里还有未解决的冲突",
            "selected_content_program 和顶层 selected_content_program 不一致",
            "source_coverage 不完整",
            "缺 main_proof_loop",
            "辅助信息秒数超标",
            "ending_in_task 必须为 true",
            "却没有 proof_answer_shot",
            "sku_eligibility=false",
            "asset_eligibility=false",
            "eligibility_conflicts 非空",
            "adaptive_fusion（融合创意规格）缺少必填状态字段",
            "选用了 Hook",
            "选用了 Play",
            "选用了 Style",
            "只是给通用模板换皮",
            "必须写清因果可观察表演",
            "只写了情绪标签",
            "奇观钩子",
            "开场信息出现太晚",
            "观众读不懂开场问题/欲望",
            "未经授权的开场留白",
            "static_product_intro=true",
            "主证明时长不足",
            "回访了旧场景",
            "泰国本地化选角",
        ):
            self.assertIn(fragment, errors)

    def test_validator_blocks_overloaded_and_unstable_product_contract(self):
        validator = load_validator()
        contract = {
            "current_sku_lock": {"object_state": "physical", "unresolved_conflicts": []},
            "selected_content_program": "single_loop",
            "program_lock": {
                "selected_content_program": "single_loop",
                "source_coverage": {
                    "exact_sku_form": "exact",
                    "duration_fit": "exact",
                    "evidence_basis": "observed",
                },
                "main_proof_loop": "one task",
                "minimum_main_proof_seconds": 7,
                "auxiliary_seconds": 0,
                "ending_in_task": True,
            },
            "proof_answer_shot": "shot_2",
            "sku_eligibility": True,
            "asset_eligibility": True,
            "eligibility_conflicts": [],
            "adaptive_fusion": {
                "product_specific_tension": "problem",
                "opening_event": "event",
                "opening_state": "before",
                "product_causal_action": "action",
                "proof_state": "proof",
                "end_state": "after",
            },
            "platform": "抖音",
            "duration_seconds": 15,
            "content_budget": {
                "main_selling_points": 1,
                "supporting_selling_points": 3,
                "auxiliary_information_beats": 4,
                "active_selling_point_ids": ["a", "b", "c", "d"],
            },
            "product_entity_contract": {
                "instance_budget": 1,
                "multi_instance_authority": "none",
                "immutable_signature": ["wood handle", "oval brush head"],
                "shot_entity_ledger": [
                    {
                        "shot_id": "shot_2",
                        "instance_count": 2,
                        "left_hand_job": "",
                        "right_hand_job": "",
                        "other_similar_objects": ["wood oval"],
                        "high_risk_interactions": ["flip", "occlusion"],
                        "occlusion_ratio": 0.8,
                        "reanchor_after_occlusion": False,
                    }
                ],
            },
            "speech_rhythm_contract": {
                "language": "zh",
                "profile": "douyin_native",
                "target_rate": 7.0,
                "max_rate": 8.0,
                "line_budgets": [{"rate": 8.2}],
            },
            "short_form_execution": {
                "first_event_at_seconds": 0,
                "product_in_real_task_at_seconds": 1,
                "static_product_intro": False,
                "effective_visual_beats": 6,
                "native_scores": [2, 2, 2, 2, 2, 2, 2, 2],
                "platform_execution_floor_preserved": True,
                "style_native_adapter": "phone native",
                "main_proof_seconds": 8,
                "scene_sequence": ["bathroom"],
            },
        }
        errors = "\n".join(validator.validate_contract(contract))
        for fragment in (
            "卖点总数超出时长预算",
            "辅助信息节拍超标",
            "商品实例数（2）超过 instance_budget",
            "多件同款商品却没有 multi_instance_authority 授权",
            "堆叠了多个高风险商品交互",
            "没写左右手分工",
            "含糊的相似物体",
            "遮挡过半",
            "opening_hook_contract",
            "抖音原生中文语速超出范围",
            "口播语速上限超过人类短视频天花板",
            "有台词的语速超过了自己声明的 max_rate 上限",
        ):
            self.assertIn(fragment, errors)

    def test_validator_accepts_closed_native_localized_contract(self):
        validator = load_validator()
        good_contract = {
            "current_sku_lock": {
                "product_form": "short_handle",
                "material": "synthetic_soft",
                "unresolved_conflicts": [],
            },
            "selected_content_program": "wet_use_loop",
            "program_lock": {
                "selected_content_program": "wet_use_loop",
                "source_coverage": {
                    "exact_sku_form": "adjacent",
                    "duration_fit": "compressed",
                    "evidence_basis": "observed_cluster",
                },
                "main_proof_loop": "continuous wet-use coverage",
                "minimum_main_proof_seconds": 8,
                "auxiliary_seconds": 0.8,
                "ending_in_task": True,
            },
            "product_forms": ["short_handle"],
            "hook_claims": ["foam_coverage"],
            "proof_answer_shot": "shot_3",
            "sku_eligibility": True,
            "asset_eligibility": True,
            "eligibility_conflicts": [],
            "platform": "TikTok Shop",
            "duration_seconds": 15,
            "content_budget": {
                "main_selling_points": 1,
                "supporting_selling_points": 1,
                "auxiliary_information_beats": 2,
                "active_selling_point_ids": ["usp", "support"],
            },
            "product_entity_contract": {
                "instance_budget": 1,
                "multi_instance_authority": "none",
                "immutable_signature": ["short handle", "synthetic soft bristles"],
                "shot_entity_ledger": [
                    {
                        "shot_id": "shot_1",
                        "instance_count": 1,
                        "left_hand_job": "holds the handle",
                        "right_hand_job": "keeps target surface stable",
                        "other_similar_objects": [],
                        "high_risk_interactions": [],
                        "occlusion_ratio": 0.1,
                    }
                ],
            },
            "speech_rhythm_contract": {
                "language": "Thai",
                "profile": "douyin_native",
                "target_rate": 0,
                "max_rate": 0,
                "line_budgets": [],
            },
            "opening_hook_contract": {
                "hook_question": "why is coverage uneven",
                "hook_carrier": "self_evident_visual",
                "first_information_at_seconds": 0.0,
                "viewer_can_name_problem_or_desire_by_seconds": 0.7,
                "spoken_hook": "",
                "on_screen_hook": "",
                "visible_contrast_or_consequence": "thin patch beside dense foam",
                "distinctive_sound_and_causal_result": "",
                "unframed_silence_seconds": 0.0,
                "silent_opening_authority": "none",
                "product_answer_at_seconds": 0.0,
            },
            "short_form_execution": {
                "first_event_at_seconds": 0.0,
                "product_in_real_task_at_seconds": 0.0,
                "static_product_intro": False,
                "effective_visual_beats": 7,
                "native_scores": [2, 2, 2, 2, 2, 2, 2, 2],
                "platform_execution_floor_preserved": True,
                "style_native_adapter": "warm real-bathroom phone UGC",
                "main_proof_seconds": 10,
                "scene_sequence": ["bathroom"],
            },
            "localization": {
                "target_market": "Thailand",
                "spoken_language": "Thai",
                "cast_localization": "thai_local",
                "character_reference_authority": "agent_generated",
            },
            "adaptive_fusion": {
                "product_specific_tension": "manual washing does not build enough foam",
                "opening_event": "brush enters wet cleanser and immediately starts working",
                "opening_state": "thin uneven lather",
                "product_causal_action": "same referenced brush works cleanser in tight circles",
                "proof_state": "dense even foam covers the same area",
                "end_state": "task completed with visible coverage",
                "selected_modules": {"hook": False, "play": True, "style": True},
                "module_observable_effects": {
                    "play": "hands-on progression from baseline to coverage",
                    "style": "raw phone macro and product-action sound",
                },
                "style_modulation": "raw, intimate, kinetic, action-sound led",
                "generic_template_skin_only": False,
            },
            **persuasion_quality_fields(),
            "human_performance": {"required": False},
            "spectacle_causality": {"required": False},
        }
        self.assertEqual(validator.validate_contract(good_contract), [])

    def test_validator_accepts_product_hook_play_style_adaptive_human_contract(self):
        validator = load_validator()
        contract = {
            "current_sku_lock": {
                "product_form": "spray",
                "material": "confirmed package",
                "unresolved_conflicts": [],
            },
            "selected_content_program": "intrusion_counteraction",
            "program_lock": {
                "selected_content_program": "intrusion_counteraction",
                "source_coverage": {
                    "exact_sku_form": "exact",
                    "duration_fit": "exact",
                    "evidence_basis": "general_mechanism",
                },
                "main_proof_loop": "intrusion to counteraction to verification",
                "minimum_main_proof_seconds": 7,
                "auxiliary_seconds": 0,
                "ending_in_task": True,
            },
            "product_forms": ["spray"],
            "hook_claims": ["odor_intrusion"],
            "proof_answer_shot": "shot_4",
            "sku_eligibility": True,
            "asset_eligibility": True,
            "eligibility_conflicts": [],
            "platform": "TikTok",
            "duration_seconds": 15,
            "content_budget": {
                "main_selling_points": 1,
                "supporting_selling_points": 0,
                "auxiliary_information_beats": 1,
                "active_selling_point_ids": ["usp"],
            },
            "product_entity_contract": {
                "instance_budget": 1,
                "multi_instance_authority": "none",
                "immutable_signature": ["spray bottle", "confirmed label"],
                "shot_entity_ledger": [
                    {
                        "shot_id": "shot_3",
                        "instance_count": 1,
                        "left_hand_job": "holds bottle body",
                        "right_hand_job": "presses trigger",
                        "other_similar_objects": [],
                        "high_risk_interactions": ["spray"],
                        "occlusion_ratio": 0.1,
                    }
                ],
            },
            "speech_rhythm_contract": {
                "language": "English",
                "profile": "douyin_native",
                "target_rate": 3.7,
                "max_rate": 4.0,
                "line_budgets": [{"line": "opening", "rate": 3.8}],
            },
            "opening_hook_contract": {
                "hook_question": "what is disrupting the task",
                "hook_carrier": "spoken_line",
                "first_information_at_seconds": 0.0,
                "viewer_can_name_problem_or_desire_by_seconds": 0.6,
                "spoken_hook": "What is that smell?",
                "on_screen_hook": "",
                "visible_contrast_or_consequence": "character visibly recoils",
                "distinctive_sound_and_causal_result": "",
                "unframed_silence_seconds": 0.0,
                "silent_opening_authority": "none",
                "product_answer_at_seconds": 2.2,
            },
            "short_form_execution": {
                "first_event_at_seconds": 0.0,
                "product_in_real_task_at_seconds": 2.2,
                "static_product_intro": False,
                "effective_visual_beats": 6,
                "native_scores": [2, 2, 2, 2, 2, 2, 2, 2],
                "platform_execution_floor_preserved": True,
                "style_native_adapter": "heightened phone-real performance",
                "main_proof_seconds": 9,
                "scene_sequence": ["primary_world"],
            },
            "localization": {
                "target_market": "Singapore",
                "spoken_language": "English",
                "cast_localization": "singapore_local",
                "character_reference_authority": "agent_generated",
            },
            "adaptive_fusion": {
                "product_specific_tension": "an unwanted sensory intrusion disrupts a routine",
                "opening_event": "the intrusion visibly enters the character's space",
                "opening_state": "character and environment are disrupted",
                "product_causal_action": "the character counters it with the referenced product",
                "proof_state": "the same task state visibly changes after use",
                "end_state": "the character verifies the change before concluding",
                "selected_modules": {"hook": True, "play": True, "style": True},
                "module_observable_effects": {
                    "hook": "magnifies the product tension as a first-frame event",
                    "play": "turns disruption into counteraction and verification",
                    "style": "sets heightened but phone-real performance and close camera",
                },
                "style_modulation": "phone-real, heightened, kinetic, intimate",
                "generic_template_skin_only": False,
            },
            **persuasion_quality_fields(),
            "hook_acceptance_contract": split_screen_hook_contract(),
            "human_performance": {
                "required": True,
                "trigger_source": "the visible intrusion",
                "observable_response": "eyes narrow, breath pauses, body turns away",
                "action_intent": "regain control of the immediate space",
                "result_response": "checks the changed state, then shoulders release",
                "environment_interaction": "the event visibly disturbs clothing and nearby objects",
                "dialogue_delivery": "short clipped opening, slower verdict after verification",
                "emotion_labels_only": False,
            },
            "spectacle_causality": {
                "required": True,
                "spectacle_mechanism": "extreme environmental contrast",
                "product_relevant_force": "the same intrusion the product addresses",
                "visible_effect_on_character_or_task": "character and task are physically disrupted",
                "counteraction_or_progression": "disruption directly triggers the product action",
                "handoff_to_proof": "the counteraction continues into the proof shot",
            },
        }
        self.assertEqual(validator.validate_contract(contract), [])

    def test_validator_blocks_default_override_of_user_selected_hook(self):
        validator = load_validator()
        acceptance = split_screen_hook_contract()
        acceptance["conflict_resolution"] = {
            "status": "unresolved",
            "default_override_applied": True,
            "user_confirmation": "",
        }
        contract = {
            "adaptive_fusion": {
                "product_specific_tension": "problem",
                "opening_event": "event",
                "opening_state": "before",
                "product_causal_action": "action",
                "proof_state": "proof",
                "end_state": "after",
                "selected_modules": {"hook": True},
                "module_observable_effects": {"hook": "split contrast"},
                "generic_template_skin_only": False,
            },
            "hook_acceptance_contract": acceptance,
        }
        errors = "\n".join(validator.validate_contract(contract))
        self.assertIn("Hook 与完整脚本/默认推荐还有未解决冲突", errors)
        self.assertIn("用户显式选中的 Hook 不能被 UI 默认推荐覆盖", errors)

    # ------------------------------------------------------------------ #
    # 最终 Prompt 校验器（瘦身后:结构 + 禁止项缺席 + 自相矛盾,中文 errors）
    # ------------------------------------------------------------------ #
    def test_final_prompt_validator_rejects_forbidden_terms_and_contradiction(self):
        validator = load_prompt_validator()
        prompt = """
        全片无字幕，不出现任何文字；风格为精致缓慢品牌广告。
        0-2秒：产品静置，出现花字“立即购买”。
        2-5秒：用动物鬃毛工具快速起泡。
        5-9秒：切换干刷并悬挂收纳，口播“绝对不刺激”。
        9-15秒：产品斜放在毛巾上，缓慢推镜。
        """
        contract = {
            "forbidden_sku_terms": ["动物鬃毛"],
            "unsupported_claim_terms": ["绝对不刺激"],
            "forbidden_imports": ["干刷", "悬挂收纳"],
        }
        errors, _warnings = validator.validate_prompt(prompt, contract)
        errors = "\n".join(errors)
        self.assertIn("禁用的 SKU 变体/材质术语「动物鬃毛」", errors)
        self.assertIn("无证据支撑的宣称「绝对不刺激」", errors)
        self.assertIn("被禁止的方案外来元素「干刷」", errors)
        self.assertIn("被禁止的方案外来元素「悬挂收纳」", errors)
        self.assertIn("字幕/画面文字指令自相矛盾", errors)

    def test_final_prompt_validator_requires_parseable_timeline(self):
        validator = load_prompt_validator()
        prompt = "这是一段没有任何时间戳分镜的散文描述，只讲氛围不给节拍。"
        errors, _warnings = validator.validate_prompt(prompt, {})
        self.assertIn("找不到可解析的分镜时间轴", "\n".join(errors))

    def test_final_prompt_validator_accepts_clean_single_loop(self):
        validator = load_prompt_validator()
        prompt = """
        真实浴室手机竖屏，轻微手持。短柄、合成软毛始终不变。
        0-2秒：浴室内刷头已经刷动湿润手臂，泡沫刚形成。
        2-6秒：同一浴室近景继续刷动，看刷面贴合和泡沫展开。
        6-11秒：同一动作换到肩上手机视角，连续覆盖同一片区域。
        11-15秒：仍在刷动中检查覆盖，边用边说自然 CTA。
        """
        contract = {
            "forbidden_sku_terms": ["动物鬃毛"],
            "unsupported_claim_terms": ["绝对不刺激"],
            "forbidden_imports": ["干刷", "悬挂收纳"],
        }
        errors, _warnings = validator.validate_prompt(prompt, contract)
        self.assertEqual(errors, [])

    def test_final_prompt_validator_hook_displaced_is_warning_not_block(self):
        """Hook 证据被挤出开场窗：只提示、不再判 ok:false（语义层降级为 warnings）。"""
        validator = load_prompt_validator()
        prompt = """
        0-4秒：单画面 UGC 中景，人物举起商品介绍。
        4-8秒：左右分屏，同时对照使用前后。
        8-15秒：商品特写与 CTA。
        """
        errors, warnings = validator.validate_prompt(
            prompt, {"hook_acceptance_contract": split_screen_hook_contract()}
        )
        # 不再进 errors，因此结构完好的 Prompt 依旧算通过
        self.assertEqual(errors, [])
        self.assertIn("Hook 验收项 split-composition", "\n".join(warnings))

    def test_final_prompt_validator_accepts_hook_in_opening_window(self):
        validator = load_prompt_validator()
        prompt = """
        0-3秒：左右分屏，同时对照使用前后，右屏商品开始工作。
        3-10秒：右屏扩展为全屏完成证明。
        10-15秒：实际使用中收束 CTA。
        """
        errors, warnings = validator.validate_prompt(
            prompt, {"hook_acceptance_contract": split_screen_hook_contract()}
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    # ------------------------------------------------------------------ #
    # 故事脚本校验器（瘦身后:确定性结构检查,中文 errors）
    # ------------------------------------------------------------------ #
    def test_story_script_validator_rejects_leak_and_extra_sections(self):
        validator = load_story_validator()
        story = """# 故事脚本

Hook Scope：0.0-2.5秒
- Bridge：2.5秒后
- Body takeover：3.2秒后

| 镜号 | 时长 | 画面描述 | 景别 | 光影氛围 | 对白·旁白 | 音效 | 运镜 |
|---|---|---|---|---|---|---|---|
| 1 | 2.5s | 泡沫声和刷毛压入皮肤的微距画面 | 微距 | 暖白 | [旁白]一泵沐浴露，刷起来泡沫唰唰满 | 泡沫声、刷毛声 | 手持微距 |
| 2 | 12.5s | 同一浴室继续完成清洁 | 近景 | 暖白 | [旁白]刷开更均匀 | 刷毛声 | 跟拍 |

**全片 BGM**：前2.5秒留白只留环境音，随后鼓点进入。
"""
        result = validator.validate_story_text(story, {"duration_seconds": 15})
        self.assertFalse(result["ok"])
        joined = "\n".join(result["errors"])
        self.assertIn("多余的、用户不该看到的段落", joined)
        self.assertIn("泄漏了内部工作流标签「Hook Scope」", joined)
        self.assertIn("泄漏了内部工作流标签「Bridge」", joined)
        self.assertIn("泄漏了内部工作流标签「Body takeover」", joined)

    def test_story_script_validator_rejects_duration_mismatch(self):
        validator = load_story_validator()
        story = """# 故事脚本

| 镜号 | 时长 | 画面描述 | 景别 | 光影氛围 | 对白·旁白 | 音效 | 运镜 |
|---|---|---|---|---|---|---|---|
| 1 | 2.5s | 泡沫刷动微距 | 微距 | 暖白 | [旁白]泡沫满满 | 泡沫声 | 手持 |
| 2 | 5s | 同一浴室继续清洁 | 近景 | 暖白 | [旁白]刷得更匀 | 刷毛声 | 跟拍 |

**全片 BGM**：0秒起低音量鼓点铺底。
"""
        result = validator.validate_story_text(story, {"duration_seconds": 15})
        self.assertFalse(result["ok"])
        self.assertIn("总时长对不上", "\n".join(result["errors"]))

    def test_story_script_validator_accepts_clean_frozen_format(self):
        validator = load_story_validator()
        story = """# 故事脚本

| 镜号 | 时长 | 画面描述 | 景别 | 光影氛围 | 对白·旁白 | 音效 | 运镜 |
|---|---|---|---|---|---|---|---|
| 1 | 2.5s | 泡沫声和刷毛压入皮肤的微距画面 | 微距 | 暖白 | [旁白]一泵沐浴露，刷起来泡沫唰唰满 | 泡沫声、刷毛声 | 手持微距 |
| 2 | 12.5s | 同一浴室继续完成清洁 | 近景 | 暖白 | [旁白]刷开更均匀 | 刷毛声 | 跟拍 |

**全片 BGM**：0秒起低音量轻快鼓点铺底，首句旁白时自动压低，刷毛动作落点抬起节拍。
"""
        result = validator.validate_story_text(story, {"duration_seconds": 15})
        self.assertEqual(result["errors"], [])

    def test_story_script_validator_hook_displaced_is_warning_not_block(self):
        """Hook 证据挪出开场窗：只提示、不再阻断 ok（语义层降级为 warnings）。"""
        validator = load_story_validator()
        story = """# 故事脚本

| 镜号 | 时长 | 画面描述 | 景别 | 光影氛围 | 对白·旁白 | 音效 | 运镜 |
|---|---|---|---|---|---|---|---|
| 1 | 4s | 单画面 UGC 中景，人物举起商品介绍 | 中景 | 自然 | 先看这个 | 环境声 | 手持 |
| 2 | 4s | 左右分屏，同时对照使用前后 | 近景 | 明亮 | 对比很明显 | 转场声 | 同屏对照 |
| 3 | 7s | 商品完成证明并在使用中收束 | 特写 | 明亮 | 现在就试试 | 动作声 | 跟拍 |

**全片 BGM**：轻快鼓点。
"""
        result = validator.validate_story_text(
            story,
            {
                "duration_seconds": 15,
                "hook_acceptance_contract": split_screen_hook_contract(),
            },
        )
        # 结构/时长都对，Hook 证据只作提示，因此整体判通过
        self.assertTrue(result["ok"])
        self.assertEqual(result["errors"], [])
        self.assertIn("Hook 验收项 split-composition", "\n".join(result["warnings"]))

    def test_story_script_validator_accepts_hook_in_opening_window(self):
        validator = load_story_validator()
        story = """# 故事脚本

| 镜号 | 时长 | 画面描述 | 景别 | 光影氛围 | 对白·旁白 | 音效 | 运镜 |
|---|---|---|---|---|---|---|---|
| 1 | 3s | 左右分屏，同时对照使用前后 | 近景 | 明亮 | 差别在这里 | 环境声 | 同屏对照 |
| 2 | 12s | 右屏扩展为全屏，商品完成证明并在使用中收束 | 特写 | 明亮 | 现在就试试 | 动作声 | 跟拍 |

**全片 BGM**：轻快鼓点。
"""
        result = validator.validate_story_text(
            story,
            {
                "duration_seconds": 15,
                "hook_acceptance_contract": split_screen_hook_contract(),
            },
        )
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])

    def test_story_script_validator_missing_quality_evidence_is_warning_not_block(self):
        """缺说服质量证据词：只提示、不再判 ok:false，避免 Agent 为迁就词表空转。"""
        validator = load_story_validator()
        story = """# 故事脚本

| 镜号 | 时长 | 画面描述 | 景别 | 光影氛围 | 对白·旁白 | 音效 | 运镜 |
|---|---|---|---|---|---|---|---|
| 1 | 5s | 人物拿起商品展示包装 | 中景 | 明亮 | 这个看起来不错 | 环境声 | 手持 |
| 2 | 5s | 人物对镜微笑 | 近景 | 明亮 | 效果真好 | 转场声 | 推近 |
| 3 | 5s | 商品定格 | 特写 | 明亮 | 点击商品卡 | 提示音 | 定镜 |

**全片 BGM**：轻快鼓点。
"""
        contract = {"duration_seconds": 15, **persuasion_quality_fields()}
        result = validator.validate_story_text(story, contract)
        # 结构/时长都对：缺证据词不再阻断，整体判通过
        self.assertTrue(result["ok"])
        self.assertEqual(result["errors"], [])
        joined = "\n".join(result["warnings"])
        self.assertIn("说服质量验收项 proof-action", joined)
        self.assertIn("说服质量验收项 proof-result", joined)
        self.assertIn("说服质量验收项 changed-outcome", joined)

    def test_story_script_validator_accepts_ordered_quality_evidence(self):
        validator = load_story_validator()
        story = """# 故事脚本

| 镜号 | 时长 | 画面描述 | 景别 | 光影氛围 | 对白·旁白 | 音效 | 运镜 |
|---|---|---|---|---|---|---|---|
| 1 | 4s | 人物对准污渍按压喷头 | 近景 | 自然 | 先看这一处 | 喷头声 | 手持跟拍 |
| 2 | 5s | 同一位置的污渍脱离，露出干净表面 | 特写 | 明亮 | 这才是我要的结果 | 擦拭声 | 微距推近 |
| 3 | 3s | 人物检查结果后决定带走 | 中景 | 温暖 | 我决定带走 | 环境声 | 跟拍 |
| 4 | 3s | 商品与已完成的表面同框 | 特写 | 明亮 | 想解决同样问题，点击商品卡 | 提示音 | 稳定定镜 |

**全片 BGM**：轻快鼓点。
"""
        contract = {"duration_seconds": 15, **persuasion_quality_fields()}
        result = validator.validate_story_text(story, contract)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])
        self.assertEqual(len(result["details"]["quality_requirements_checked"]), 4)

    # ------------------------------------------------------------------ #
    # 语速工具
    # ------------------------------------------------------------------ #
    def test_count_chars_has_douyin_native_profile(self):
        counter = load_count_chars()
        self.assertIn("douyin", counter.SCENES)
        self.assertEqual(counter.RATES["zh"]["douyin"], (5.5, 6.5))
        _, lower, upper, _, _, effective = counter.estimate_speech(
            "这把刷子一打圈泡沫马上起来", "zh", scene="douyin"
        )
        self.assertGreater(effective, 0)
        self.assertLess(lower, upper)


    # ------------------------------------------------------------------ #
    # 线上故障回归：脚本入参易用性（16 个异常 Trace 收敛出的三类根因）
    # ------------------------------------------------------------------ #
    def test_story_contract_accepts_inline_json_and_path(self):
        """真实故障：--contract 传内联 JSON 被当成路径，抛 FileNotFoundError。"""
        validator = load_story_validator()
        self.assertEqual(
            validator._load_contract('{"duration_seconds": 15}'),
            {"duration_seconds": 15},
        )
        self.assertEqual(validator._load_contract(None), {})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "c.json"
            path.write_text('{"duration_seconds": 28}', encoding="utf-8")
            self.assertEqual(
                validator._load_contract(str(path)), {"duration_seconds": 28}
            )
        # 文件不存在：报中文可执行说明，而不是 traceback
        with self.assertRaises(validator.ContractInputError) as ctx:
            validator._load_contract("_internal/not_there.json")
        self.assertIn("不存在", str(ctx.exception))
        self.assertIn("内联 JSON", str(ctx.exception))

    def test_final_prompt_contract_is_optional_and_accepts_inline(self):
        """真实故障：漏传 --contract 吃到 argparse usage、退出码 2。"""
        validator = load_prompt_validator()
        self.assertEqual(validator._load_contract(None), {})
        self.assertEqual(
            validator._load_contract('{"forbidden_sku_terms": ["钢丝球"]}'),
            {"forbidden_sku_terms": ["钢丝球"]},
        )
        # 单个词写成字符串也当作一项
        self.assertEqual(validator._as_list("钢丝球"), ["钢丝球"])
        with self.assertRaises(validator.ContractInputError):
            validator._load_contract("/workspace/.skill_tmp/x/internal-contract.json")
        # --contract 省略时禁止项为空，正确产物仍能过
        prompt = "各个分镜\n0-3秒：近景开箱。\n3-8秒：特写展示。"
        self.assertEqual(validator.validate_prompt(prompt, {}), ([], []))

    def test_final_prompt_cli_runs_without_contract(self):
        """端到端跑 CLI：不传 --contract 应退出 0，并带 note 说明未检查禁止项。"""
        with tempfile.TemporaryDirectory() as tmp:
            prompt = Path(tmp) / "视频生成Prompt.md"
            prompt.write_text("各个分镜\n0-3秒：近景开箱。\n3-8秒：特写展示。",
                              encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SKILL_ROOT / "scripts/validate_final_prompt.py"),
                 str(prompt)],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload["ok"])
            self.assertIn("note", payload)

    def test_merge_images_normalizes_real_world_input_shapes(self):
        """真实故障：顶层数组 / images / path / label 写法导致 AttributeError、tiles 为空。"""
        merge = load_merge_images()
        if merge is None:
            self.skipTest("Pillow 不可用")
        # 形态一：顶层直接是数组 + label
        spec, warns = merge.normalize_spec(
            [{"image": "/a.png", "label": "正面", "desc": "封盖未开启"}], "product-views")
        self.assertEqual(spec["tiles"][0]["image"], "/a.png")
        self.assertEqual(spec["tiles"][0]["view"], "正面")
        self.assertTrue(warns)
        # 形态二：images + path + label + note
        spec, warns = merge.normalize_spec(
            {"mode": "product-views", "cols": 2,
             "images": [{"path": "/b.png", "label": "背面", "note": "条码"}]},
            "product-views")
        self.assertEqual(spec["tiles"][0]["image"], "/b.png")
        self.assertEqual(spec["tiles"][0]["view"], "背面")
        self.assertEqual(spec["tiles"][0]["desc"], "条码")
        # 正式写法不产生任何告警
        spec, warns = merge.normalize_spec(
            {"title": "t", "tiles": [{"view": "正面", "image": "/c.png", "desc": "d"}]},
            "product-views")
        self.assertEqual(warns, [])
        # storyboard 自动补 index
        spec, _ = merge.normalize_spec({"tiles": [{"image": "/d.png"}]}, "storyboard")
        self.assertEqual(spec["tiles"][0]["index"], 1)
        # 真错仍拦：没有格子 / 格内无图片路径
        with self.assertRaises(merge.SpecError):
            merge.normalize_spec({"title": "x"}, "product-views")
        with self.assertRaises(merge.SpecError):
            merge.normalize_spec([{"view": "正面"}], "product-views")

    def test_count_chars_capacity_lookup_without_lines(self):
        """真实故障：只给 --target 想问容量，却吃到 usage + 退出 1。"""
        counter = load_count_chars()
        out = counter.format_capacity("zh", "fast", 20)
        self.assertIn("容量反查", out)
        # 区间与速率表一致：20s * (5.3~6.0) = 106~120 字
        self.assertIn("106~120 字", out)
        proc = subprocess.run(
            [sys.executable, str(SKILL_ROOT / "scripts/count_chars.py"),
             "--scene", "fast", "--lang", "zh", "--target", "20"],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("容量反查", proc.stdout)
        # 反查的稳妥量拿去正向核算，必须确实落在目标内
        _, lower, upper, _, _, _ = counter.estimate_speech("一" * 106, "zh", scene="fast")
        self.assertLessEqual(upper, 20.0 + 1e-6)

    def test_docs_teach_contract_arg_forms(self):
        """文档必须写明两种 --contract 写法与可省略，避免 Agent 再试错或读源码。"""
        schemas = read("references/contract-json-schemas.md")
        for phrase in ("内联 JSON", "相对路径是相对当前工作目录"):
            self.assertIn(phrase, schemas)
        self.assertIn("--contract '{\"duration_seconds\": 15}'", schemas)
        assets = read("references/base/assets-and-execution.md")
        self.assertIn("同义写法做了兼容归一", assets)
        ratio = read("references/base/dialogue-ratio.md")
        self.assertIn("容量反查", ratio)



    def test_hook_auto_search_fallback_is_wired(self):
        """用户完全没带 Hook 时，第 3.0 步须用 pippit_omni_search 检索补齐。

        钉住三件事：工具已在 allowed-tools 声明、只允许传 marketing_hook、
        空返回属正常情形不阻塞；并且搜来的 Hook 必须以 agent_selected 落合同，
        不能冒充 user_selected 而绕过「默认值不得覆盖用户明选 Hook」这道门。
        """
        skill = read("SKILL.md")
        self.assertIn("pippit_omni_search", skill)
        self.assertRegex(skill, r"(?m)^allowed-tools:")

        step3 = read("references/workflow/step-3-hook-style-play.md")
        for phrase in (
            "### 3.0 用户未提供 Hook 时自动搜索补齐（前置）",
            "pippit_omni_search",
            "marketing_hook",
            "只要存在任一形式的 Hook",   # 已有 Hook 时必须跳过，不覆盖用户选择
            "返回为空就直接忽略",         # 空结果不阻塞
            "agent_selected",             # 与 hook_acceptance_contract 衔接
        ):
            self.assertIn(phrase, step3)
        # 搜索补齐不得豁免既有校验门
        self.assertIn("8 项阻塞检查", step3)

        schemas = read("references/contract-json-schemas.md")
        self.assertIn("检索补齐的填 `agent_selected`", schemas)

if __name__ == "__main__":
    unittest.main(verbosity=2)