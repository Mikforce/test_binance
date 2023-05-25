from unittest import TestCase
from main import create_binance_orders
import unittest
import random
import math
from binance.client import Client

# введите свои ключи API здесь
client = Client(api_key='', api_secret='')
def test_create_orders_quantity():
    volume = 1000  # $1000
    number = 5
    amountDif = 100  # +- $100
    side = 'BUY'
    priceMin = 40000
    priceMax = 50000

    symbol = 'BTCUSDT'  # выбираем пару BTC/USDT
    ticker = client.get_ticker(symbol=symbol)
    last_price = float(ticker['lastPrice'])
    quantity = volume / last_price

    for i in range(number):
        # Вычисляем объем для каждого ордера
        half_dif = amountDif / 2
        amount = round(random.uniform(quantity/number-half_dif, quantity/number+half_dif), 8)

        assert amount <= quantity/number+half_dif and amount >= quantity/number-half_dif

def test_create_orders_price():
    volume = 1000  # $1000
    number = 5
    amountDif = 100  # +- $100
    side = 'BUY'
    priceMin = 40000
    priceMax = 50000

    symbol = 'BTCUSDT'  # выбираем пару BTC/USDT
    step_size = float(client.get_symbol_info(symbol)['filters'][0]['tickSize'])

    for i in range(number):
        # Вычисляем цену для каждого ордера
        price = round(random.uniform(priceMin, priceMax), int(-math.log10(step_size)))

        assert price <= priceMax and price >= priceMin

def test_create_order_on_exchange():
    volume = 1000  # $1000
    number = 1
    amountDif = 100  # +- $100
    side = 'BUY'
    priceMin = 40000
    priceMax = 50000

    symbol = 'BTCUSDT'  # выбираем пару BTC/USDT

    for i in range(number):
        # Вычисляем объем и цену для каждого ордера
        ticker = client.get_ticker(symbol=symbol)
        last_price = float(ticker['lastPrice'])
        quantity = volume / last_price
        half_dif = amountDif / 2
        amount = round(random.uniform(quantity/number-half_dif, quantity/number+half_dif), 8)
        step_size = float(client.get_symbol_info(symbol)['filters'][0]['tickSize'])
        price = round(random.uniform(priceMin, priceMax), int(-math.log10(step_size)))

        # Создаем ордер на бирже
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=amount,
            price=price
        )

        assert order is not None

def test_create_order_side():
    volume = 1000  # $1000
    number = 1
    amountDif = 100  # +- $100
    priceMin = 40000
    priceMax = 50000

    symbol = 'BTCUSDT'  # выбираем пару BTC/USDT

    for i in range(number):
        # Вычисляем объем и цену для каждого ордера
        ticker = client.get_ticker(symbol=symbol)
        last_price = float(ticker['lastPrice'])
        quantity = volume / last_price
        half_dif = amountDif / 2
        amount = round(random.uniform(quantity/number-half_dif, quantity/number+half_dif), 8)
        step_size = float(client.get_symbol_info(symbol)['filters'][0]['tickSize'])
        price = round(random.uniform(priceMin, priceMax), int(-math.log10(step_size)))

        # Определяем сторону ордера на основе максимальной и минимальной цены
        if price < last_price:
            side = 'BUY'
        else:
            side = 'SELL'

        # Создаем ордер на бирже
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=amount,
            price=price
        )

        assert order['side'] == side


def test_create_orders_price_step():
    volume = 1000  # $1000
    number = 5
    amountDif = 100  # +- $100
    side = 'BUY'
    priceMin = 40000
    priceMax = 50000

    symbol = 'BTCUSDT'  # выбираем пару BTC/USDT
    step_size = float(client.get_symbol_info(symbol)['filters'][0]['tickSize'])

    for i in range(number):
        # Вычисляем цену для каждого ордера
        price = round(random.uniform(priceMin, priceMax), int(-math.log10(step_size)))

        assert math.isclose((price - priceMin) % step_size, 0, rel_tol=1e-9)


if __name__ == '__main__':
    unittest.main()