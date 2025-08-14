import pytest
from pancanki.template import Template

def test_create_template_from_dict():
    template_data = {
        'name': 'Test Template',
        'ord': 1,
        'qfmt': '{{Question}}',
        'afmt': '{{Answer}}',
        'did': '123',
        'bafmt': '',
        'bqfmt': ''
    }
    template = Template(create_from=template_data)
    assert template.name == 'Test Template'
    assert template.ordinal == 1
    assert template.question_format == '{{Question}}'
    assert template.answer_format == '{{Answer}}'
    assert template.deck_id == '123'

def test_template_str_and_json():
    template = Template(name='Test Template', question_format='{{Question}}', answer_format='{{Answer}}')
    assert str(template) == template.json
    assert 'Test Template' in str(template)
