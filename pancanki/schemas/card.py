from pydantic import BaseModel


class Card(BaseModel):
	id: int
	nid: int
	did: int
	ord: int
	mod: int
	usn: int = 0
	type: int = 0
	queue: int
	due: int
	ivl: int
	factor: int
	reps: int
	lapses: int
	left: int
	odue: int
	odid: int
	flags: int
	data: str = None	

	class Config:
		orm = True