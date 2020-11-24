import json
import copy
from typing import List, Dict, NamedTuple


class Field:
	ordinal: str = None
	req: List = None

	def __init__(self, name: str, media: List[str] = None, **extras):
		self.name = name
		self.media = media if media else []
		self.required_for = required_for if required_for else []
		self.extras = extras
		

class NoteType:
	deck_id: str = None

	note_type_map = {
		'standard': 0,
		'cloze': 1
	}

	def __init__(self, note_type_id, deck_id: str, fields: List[Field] = None, templates: List[Dict] = None, style: str = None, **extras):
		self.note_type_id = note_type_id
		self.deck_id = deck_id		
		self.templates = templates
		self.style = style

		if self._valid_fields(fields):
			self.fields = fields

		if self._valid_extras(extras):
			self.extras = extras

		for i, template in enumerate(self.templates):
			template.ordinal = i

		for i, field in enumerate(self.fields):
			field.ordinal = i

	def __str__(self):
		return json.dumps(self.prepare())

	def _valid_extras(self, extras):
		return True

	def _valid_fields(self, fields):
		template_names = set([template['name'] for template in self.templates])

		for field in fields:
			if field.required_for:
				for template_name in field.required_for:
					if template_name not in template_names:
						raise 'Field is required for a template that does not exist.'

		return True

	def _prepare_req(self):
		""" ...

			This method is heavily inspired from kerrickstanley et al over at genanki since I couldn't think of
			a better solution to implement myself - and if I did it would probably be extremely similar to it...

			See: https://github.com/kerrickstaley/genanki/blob/master/genanki/model.py#L32
		"""
		req = []

		field_names = [field.name for field in fields]
		garbage_value = '_1GarabGE_'

		for template in self.templates:
			field_values = {field: garb for field in field_names}
			required_fields = []

			for field_ordinal, field in enumerate(field_names):
				fv_copy = copy.copy(field_values)
				fv_copy[field] = ''

				rendered = pystache.render(template.question_format, fv_copy)

				if garbage_value not in rendered:
					required_fields.append(field_ordinal)

			if required_fields:
				req.append([template.ordinal, 'all', required_fields])
				continue

		for template in self.templates:
			field_values = {field: garb for field in field_names}
			required_fields = []

			for field_ordinal, field in enumerate(field_names):
				fv_copy = copy.copy(field_values)
				fv_copy[field] = garbage_value

				rendered = pystache.render(template.question_format, fv_copy)

				if garbage_value in rendered:
					required_fields.append(field_ordinal)

			if required_fields:
				req.append([template.ordinal, 'any', required_fields])
		
		return req

	def prepare(self):
		note_type = {
			self.note_type_id: {
				'css': style if style else '',
				'did': self.deck_id,
				'flds': [ {
						'font': fld.extras.get('font_family', ''),
						'media': fld.media,
						'name': fld.name,
						'ord': fld.ordinal,
						'rtl': fld.extras.get('right_to_left_script', False),
						'size': fld.extras.get('font_size', ''),
						'sticky': fld.extras.get('sticky', '')
					} for fld in self.fields ],
				'id': self.note_type_id,
				'latexPre': self.extras.get('latex_pre', ''),
				'latexPost': self.extras.get('latex_post', ''),
				'mod': 0,
				'name': self.name,
				'req': self._prepare_req(),
				'sortf': 0,
				'tags': [],
				'tmpls': [ {
						'afmt': tmpl.answer_format,
						'bafmt': tmpl.extras.get('browser_answer_format', ''),
						'bqfmt': tmpl.extras.get('browser_question_format', ''),
						'did': None,
						'name': tmpl.name,
						'ord': tmpl.ordinal,
						'qfmt': template.question_format
					} for tmpl in self.templates ],
				'type': self.note_type_map[self.extras.get('type', 0)],
				'usn': 0,
				'vers': []
			}
		}
	
	return note_type
