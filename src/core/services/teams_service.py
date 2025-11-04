# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db
from src.core.models import Team


def list_teams() -> list[Team]:
    """List teams.

    Returns:
        list[Team]: List of teams.
    """
    return Team.query.order_by(Team.created_at.desc()).all()


def create_team(data: dict) -> Team:
    """Create team.

    Args:
        data (dict): Data to create team.

    Returns:
        Team: Created team.
    """
    team = Team(name=data.get("name"), description=data.get("description"))
    db.session.add(team)
    db.session.commit()

    return team


def get_team(team_id: int) -> Team | None:
    """Get team by ID.

    Args:
        team_id (int): Team ID.

    Returns:
        Team | None: Team or None if not found.
    """
    return Team.query.get(team_id)


def update_team(team_id: int, data: dict) -> Team | None:
    """Update team.

    Args:
        team_id (int): Team ID.
        data (dict): Data to update.

    Returns:
        Team | None: Updated team or None if not found.
    """
    team = Team.query.get(team_id)
    if not team:
        return None

    for field in ["name", "description", "state"]:
        if field in data and data[field] is not None:
            setattr(team, field, data[field])

    db.session.commit()

    return team


def set_team_state(team_id: int, state: bool) -> Team | None:
    """Set team state.

    Args:
        team_id (int): Team ID.
        state (bool): State to set.

    Returns:
        Team | None: Updated team or None if not found.
    """
    team = Team.query.get(team_id)
    if not team:
        return None

    team.state = bool(state)
    db.session.commit()

    return team


__all__ = [
    "create_team",
    "get_team",
    "list_teams",
    "set_team_state",
    "update_team",
]
