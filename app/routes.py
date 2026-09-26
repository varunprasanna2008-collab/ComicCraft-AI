from typing import Optional

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
)
from fastapi.templating import (
    Jinja2Templates,
)

from app.ai.gemini_flash import (
    generate_outline,
)

from app.ai.gemini_pro import (
    generate_story,
)

from app.ai.image_generator import (
    generate_image,
)

from app.config import (
    TEMPLATES_DIR,
)

from app.schemas import (
    PromptRequest,
)

from app.services.exporters import (
    save_pdf,
)

from app.services.layout_builder import (
    build_comic_layout,
)


router = APIRouter()

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ---------------------------------------------------------
# Home
# ---------------------------------------------------------

@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
        },
    )


# ---------------------------------------------------------
# Generate comic
# ---------------------------------------------------------

@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate_comic(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):
    try:
        # ---------------------------------------------
        # 1. Generate outline
        # ---------------------------------------------

        outline = generate_outline(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        # ---------------------------------------------
        # 2. Generate story
        # ---------------------------------------------

        story = generate_story(
            outline=outline,
            character_name=character_name,
            tone=tone,
        )

        # ---------------------------------------------
        # 3. Generate images
        # ---------------------------------------------

        image_paths = []

        for index, panel in enumerate(
            outline,
            start=1,
        ):
            image_path = generate_image(
                prompt=panel["image_prompt"],
                panel_number=index,
            )

            image_paths.append(
                image_path
            )

        # ---------------------------------------------
        # 4. Build layout
        # ---------------------------------------------

        layout = build_comic_layout(
            outline=outline,
            story=story,
            image_paths=image_paths,
        )

        # ---------------------------------------------
        # 5. Create PDF
        # ---------------------------------------------

        pdf_path = save_pdf(
            layout
        )

        return templates.TemplateResponse(
            request,
            "comic_preview.html",
            {
                "request": request,
                "layout": layout,
                "pdf_path": pdf_path,
                "story_prompt": story_prompt,
                "character_name": character_name,
                "setting": setting,
                "tone": tone,
                "art_style": art_style,
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ---------------------------------------------------------
# JSON API
# ---------------------------------------------------------

@router.post(
    "/generate-comic/json",
)
async def generate_comic_json(
    payload: PromptRequest,
):
    try:
        outline = generate_outline(
            story_prompt=payload.story_prompt,
            character_name=payload.character_name,
            setting=payload.setting,
            tone=payload.tone,
            art_style=payload.art_style,
        )

        story = generate_story(
            outline=outline,
            character_name=payload.character_name,
            tone=payload.tone,
        )

        image_paths = []

        for index, panel in enumerate(
            outline,
            start=1,
        ):
            image_paths.append(
                generate_image(
                    prompt=panel["image_prompt"],
                    panel_number=index,
                )
            )

        layout = build_comic_layout(
            outline=outline,
            story=story,
            image_paths=image_paths,
        )

        pdf_path = save_pdf(
            layout
        )

        return {
            "success": True,
            "message": (
                "Comic generated successfully."
            ),
            "panels": layout,
            "pdf_path": pdf_path,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Image testing
# ---------------------------------------------------------

@router.post(
    "/test-image",
)
async def test_image(
    prompt: str = Form(
        "A heroic fox in an enchanted forest, comic book style"
    ),
):
    try:
        image_path = generate_image(
            prompt=prompt,
            panel_number=999,
        )

        return {
            "success": True,
            "image_path": image_path,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Export success
# ---------------------------------------------------------

@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
    pdf_path: Optional[str] = None,
):
    return templates.TemplateResponse(
        request,
        "export_success.html",
        {
            "request": request,
            "pdf_path": pdf_path,
        },
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@router.get(
    "/health",
)
async def health():
    return {
        "status": "ok",
        "service": "ComicCraft",
    }