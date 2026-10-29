from pydantic import BaseModel


class Source(BaseModel):
	id: str
	title: str
	source: str
	favicon: str | None = None
	cited: bool = False


class Data(BaseModel):
	category: str
	question: str
	sources: list[Source]
	content: str