import random
import math
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import pytest
import requests

try:
    response = requests.get('https://api.binance.com/api/v3/ticker/price', params={'symbol': 'BTCUSDT'})
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print('Ошибка при запросе к API: ', e)

# введите свои ключи API здесь
client = Client(api_key='', api_secret='')


def create_binance_orders(data):
    # Проверка введенных данных на достоверность
    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary")
    required_keys = ['volume', 'number', 'amountDif', 'side', 'priceMin', 'priceMax']
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key '{key}' in input data")

    volume = data['volume']
    if not isinstance(volume, (int, float)) or volume <= 0:
        raise ValueError("Volume must be a positive number")

    number = data['number']
    if not isinstance(number, int) or number <= 0:
        raise ValueError("Number of orders must be a positive integer")

    amountDif = data['amountDif']
    if not isinstance(amountDif, (int, float)) or amountDif < 0:
        raise ValueError("Amount difference must be a non-negative number")

    side = data['side']
    if side not in ['BUY', 'SELL']:
        raise ValueError("Side must be either 'BUY' or 'SELL'")

    priceMin = data['priceMin']
    if not isinstance(priceMin, (int, float)) or priceMin <= 0:
        raise ValueError("Minimum price must be a positive number")

    priceMax = data['priceMax']
    if not isinstance(priceMax, (int, float)) or priceMax <= 0:
        raise ValueError("Maximum price must be a positive number")

    try:
        # Получение информации о ticker для выбранного символа
        symbol = 'BTCUSDT'
        ticker = client.get_ticker(symbol=symbol)
        last_price = float(ticker['lastPrice'])

        # Расчет необходимого количества монет исходя из текущей цены
        quantity = volume / last_price

        # Определение размера шага округления цены до необходимого десятичного разряда
        step_size = float(client.get_symbol_info(symbol)['filters'][0]['tickSize'])

        # Определение диапазона объемов, в пределах которого мы случайным образом будем выбирать объем для каждого ордера
        half_dif = amountDif / 2

        # Создание указанного количества заказов
        for i in range(number):
            # Случайный выбор цены в заданном ценовом диапазоне
            price = round(random.uniform(priceMin, priceMax), int(-math.log10(step_size)))

            # Случайный выбор объема в заданном диапазоне
            amount = round(random.uniform(quantity / number - half_dif, quantity / number + half_dif), 8)

            # Создание заявки на бирже
            order = client.create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=amount,
                price=price
            )

            # Печать информации о созданном заказе
            print(f"Order {order['side']} created: {order['executedQty']} {symbol} at {order['price']} {order['time']}")

    except BinanceAPIException as e:
        # обработка ошибки, связанной с запросом к API Binance
        print(f"Binance API Exception: {e}")

    except BinanceRequestException as e:
        # обработка ошибки, связанной с выполнением запроса
        print(f"Binance Request Exception: {e}")

    except Exception as e:
        # обработка остальных ошибок
        print(f"Unknown Exception: {e}")


front = {
   "volume": 10000.0,  # Объем в долларах
   "number": 5,  # На сколько ордеров нужно разбить этот объем
   "amountDif": 50.0,  # Разброс в долларах, в пределах которого случайным образом выбирается объем в верхнюю и нижнюю сторону
   "side": "SELL",  # Сторона торговли (SELL или BUY)
   "priceMin": 200.0,  # Нижний диапазон цены, в пределах которого нужно случайным образом выбрать цену
   "priceMax": 300.0  # Верхний диапазон цены, в пределах которого нужно случайным образом выбрать цену
    }

create_binance_orders(front)






def test_create_binance_orders_invalid_data_type():
    with pytest.raises(TypeError):
        create_binance_orders("invalid_data_type")

def test_create_binance_orders_missing_required_key():
    data = {
        'volume': 0.01,
        'number': 2,
        'amountDif': 0.001,
        'side': 'BUY',
        'priceMin': 60000,
    }
    with pytest.raises(ValueError):
        create_binance_orders(data)

def test_create_binance_orders_invalid_volume():
    data = {
        'volume': -0.01,
        'number': 2,
        'amountDif': 0.001,
        'side': 'BUY',
        'priceMin': 60000,
        'priceMax': 62000
    }
    with pytest.raises(ValueError):
        create_binance_orders(data)

def test_create_binance_orders_invalid_number():
    data = {
        'volume': 0.01,
        'number': -2,
        'amountDif': 0.001,
        'side': 'BUY',
        'priceMin': 60000,
        'priceMax': 62000
    }
    with pytest.raises(ValueError):
        create_binance_orders(data)

def test_create_binance_orders_invalid_amountDif():
    data = {
        'volume': 0.01,
        'number': 2,
        'amountDif': -0.001,
        'side': 'BUY',
        'priceMin': 60000,
        'priceMax': 62000
    }
    with pytest.raises(ValueError):
        create_binance_orders(data)

def test_create_binance_orders_invalid_side():
    data = {
        'volume': 0.01,
        'number': 2,
        'amountDif': 0.001,
        'side': 'invalid_side',
        'priceMin': 60000,
        'priceMax': 62000
    }
    with pytest.raises(ValueError):
        create_binance_orders(data)

def test_create_binance_orders_invalid_priceMin():
    data = {
        'volume': 0.01,
        'number': 2,
        'amountDif': 0.001,
        'side': 'BUY',
        'priceMin': -60000,
        'priceMax': 62000
    }
    with pytest.raises(ValueError):
        create_binance_orders(data)

def test_create_binance_orders_invalid_priceMax():
    data = {
        'volume': 0.01,
        'number': 2,
        'amountDif': 0.001,
        'side': 'BUY',
        'priceMin': 60000,
        'priceMax': -62000
    }
    with pytest.raises(ValueError):
        create_binance_orders(data)

