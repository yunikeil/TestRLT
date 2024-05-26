from datetime import datetime
from typing import Literal
from pydantic import BaseModel, field_validator


class InputData(BaseModel):
    """Модель для валидации пользовательского ввода

    :raises ValueError: Неверный формат ввода даты
    """
    dt_from: datetime
    dt_upto: datetime
    group_type: Literal["hour", "day", "month"]

    @field_validator("dt_from", "dt_upto", mode="before")
    def parse_datetime(cls, value):
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid datetime format")
            
        raise TypeError("String or datetime object expected")

