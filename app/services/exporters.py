import os
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

from fpdf import FPDF

from app.config import (
    EXPORTS_DIR,
    STATIC_DIR,
)


class ComicPDF(FPDF):
    """
    Custom PDF class for ComicCraft.
    """

    def header(self):
        self.set_font(
            "Helvetica",
            "B",
            16,
        )

        self.cell(
            0,
            10,
            "ComicCraft",
            align="C",
        )

        self.ln(15)


def _static_path_from_url(
    image_url: str,
) -> Path:
    """
    Convert:

    /static/panels/example.png

    into:

    <project>/static/panels/example.png
    """

    clean = unquote(
        image_url.split("?")[0]
    )

    prefix = "/static/"

    if clean.startswith(prefix):
        relative = clean[len(prefix):]
        return STATIC_DIR / relative

    return Path(clean)


def save_pdf(
    layout: list,
) -> str:
    """
    Build a multi-page PDF from comic panels.

    Returns a browser-accessible URL.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"comiccraft_{timestamp}.pdf"
    )

    output_path = (
        EXPORTS_DIR / filename
    )

    pdf = ComicPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for panel in layout:
        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18,
        )

        title = (
            f"Panel {panel['panel_number']}: "
            f"{panel['title']}"
        )

        pdf.multi_cell(
            0,
            10,
            title,
        )

        image_path = _static_path_from_url(
            panel.get(
                "image_path",
                "",
            )
        )

        if image_path.exists():
            try:
                pdf.image(
                    str(image_path),
                    x=15,
                    y=35,
                    w=180,
                )

                pdf.set_y(145)

            except Exception:
                pdf.set_y(40)

        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        description = (
            panel.get(
                "scene_description",
                "",
            )
        )

        if description:
            pdf.multi_cell(
                0,
                7,
                f"Scene: {description}",
            )

        caption = panel.get(
            "caption",
            "",
        )

        if caption:
            pdf.ln(2)

            pdf.multi_cell(
                0,
                7,
                f"Caption: {caption}",
            )

        narration = panel.get(
            "narration",
            "",
        )

        if narration:
            pdf.ln(2)

            pdf.multi_cell(
                0,
                7,
                f"Narration: {narration}",
            )

        dialogue = panel.get(
            "dialogue",
            "",
        )

        if dialogue:
            pdf.ln(2)

            pdf.set_font(
                "Helvetica",
                "I",
                11,
            )

            pdf.multi_cell(
                0,
                7,
                f"Dialogue: {dialogue}",
            )

    pdf.output(
        str(output_path)
    )

    return (
        f"/static/exports/{filename}"
    )