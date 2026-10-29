import logging
import re
from html import escape
from urllib.parse import urlparse

from app.models import Source

logger = logging.getLogger(__name__)

# Matches <ref>id</ref>. The capture group makes re.split keep the ids,
# so split results alternate: text, id, text, id, ..., text
REF_PATTERN = re.compile(r"<ref>(.*?)</ref>")

# The only HTML tags from the model's answer that we let through
ALLOWED_TAGS = ("b",)

ALLOWED_URL_SCHEMES = {"http", "https"}
FAVICON_URL = "https://www.google.com/s2/favicons?domain={domain}&sz=64"


def find_cited_ids(content: str) -> set[str]:
	"""Return every source id that the answer cites with <ref>id</ref>."""
	return set(REF_PATTERN.findall(content))


def favicon_url(source_url: str) -> str | None:
	"""Return a favicon image URL for the website of a source, if it has a host."""
	domain = urlparse(source_url).hostname
	if domain is None:
		return None
	return FAVICON_URL.format(domain=domain)


def link_citations(content: str, sources: list[Source]) -> str:
	"""Return the answer as safe HTML with each <ref> replaced by a numbered link.

	The number is the source's position in the sources list, so a link
	matches the numbered list of sources shown below the answer.
	"""
	sources_by_id = {
		source.id: (number, source) for number, source in enumerate(sources, start=1)
	}

	rendered = []
	for index, part in enumerate(REF_PATTERN.split(content)):
		if index % 2 == 0:
			rendered.append(_escape_text(part))
		else:
			link = _render_link(part, sources_by_id)
			if not link and rendered:
				# A dropped citation shouldn't leave a stray space before the punctuation
				rendered[-1] = rendered[-1].rstrip(" ")
			rendered.append(link)
	return "".join(rendered)


def _escape_text(text: str) -> str:
	"""Escape all HTML in the text, then turn the allowed tags back on."""
	escaped = escape(text, quote=False)
	for tag in ALLOWED_TAGS:
		escaped = escaped.replace(f"&lt;{tag}&gt;", f"<{tag}>").replace(
			f"&lt;/{tag}&gt;", f"</{tag}>"
		)
	return escaped


def _render_link(source_id: str, sources_by_id: dict[str, tuple[int, Source]]) -> str:
	"""Return the link for a cited source, or nothing if the id or URL is unusable."""
	if source_id not in sources_by_id:
		logger.warning("Dropping citation with unknown source id: %s", source_id)
		return ""

	number, source = sources_by_id[source_id]
	if urlparse(source.source).scheme not in ALLOWED_URL_SCHEMES:
		logger.warning("Dropping citation with unsafe URL for source: %s", source_id)
		return ""

	href = escape(source.source, quote=True)
	return f'<a href="{href}" target="_blank" rel="noopener noreferrer">[{number}]</a>'