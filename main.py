import random
import math
from binance.client import Client

# введите свои ключи API здесь
client = Client(api_key='', api_secret='')

def create_orders(volume, number, amountDif, side, priceMin, priceMax):
    # из объема в долларах нужно вычислить количество монет, используя текущий курс пары
    symbol = 'BTCUSDT'  # выбираем пару BTC/USDT
    ticker = client.get_ticker(symbol=symbol)
    last_price = float(ticker['lastPrice'])
    quantity = volume / last_price

    # определяем шаг цены, чтобы потом округлять цену до нужного количества знаков после запятой
    step_size = float(client.get_symbol_info(symbol)['filters'][0]['tickSize'])

    # вычисляем диапазон объема, в пределах которого мы будем выбирать объем каждого ордера
    half_dif = amountDif / 2

    for i in range(number):
        # выбираем случайную цену в заданном диапазоне
        price = round(random.uniform(priceMin, priceMax), int(-math.log10(step_size)))

        # выбираем случайный объем в заданном диапазоне
        amount = round(random.uniform(quantity/number-half_dif, quantity/number+half_dif), 8)

        # создаем ордер на бирже
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=amount,
            price=price
        )

        # выводим информацию об ордере
        print(f"Order{order['side']} created: {order['executedQty']} {symbol} at {order['price']} {order['time']}")