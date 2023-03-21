import re


async def date_time_validator(date_time: str) -> bool:
    pattern = "(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)[0-9]{2} (2[0-3]|[0-1][0-9]).[0-5][0-9]"
    res = re.fullmatch(pattern, date_time)
    return True if res else False
