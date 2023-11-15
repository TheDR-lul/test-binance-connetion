import json
import sys
import ccxt
import logging
import asyncio
from datetime import datetime

class BinanceModule:
    def __init__(self):
        self.binance_client = ccxt.binance()  # Используем ccxt для взаимодействия с Binance

    async def execute_market_order(self, trade, leverage):
        try:
            symbol = trade['symbol']
            buy_quantity = trade['buy_quantity']
            side = ccxt.binance_constants.SIDE_BUY
            order_type = ccxt.binance_constants.ORDER_TYPE_MARKET
            params = {'leverage': leverage}

            order = await self.binance_client.create_order(
                symbol=symbol,
                type=order_type,
                side=side,
                quantity=buy_quantity,
                params=params
            )

            logging.info(f"Покупка {symbol} выполнена: {order}")
        except Exception as e:
            logging.info(f"Ошибка при выполнении покупки: {e}")
            raise

    async def fetch_ticker_price(self, symbol):
        try:
            ticker = await self.binance_client.fetch_ticker(symbol)
            return ticker['ask']  # Мы используем ask цену, но вы можете выбрать любую другую
        except Exception as e:
            logging.info(f"Ошибка при получении цены тикера для {symbol}: {e}")
            raise

    async def fetch_klines(self, symbol, interval):
        try:
            klines = await self.binance_client.fetch_ohlcv(symbol, interval)
            return klines
        except Exception as e:
            logging.info(f"Ошибка при получении свечей для {symbol} с интервалом {interval}: {e}")
            raise

    async def fetch_symbol_info(self, symbol):
        try:
            symbol_info = await self.binance_client.fetch_ticker(symbol)
            return symbol_info
        except Exception as e:
            logging.info(f"Ошибка при получении информации о символе {symbol}: {e}")
            raise

    async def calculate_quantity(self, close_price):
        try:
            # Используем логику из вашего кода
            equity = await self.binance_client.fetch_balance()
            total_balance = equity['total']['USDT']
            risk_percentage = 1  # Уровень риска в процентах
            risk_amount = total_balance * risk_percentage / 100
            quantity = risk_amount / close_price
            return quantity
        except Exception as e:
            logging.info(f"Ошибка при расчете количества: {e}")
            raise

    async def kline_listener(self, symbol, loop, callback):
        async def on_kline(message):
            try:
                kline = json.loads(message)
                await callback(kline)
            except Exception as e:
                logging.info(f"Ошибка в обработке свечи: {e}")

        while True:
            try:
                klines = await self.fetch_klines(symbol, '5m')
                for kline in klines:
                    await on_kline(json.dumps({'k': kline, 's': symbol}))
                await asyncio.sleep(1)
            except ccxt.NetworkError as e:
                logging.info(f'Сетевая ошибка: {e}')
                await asyncio.sleep(5)  # При возникновении ошибки сети ждем 5 секунд и повторяем
            except KeyboardInterrupt:
                logging.info(f'Прерывание с клавиатуры. Завершение программы.')
                await self.close_binance_async()
                sys.exit(0)
            except Exception as e:
                logging.info(f'Ошибка: {e}')
                raise

    async def close_binance_async(self):
        # Реализуйте закрытие соединения с Binance
        pass