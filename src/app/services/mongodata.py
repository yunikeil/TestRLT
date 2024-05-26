import asyncio
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from core.settings import config
from core.database.mongodb import mongo_client
from app.schemas.input import InputData


DATE_FORMATS = {
    "hour": "%Y-%m-%dT%H:00:00",
    "day": "%Y-%m-%dT00:00:00",
    "month": "%Y-%m-01T00:00:00"
}


async def aggregate_salary_data(form_data: InputData):
    """Функция для агрегации зарплат

    :param form_data: Модель данных пользовательского ввода
    :type form_data: InputData
    :return: Возвращает словарь данных, результат агрегации
    :rtype: dict[str, list]
    """
    db = mongo_client[config.MONGODB_DATABASE]
    collection = db[config.MONGODB_COLLECTION]
    
    date_format = DATE_FORMATS.get(form_data.group_type)

    pipeline = [
        {"$match": {
            "dt": {
                "$gte": form_data.dt_from,
                "$lte": form_data.dt_upto
            }
        }},
        {"$group": {
            "_id": {"$dateToString": {"format": date_format, "date": "$dt"}},
            "total_salary": {"$sum": "$value"}
        }},
        {"$sort": {"_id": 1}}
    ]

    query = await collection.aggregate(pipeline).to_list(length=None)
    
    def increment_date(date: datetime, interval: str):
        if interval == 'day':
            return date + timedelta(days=1)
        elif interval == 'month':
            return date + relativedelta(months=1)
        elif interval == 'year':
            return date + relativedelta(years=1)
    
    # Создаем список всех дат в заданном диапазоне с учетом формата
    all_dates = []
    current_date = form_data.dt_from
    while current_date <= form_data.dt_upto:
        all_dates.append(current_date.strftime(date_format))
        current_date = increment_date(current_date, form_data.group_type)

    # Заполняем недостающие дни и устанавливаем для них salary = 0
    result = {
        "dataset": [],
        "labels": []
    }
    for date_str in all_dates:
        found = False
        for entry in query:
            if entry['_id'] == date_str:
                result["dataset"].append(entry["total_salary"])
                result["labels"].append(entry["_id"])
                found = True
                break
        if not found:
            result["dataset"].append(0)
            result["labels"].append(date_str)

    return result
