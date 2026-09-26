from typing import Dict, List


def build_comic_layout(
    outline: List[Dict],
    story: List[Dict],
    image_paths: List[str],
) -> List[Dict]:
    """
    Combine outline, story and image paths
    into the final comic layout.
    """

    story_by_panel = {
        item["panel_number"]: item
        for item in story
    }

    layout = []

    for index, panel in enumerate(outline):
        number = panel["panel_number"]

        story_data = story_by_panel.get(
            number,
            {},
        )

        image_path = (
            image_paths[index]
            if index < len(image_paths)
            else ""
        )

        layout.append(
            {
                "panel_number": number,
                "title": panel.get(
                    "title",
                    f"Panel {number}",
                ),
                "scene_description": panel.get(
                    "scene_description",
                    "",
                ),
                "image_prompt": panel.get(
                    "image_prompt",
                    "",
                ),
                "caption": story_data.get(
                    "caption",
                    "",
                ),
                "narration": story_data.get(
                    "narration",
                    "",
                ),
                "dialogue": story_data.get(
                    "dialogue",
                    "",
                ),
                "image_path": image_path,
            }
        )

    return layout