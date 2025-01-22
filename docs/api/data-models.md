# Data Models

This section provides information about the data models used in the API.

## AuxKnowAnswer

```json
{
  "is_final": "boolean",
  "answer": "string",
  "citations": ["string"]
}
```

## AuxKnowConfig

```json
{
  "auto_model_routing": "boolean",
  "auto_query_restructuring": "boolean",
  "answer_length_in_paragraphs": "integer",
  "lines_per_paragraph": "integer"
}
```

## AuxKnowSession

```json
{
  "session_id": "string",
  "context": [{ "question": "string", "answer": "string" }],
  "auxknow": "AuxKnow",
  "closed": "boolean"
}
```
