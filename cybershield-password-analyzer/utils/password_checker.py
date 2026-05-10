import re
import os

# Load common passwords once at module level
_COMMON_PASSWORDS = set()
_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'common_passwords.txt')
try:
    with open(_data_path, 'r') as f:
        _COMMON_PASSWORDS = {line.strip().lower() for line in f if line.strip()}
except FileNotFoundError:
    pass


def check_password(password: str) -> dict:
    """
    Analyze password strength and return detailed results.
    Returns a dict with score, level, checks, and recommendations.
    """
    if not password:
        return {
            "score": 0,
            "level": "None",
            "color": "#555",
            "checks": {},
            "recommendations": ["Please enter a password."],
            "is_common": False,
            "entropy": 0,
        }

    checks = {
        "length_8":       len(password) >= 8,
        "length_12":      len(password) >= 12,
        "length_16":      len(password) >= 16,
        "has_upper":      bool(re.search(r'[A-Z]', password)),
        "has_lower":      bool(re.search(r'[a-z]', password)),
        "has_digit":      bool(re.search(r'\d', password)),
        "has_special":    bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\":\\|,.<>\/?`~]', password)),
        "no_spaces":      ' ' not in password,
        "no_repeating":   not bool(re.search(r'(.)\1{2,}', password)),
        "no_sequential":  not _has_sequential(password),
    }

    is_common = password.lower() in _COMMON_PASSWORDS

    # --- Scoring ---
    score = 0
    if checks["length_8"]:   score += 1
    if checks["length_12"]:  score += 1
    if checks["length_16"]:  score += 1
    if checks["has_upper"]:  score += 1
    if checks["has_lower"]:  score += 1
    if checks["has_digit"]:  score += 1
    if checks["has_special"]: score += 2
    if checks["no_repeating"]: score += 1
    if checks["no_sequential"]: score += 1

    if is_common:
        score = max(0, score - 4)

    # Normalize to 0–100
    max_score = 10
    percent = min(100, int((score / max_score) * 100))

    # --- Level ---
    if percent < 25 or is_common:
        level, color = "Weak", "#e74c3c"
    elif percent < 50:
        level, color = "Fair", "#e67e22"
    elif percent < 75:
        level, color = "Good", "#f1c40f"
    elif percent < 90:
        level, color = "Strong", "#2ecc71"
    else:
        level, color = "Very Strong", "#00d4ff"

    # --- Recommendations ---
    recs = []
    if is_common:
        recs.append("This is a commonly used password - change it immediately.")
    if not checks["length_8"]:
        recs.append("Use at least 8 characters.")
    elif not checks["length_12"]:
        recs.append("Increase length to 12+ characters for better security.")
    elif not checks["length_16"]:
        recs.append("16+ characters makes your password significantly harder to crack.")
    if not checks["has_upper"]:
        recs.append("Add uppercase letters (A–Z).")
    if not checks["has_lower"]:
        recs.append("Add lowercase letters (a–z).")
    if not checks["has_digit"]:
        recs.append("Include numbers (0–9).")
    if not checks["has_special"]:
        recs.append("Include special characters (e.g. !, @, #, $).")
    if not checks["no_repeating"]:
        recs.append("Avoid repeated characters (e.g. 'aaa', '111').")
    if not checks["no_sequential"]:
        recs.append("Avoid sequential patterns (e.g. 'abc', '123', 'qwerty').")
    if not recs:
        recs.append("✅ Great password! Keep it secret and don't reuse it.")

    entropy = _calc_entropy(password)

    return {
        "score": percent,
        "level": level,
        "color": color,
        "checks": checks,
        "recommendations": recs,
        "is_common": is_common,
        "entropy": round(entropy, 1),
        "length": len(password),
    }


def _has_sequential(password: str) -> bool:
    """Detect keyboard walks and alphabetical/numeric sequences."""
    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "qwertyuiop", "asdfghjkl", "zxcvbnm",
        "01234567890",
    ]
    p = password.lower()
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in p:
                return True
    return False


def _calc_entropy(password: str) -> float:
    """Estimate password entropy in bits."""
    pool = 0
    if re.search(r'[a-z]', password): pool += 26
    if re.search(r'[A-Z]', password): pool += 26
    if re.search(r'\d', password):    pool += 10
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\":\\|,.<>\/?`~]', password): pool += 32
    if pool == 0:
        return 0.0
    import math
    return len(password) * math.log2(pool)
