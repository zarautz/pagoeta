import json
import time
import urllib

from datetime import datetime
from django.conf import settings
from lxml import html, etree
from requests import get
from requests.exceptions import RequestException

from .helpers import AstronomicalObserver
from pagoeta.apps.core.exceptions import ServiceUnavailableException
from pagoeta.apps.core.scrapers import BaseScraper


class ForecastScraperWrapper(object):
    def __init__(self, date_list):
        self.date_list = date_list
        self.astronomical_observer = AstronomicalObserver(self.date_list)
        self.kosta_scraper = KostaScraper()
        self.tide_scraper = TideScraper(self.date_list)
        self.wave_scraper = WaveScraper(self.date_list)
        self.weather_scraper = WeatherScraper(self.date_list)

    def get_source(self):
        source = {}
        source.update(self.kosta_scraper.source)
        source.update(self.tide_scraper.source)
        source.update(self.wave_scraper.source)
        source.update(self.weather_scraper.source)
        return source

    def get_data(self):
        astronomical_data = self.astronomical_observer.get_data()
        tide_data = self.tide_scraper.get_data()
        wave_data = self.wave_scraper.get_data()
        weather_data = self.weather_scraper.get_data()
        data = []

        for date_str in [str(date) for date in self.date_list]:
            weather = weather_data[date_str] if date_str in weather_data else None
            if weather:
                weather['pressure'] = wave_data[date_str]['weather']['pressure'] if date_str in wave_data else None

            data.append({
                'date': date_str,
                'astronomy': astronomical_data[date_str],
                'charts': wave_data[date_str]['charts'] if date_str in wave_data else None,
                'tide': tide_data[date_str] if date_str in tide_data else None,
                'wave': wave_data[date_str]['wave'] if date_str in wave_data else None,
                'weather': weather,
                'wind': wave_data[date_str]['wind'] if date_str in wave_data else None,
            })

        return data

    def get_live_data(self):
        return self.kosta_scraper.get_live_data()


class KostaScraper(BaseScraper):
    source = {'AZTI-Tecnalia': 'http://www.kostasystem.com/en/video-measurement/zarautz-2/'}

    def get_live_data(self):
        return self.parse_html()

    def parse_html(self, source=None):
        """HTML source can be passed for testing purposes."""
        if not source:
            try:
                url = ('http://www.kostasystem.com/en/video-measurement/zarautz-2/')
                source = get(url).text
            except RequestException:
                raise ServiceUnavailableException

        data = {'snapshots': [], 'timex': []}

        for i, img in enumerate(html.fromstring(source).cssselect('a.monitorizaciones img')):
            """KOSTASystem images have always the same URL, so we need to add a timestamp to cheat XeroxImage."""
            photo_type = 'snapshots' if i < 2 else 'timex'
            src = img.get('src') + '?' + str(time.time())
            data[photo_type].append(self.get_xerox_image_sources(src)['source'])

        return data


class TideScraper(object):
    source = {'Gipuzkoako Foru Aldundia': 'http://www.gipuzkoaingurumena.eus/'}

    def __init__(self, date_list):
        self.formatted_date_dict = {}
        for date in date_list:
            self.formatted_date_dict[date.strftime('%d/%m/%Y')] = date
        self.ymonths = sorted(list(set(['%s-%s' % (date.year, date.month) for date in date_list])))

    def get_url(self, ymonth):
        ym = str(ymonth).split('-')
        base_url = 'http://www.gipuzkoaingurumena.eus/es/c/portal/layout'
        portlet = 'DCJmareas_WAR_DCJmareasportlet_INSTANCE_3Y41WFd6kR9h'
        params = {
            'p_l_id': 613952,
            'p_p_id': portlet,
            '_' + portlet + '_mes': ym[1],
            '_' + portlet + '_anyo': ym[0]
        }

        return base_url + '?' + urllib.urlencode(params)

    def get_data(self):
        data = {}
        for ymonth in self.ymonths:
            data.update(self.parse_html(ymonth))

        return data

    def parse_html(self, ymonth, source=None):
        """HTML source can be passed for testing purposes."""
        if not source:
            try:
                source = get(self.get_url(ymonth)).text
            except RequestException:
                raise ServiceUnavailableException

        data = {}

        for row, tr in enumerate(html.fromstring(source).cssselect('table.footable tbody > tr')):
            cols = tr.cssselect('td')
            date_formatted = cols[0].text_content().strip()

            if date_formatted in self.formatted_date_dict:
                date_str = str(self.formatted_date_dict[date_formatted])
                data[date_str] = {'low': [], 'high': []}
                cols.pop(0)
            else:
                continue

            for col, td in enumerate(cols):
                """mod % 2 to detect even cols."""
                tide = 'high' if ((col % 2) == 0) else 'low'
                text = td.text_content().strip()
                if text != '':
                    data[date_str][tide].append(text)

        return data


class WaveScraper(object):
    source = {'Magicseaweed Ltd': 'http://magicseaweed.com/Zarautz-Surf-Report/1061/'}

    def __init__(self, date_list):
        self.date_str_list = [str(date) for date in date_list]

    def get_data(self):
        return self.parse_json()

    def parse_json(self, source=None):
        """JSON source can be passed for testing purposes."""
        if not source:
            try:
                url = 'http://magicseaweed.com/api/%s/forecast/?spot_id=1061&units=eu'
                source = get(url % settings.MAGICSEAWEED_API_KEY).text
            except RequestException:
                raise ServiceUnavailableException

        data = {}

        for element in json.loads(source):
            date_str = datetime.fromtimestamp(element['localTimestamp']).strftime('%Y-%m-%d')

            if date_str in self.date_str_list:
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


class WeatherScraper(object):
    source = {'AEMET': 'http://www.aemet.es/es/eltiempo/prediccion/municipios/zarautz-id20079'}

    def __init__(self, date_list):
        self.date_str_list = [str(date) for date in date_list]

    def get_data(self):
        return self.parse_xml()

    def parse_xml(self, source=None):
        """XML source can be passed for testing purposes."""
        if not source:
            try:
                source = get('http://www.aemet.es/xml/municipios/localidad_20079.xml').text.encode('utf-8')
            except RequestException:
                raise ServiceUnavailableException

        try:
            root = etree.fromstring(source)
        except etree.XMLSyntaxError:
            raise ServiceUnavailableException

        data = {}

        for element in root.iter('dia'):
            date_str = element.get('fecha')

            if date_str in self.date_str_list:
                el = element
                temp_min = el.xpath('.//temperatura/minima')[0].text if el.xpath('.//temperatura/minima') else None
                temp_max = el.xpath('.//temperatura/maxima')[0].text if el.xpath('.//temperatura/maxima') else None
                uv_max = el.find('uv_max').text if el.find('uv_max') is not None else None
                data[date_str] = {
                    'tempMin': int(temp_min) if temp_min else None,
                    'tempMax': int(temp_max) if temp_max else None,
                    'uvMax': int(uv_max) if uv_max else None,
                    'forecast': self.parse_forecast_subelements(element),
                }

        return data

    def parse_forecast_subelements(self, element):
        period_groups = {
            1: ('00-06', '06-12', '12-18', '18-24'),
            2: ('00-12', '12-24'),
            3: ('00-24',)
        }
        forecast_data = []

        if element.xpath('.//estado_cielo[@periodo="00-06"]'):
            period_group = 1
        elif element.xpath('.//estado_cielo[@periodo="00-12"]'):
            period_group = 2
        else:
            period_group = 3

        if period_group == 3:
            period = period_groups[period_group][0]
            forecast_data.append(self.parse_forecast(element, period, False))
        else:
            for period in period_groups[period_group]:
                """We need to check if data for a given period exists,
                because AEMET hides the data once the period is over."""
                if element.xpath('.//estado_cielo[@periodo="%s"]' % period)[0].text:
                    forecast_data.append(self.parse_forecast(element, period, True))

        return forecast_data

    def parse_forecast(self, element, period, is_detailed=False):
        wind_map = {'N': 'N', 'NE': 'NE', 'E': 'E', 'SE': 'SE', 'S': 'S', 'SO': 'SW', 'O': 'W', 'NO': 'NW', 'C': 'C'}
        xpattern = ('[@periodo="%s"]' % period) if is_detailed else ''

        return {
            'period': period,
            'code': int(element.xpath('.//estado_cielo%s' % xpattern)[0].text.replace('n', '')),
            'precipitationProb': int(element.xpath('.//prob_precipitacion%s' % xpattern)[0].text),
            'windDirection': wind_map[element.xpath('.//viento%s/direccion' % xpattern)[0].text],
            'windSpeed': int(element.xpath('.//viento%s/velocidad' % xpattern)[0].text),
        }
