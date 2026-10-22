import json
import os
from pathlib import Path
from pydantic import BaseModel
from aigc_agent.capabilities.skill_hub import SkillHub
from aigc_agent.harness.events.bus import EventBus
from aigc_agent.harness.model.config import ModelsConfig, TextConfig, ProviderConfig, RetryConfig
from aigc_agent.harness.model.gateway import ModelGateway
from aigc_agent.domain.storyboard.passport import Character, render_passport
from .prompts import PLATFORM

ROOT = Path(__file__).resolve().parents[1]


class Runtime:
    def __init__(self):
        self.bus = EventBus("mo2-web")
        self.hub = SkillHub(ROOT / "runtime-skills")
        self.hub.load()
        self.model = os.environ.get("DEEPSEEK_MODEL", "deepseek-flash")
        self.key = os.environ.get("DEEPSEEK_API_KEY", "")
        provider = ProviderConfig(
            key="deepseek", vendor="deepseek", base_url="https://api.deepseek.com",
            api_key=self.key, model=self.model, max_output_tokens=12000, stream=False,
            timeout_seconds=120, retry=RetryConfig(max_attempts=2, connect_max_attempts=2),
        )
        self.gateway = ModelGateway(ModelsConfig(text=TextConfig(
            providers={"deepseek": provider}, roles={"main_agent": "deepseek"},
            pricing_estimate=None,
        )), self.bus)

    async def generate(self, skill_name: str, instruction: str, payload: dict, schema: type[BaseModel]):
        if not self.key:
            raise RuntimeError("请在项目 .env 配置 DEEPSEEK_API_KEY 并重启服务；真实生成尚未连接。")
        skill = self.hub.get(skill_name)
        if not skill or not skill.active:
            raise RuntimeError(f"Skill 未启用：{skill_name}")
        # Reuse the original project's character continuity renderer.
        anchors = [render_passport(Character.from_dict(x)) for x in payload.pop("characters", [])]
        system = "\n\n".join([PLATFORM, skill.body, instruction,
            "人物连续性：" + "\n".join(anchors),
            "输出 JSON Schema：" + json.dumps(schema.model_json_schema(), ensure_ascii=False)])
        response = await self.gateway.chat("main_agent", [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ], response_format="json", extra_body={"thinking": {"type": "disabled"}})
        # No partial acceptance: invalid JSON/schema leaves saved results untouched.
        return schema.model_validate_json(response.text)
