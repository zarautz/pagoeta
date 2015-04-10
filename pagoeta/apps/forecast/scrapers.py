import re

from lxml import html, etree
from lxml.cssselect import CSSSelector
from requests import get

from .helpers import AstronomicalObserver


class ForecastScraperWrapper():
    def __init__(self, date_list):
        self.date_list = date_list
        self.astronomical_observer = AstronomicalObserver(self.date_list)
        self.tide_scraper = TideScraper(self.date_list)
        self.weather_scraper = WeatherScraper(self.date_list)

    def get_source(self):
        source = {}
        source.update(self.tide_scraper.get_source())
        source.update(self.weather_scraper.get_source())
        return source

    def get_data(self):
        astronomical_data = self.astronomical_observer.get_data()
        tide_data = self.tide_scraper.get_data()
        weather_data = self.weather_scraper.get_data()
        data = []

        for date_str in [str(date) for date in self.date_list]:
            data.append({
                'date': date_str,
                'astronomy': astronomical_data[date_str],
                'tide': tide_data[date_str],
                'weather': weather_data[date_str] if date_str in weather_data else None
            })

        return data


class TideScraper():
    def __init__(self, date_list):
        self.formatted_date_dict = {}
        for date in date_list:
            self.formatted_date_dict[date.strftime('%d/%m/%Y')] = date
        self.months = sorted(list(set([date.month for date in date_list])))

    def get_source(self):
        return { 'Gipuzkoako Foru Aldundia': 'http://www.gipuzkoa.eus/' }

    def get_data(self):
        data = {}
        for month in self.months:
            data.update(self.parse_html(month))

        return data

    def parse_html(self, month):
        url = 'http://www4.gipuzkoa.net/MedioAmbiente/gipuzkoaingurumena/eu/secciones/playas/mareas.asp?filtroMesMarea=%d' % month
        source = get(url).text
        data = {}

        for row, tr in enumerate(html.fromstring(source).cssselect('.tabla tbody > tr')):
            cols = tr.cssselect('td')
            date_formatted = cols[0].text_content().strip()

            if date_formatted in self.formatted_date_dict:
                date_str = str(self.formatted_date_dict[date_formatted])
                data[date_str] = { 'low': [], 'high': [] }
                cols.pop(0)
            else:
                continue

            for col, td in enumerate(cols):
                """mod % 2 to detect even cols"""
                tide = 'high' if ((col % 2) == 0) else 'low'
                data[date_str][tide].append(td.text_content().strip())

        return data


class WeatherScraper():
    def __init__(self, date_list):
        self.date_str_list = [str(date) for date in date_list]

    def get_source(self):
        return { 'AEMET': 'http://www.aemet.es/' }

    def get_data(self):
        return self.parse_xml()

    def parse_xml(self):
        url = 'http://www.aemet.es/xml/municipios/localidad_20079.xml'
        source = get(url).text.encode('utf-8')
        root = etree.fromstring(source)
        data = {}

        for element in root.iter('dia'):
            date_str = element.get('fecha')

            if date_str in self.date_str_list:
                data[date_str] = {
                    'tempMin': int(element.xpath('.//temperatura/minima')[0].text),
                    'tempMax': int(element.xpath('.//temperatura/maxima')[0].text),
                    'uvMax': int(element.find('uv_max').text) if element.find('uv_max') is not None else None,
                    'forecast': self.parse_forecast_subelements(element),
                }

        return data

    def parse_forecast_subelements(self, element):
        period_groups = {
            1: ('00-06', '06-12', '12-18', '18-24'),
            2: ('00-12', '12-24'),
            3: ('00-24',)
        }
        wind_direction_map = { 'N': 'N', 'NE': 'NE', 'E': 'E', 'SE': 'SE', 'S': 'S', 'SO': 'SW', 'O': 'W', 'NO': 'NW', 'C':'C' }
        forecast_data = []

        if element.xpath('.//estado_cielo[@periodo="00-06"]'):
            period_group = 1
        elif element.xpath('.//estado_cielo[@periodo="00-12"]'):
            period_group = 2
        else:
            period_group = 3

        if period_group < 3:
            for period in period_groups[period_group]:
                """We need to check if data for a given period exists,
                because AEMET hides the data once the period has passed."""
                if element.xpath('.//estado_cielo[@periodo="%s"]' % period)[0].text:
                    forecast_data.append({
                        'period': period,
                        'code': int(element.xpath('.//estado_cielo[@periodo="%s"]' % period)[0].text.replace('n', '')),
                        'precipitationProb': int(element.xpath('.//prob_precipitacion[@periodo="%s"]' % period)[0].text),
                        'windDirection': element.xpath('.//viento/direccion')[0].text,
                        'windSpeed': int(element.xpath('.//viento[@periodo="%s"]/velocidad' % period)[0].text),
                    })

        else:
            period = period_groups[period_group][0]
            forecast_data.append({
                'period': period,
                'code': int(element.find('estado_cielo').text.replace('n', '')),
                'precipitationProb': int(element.find('prob_precipitacion').text),
                'windDirection': element.xpath('.//viento/direccion')[0].text,
                'windSpeed': int(element.xpath('.//viento/velocidad')[0].text),
            })

        return forecast_data
