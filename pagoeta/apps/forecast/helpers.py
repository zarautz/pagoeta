import ephem

from operator import itemgetter


class AstronomicalObserver():
    def __init__(self, date_list):
        self.date_list = date_list

    def get_data(self):
        observer = ephem.Observer()
        observer.lat, observer.lon, observer.elevation = '43.284410', '-2.172193', 7
        sun, moon = ephem.Sun(), ephem.Moon()
        data = {}

        for date in self.date_list:
            observer.date = date
            moon.compute(observer)
            moon_phases = self.get_sortered_moon_phases(date)

            data[str(date)] = {
                'sunrise': ephem.localtime(observer.previous_rising(sun)).strftime('%H:%M'),
                'sunset': ephem.localtime(observer.next_setting(sun)).strftime('%H:%M'),
                'moon': {
                    'illuminatedPercent': int(moon.moon_phase * 100),
                    'phaseChangesToday': (date == moon_phases[0]['date'].date()),
                    'nextPhase': moon_phases[0]['code'],
                    'nextPhaseDatetime': moon_phases[0]['date'],
                    'nextFullMoon': [phase for phase in moon_phases if phase['code'] == 'full'][0]['date'],
                    'nextNewMoon': [phase for phase in moon_phases if phase['code'] == 'new'][0]['date'],
                }
            }

        return data


    def get_sortered_moon_phases(self, date):
        """Returns next moon phase dates, ordered by date."""
        phases = [
            { 'code': 'new', 'date': ephem.localtime(ephem.next_new_moon(date)) },
            { 'code': 'q1', 'date': ephem.localtime(ephem.next_first_quarter_moon(date)) },
            { 'code': 'full', 'date': ephem.localtime(ephem.next_full_moon(date)) },
            { 'code': 'q3', 'date': ephem.localtime(ephem.next_last_quarter_moon(date)) },
        ]
        phases.sort(key = itemgetter('date'))

        return phases
