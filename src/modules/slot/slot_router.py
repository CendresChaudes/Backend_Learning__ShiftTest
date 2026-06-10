"""Роутер для слотов."""

from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, Query, status

from src.core.auth.auth_utils import require_roles
from src.modules.user.user_entity import ERole, UserEntity

from .slot_dto import SlotDTO
from .slot_service import get_slot_service

if TYPE_CHECKING:
    from .slot_service import SlotService

router = APIRouter(prefix="/slots", tags=["Слоты"])


@router.get(
    path="/",
    summary="Получить все свободные слоты",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Свободные слоты успешно получены",
            "content": {
                "application/json": {
                    "schema": {"type": "array", "items": SlotDTO.model_json_schema()}
                }
            },
        },
    },
)
async def get_slots(
    date: Annotated[str, Query(description="Дата в формате DD.MM.YYYY")],
    slot_service: Annotated["SlotService", Depends(get_slot_service)],
    _user: Annotated[
        UserEntity, Depends(require_roles(ERole.admin.value, ERole.basic.value))
    ],
) -> list[SlotDTO]:
    """Получить все свободные слоты."""

    return await slot_service.get_all_free_by_date(date=date)


__all__ = ["router"]
