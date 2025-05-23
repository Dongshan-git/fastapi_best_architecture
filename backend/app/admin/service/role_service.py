#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_data_rule import data_rule_dao
from backend.app.admin.crud.crud_menu import menu_dao
from backend.app.admin.crud.crud_role import role_dao
from backend.app.admin.model import Role
from backend.app.admin.schema.role import (
    CreateRoleParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleRuleParam,
)
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client


class RoleService:
    """角色服务类"""

    @staticmethod
    async def get(*, pk: int) -> Role:
        """
        获取角色详情

        :param pk: 角色 ID
        :return:
        """
        async with async_db_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            return role

    @staticmethod
    async def get_all() -> Sequence[Role]:
        """获取所有角色"""
        async with async_db_session() as db:
            roles = await role_dao.get_all(db)
            return roles

    @staticmethod
    async def get_by_user(*, pk: int) -> Sequence[Role]:
        """
        获取用户的角色列表

        :param pk: 用户 ID
        :return:
        """
        async with async_db_session() as db:
            roles = await role_dao.get_by_user(db, user_id=pk)
            return roles

    @staticmethod
    async def get_select(*, name: str | None, status: int | None) -> Select:
        """
        获取角色列表查询条件

        :param name: 角色名称
        :param status: 状态
        :return:
        """
        return await role_dao.get_list(name=name, status=status)

    @staticmethod
    async def create(*, obj: CreateRoleParam) -> None:
        """
        创建角色

        :param obj: 角色创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get_by_name(db, obj.name)
            if role:
                raise errors.ForbiddenError(msg='角色已存在')
            await role_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateRoleParam) -> int:
        """
        更新角色

        :param pk: 角色 ID
        :param obj: 角色更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            if role.name != obj.name:
                role = await role_dao.get_by_name(db, obj.name)
                if role:
                    raise errors.ForbiddenError(msg='角色已存在')
            count = await role_dao.update(db, pk, obj)
            for user in await role.awaitable_attrs.users:
                await redis_client.delete_prefix(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_role_menu(*, pk: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        更新角色菜单

        :param pk: 角色 ID
        :param menu_ids: 菜单 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            for menu_id in menu_ids.menus:
                menu = await menu_dao.get(db, menu_id)
                if not menu:
                    raise errors.NotFoundError(msg='菜单不存在')
            count = await role_dao.update_menus(db, pk, menu_ids)
            for user in await role.awaitable_attrs.users:
                await redis_client.delete_prefix(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_role_rule(*, pk: int, rule_ids: UpdateRoleRuleParam) -> int:
        """
        更新角色数据规则

        :param pk: 角色 ID
        :param rule_ids: 权限规则 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            for rule_id in rule_ids.rules:
                rule = await data_rule_dao.get(db, rule_id)
                if not rule:
                    raise errors.NotFoundError(msg='数据规则不存在')
            count = await role_dao.update_rules(db, pk, rule_ids)
            for user in await role.awaitable_attrs.users:
                await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        删除角色

        :param pk: 角色 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await role_dao.delete(db, pk)
            for _pk in pk:
                role = await role_dao.get(db, _pk)
                if role:
                    for user in await role.awaitable_attrs.users:
                        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count


role_service: RoleService = RoleService()
