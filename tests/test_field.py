import pytest
from pancanki.field import Field

def test_create_field_from_dict():
    field_data = {
        'name': 'Test Field',
        'ord': 1,
        'font': 'Arial',
        'size': 20,
        'rtl': False,
        'sticky': True,
        'media': []
    }
    field = Field(create_from=field_data)
    assert field.name == 'Test Field'
    assert field.ordinal == 1
    assert field.font_family == 'Arial'
    assert field.font_size == 20
    assert field.right_to_left_script is False
    assert field.sticky is True
    assert field.media == []

def test_field_str_and_json():
    field = Field(name='Test Field')
    assert str(field) == field.json
    assert 'Test Field' in str(field)
