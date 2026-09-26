from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200

    assert "ComicCraft" in response.text


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_generate_json():
    payload = {
        "story_prompt": (
            "A brave fox discovers a magical tree."
        ),
        "character_name": "Finn",
        "setting": "enchanted forest",
        "tone": "adventurous",
        "art_style": "comic book",
    }

    response = client.post(
        "/generate-comic/json",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert len(data["panels"]) == 5

    assert data["pdf_path"].endswith(
        ".pdf"
    )