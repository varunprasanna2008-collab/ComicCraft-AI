import re
import uuid
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw
from huggingface_hub import InferenceClient

from app.config import (
    HF_API_KEY,
    HF_IMAGE_MODEL,
    IMAGE_PROVIDER,
    LOCAL_IMAGE_MODEL,
    PANELS_DIR,
)

# Optional global cache for local diffusers pipeline
_LOCAL_PIPELINE = None


def _safe_filename(text: str) -> str:
    # Sanitize string to contain only safe alphanumeric characters and hyphens/underscores
    text = re.sub(r"[^a-zA-Z0-9_-]+", "_", text)
    return text[:80].strip("_") or "panel"


def _create_mock_image(
    prompt: str,
    output_path: Path,
) -> None:
    width = 1024
    height = 768

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    draw.rectangle((20, 20, width - 20, height - 20), outline="black", width=8)
    draw.text((60, 60), "ComicCraft", fill="black")
    draw.text((60, 150), prompt[:500], fill="black")
    draw.text((60, 680), "AI Image Placeholder", fill="black")

    image.save(output_path, format="PNG")


def _generate_huggingface(
    prompt: str,
    output_path: Path,
) -> None:
    if not HF_API_KEY:
        raise RuntimeError("HF_API_KEY is missing.")

    client = InferenceClient(api_key=HF_API_KEY)

    try:
        image = client.text_to_image(
            prompt=prompt,
            model=HF_IMAGE_MODEL,
        )
    except Exception as exc:
        raise RuntimeError(f"Hugging Face image generation failed: {exc}") from exc

    if image is None:
        raise RuntimeError("Hugging Face returned no image.")

    image.save(output_path, format="PNG")


def _generate_local_diffusers(
    prompt: str,
    output_path: Path,
) -> None:
    global _LOCAL_PIPELINE
    try:
        import torch
        from diffusers import StableDiffusionPipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local image generation requires torch and diffusers."
        ) from exc

    if _LOCAL_PIPELINE is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _LOCAL_PIPELINE = StableDiffusionPipeline.from_pretrained(LOCAL_IMAGE_MODEL)
        _LOCAL_PIPELINE = _LOCAL_PIPELINE.to(device)

    image = _LOCAL_PIPELINE(
        prompt,
        num_inference_steps=20,
    ).images[0]

    image.save(output_path, format="PNG")


def generate_image(
    prompt: str,
    panel_number: int = 1,
) -> str:
    # Fixed tuple issue by building string properly
    safe_prompt = _safe_filename(prompt)
    unique_id = uuid.uuid4().hex[:8]
    filename = f"panel_{panel_number}_{unique_id}_{safe_prompt}.png"

    PANELS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PANELS_DIR / filename

    provider = IMAGE_PROVIDER.lower().strip()

    if provider == "huggingface":
        _generate_huggingface(prompt, output_path)
    elif provider == "local":
        _generate_local_diffusers(prompt, output_path)
    else:
        _create_mock_image(prompt, output_path)

    return f"/static/panels/{filename}"