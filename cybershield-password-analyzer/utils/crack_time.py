import math


# Assumed guesses per second for different attack scenarios
ATTACK_SPEEDS = {
    "Online (throttled)":     100,          # 100 guesses/sec — rate-limited web form
    "Online (unthrottled)":   10_000,       # 10K/sec — no rate limiting
    "Offline (MD5)":          10_000_000_000,   # 10B/sec — fast hash cracking rig
    "Offline (bcrypt)":       10_000,       # 10K/sec — bcrypt is intentionally slow
}


def estimate_crack_time(entropy_bits: float) -> dict:
    """
    Given password entropy in bits, estimate crack time for various attack speeds.
    Returns a dict mapping scenario name → human-readable time string.
    """
    if entropy_bits <= 0:
        return {k: "Instant" for k in ATTACK_SPEEDS}

    total_combinations = 2 ** entropy_bits
    results = {}

    for scenario, guesses_per_sec in ATTACK_SPEEDS.items():
        seconds = total_combinations / guesses_per_sec
        results[scenario] = _format_time(seconds)

    return results


def _format_time(seconds: float) -> str:
    if seconds < 1:
        return "Less than a second"
    if seconds < 60:
        return f"{int(seconds)} second{'s' if seconds != 1 else ''}"
    if seconds < 3_600:
        m = int(seconds / 60)
        return f"{m} minute{'s' if m != 1 else ''}"
    if seconds < 86_400:
        h = int(seconds / 3_600)
        return f"{h} hour{'s' if h != 1 else ''}"
    if seconds < 31_536_000:
        d = int(seconds / 86_400)
        return f"{d} day{'s' if d != 1 else ''}"
    if seconds < 3_153_600_000:
        y = int(seconds / 31_536_000)
        return f"{y:,} year{'s' if y != 1 else ''}"
    if seconds < 3.154e13:
        y = int(seconds / 31_536_000)
        return f"{y:,.0e} years"
    return "Longer than the age of the universe"
