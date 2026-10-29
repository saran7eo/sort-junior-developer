from gliner2 import GLiNER2
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig, RecognizerResult

# The labels we ask the model to look for
LABELS = ["full_name", "first_name", "last_name", "email", "phone_number"]

# Several model labels collapse into one Presidio entity type,
# so "Alex Smith", "Alex" and "Smith" all become NAME
LABEL_TO_ENTITY = {
	"full_name": "NAME",
	"first_name": "NAME",
	"last_name": "NAME",
	"email": "EMAIL",
	"phone_number": "PHONE",
}

# What each entity type is replaced with
OPERATORS = {
	entity: OperatorConfig("replace", {"new_value": f"[{entity}]"})
	for entity in set(LABEL_TO_ENTITY.values())
}

anonymizer = AnonymizerEngine()


def redact_pii(text: str, model: GLiNER2) -> str:
	"""Replace names, emails and phone numbers in text with placeholders."""
	result = model.extract_entities(
		text, LABELS, include_spans=True, include_confidence=True
	)

	# The model groups finds by label, so flatten them into one list
	# of Presidio results (entity type + character range + score)
	findings = [
		RecognizerResult(
			entity_type=LABEL_TO_ENTITY[label],
			start=find["start"],
			end=find["end"],
			score=find["confidence"],
		)
		for label, finds in result["entities"].items()
		for find in finds
	]

	# One call with every span at once: offsets refer to the original
	# string, and Presidio merges overlapping spans of the same type
	return anonymizer.anonymize(
		text=text, analyzer_results=findings, operators=OPERATORS
	).text