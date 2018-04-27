from .base import DateListType, XmlParser


class AemetParser(XmlParser):
    source_encoding = 'ISO-8859-15'

    def parse(self, *, dates: DateListType = []):
        data = {}
        date_str_list = [str(date) for date in dates]

        for element in self.tree.iter('dia'):
            date_str = element.get('fecha')

            if date_str in date_str_list:
                el = element
                temp_min = el.xpath('.//temperatura/minima')[0].text if el.xpath('.//temperatura/minima') else None
                temp_max = el.xpath('.//temperatura/maxima')[0].text if el.xpath('.//temperatura/maxima') else None
                uv_max = el.find('uv_max').text if el.find('uv_max') is not None else None
                data[date_str] = {
                    'temp_min': int(temp_min) if temp_min else None,
                    'temp_max': int(temp_max) if temp_max else None,
                    'uv_max': int(uv_max) if uv_max else None,
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
            'precipitation_prob': int(element.xpath('.//prob_precipitacion%s' % xpattern)[0].text),
            'wind_direction': wind_map[element.xpath('.//viento%s/direccion' % xpattern)[0].text],
            'wind_speed': int(element.xpath('.//viento%s/velocidad' % xpattern)[0].text),
        }
