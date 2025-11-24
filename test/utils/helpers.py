from datetime import UTC, datetime, timedelta
import uuid


def _uniq(prefix: str = "anon", suffix_len: int = 8) -> str:
    """Generate a unique string with a prefix.

    - Uses UUID4 and takes the first `suffix_len` hex characters.
    - Default prefix is "anon" and suffix length is 8 characters.

    Args:
        prefix (str, optional): Prefix for the string. Defaults to "anon".
        suffix_len (int, optional): Length of the suffix hexadecimal (1..32). Defaults to 8.

    Returns:
        str: Unique string formed by `<prefix>-<hex>`.
    """
    size = max(1, min(32, int(suffix_len)))  # Validate suffix length

    return f"{prefix}-{uuid.uuid4().hex[:size]}"


def expires_at_future(*, days: int = 1, minutes: int = 0, seconds: int = 0) -> str:
    """Return a future `expires_at` ISO8601 timestamp (UTC).

    Args:
        days (int): Days in the future. Defaults to 1.
        minutes (int): Minutes in the future. Defaults to 0.
        seconds (int): Seconds in the future. Defaults to 0.

    Returns:
        str: ISO8601 timestamp with UTC timezone.
    """
    delta = timedelta(days=days, minutes=minutes, seconds=seconds)

    return (datetime.now(UTC) + delta).isoformat()


def expires_at_past(*, days: int = 0, minutes: int = 1, seconds: int = 0) -> str:
    """Return a past `expires_at` ISO8601 timestamp (UTC).

    Args:
        days (int): Days in the past. Defaults to 0.
        minutes (int): Minutes in the past. Defaults to 1.
        seconds (int): Seconds in the past. Defaults to 0.

    Returns:
        str: ISO8601 timestamp with UTC timezone.
    """
    delta = timedelta(days=days, minutes=minutes, seconds=seconds)

    return (datetime.now(UTC) - delta).isoformat()


__all__ = ["_uniq", "expires_at_future", "expires_at_past"]
