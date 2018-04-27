import datetime

from typing import Dict, List

from .base import JsonParser


class MagicseaweedParser(JsonParser):
    def parse(self, *, dates: List[datetime.date]) -> Dict[datetime.date, dict]:
        data = {}
        date_str_list = [str(date) for date in dates]

        for element in self.json:
            date_str = datetime.datetime.fromtimestamp(element['localTimestamp']).strftime('%Y-%m-%d')

            if date_str in date_str_list:
                data[date_str] = {
                    'charts': element['charts'],
                    'wave': {
                        'rating': {
                            'solid': element['solidRating'],
                            'faded': element['fadedRating'],
                        },
                        'swell': element['swell'],
                    },
                    'weather': element['condition'],
                    'wind': element['wind'],
                }

        return data
