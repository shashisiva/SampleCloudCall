# storage.py
import json
import os
from datetime import datetime
from uuid import uuid4

DATA_DIR = "data"
JSON_PATH = os.path.join(DATA_DIR, "issues.json")
IMAGES_DIR = os.path.join(DATA_DIR, "images")


def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_issues():
    ensure_storage()
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file got corrupted, fall back safely
        return []


def save_issues(all_issues):
    ensure_storage()
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(all_issues, f, indent=2, ensure_ascii=False)


def save_uploaded_image(uploaded_file):
    """
    Saves the image to data/images and returns the saved relative path.
    """
    if uploaded_file is None:
        return None

    ensure_storage()

    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png"]:
        ext = ".jpg"  # safe fallback

    unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex}{ext}"
    image_path = os.path.join(IMAGES_DIR, unique_name)

    # Streamlit uploaded_file -> bytes
    img_bytes = uploaded_file.getvalue()
    with open(image_path, "wb") as f:
        f.write(img_bytes)

    return image_path  # store this in JSON


def add_issue(issue_dict):
    """
    Adds one issue record into the JSON file.
    """
    all_issues = load_issues()
    all_issues.append(issue_dict)
    save_issues(all_issues)
