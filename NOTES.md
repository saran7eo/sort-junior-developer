# Notes

## What I built

- **Backend (`GET /data`)**: redacts the client's details from each question, turns `<ref>` tags in the answer into numbered links, flags which sources are cited, and adds a favicon URL for each source.
- **Frontend**: fetches `/data` on the server and renders each item as a card with the redacted question, the answer with working citation links, and a numbered list of all its sources with favicons.

## Choices I made

**Redaction** (`backend/app/redaction.py`)
- The model looks for `full_name`, `first_name`, `last_name`, `email` and `phone_number` with `include_spans=True`. I kept the default confidence threshold (0.5) because the scores on the mock data were all above 0.99.
- Finds are grouped by label in the model output, so I flatten them into Presidio `RecognizerResult`s. The three name labels map to one `NAME` entity type.
- Everything goes through a single `AnonymizerEngine.anonymize` call. Offsets refer to the original string, so replacing one span at a time would shift the others. Presidio also merges overlapping spans of the same type, so "Sarah Jones", "Sarah" and "Jones" become one `[NAME]`. I checked this on all four mock questions.
- Redaction fails closed: if the model errors, the endpoint returns a 500 and never the raw question.

**Citations** (`backend/app/citations.py`)
- Each `<ref>id</ref>` becomes a link numbered by the source's position in the sources list, so `[2]` in the answer matches `[2]` in the sources list.
- The debt item cites an id (`dOQ-BJgBLViOYD1OzWM`) that doesn't exist in its sources (a character is missing). I drop an unknown citation and log a warning instead of failing the whole response, and I remove the space it would otherwise leave before the punctuation.
- A source counts as cited if its id appears in a `<ref>`. Repeated citations get a link each time.

**Safe HTML**
- The answer text (the `content` field) looks like AI-assistant output and may contain unexpected markup, so I treat it as untrusted input. The backend escapes all HTML except `<b>` and only emits its own `<a>` links, with `rel="noopener noreferrer"` and `target="_blank"`, and only for `http` and `https` URLs. The frontend then renders the string with `dangerouslySetInnerHTML`, which is safe because of that escaping.
- I considered returning structured segments (text, bold, citation) and rendering them in React instead. That's cleaner, but the brief asks for the backend to return the finished content, and it would have taken longer.

**Favicons**
- I use Google's favicon service (`s2/favicons?domain=...`). Only public domain names are sent, never client data. The downside is a dependency on a third-party service.

**Frontend**
- `page.tsx` fetches on the server inside the existing `Suspense` and shows a clear message if the backend is down. `Content.tsx` only renders.
- Uncited sources are shown too, with a "Not cited in the answer" tag, as the brief asks.

## What didn't work / things I noticed

- Loading the model prints a transformers warning about the model type `extractor`. It works fine, so I left it.

## What I'd do next

- Add tests (pytest) for the citation logic and the redaction on the mock data. I only checked these by hand and against the `/docs` page.
- Cache the redaction. It runs the model on every request.
- Return the answer as structured segments instead of HTML.
- Handle a favicon that fails to load.

# Notes

## What I built

- **Backend (`GET /data`)**: redacts the client's details from each question, turns `<ref>` tags in the answer into numbered links, flags which sources are cited, and adds a favicon URL for each source.
- **Frontend**: fetches `/data` on the server and renders each item as a card with the redacted question, the answer with working citation links, and a numbered list of all its sources with favicons.

## Choices I made

**Redaction** (`backend/app/redaction.py`)
- The model looks for `full_name`, `first_name`, `last_name`, `email` and `phone_number` with `include_spans=True`. I kept the default confidence threshold (0.5) because the scores on the mock data were all above 0.99.
- Finds are grouped by label in the model output, so I flatten them into Presidio `RecognizerResult`s. The three name labels map to one `NAME` entity type.
- Everything goes through a single `AnonymizerEngine.anonymize` call. Offsets refer to the original string, so replacing one span at a time would shift the others. Presidio also merges overlapping spans of the same type, so "Sarah Jones", "Sarah" and "Jones" become one `[NAME]`. I checked this on all four mock questions.
- Redaction fails closed: if the model errors, the endpoint returns a 500 and never the raw question.

**Citations** (`backend/app/citations.py`)
- Each `<ref>id</ref>` becomes a link numbered by the source's position in the sources list, so `[2]` in the answer matches `[2]` in the sources list.
- The debt item cites an id (`dOQ-BJgBLViOYD1OzWM`) that doesn't exist in its sources (a character is missing). I drop an unknown citation and log a warning instead of failing the whole response, and I remove the space it would otherwise leave before the punctuation.
- A source counts as cited if its id appears in a `<ref>`. Repeated citations get a link each time.

**Safe HTML**
- The answer text (the `content` field) looks like AI-assistant output and may contain unexpected markup, so I treat it as untrusted input. The backend escapes all HTML except `<b>` and only emits its own `<a>` links, with `rel="noopener noreferrer"` and `target="_blank"`, and only for `http` and `https` URLs. The frontend then renders the string with `dangerouslySetInnerHTML`, which is safe because of that escaping.
- I considered returning structured segments (text, bold, citation) and rendering them in React instead. That's cleaner, but the brief asks for the backend to return the finished content, and it would have taken longer.

**Favicons**
- I use Google's favicon service (`s2/favicons?domain=...`). Only public domain names are sent, never client data. The downside is a dependency on a third-party service.

**Frontend**
- `page.tsx` fetches on the server inside the existing `Suspense` and shows a clear message if the backend is down. `Content.tsx` only renders.
- Uncited sources are shown too, with a "Not cited in the answer" tag, as the brief asks.

## What didn't work / things I noticed

- Loading the model prints a transformers warning about the model type `extractor`. It works fine, so I left it.

## What I'd do next

- Add tests (pytest) for the citation logic and the redaction on the mock data. I only checked these by hand and against the `/docs` page.
- Cache the redaction. It runs the model on every request.
- Return the answer as structured segments instead of HTML.
- Handle a favicon that fails to load.

## AI use

I used Claude (Anthropic) to help plan the approach and to draft the backend and frontend code.