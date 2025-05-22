#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
user_service.py  (Light Version)
================================
Responsibilities:
    • Login authentication
    • Read current user profile (read-only, no modifications)

Dependencies:
    src.entities.user.User
    src.repositories.user_repository.UserRepository
"""

from __future__ import annotations
from typing import Tuple, Optional

from src.entities.user import User
from src.repositories.user_repository import UserRepository


class UserService:
    """Encapsulates business logic *for the user only*"""

    def __init__(self):
        self._repo = UserRepository()

    # ───────── Login ─────────
    def login(self, email: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        Authenticate email + password

        Returns:
            success : bool           True=successful
            user    : Optional[User] Returns User on success
            message : str            Description message
        """
        email = (email or "").strip()
        user = self._repo.authenticate(email, password)
        if user:
            return True, user, "Login success."
        if self._repo.get_by_email(email):
            return False, None, "Password incorrect."
        return False, None, "Account not found."

    # ───────── User Profile (Read-only) ─────────
    @staticmethod
    def get_profile(user: User) -> dict:
        """
        Convert User to displayable dict (without password)
        """
        profile = user.to_dict().copy()
        profile.pop("password", None)      # Don't expose password to the UI
        return profile


# ────────────────── Added: Update User Profile ──────────────────
    def update_profile(self, user: User, field: str, new_val: str) -> bool:
        """
        Only allows updating the following fields: name / phone / address / date_of_birth / gender / medical_history
        email and role cannot be changed.
        """
        allowed = {
            "name", "phone", "address",
            "date_of_birth", "gender", "medical_history"
        }
        if field not in allowed:
            return False
        # Call the entity's setter
        setattr(user, field, new_val.strip())
        return self._repo.update_user(user)
