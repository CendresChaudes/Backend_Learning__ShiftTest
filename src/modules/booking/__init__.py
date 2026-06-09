"""Модуль для работы c бронированием временных слотов комнат."""

from .booking_entity import BookingEntity
from .booking_router import router as booking_router

__all__ = ["BookingEntity", "booking_router"]
