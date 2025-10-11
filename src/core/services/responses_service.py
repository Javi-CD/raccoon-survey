from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError

from src.core.database import db
from src.core.models import Question, Response, Survey, SurveyToken


def _lock_and_get_token(token_str: str) -> SurveyToken:
    """Lock and retrieve a SurveyToken by token string.

    This method queries the database for a SurveyToken with the given token string,
    applying a FOR UPDATE lock to ensure exclusive access. If no token is found,
    a LookupError is raised.

    Args:
        token_str (str): The unique token string used to identify the SurveyToken.

    Raises:
        LookupError: If no SurveyToken with the given token string exists.

    Returns:
        SurveyToken: The SurveyToken instance corresponding to the given token string.
    """
    token_q = SurveyToken.query.filter_by(token=token_str).with_for_update()
    token = token_q.first()
    if token is None:
        raise LookupError("token_not_found")

    return token


def _validate_token_membership(token: SurveyToken, survey_id: int | None) -> None:
    """Validate that a SurveyToken belongs to a specific Survey.

    This method checks if the SurveyToken's survey_id matches the provided survey_id.
    If they do not match, a ValueError is raised.

    Args:
        token (SurveyToken): The SurveyToken instance to validate.
        survey_id (int | None): The ID of the Survey to compare against. If None,
            the token's survey_id is not checked.

    Raises:
        ValueError: If the token's survey_id does not match the provided survey_id.
    """
    if survey_id is not None and token.survey_id != survey_id:
        raise ValueError("token_not_for_survey")


def _validate_token_freshness(token: SurveyToken, now: datetime) -> None:
    """Validate that a SurveyToken is fresh and not expired.

    This method checks if the SurveyToken has already been used or if its expiration
    time (if set) is in the past. If either condition is true, a ValueError is raised.

    Args:
        token (SurveyToken): The SurveyToken instance to validate.
        now (datetime): The current datetime to compare against the token's expiration time.

    Raises:
        ValueError: If the token has already been used.
        ValueError: If the token is expired.
    """
    if token.is_used:
        raise ValueError("token_already_used")

    if token.expires_at:
        expires_at = token.expires_at
        if getattr(expires_at, "tzinfo", None) is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at < now:
            raise ValueError("token_expired")


def _get_and_validate_survey(token: SurveyToken) -> Survey:
    """Retrieve a Survey by its ID, validating its state.

    This method queries the database for a Survey with the ID stored in the given SurveyToken.
    If no Survey is found, a LookupError is raised. If the Survey is inactive or not anonymous,
    ValueError exceptions are raised.

    Args:
        token (SurveyToken): The SurveyToken instance containing the survey_id.

    Raises:
        LookupError: If no Survey with the token's survey_id exists.
        ValueError: If the Survey is inactive.
        ValueError: If the Survey is not anonymous.

    Returns:
        Survey: The Survey instance corresponding to the token's survey_id.
    """
    survey = Survey.query.get(token.survey_id)
    if survey is None:
        raise LookupError("survey_not_found")
    if not survey.state:
        raise ValueError("survey_inactive")
    if not survey.is_anonymous:
        raise ValueError("survey_not_anonymous")

    return survey


def _get_active_questions(survey_id: int) -> list[Question]:
    """Retrieve active questions for a specific Survey.

    This method queries the database for all active (state=True) questions
    associated with the given survey_id, ordered by their order_position.
    If no active questions are found, a ValueError is raised.

    Args:
        survey_id (int): The ID of the Survey to retrieve questions for.

    Raises:
        ValueError: If no active questions are found for the given survey_id.

    Returns:
        list[Question]: A list of active Question instances for the specified Survey.
    """
    questions = (
        Question.query.filter_by(survey_id=survey_id, state=True)
        .order_by(Question.order_position.asc())
        .all()
    )
    if not questions:
        raise ValueError("no_questions_available")

    return questions


def _normalize_and_validate_responses(
    responses: Iterable[dict], questions: list[Question]
) -> list[tuple[int, str]]:
    """Normalize and validate responses for a Survey.

    This method processes a list of response dictionaries, validating each against
    the provided list of active questions. It normalizes question IDs and answers,
    checks for required questions, and ensures that each question ID is unique.

    Args:
        responses (Iterable[dict]): A list of response dictionaries, each containing
            'question_id' and 'answer' keys.
        questions (list[Question]): A list of active Question instances for the Survey.

    Raises:
        ValueError: If any response is missing 'question_id' or 'answer'.
        ValueError: If any question ID in the responses is not found in the questions list.
        ValueError: If any question ID is repeated in the responses.
        ValueError: If any required question is missing in the responses.

    Returns:
        list[tuple[int, str]]: A list of normalized (question_id, answer) tuples.
    """
    question_map = {q.id: q for q in questions}
    required_ids = {q.id for q in questions if q.is_required}

    provided_ids: set[int] = set()
    normalized: list[tuple[int, str]] = []
    for item in responses or []:
        qid = item.get("question_id")
        ans = item.get("answer")
        if qid is None:
            raise ValueError("missing_question_id")
        if ans is None:
            raise ValueError("missing_answer")
        if qid not in question_map:
            raise ValueError("question_not_in_survey")

        provided_ids.add(int(qid))
        normalized.append((int(qid), str(ans)))

    if not required_ids.issubset(provided_ids):
        missing = sorted(required_ids - provided_ids)

        raise ValueError(f"missing_required_questions:{missing}")

    return normalized


def _check_idempotency(token_id: int) -> None:
    """Check if a token has already been used for submitting responses.

    This method queries the database to count the number of Response records
    associated with the given token_id. If the count is greater than zero,
    it indicates that the token has already been used, and a ValueError is raised.

    Args:
        token_id (int): The ID of the SurveyToken to check for idempotency.

    Raises:
        ValueError: If the token has already been used (i.e., count > 0).
    """
    existing_count = Response.query.filter_by(survey_token_id=token_id).count()
    if existing_count > 0:
        raise ValueError("already_submitted")


def _persist_responses_and_mark_token(
    token: SurveyToken, normalized: list[tuple[int, str]], now: datetime
) -> int:
    """Persist normalized responses and mark the token as used.

    This method creates Response records in the database for each normalized response,
    associating them with the given SurveyToken. It also updates the token's is_used
    and used_at fields to mark it as used.

    Args:
        token (SurveyToken): The SurveyToken instance to be marked as used.
        normalized (list[tuple[int, str]]): A list of normalized (question_id, answer) tuples.
        now (datetime): The current datetime to be used for marking the token as used.

    Raises:
        RuntimeError: If a database integrity error occurs.
        RuntimeError: If a general database error occurs.

    Returns:
        int: The number of responses successfully persisted.
    """
    try:
        response_rows: list[Response] = [
            Response(question_id=qid, survey_token_id=token.id, answer=ans)
            for (qid, ans) in normalized
        ]
        for r in response_rows:
            db.session.add(r)

        token.is_used = True
        token.used_at = now

        db.session.commit()
        return len(normalized)

    except IntegrityError as e:
        db.session.rollback()
        raise RuntimeError("db_integrity_error") from e
    except Exception as e:
        db.session.rollback()
        raise RuntimeError("db_error") from e


def submit_anonymous_responses(
    *,
    token_str: str,
    responses: Iterable[dict],
    survey_id: int | None = None,
) -> dict:
    """Submit anonymous responses using a one-time survey token.

    Implements idempotence: if the token has already been used or responses already exist
    associated with the token, rejects double sending.

    Args:
        token_str (str): Survey token (UUID/string)
        responses (Iterable[dict]): List of responses with {question_id, answer}
        survey_id (int | None, optional): Additional membership validation. Defaults to None.

    Returns:
        dict: Summary of operation {saved_count, token_id, survey_id}
    """
    now = datetime.now(UTC)

    # Token retrieval and validations
    token = _lock_and_get_token(token_str)
    _validate_token_membership(token, survey_id)
    _validate_token_freshness(token, now)

    # Survey validation
    survey = _get_and_validate_survey(token)

    # Questions retrieval and payload validation
    questions = _get_active_questions(survey.id)
    normalized = _normalize_and_validate_responses(responses, questions)

    # Idempotence check
    _check_idempotency(token.id)

    # Persistence
    saved_count = _persist_responses_and_mark_token(token, normalized, now)

    return {
        "saved_count": saved_count,
        "token_id": token.id,
        "survey_id": token.survey_id,
    }
