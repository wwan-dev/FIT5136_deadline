#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
user_service.py  (轻量版)
=========================
职责：
    • 登录认证
    • 读取当前用户资料（只读，不修改）

依赖：
    src.entities.user.User
    src.repositories.user_repository.UserRepository
"""

from __future__ import annotations
from typing import Tuple, Optional

from src.entities.user import User
from src.repositories.user_repository import UserRepository


class UserService:
    """封装 *仅限用户本身* 的业务逻辑"""

    def __init__(self):
        self._repo = UserRepository()

    # ───────── 登录 ─────────
    def login(self, email: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        验证邮箱 + 密码

        Returns:
            success : bool           True=成功
            user    : Optional[User] 成功时返回 User
            message : str            描述信息
        """
        email = (email or "").strip()
        user = self._repo.authenticate(email, password)
        if user:
            return True, user, "Login success."
        if self._repo.get_by_email(email):
            return False, None, "Password incorrect."
        return False, None, "Account not found."

    # ───────── 个人资料（只读） ─────────
    @staticmethod
    def get_profile(user: User) -> dict:
        """
        将 User 转为可用于展示的 dict（不含密码）
        """
        profile = user.to_dict().copy()
        profile.pop("password", None)      # 不向界面暴露密码
        return profile
