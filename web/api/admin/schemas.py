from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.common import CommonUserSchema, Pagination


class CreateRoleRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название роли")


class GetRoleResponse(BaseModel):
    id: UUID = Field(...)
    name: str = Field(..., min_length=1, max_length=50, description="Название роли")
    created_at: datetime = Field(..., description="Дата и время создания роли")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления роли")

    class Config:
        from_attributes = True


class UpdateRoleRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Новое название роли")


class GetUserResponse(CommonUserSchema):
    role_id: UUID = Field(...)
    is_active: bool = Field(..., description="Активен ли пользователь")
    is_verified: bool = Field(..., description="Подтверждёна ли почта пользователя")
    created_at: datetime = Field(..., description="Дата и время создания пользователя")


class PaginatedUsersResponse(Pagination):
    users: List[GetUserResponse] = Field(..., description="Список пользователей")


class CreateUserRequest(CommonUserSchema):
    password: str = Field(..., min_length=8, max_length=128, description="Пароль пользователя")
    role_id: UUID = Field(..., description="ID роли пользователя")


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Новое имя пользователя")
    email: Optional[EmailStr] = Field(None, description="Новая электронная почта пользователя")
    role_id: Optional[UUID] = Field(None, description="Новая роль пользователя")
    is_active: Optional[bool] = Field(None, description="Активен ли пользователь")
    is_verified: Optional[bool] = Field(None, description="Подтверждён ли пользователь")
