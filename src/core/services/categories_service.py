# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db
from src.core.models import Category


def list_categories(active_only: bool = True) -> list[Category]:
    """List categories.

    Args:
        active_only (bool, optional): If True, returns only active categories.
            By default True.

    Returns:
        list[Category]: List of categories ordered by name.
    """
    query = Category.query

    if active_only:
        query = query.filter(Category.state.is_(True))

    return query.order_by(Category.name.asc()).all()


def create_category(data: dict) -> Category:
    """Create category.

    Args:
        data (dict): Creation data. Requires `name`.

    Returns:
        Category: Created category.
    """
    category = Category(
        name=data.get("name"),
        description=data.get("description"),
    )
    db.session.add(category)
    db.session.commit()

    return category


def get_category(category_id: int) -> Category | None:
    """Get category by ID.

    Args:
        category_id (int): Category ID.

    Returns:
        Category | None: Category or None if it does not exist.
    """
    return Category.query.get(category_id)


def update_category(category_id: int, data: dict) -> Category | None:
    """Update category.

    Args:
        category_id (int): Category ID.
        data (dict): Fields to update.

    Returns:
        Category | None: Category updated or None if it does not exist.
    """
    category = Category.query.get(category_id)
    if not category:
        return None

    for field in ["name", "description", "state"]:
        if field in data:
            setattr(category, field, data[field])

    db.session.commit()

    return category


def set_category_state(category_id: int, state: bool) -> Category | None:
    """Set category state (soft-delete).

    Args:
        category_id (int): Category ID.
        state (bool): State to set.

    Returns:
        Category | None: Updated category or None if not found.
    """
    category = Category.query.get(category_id)

    if not category:
        return None

    category.state = bool(state)
    db.session.commit()

    return category


__all__ = [
    "create_category",
    "get_category",
    "list_categories",
    "set_category_state",
    "update_category",
]
