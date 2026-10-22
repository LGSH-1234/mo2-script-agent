import io
import zipfile
import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter
from web_app.app import create_app
from web_app.script_import import extract_text
from web_app.models import Board, PromptResult
from web_app import sample


def docx(text):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as archive:
        archive.writestr('word/document.xml', f'<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>')
    return output.getvalue()


def test_import_preserves_source_and_skips_writer(tmp_path, monkeypatch):
    app = create_app(tmp_path)
    calls = []
    source = '清晨，小雨打开窗户。小雨说：“今天一定会很好。”'
    async def generate(skill, instruction, payload, schema):
        calls.append(skill)
        if schema is Board:
            assert source in payload['script']['scenes'][0]['action']
            assert payload['duration'] == 60 and payload['ratio'] == '9:16'
            assert payload['director_notes'] == '自然光'
            rows = sample.sample_shots()
            for row in rows:
                row.source_scene = 'S1'
            return Board(shots=rows)
        if schema is PromptResult:
            return PromptResult(prompts=[{'id': s['id'], 'prompt': '完整提示词'} for s in payload['shots']])
        pytest.fail('导入流程不应调用脚本编写')
    monkeypatch.setattr(app.state.runtime, 'generate', generate)
    with TestClient(app) as client:
        response = client.post('/api/projects/from-script', data={'duration':'60','ratio':'9:16','notes':'自然光'}, files=[('files', ('example.docx', docx(source)))])
        assert response.status_code == 200, response.text
        p = response.json()
        assert calls == [] and p['shots'] == []
        assert source in p['script']['scenes'][0]['action']
        board = client.post(f'/api/projects/{p["id"]}/board/generate', json={'version':p['version']})
        assert board.status_code == 200, board.text
        assert calls == ['mo2-storyboard', 'mo2-video-prompt']
        assert board.json()['approved_version'] is None
        assert client.get(f'/api/projects/{p["id"]}/jobs').json() == []


def test_invalid_import_does_not_create_project(tmp_path):
    with TestClient(create_app(tmp_path)) as client:
        for name, raw in [('broken.docx',b'broken'),('empty.txt',b' '),('long.txt',b'a'*50001),('bad.pdf',b'bad')]:
            response = client.post('/api/projects/from-script', files=[('files',(name,raw))])
            assert response.status_code == 422, response.text
        assert client.get('/api/projects').json() == []


def test_pdf_and_text_extraction():
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)
    from pypdf.generic import DecodedStreamObject, NameObject, DictionaryObject
    page = writer.pages[0]
    font = DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
    page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
    stream = DecodedStreamObject(); stream.set_data(b'BT /F1 12 Tf 20 200 Td (A woman opens a letter.) Tj ET')
    page[NameObject('/Contents')] = writer._add_object(stream)
    data = io.BytesIO();writer.write(data)
    assert 'opens a letter' in extract_text('script.pdf',data.getvalue())
    assert extract_text('script.txt','开窗'.encode('utf-16')) == '开窗'
    assert 'Hello' in extract_text('script.rtf',b'{\\rtf1 Hello\\par world}')
