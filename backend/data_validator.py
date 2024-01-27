import data_fetcher

def get_userfriendly_data(time, data, unit) -> list[str]:
    DATA: dict = {
        'data': data
    }
    days: list = []
    hours: list = []
    for day in time:
        date, hour = day.split('T')
        if not date in days:
            days.append(date)
        hours.append(hour)
    DATA['days'] = tuple(days)
    DATA['hours'] = tuple(hours)
    
    return DATA