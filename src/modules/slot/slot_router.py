"""Роутер для слотов."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import ValidationError

from src.core.auth.auth_utils import require_roles
from src.modules.user import ERole, UserEntity

from .slot_dto import SlotDTO
from .slot_service import SlotService, get_slot_service
from .slot_utils import DateModel

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
    slot_service: Annotated[SlotService, Depends(get_slot_service)],
    _user: Annotated[
        UserEntity, Depends(require_roles(ERole.admin.value, ERole.basic.value))
    ],
) -> list[SlotDTO]:
    """Получить все свободные слоты."""

    try:
        DateModel.model_validate({"date": date})
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error.errors()[0]["msg"]
        ) from error

    return await slot_service.get_all_free_by_date(date=date)


__all__ = ["router"]
