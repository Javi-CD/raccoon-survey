# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations  # noqa: I001

import os
import uuid
from datetime import UTC, datetime, timedelta

from flask import current_app
from werkzeug.security import generate_password_hash

from src.core import create_app
from src.core.database import db
from src.core.models import (
    AuditLog,
    Category,
    Question,
    QuestionCategory,
    Role,
    Survey,
    SurveyToken,
    Team,
    User,
)


def get_or_create_role(name: str, description: str | None = None) -> Role:
    """Get or create a role.

    Args:
        name (str): Role name.
        description (str | None, optional): Role description. Defaults to None.

    Returns:
        Role: Role instance.
    """
    role = Role.query.filter_by(name=name).first()
    if role:
        return role

    role = Role(name=name, description=description, created_at=datetime.now(UTC))
    db.session.add(role)

    return role


def get_or_create_team(name: str, description: str | None = None) -> Team:
    """Get or create a team.

    Args:
        name (str): Team name.
        description (str | None, optional): Team description. Defaults to None.

    Returns:
        Team: Team instance.
    """
    team = Team.query.filter_by(name=name).first()
    if team:
        return team

    team = Team(name=name, description=description, created_at=datetime.now(UTC))
    db.session.add(team)

    return team


def get_or_create_user(
    email: str, name: str, password_hash: str, team: Team | None, role: Role | None
) -> User:
    """Get or create a user.

    Args:
        email (str): User email.
        name (str): User name.
        password_hash (str): User password hash.
        team (Team | None): User team. Defaults to None.
        role (Role | None): User role. Defaults to None.

    Returns:
        User: User instance.
    """
    user = User.query.filter_by(email=email).first()
    if user:
        return user

    user = User(
        email=email,
        name=name,
        password_hash=password_hash,
        created_at=datetime.now(UTC),
    )
    if team:
        user.team = team
    if role:
        user.role = role
    db.session.add(user)

    return user


def get_or_create_category(name: str, description: str | None = None) -> Category:
    """Get or create a category.

    Args:
        name (str): Category name.
        description (str | None, optional): Category description. Defaults to None.

    Returns:
        Category: Category instance.
    """
    category = Category.query.filter_by(name=name).first()
    if category:
        return category

    category = Category(
        name=name, description=description, created_at=datetime.now(UTC)
    )
    db.session.add(category)

    return category


def get_or_create_survey(
    title: str,
    team: Team,
    created_by_user: User,
    description: str | None = None,
    is_anonymous: bool = True,
    expires_days: int = 30,
) -> Survey:
    """Get or create a survey.

    Args:
        title (str): Survey title.
        team (Team): Survey team.
        created_by_user (User): Survey created by user.
        description (str | None, optional): Survey description. Defaults to None.
        is_anonymous (bool, optional): Survey is anonymous. Defaults to True.
        expires_days (int, optional): Survey expires days. Defaults to 30.

    Returns:
        Survey: Survey instance.
    """
    survey = Survey.query.filter_by(title=title, team_id=team.id).first()
    if survey:
        return survey

    survey = Survey(
        title=title,
        description=description,
        is_anonymous=is_anonymous,
        team=team,
        created_by_user=created_by_user,
        expires_at=datetime.now(UTC) + timedelta(days=expires_days),
        created_at=datetime.now(UTC),
    )

    db.session.add(survey)
    return survey


def get_or_create_question(
    survey: Survey,
    text: str,
    type_: str,
    options: dict | None = None,
    is_required: bool = False,
    order_position: int = 0,
) -> Question:
    """Get or create a question.

    Args:
        survey (Survey): Question survey.
        text (str): Question text.
        type_ (str): Question type.
        options (dict | None, optional): Question options. Defaults to None.
        is_required (bool, optional): Question is required. Defaults to False.
        order_position (int, optional): Question order position. Defaults to 0.

    Returns:
        Question: Question instance.
    """
    question = Question.query.filter_by(
        survey_id=survey.id, text=text, type=type_
    ).first()
    if question:
        return question

    question = Question(
        survey=survey,
        text=text,
        type=type_,
        options=options,
        is_required=is_required,
        order_position=order_position,
        created_at=datetime.now(UTC),
    )
    db.session.add(question)

    return question


def ensure_question_category(
    question: Question, category: Category, assigned_by: User | None
) -> QuestionCategory:
    """Get or create a question category.

    Args:
        question (Question): Question category question.
        category (Category): Question category category.
        assigned_by (User | None): Question category assigned by user. Defaults to None.

    Returns:
        QuestionCategory: Question category instance.
    """
    qc = QuestionCategory.query.filter_by(
        question_id=question.id, category_id=category.id
    ).first()
    if qc:
        return qc

    qc = QuestionCategory(
        question=question,
        category=category,
        assigned_by_user=assigned_by,
        created_at=datetime.now(UTC),
    )
    db.session.add(qc)

    return qc


def ensure_tokens(survey: Survey, team: Team, count: int = 5) -> list[SurveyToken]:
    """Get or create survey tokens.

    Args:
        survey (Survey): Survey tokens survey.
        team (Team): Survey tokens team.
        count (int, optional): Survey tokens count. Defaults to 5.

    Returns:
        list[SurveyToken]: Survey tokens list.
    """
    existing = SurveyToken.query.filter_by(survey_id=survey.id, team_id=team.id).all()
    if existing:
        return existing

    tokens: list[SurveyToken] = []
    expiry = survey.expires_at or (datetime.now(UTC) + timedelta(days=30))

    for _ in range(count):
        token = SurveyToken(
            survey=survey,
            team=team,
            token=str(uuid.uuid4()),
            employee_identifier=None,
            is_used=False,
            expires_at=expiry,
            created_at=datetime.now(UTC),
        )
        db.session.add(token)
        tokens.append(token)

    return tokens


def log_audit(
    entity_type: str,
    entity_id: int,
    action: str,
    user: User | None,
    previous_data: dict | None = None,
    new_data: dict | None = None,
    metadata: dict | None = None,
    triggered_by: str = "manual",
) -> AuditLog:
    """Log an audit entry.

    Args:
        entity_type (str): Audit entity type.
        entity_id (int): Audit entity id.
        action (str): Audit action.
        user (User | None): Audit changed by user. Defaults to None.
        previous_data (dict | None, optional): Audit previous data. Defaults to None.
        new_data (dict | None, optional): Audit new data. Defaults to None.
        metadata (dict | None, optional): Audit metadata. Defaults to None.
        triggered_by (str, optional): Audit triggered by. Defaults to "manual".

    Returns:
        AuditLog: Audit log instance.
    """
    entry = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        changed_by_user=user,
        previous_data=previous_data,
        new_data=new_data,
        metadata_=metadata,
        triggered_by=triggered_by,
        created_at=datetime.now(UTC),
    )
    db.session.add(entry)

    return entry


def seed() -> dict[str, int]:
    """Seed the database with initial data.

    Returns:
        dict[str, int]: Dictionary with entity counts.
    """
    # Base entities
    admin_role = get_or_create_role("admin", "Administrator role")
    hr_role = get_or_create_role("hr", "Human Resources role")  # noqa: F841

    team_hr = get_or_create_team("HR", "Human Resources Team")

    # Default admin
    admin_email = current_app.config.get("DEFAULT_USER_ADMIN_EMAIL", None)
    admin_name = current_app.config.get("DEFAULT_USER_ADMIN_NAME", None)
    admin_password = current_app.config.get("DEFAULT_USER_ADMIN_PASSWORD", None)

    # Hash the admin password
    admin_password_hash = generate_password_hash(admin_password)

    admin_user = get_or_create_user(
        email=admin_email,
        name=admin_name,
        password_hash=admin_password_hash,
        team=team_hr,
        role=admin_role,
    )

    # Categories
    cat_culture = get_or_create_category("Culture", "Company culture and values")
    cat_compensation = get_or_create_category("Compensation", "Salary and benefits")

    # Survey and Questions
    survey = get_or_create_survey(
        title="Employee Satisfaction Survey",
        description="Baseline survey to measure satisfaction",
        team=team_hr,
        created_by_user=admin_user,
        is_anonymous=True,
        expires_days=30,
    )

    q1 = get_or_create_question(
        survey,
        text="How satisfied are you with your job?",
        type_="rating",
        options={"min": 1, "max": 5, "labels": ["Very Low", "Very High"]},
        is_required=True,
        order_position=1,
    )

    q2 = get_or_create_question(  # noqa: F841
        survey,
        text="What could we improve?",
        type_="text",
        options=None,
        is_required=False,
        order_position=2,
    )

    # Link categories to questions
    ensure_question_category(q1, cat_culture, assigned_by=admin_user)
    ensure_question_category(q1, cat_compensation, assigned_by=admin_user)

    # Tokens
    ensure_tokens(survey, team_hr, count=5)

    # Flush to assign IDs for audit
    db.session.flush()

    # Audit logs (basic)
    log_audit(
        "survey",
        survey.id,
        "create",
        admin_user,
        previous_data=None,
        new_data={"title": survey.title},
    )
    log_audit("category", cat_culture.id, "create", admin_user)
    log_audit("category", cat_compensation.id, "create", admin_user)

    db.session.commit()

    return {
        "roles": Role.query.count(),
        "teams": Team.query.count(),
        "users": User.query.count(),
        "categories": Category.query.count(),
        "surveys": Survey.query.count(),
        "questions": Question.query.count(),
        "survey_tokens": SurveyToken.query.count(),
        "audit_logs": AuditLog.query.count(),
    }


def main() -> None:
    """Main function to seed the database."""
    try:
        override_config: dict[str, str] = {}
        db_url_env = os.getenv("DATABASE_URL")

        if not db_url_env or db_url_env.startswith("sqlite:///"):
            raw_path = (
                db_url_env.replace("sqlite:///", "")
                if db_url_env
                else "src/core/database/raccoon.db"
            )
            abs_path = os.path.abspath(raw_path)
            override_config["SQLALCHEMY_DATABASE_URI"] = (
                f"sqlite:///{abs_path.replace('\\', '/')}"
            )

        app = create_app(override_config or None)

        with app.app_context():
            db_url = current_app.config.get("SQLALCHEMY_DATABASE_URI")

            if db_url and db_url.startswith("sqlite:///"):
                path = db_url.replace("sqlite:///", "")
                dir_path = os.path.dirname(path)

                if dir_path and not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                if path and not os.path.exists(path):
                    open(path, "a").close()

            summary = seed()
            print("Seed completed:")

            for k, v in summary.items():
                print(f"- {k}: {v}")
    except Exception as e:
        print(f"Error seeding database: {e}")
        raise e


if __name__ == "__main__":
    main()
