import json
import re
from typing import Any


def extract_json(text: str) -> Any:
    """
    Extract JSON from an AI response.

    Supports:
    - Normal JSON
    - ```json ... ```
    - ``` ... ```
    """

    if not text:
        raise ValueError("AI returned an empty response.")

    cleaned = text.strip()

    # Remove Markdown code fences.
    cleaned = re.sub(
        r"^```json\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"^```\s*",
        "",
        cleaned,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try to locate JSON object/array.
    first_array = cleaned.find("[")
    last_array = cleaned.rfind("]")

    if first_array != -1 and last_array != -1:
        candidate = cleaned[first_array:last_array + 1]

        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    first_object = cleaned.find("{")
    last_object = cleaned.rfind("}")

    if first_object != -1 and last_object != -1:
        candidate = cleaned[first_object:last_object + 1]

        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    raise ValueError(
        "Could not extract valid JSON from AI response."
    )