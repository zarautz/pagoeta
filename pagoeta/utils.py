import datetime


def get_next_dates(days: int = 7, include_today: bool = True):
    today = datetime.datetime.today().date()
    dates = [today + datetime.timedelta(days=x) for x in range(0, days)]
    return dates