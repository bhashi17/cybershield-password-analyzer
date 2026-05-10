import secrets
import string


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
) -> str:
    """
    Generate a cryptographically secure random password.
    """
    if length < 4:
        length = 4
    if length > 128:
        length = 128

    pool = ""
    required_chars = []

    if use_lower:
        pool += string.ascii_lowercase
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        pool += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        pool += string.digits
        required_chars.append(secrets.choice(string.digits))
    if use_special:
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        pool += special
        required_chars.append(secrets.choice(special))

    if not pool:
        pool = string.ascii_letters + string.digits

    # Fill remaining length with random pool characters
    remaining = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(pool) for _ in range(remaining)]

    # Shuffle so required chars aren't always at the start
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def generate_passphrase(word_count: int = 4) -> str:
    """Generate a memorable passphrase from random words."""
    wordlist = [
        "apple", "bridge", "castle", "dragon", "eagle", "forest", "galaxy",
        "harbor", "island", "jungle", "knight", "lantern", "mountain", "nebula",
        "ocean", "phoenix", "quantum", "river", "storm", "thunder", "umbrella",
        "valley", "winter", "xenon", "yellow", "zenith", "arrow", "beacon",
        "coral", "delta", "ember", "falcon", "glacier", "horizon", "ivory",
        "jasper", "kelp", "lotus", "marble", "nexus", "orbit", "prism",
        "quartz", "radar", "silver", "titan", "ultra", "vapor", "wolf",
    ]
    words = [secrets.choice(wordlist) for _ in range(word_count)]
    separator = secrets.choice(["-", "_", ".", "@"])
    number = secrets.randbelow(900) + 100  # 100–999
    return separator.join(words) + str(number)
