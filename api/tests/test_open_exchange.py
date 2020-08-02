import unittest
import requests

from unittest.mock import patch

from api.open_exchange import OpenExchange

FAKE_RATES = {
    'BRL': 5.15,
    'EUR': 0.90
}


def fake_200():
    r = requests.Response()
    r.status_code = 200
    r.json = lambda: {'rates': FAKE_RATES}
    return r


def fake_500():
    r = requests.Response()
    r.status_code = 500
    return r


class TestIntegrationOpenExchange(unittest.TestCase):
    exchange = OpenExchange('9e99dd7952614fb494bc2fa538c7a7c4')

    def test_get_currencies_rate_should_return_all_currencies_rates(self):
        currencies = self.exchange.get_currencies_rate()

        self.assertIsInstance(currencies, dict)
        self.assertIsNotNone(currencies['BRL'])

    def test_get_currency_rate_should_return_current_rate(self):
        currency_rate = self.exchange.get_currency_rate('BRL')
        self.assertIsInstance(currency_rate, float)


class TestOpenExchange(unittest.TestCase):
    exchange = OpenExchange('9e99dd7952614fb494bc2fa538c7a7c4')

    @patch('api.open_exchange.requests.get', return_value=fake_200())
    def test_get_currencies_rate_should_return_all_currencies(self, mock):
        currencies = self.exchange.get_currencies_rate()
        self.assertEqual(currencies, FAKE_RATES)

    @patch('api.open_exchange.requests.get', return_value=fake_200())
    def test_get_currency_rate_should_return_current_rate(self, mock):
        currency_rate = self.exchange.get_currency_rate('BRL')
        self.assertEqual(currency_rate, 5.15)

    @patch('api.open_exchange.requests.get', return_value=fake_500())
    def test_get_currencies_rate_should_return_empty_on_api_error(self, mock):
        currencies = self.exchange.get_currencies_rate()
        self.assertEqual(currencies, {})

    @patch('api.open_exchange.requests.get', return_value=fake_500())
    def test_get_currency_rate_should_return_none_on_api_error(self, mock):
        currency_rate = self.exchange.get_currency_rate('BRL')
        self.assertIsNone(currency_rate)