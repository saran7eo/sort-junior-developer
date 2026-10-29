import json
from pathlib import Path

from fastapi import APIRouter, Depends
from gliner2 import GLiNER2

from app.citations import favicon_url, find_cited_ids, link_citations
from app.dependencies import get_model
from app.models import Data
from app.redaction import redact_pii

router = APIRouter(tags=["data"])

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "mock.json"


def prepare_item(item: Data, model: GLiNER2) -> Data:
	"""Redact the question, link the citations and enrich the sources."""
	cited_ids = find_cited_ids(item.content)
	sources = [
		source.model_copy(
			update={
				"favicon": favicon_url(source.source),
				"cited": source.id in cited_ids,
			}
		)
		for source in item.sources
	]
	return item.model_copy(
		update={
			"question": redact_pii(item.question, model),
			"content": link_citations(item.content, sources),
			"sources": sources,
		}
	)


@router.get("/data")
def get_data(model: GLiNER2 = Depends(get_model)) -> list[Data]:
	items = json.loads(DATA_FILE.read_text(encoding="utf-8"))
	return [prepare_item(Data.model_validate(item), model) for item in items]