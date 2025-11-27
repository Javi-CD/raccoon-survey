from test.utils.helpers import (
    _create_survey,
    _create_team,
    _generate_token,
    expires_at_future,
)


def _generate_tokens(client, auth_header_admin: dict, survey_id: int, count: int = 2):
    """Generate `count` tokens using the helper `_generate_token`.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The admin authorization header.
        survey_id (int): The ID of the survey to generate tokens for.
        count (int, optional): The number of tokens to generate. Defaults to 2.

    Returns:
        list: A list of generated tokens.
    """
    tokens = []
    for _ in range(count):
        tok = _generate_token(
            client,
            auth_header_admin,
            survey_id,
            expires_at=expires_at_future(days=1),
        )
        tokens.append(tok)

    return tokens


def test_e2e_tokens_export_csv(client, auth_header_admin: dict):
    """Test the tokens export endpoint for a survey.

    This test ensures that the tokens export endpoint returns a CSV file
    containing the generated tokens for a survey.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): A dictionary containing the admin authorization header.
    """

    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])

    tokens = _generate_tokens(client, auth_header_admin, survey["id"], count=3)
    assert isinstance(tokens, list) and len(tokens) == 3

    # Export tokens CSV
    res_export = client.get(
        f"/api/v1/tokens/{survey['id']}/export",
        headers=auth_header_admin,
    )
    assert res_export.status_code == 200

    # Check response headers for CSV content
    content_type = res_export.headers.get("Content-Type", "")
    assert content_type.startswith("text/csv")
    content_disp = res_export.headers.get("Content-Disposition", "")
    assert f"survey_{survey['id']}_tokens.csv" in content_disp

    csv_text = res_export.get_data(as_text=True)

    # Verify that at least one generated token is present in the CSV
    assert any(t["token"] in csv_text for t in tokens)
