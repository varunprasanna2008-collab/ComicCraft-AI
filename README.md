# ComicCraft

ComicCraft is an AI-powered comic story creator built with:

- FastAPI
- Jinja2
- Google Gemini
- Hugging Face image generation
- Stable Diffusion / Diffusers
- Pillow
- FPDF

## Features

- Generate a five-panel comic story
- Generate narration
- Generate dialogue
- Generate image prompts
- Generate comic images
- Preview the comic in the browser
- Export the comic as PDF
- JSON API
- Image testing endpoint
- Mock image mode for development

---

# Project Structure

```text
ComicCraft/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── routes.py
│   │
│   ├── ai/
│   │   ├── gemini_flash.py
│   │   ├── gemini_pro.py
│   │   └── image_generator.py
│   │
│   ├── services/
│   │   ├── layout_builder.py
│   │   └── exporters.py
│   │
│   └── utils/
│       └── json_utils.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
│
├── static/
│   ├── css/
│   ├── js/
│   ├── panels/
│   └── exports/
│
└── tests/
    └── test_app.py