import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from web_app.app import create_app
from web_app.models import Script, Board, PromptResult, Shot
from web_app import sample


@pytest.fixture
def context(tmp_path):
    app = create_app(tmp_path)
    with TestClient(app) as client:
        yield app, client


def example(client):
    return client.post('/api/examples').json()


def test_approval_version_and_no_auto_jobs(context):
    app, c = context
    p = example(c)
    root = f'/api/projects/{p["id"]}'
    intent = {'version': p['version'], 'shot_id': p['shots'][0]['id']}
    assert c.post(root+'/jobs', json=intent).status_code == 409
    assert c.post(root+'/approve', json={'version': 1}).status_code == 200
    assert c.get(root+'/jobs').json() == []
    a = c.post(root+'/jobs', json=intent).json()
    b = c.post(root+'/jobs', json=intent).json()
    assert a['id'] == b['id']
    rows = deepcopy(p['shots'])
    rows[0]['action'] = '新的镜头动作'
    changed = c.put(root+'/board', json={'version': 1, 'shots': rows}).json()
    assert changed['approved_version'] is None
    assert changed['version'] == 2
    assert c.post(root+'/jobs', json=intent).status_code == 409
    assert c.post(root+'/approve', json={'version': 1}).status_code == 409
    assert len(c.get(root+'/jobs').json()) == 1
    assert len(c.get(root+'/versions').json()) == 2


def test_failure_retry_idempotent_and_persistence(context):
    app, c = context
    p = example(c)
    root = f'/api/projects/{p["id"]}'
    c.post(root+'/approve', json={'version': 1})
    j = c.post(root+'/jobs', json={'version': 1, 'shot_id': p['shots'][0]['id'], 'simulate_failure': True}).json()
    with app.state.store.connect() as db:
        db.execute('UPDATE jobs SET created=created-10 WHERE id=?', (j['id'],))
    assert c.get(root+'/jobs').json()[0]['status'] == 'failed'
    first = c.post(root+f'/jobs/{j["id"]}/retry').json()
    second = c.post(root+f'/jobs/{j["id"]}/retry').json()
    assert first['id'] == second['id']
    with app.state.store.connect() as db:
        db.execute('UPDATE jobs SET created=created-10 WHERE id=?', (first['id'],))
    assert c.get(root+'/jobs').json()[0]['status'] == 'succeeded'
    with TestClient(create_app(app.state.store.path.parent)) as restored:
        assert restored.get(root).json()['approved_version'] == 1
        assert len(restored.get(root+'/jobs').json()) == 2


def test_real_pipeline_contract_through_runtime_boundary(context, monkeypatch):
    app, c = context
    calls = []
    async def generate(skill, instruction, payload, schema):
        calls.append(skill)
        if schema is Script:
            return sample.SCRIPT
        if schema is Board:
            return Board(shots=sample.sample_shots())
        if schema is PromptResult:
            return PromptResult(prompts=[{'id': s['id'], 'prompt': '真实接口测试替身，不代表真实模型结果'} for s in payload['shots']])
    monkeypatch.setattr(app.state.runtime, 'generate', generate)
    p = c.post('/api/projects', json={'brief': '一个完全不同的故事'}).json()
    root = f'/api/projects/{p["id"]}'
    script = c.post(root+'/script/generate', json={'version': 1})
    assert script.status_code == 200
    board = c.post(root+'/board/generate', json={'version': 2})
    assert board.status_code == 200
    assert calls == ['mo2-script-write', 'mo2-storyboard', 'mo2-video-prompt']
    assert all(s['id'].startswith('shot-') for s in board.json()['shots'])
    assert len(c.get(root+'/versions').json()) == 3


def test_proposal_is_scoped_and_applied_explicitly(context, monkeypatch):
    app, c = context
    p = example(c)
    root = f'/api/projects/{p["id"]}'
    async def generate(skill, instruction, payload, schema):
        data = deepcopy(payload['shot'])
        data.update(action='迟疑后递出信封', prompt='同步变化后的完整提示词', id='untrusted-id')
        return Shot(**data)
    monkeypatch.setattr(app.state.runtime, 'generate', generate)
    proposal = c.post(root+'/revisions', json={'version': 1, 'shot_id': p['shots'][1]['id'], 'instruction': '只改第2镜'}).json()
    assert c.get(root).json()['shots'] == p['shots']
    changed = c.post(root+'/revisions/apply', json={'version': 1, 'proposal_id': proposal['id']}).json()
    assert changed['shots'][1]['id'] == p['shots'][1]['id']
    assert changed['shots'][1]['action'] == '迟疑后递出信封'
    assert changed['shots'][0] == p['shots'][0]
    assert changed['shots'][2:] == p['shots'][2:]
    assert c.post(root+'/revisions/apply', json={'version': 2, 'proposal_id': proposal['id']}).status_code == 409


def test_bad_output_missing_key_and_validation_preserve_content(context, monkeypatch):
    app, c = context
    p = example(c)
    root = f'/api/projects/{p["id"]}'
    app.state.runtime.key = ''
    response = c.post(root+'/script/generate', json={'version': 1})
    assert response.status_code == 503
    assert c.get(root).json() == p
    async def malformed(*args, **kwargs):
        raise ValueError('invalid JSON')
    monkeypatch.setattr(app.state.runtime, 'generate', malformed)
    assert c.post(root+'/board/generate', json={'version': 1}).status_code == 502
    assert c.get(root).json() == p
    rows = deepcopy(p['shots'])
    rows[0]['source_scene'] = 'made-up'
    assert c.put(root+'/board', json={'version': 1, 'shots': rows}).status_code == 422
    rows = deepcopy(p['shots'])
    rows[0]['duration'] = -5
    assert c.put(root+'/board', json={'version': 1, 'shots': rows}).status_code == 422
    assert c.get(root).json() == p


def test_export_and_reference_validation(context):
    app, c = context
    p = example(c)
    root = f'/api/projects/{p["id"]}'
    assert '镜号' in c.get(root+'/export').text
    assert c.get(root+'/export?format=json').json()['id'] == p['id']
    assert c.post(root+'/references?version=1', files={'file': ('bad.png', b'not an image', 'image/png')}).status_code == 422
    assert c.get(root).json()['version'] == 1


def test_runtime_uses_upstream_gateway_and_skills(context, monkeypatch):
    import asyncio
    from aigc_agent.harness.model.gateway import ModelResponse
    app, c = context
    runtime = app.state.runtime
    runtime.key = 'test-only'
    received = {}
    async def chat(role, messages, **kwargs):
        received.update(role=role, messages=messages, kwargs=kwargs)
        return ModelResponse(text=sample.SCRIPT.model_dump_json())
    monkeypatch.setattr(runtime.gateway, 'chat', chat)
    result = asyncio.run(runtime.generate('mo2-script-write', '测试', {'brief':'测试故事'}, Script))
    assert result.title == '雨夜来信'
    assert 'fdb7b7c' in received['messages'][0]['content']
    assert received['kwargs']['response_format'] == 'json'
    assert received['kwargs']['extra_body']['thinking']['type'] == 'disabled'
