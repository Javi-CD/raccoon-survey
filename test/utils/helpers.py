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


def _create_team(client, auth_header_admin: dict) -> dict:
    """Create a team.

    Args:
        client (FlaskClient): Flask test client.
        auth_header_admin (dict): Authorization header with admin credentials.

    Returns:
        dict: Created team.
    """
    name = _uniq("team")
    res = client.post(
        "/api/v1/teams/",
        json={"name": name, "description": "Test team"},
        headers=auth_header_admin,
    )
    assert res.status_code == 201

    return res.get_json()


def _create_survey(client, auth_header_admin: dict, team_id: int) -> dict:
    """Create a survey.

    Args:
        client (FlaskClient): Flask test client.
        auth_header_admin (dict): Authorization header with admin credentials.
        team_id (int): ID of the team to create the survey for.

    Returns:
        dict: Created survey.
    """
    title = _uniq("survey")
    res = client.post(
        "/api/v1/surveys/",
        json={
            "title": title,
            "description": "Anonymous survey",
            "team_id": team_id,
            "is_anonymous": True,
            "state": True,
        },
        headers=auth_header_admin,
    )
    assert res.status_code == 201

    return res.get_json()


def _create_question(
    client,
    auth_header_admin: dict,
    survey_id: int,
    *,
    text: str,
    qtype: str,
    is_required: bool = True,
    options: dict | None = None,
    order_position: int = 1,
) -> dict:
    """Create a question.

    Args:
        client (FlaskClient): Flask test client.
        auth_header_admin (dict): Authorization header with admin credentials.
        survey_id (int): ID of the survey to create the question for.
        text (str): Text of the question.
        qtype (str): Type of the question.
        is_required (bool, optional): Whether the question is required. Defaults to True.
        options (dict | None, optional): Options for the question. Defaults to None.
        order_position (int, optional): Order position of the question. Defaults to 1.

    Returns:
        dict: Created question.
    """
    payload = {
        "survey_id": survey_id,
        "text": text,
        "type": qtype,
        "is_required": is_required,
        "order_position": order_position,
    }
    if options is not None:
        payload["options"] = options

    res = client.post(
        "/api/v1/questions/",
        json=payload,
        headers=auth_header_admin,
    )
    assert res.status_code == 201

    return res.get_json()


def _generate_token(
    client, auth_header_admin: dict, survey_id: int, *, expires_at: str
) -> dict:
    """Generate a token.

    Args:
        client (FlaskClient): Flask test client.
        auth_header_admin (dict): Authorization header with admin credentials.
        survey_id (int): ID of the survey to generate a token for.
        expires_at (str): Expiration timestamp for the token.

    Returns:
        dict: Generated token.
    """
    res = client.post(
        f"/api/v1/tokens/{survey_id}/generate",
        json={"count": 1, "expires_at": expires_at},
        headers=auth_header_admin,
    )
    assert res.status_code == 201
    rows = res.get_json()
    assert isinstance(rows, list) and len(rows) == 1

    return rows[0]


__all__ = [
    "_create_question",
    "_create_survey",
    "_create_team",
    "_generate_token",
    "_uniq",
    "expires_at_future",
    "expires_at_past",
]
