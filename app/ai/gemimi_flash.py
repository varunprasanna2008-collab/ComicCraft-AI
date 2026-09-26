from typing import Dict, List

from app.config import (
    GEMINI_API_KEY,
    GEMINI_OUTLINE_MODEL,
    PANEL_COUNT,
)
from app.utils.json_utils import extract_json


def _fallback_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> List[Dict]:
    """
    Local fallback used when Gemini is not configured.

    This allows the application to be tested
    without an API key.
    """

    return [
        {
            "panel_number": 1,
            "title": "The Beginning",
            "scene_description": (
                f"{character_name} begins the adventure in "
                f"{setting}."
            ),
            "image_prompt": (
                f"{character_name} in {setting}, "
                f"opening scene, {art_style}, "
                f"{tone} mood, cinematic comic panel"
            ),
        },
        {
            "panel_number": 2,
            "title": "A Strange Discovery",
            "scene_description": (
                f"{character_name} discovers something unusual "
                f"that changes the direction of the adventure."
            ),
            "image_prompt": (
                f"{character_name} discovering something mysterious "
                f"in {setting}, {art_style}, comic illustration"
            ),
        },
        {
            "panel_number": 3,
            "title": "The Challenge",
            "scene_description": (
                f"A major challenge appears and "
                f"{character_name} must decide what to do."
            ),
            "image_prompt": (
                f"{character_name} facing a dramatic challenge "
                f"in {setting}, {art_style}, dynamic comic panel"
            ),
        },
        {
            "panel_number": 4,
            "title": "The Turning Point",
            "scene_description": (
                f"{character_name} finds a clever way "
                f"to overcome the challenge."
            ),
            "image_prompt": (
                f"{character_name} overcoming a major challenge "
                f"in {setting}, heroic moment, {art_style}"
            ),
        },
        {
            "panel_number": 5,
            "title": "A New Beginning",
            "scene_description": (
                f"The adventure reaches a satisfying conclusion "
                f"and leaves room for another journey."
            ),
            "image_prompt": (
                f"{character_name} standing proudly in {setting}, "
                f"adventure ending, {art_style}, beautiful comic panel"
            ),
        },
    ]


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> List[Dict]:
    """
    Generate a structured comic outline using Gemini.
    """

    if not GEMINI_API_KEY:
        return _fallback_outline(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style,
        )

    try:
        import google.generativeai as genai

        genai.configure(
            api_key=GEMINI_API_KEY
        )

        model = genai.GenerativeModel(
            GEMINI_OUTLINE_MODEL
        )

        prompt = f"""
You are a professional comic story planner.

Create exactly {PANEL_COUNT} comic panels.

User story:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

Return ONLY valid JSON.

The JSON must be an array.

Each item must have exactly these fields:

panel_number
title
scene_description
image_prompt

Do not include Markdown.
Do not include ```json.
Do not add explanations.

Make the story flow logically from panel 1
to panel {PANEL_COUNT}.
"""

        response = model.generate_content(prompt)

        result = extract_json(
            response.text
        )

        if not isinstance(result, list):
            raise ValueError(
                "Gemini outline response was not a list."
            )

        normalized = []

        for index, panel in enumerate(result[:PANEL_COUNT], 1):
            normalized.append(
                {
                    "panel_number": index,
                    "title": str(
                        panel.get(
                            "title",
                            f"Panel {index}",
                        )
                    ),
                    "scene_description": str(
                        panel.get(
                            "scene_description",
                            "",
                        )
                    ),
                    "image_prompt": str(
                        panel.get(
                            "image_prompt",
                            "",
                        )
                    ),
                }
            )

        while len(normalized) < PANEL_COUNT:
            fallback = _fallback_outline(
                story_prompt,
                character_name,
                setting,
                tone,
                art_style,
            )

            normalized.append(
                fallback[len(normalized)]
            )

        return normalized

    except Exception:
        # Keep application usable even if the Gemini
        # service is temporarily unavailable.
        return _fallback_outline(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style,
        )