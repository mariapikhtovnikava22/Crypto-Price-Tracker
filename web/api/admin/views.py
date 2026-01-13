from typing import List
from uuid import UUID

from exceptions.custom_exceptions import (
    EmailAlreadyExistsError,
    MissingUserIdOrTokenError,
    RoleNameAlreadyExistsError,
    RoleNotFoundError,
    UserNotFoundError,
)
from fastapi import APIRouter, Depends, HTTPException, status
from helpers.sort import get_sort_params

from app.models.common import PaginationFilters, SortParams
from app.services.roles import RoleService, get_role_service
from app.services.users import UserService, get_user_service
from web.api.admin.schemas import (
    CreateRoleRequest,
    GetRoleResponse,
    GetUserResponse,
    PaginatedUsersResponse,
    UpdateRoleRequest,
    UpdateUserRequest,
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post("/roles", response_model=GetRoleResponse)
async def create_role(
    role_data: CreateRoleRequest,
    role_service: RoleService = Depends(get_role_service),
) -> GetRoleResponse:
    try:
        return await role_service.create_role(role_data)
    except RoleNameAlreadyExistsError as exp:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exp.message)


@router.get("/roles", response_model=List[GetRoleResponse])
async def get_all_roles(
    role_service: RoleService = Depends(get_role_service),
) -> List[GetRoleResponse]:
    return await role_service.get_all_roles()


@router.get("/roles/{role_id}", response_model=GetRoleResponse)
async def get_role(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
) -> GetRoleResponse:
    try:
        return await role_service.get_role(role_id)
    except RoleNotFoundError as exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exp.message)


@router.patch("/roles/{role_id}", response_model=GetRoleResponse)
async def update_role(
    role_id: UUID,
    role_data: UpdateRoleRequest,
    role_service: RoleService = Depends(get_role_service),
) -> GetRoleResponse:
    try:
        return await role_service.update_role(role_id, role_data)
    except RoleNotFoundError as exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exp.message)


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
) -> None:
    try:
        await role_service.delete_role(role_id)
    except RoleNotFoundError as exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exp.message)


@router.get("/users", response_model=PaginatedUsersResponse)
async def get_all_users(
    pagination: PaginationFilters = Depends(),
    sort_params: SortParams = Depends(get_sort_params),
    user_service: UserService = Depends(get_user_service),
) -> PaginatedUsersResponse:
    return await user_service.get_all_users(pagination, sort_params)


@router.get("/users/{user_id}", response_model=GetUserResponse)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
) -> GetUserResponse:
    try:
        return await user_service.get_user(user_id)
    except UserNotFoundError as exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exp.message)


@router.patch("/users/{user_id}", response_model=GetUserResponse)
async def update_user(
    user_id: UUID,
    user_data: UpdateUserRequest,
    user_service: UserService = Depends(get_user_service),
) -> GetUserResponse:
    try:
        return await user_service.update_user(user_data, user_id=user_id)  # type: ignore
    except MissingUserIdOrTokenError as exp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exp.message)
    except UserNotFoundError as exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exp.message)
    except EmailAlreadyExistsError as exp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exp.message)
    except RoleNotFoundError as exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exp.message)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
) -> None:
    try:
        await user_service.delete_user(user_id=user_id)  # type: ignore
    except UserNotFoundError as exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exp.message)
