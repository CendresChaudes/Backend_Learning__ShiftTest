"""Базовая модель для всех моделей базы данных."""

from datetime import date, datetime, time, timezone
from typing import Any, Set

from sqlalchemy import text
from sqlalchemy.exc import ArgumentError, NoInspectionAvailable
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseEntity(DeclarativeBase):
    """Базовый класс для всех моделей."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return self.__prepare_repr(self, max_depth=1, max_items=8)

    def __fmt_value(self, value: object) -> str:
        if isinstance(value, (datetime, date, time)):
            return value.isoformat()
        return repr(value)

    def __prepare_repr(
        self,
        obj: Any,
        *,
        max_depth: int = 1,
        max_items: int = 10,
        _seen: Set[int] | None = None,
        _depth: int = 0,
    ) -> str:
        if _seen is None:
            _seen = set()

        oid = id(obj)

        if oid in _seen:
            return "..."

        _seen.add(oid)
        cls_name = obj.__class__.__name__

        if _depth > max_depth:
            return f"<{cls_name} ...>"

        parts: list[str] = []

        cols = None
        try:
            cols = (
                list(obj.__table__.columns.keys())
                if getattr(obj, "__table__", None)
                else None
            )
        except (AttributeError, TypeError, NoInspectionAvailable, ArgumentError):
            cols = None

        if cols:
            for col in cols:
                try:
                    val = getattr(obj, col)
                except (AttributeError, TypeError):
                    val = "<error>"

                parts.append(f"{col}={self.__fmt_value(val)}")

        obj_dict = getattr(obj, "__dict__", {})
        for name, val in obj_dict.items():
            if cols and name in cols:
                continue

            if name.startswith("_sa_"):
                continue

            if val is None:
                parts.append(f"{name}=None")
                continue

            if isinstance(val, (list, tuple, set)):
                items: list[str] = []
                for i, item in enumerate(val):
                    if i >= max_items:
                        items.append("...")
                        break
                    if hasattr(item, "__table__"):
                        items.append(
                            self.__prepare_repr(
                                item,
                                max_depth=max_depth,
                                max_items=max_items,
                                _seen=_seen,
                                _depth=_depth + 1,
                            )
                        )
                    else:
                        items.append(self.__fmt_value(item))
                parts.append(f"{name}=[{', '.join(items)}]")
            elif hasattr(val, "__table__"):
                inner = self.__prepare_repr(
                    val,
                    max_depth=max_depth,
                    max_items=max_items,
                    _seen=_seen,
                    _depth=_depth + 1,
                )

                parts.append(f"{name}={inner}")
            else:
                parts.append(f"{name}={self.__fmt_value(val)}")

        return f"<{cls_name} " + ", ".join(parts) + ">"


__all__ = ["BaseEntity"]
