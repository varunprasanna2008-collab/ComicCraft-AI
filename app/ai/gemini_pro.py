from typing import Dict, List

from app.config import (
    GEMINI_API_KEY,
    GEMINI_STORY_MODEL,
)
from app.utils.json_utils import extract_json


def _fallback_story(
    outline: List[Dict],
    character_name: str,
    tone: str,
) -> List[Dict]:
    """
    Local story fallback.
    """

    result = []

    for panel in outline:
        number = panel["panel_number"]

        result.append(
            {
                "panel_number": number,
                "caption": (
                    f"The story moves forward in panel {number}."
                ),
                "narration": (
                    f"{character_name} continues the journey, "
                    f"facing the events with courage."
                ),
                "dialogue": (
                    f"{character_name}: "
                    f"We have to keep going!"
                ),
            }
        )

    return result


def generate_story(
    outline: List[Dict],
    character_name: str,
    tone: str,
) -> List[Dict]:
    """
    Expand the panel outline into narration and dialogue.
    """

    if not GEMINI_API_KEY:
        return _fallback_story(
            outline,
            character_name,
            tone,
        )

    try:
        import google.generativeai as genai

        genai.configure(
            api_key=GEMINI_API_KEY
        )

        model = genai.GenerativeModel(
            GEMINI_STORY_MODEL
        )

        prompt = f"""
You are a professional comic book writer.

Main character:
{character_name}

Tone:
{tone}

Panel outline:
{outline}

Create narration and dialogue for every panel.

Return ONLY valid JSON.

Return an array where each item contains:

panel_number
caption
narration
dialogue

Do not include Markdown.
Do not include code fences.
"""

        response = model.generate_content(prompt)

        result = extract_json(
            response.text
        )

        if not isinstance(result, list):
            raise ValueError(
                "Gemini story response was not a list."
            )

        story = []

        for panel in outline:
            number = panel["panel_number"]

            matching = next(
                (
                    item
                    for item in result
                    if int(
                        item.get(
                            "panel_number",
                            0,
                        )
                    ) == number
                ),
                {},
            )

            story.append(
                {
                    "panel_number": number,
                    "caption": str(
                        matching.get(
                            "caption",
                            "",
                        )
                    ),
                    "narration": str(
                        matching.get(
                            "narration",
                            "",
                        )
                    ),
                    "dialogue": str(
                        matching.get(
                            "dialogue",
                            "",
                        )
                    ),
                }
            )

        return story

    except Exception:
        return _fallback_story(
            outline,
            character_name,
            tone,
        )