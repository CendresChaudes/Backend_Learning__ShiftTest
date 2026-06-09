"""Модуль для работы с временными слотами комнаты."""

from .slot_dto import SlotCreateDTO, SlotDTO, SlotUpdateDTO
from .slot_entity import SlotEntity
from .slot_service import SlotService, get_slot_service

__all__ = [
    "SlotEntity",
    "SlotCreateDTO",
    "SlotDTO",
    "SlotUpdateDTO",
    "SlotService",
    "get_slot_service",
]
