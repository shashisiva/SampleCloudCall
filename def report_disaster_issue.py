import re
from datetime import datetime


# -------------------------
# Helpers (separate)
# -------------------------

def clean(x):
    return str(x).strip() if x is not None else ""


def is_missing(x):
    return clean(x) == ""


def safe_int(x, default=3):
    try:
        return int(clean(x))
    except Exception:
        return default


def safe_float(x):
    try:
        s = clean(x)
        return float(s) if s != "" else None
    except Exception:
        return None






def contains_banned_words(text, banned_words):
    t = clean(text).lower()
    for w in banned_words:
        if w in t:
            return True
    return False


def mock_save_to_db(report_dict):
    """Mock DB save: prints what would be saved and returns a fake id."""
    print("\n✅ [MOCK DB] Saving report...")
    for k, v in report_dict.items():
        print(f"   - {k}: {v}")
    print("✅ [MOCK DB] Saved!\n")
    return 1


# -------------------------
# Core function (NO input() here)
# -------------------------

def report_disaster_issue(issue_data, lang):
    """
    Core logic:
    - Validate mandatory fields
    - Validate category/lang
    - Basic "bad data" check
    - Mock save to DB
    """

    # Simple settings
    ALLOWED_LANGS = ["en", "si", "ta"]
    ALLOWED_CATEGORIES = ["rain", "flood", "landslide", "wind", "fire", "tsunami", "cyclone", "other"]
    BANNED_WORDS = ["porn", "nude", "xxx", "sex", "bad", "pig", "stupid"]



    # 2) Pull fields
    description = clean(issue_data.get("description"))
    category = clean(issue_data.get("category")).lower()
    province = clean(issue_data.get("province"))
    city = clean(issue_data.get("city"))
    area = clean(issue_data.get("area"))

   
   

    # 3) Mandatory fields check
    missing = []
    if is_missing(description): missing.append("description")
    if is_missing(category): missing.append("category")
    if is_missing(province): missing.append("province")
    if is_missing(city): missing.append("city")
    if is_missing(area): missing.append("area")

    if missing:
        return {"success": False, "message": "Missing fields: " + ", ".join(missing)}

    # 4) Validate category
    if category not in ALLOWED_CATEGORIES:
        return {"success": False, "message": "Category not allowed."}



    # 6) Bad/unacceptable data check
    if contains_banned_words(description, BANNED_WORDS):
        return {"success": False, "message": "Not acceptable description."}

    
    

    # 8) Build report dict
    report = {
        "created_at_utc": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "language": lang,
        "category": category,
        "description": description,
        "province": province,
        "city": city,
        "area": area,
      
    }

    # 9) Mock save to DB
    report_id = mock_save_to_db(report)

    return {"success": True, "message": "Saved OK (mock)", "report_id": report_id}


# -------------------------
# Main (asks for inputs)
# -------------------------

def main():
    print("\n=== Cloud Call: Report Disaster Issue ===")

    lang = clean(input("Language (en/si/ta): "))

    issue_data = {
        "description": clean(input("Issue description: ")),
        "category": clean(input("Category (rain/flood/landslide/wind/fire/tsunami/cyclone/other): ")),
        "province": clean(input("Province: ")),
        "city": clean(input("City: ")),
        "area": clean(input("Area: ")),
        }

    result = report_disaster_issue(issue_data, lang)
    print("Result:", result)


if __name__ == "__main__":
    main()
