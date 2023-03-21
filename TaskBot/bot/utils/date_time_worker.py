import datetime


async def get_selected_datetime(date_time: str):
    date, time = date_time.split()
    splited_date = list(map(int, date.split(".")))
    splited_time = list(map(int, time.split(":")))
    selected_datetime = datetime.datetime(year=splited_date[-1],
                                          month=splited_date[1],
                                          day=splited_date[0],
                                          hour=splited_time[0],
                                          minute=splited_time[1])
    return selected_datetime


async def is_past_date(date_time: str) -> bool:
    selected_datetime = await get_selected_datetime(date_time=date_time)
    today = datetime.datetime.now()
    return selected_datetime < today
