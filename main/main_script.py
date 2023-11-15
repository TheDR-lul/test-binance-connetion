import asyncio
import json
import logging
import sys
from datetime import datetime
import talib
import os

# Добавляем текущий каталог в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.join(current_dir, 'modules')
sys.path.append(modules_path)

# Импорт модулей
from modules.binance_module import BinanceModule
from modules.trading_strategy import TradingStrategy
from modules.trade_metrics import calculate_trade_metrics
from modules.trade_statistics import calculate_and_export_statistics_after_sell, save_trade_data

# Глобальные переменные
active_pairs = set()
current_trades = {}
leverage = 20  # Плечо для сделок
active_pairs_count = 0
white_list = ['BTCUSDT', 'ETHUSDT']  # Ваш список торговых пар

# Инициализация объектов модулей
binance = BinanceModule()

# Инициализация стратегии
strategy = TradingStrategy()

# Инициализация статистики
statistics_df = save_trade_data({'test': 'data'})

# Настройки стратегии
rsi_period = strategy.get('rsi_period', 14)
rsi_overbought = int(strategy.get('rsi_overbought', 70))
rsi_oversold = int(strategy.get('rsi_oversold', 30))
profit_target_percent = float(strategy.get('profit_target_percent', 1.0))
commission_rate = float(strategy.get('commission_rate', 0.0004))
default_rsi_period = 14

async def on_kline(message):
    try:
        kline = json.loads(message)
        symbol = kline['s']
        close_price = float(kline['k']['c'])

        rsi = await calculate_rsi(symbol, close_price)

        if symbol in white_list:
            await check_and_set_leverage(symbol)

            if rsi is not None:
                await check_trade_conditions(symbol, close_price, rsi)

    except Exception as e:
        logging.info(f"Ошибка в обработке свечи: {e}")
    async def check_trade_conditions(symbol, close_price, rsi):
     global active_pairs_count

    try:
        if symbol not in current_trades and rsi < rsi_oversold:
            await execute_buy_order(symbol, close_price, rsi)

        elif symbol in current_trades and rsi >= rsi_overbought:
            await close_trade(symbol)
    except Exception as e:
        logging.info(f"Ошибка при проверке условий для сделки: {e}")






async def execute_buy_order(symbol, close_price, rsi):
    try:
        trade = {
            'symbol': symbol,
            'entry_time': datetime.now().strftime('%d,%m %H:%M:%S'),
            'entry_price': close_price,
            'buy_quantity': binance.calculate_quantity(close_price),
            'rsi_entry': rsi
        }

        await binance.execute_market_order(trade, leverage)
        current_trades[symbol] = trade
        current_trades[symbol]['profit_target_price'] = trade['entry_price'] * (1 + profit_target_percent / 100)
        active_pairs.add(symbol)
        active_pairs_count += 1
    except Exception as e:
        logging.info(f"Ошибка при выполнении покупки: {e}")
        await close_trade(symbol)
async def close_trade(symbol):
    try:
        trade = current_trades[symbol]
        close_price = await binance.fetch_ticker_price(symbol)
        trade['exit_time'] = datetime.now().strftime('%d,%m %H:%M:%S')
        trade['exit_price'] = close_price
        trade['rsi_exit'] = await calculate_rsi(symbol, close_price)

        await calculate_and_export_statistics_after_sell(trade)
        del current_trades[symbol]
        active_pairs_count -= 1
    except Exception as e:
        logging.info(f"Ошибка при закрытии сделки: {e}")

async def calculate_rsi(symbol, close_price):
    try:
        klines = await binance.fetch_klines(symbol, '5m')
        closes = [float(x[4]) for x in klines]
        rsi = talib.RSI(closes, timeperiod=int(rsi_period))
        return rsi[-1]
    except Exception as e:
        logging.info(f"Ошибка при расчете RSI для {symbol}: {e}")
        return None

async def check_and_set_leverage(symbol):
    try:
        symbol_info = await binance.fetch_symbol_info(symbol)
        max_leverage = symbol_info['leverage']

        global leverage
        if leverage > max_leverage:
            logging.info(f"Установленное плечо {leverage} для {symbol} превышает максимально допустимое значение. "
                         f"Установить максимальное кредитное плечо: {max_leverage}.")
            leverage = max_leverage
    except Exception as e:
        logging.info(f"Ошибка при проверке и установке плеча: {e}")

async def main():
    try:
        loop = asyncio.get_event_loop()

        # Добавление кнопки "Старт"
        start_button = input("Для начала работы введите 'start': ")
        if start_button.lower() != 'start':
            logging.info("Работа программы отменена.")
        else:
            # Загрузка стратегии из файла
            strategy.load_strategy()

            # Включение/выключение ограничителя по волатильности
            volatility_enabled = input(f"Включить ограничитель по волатильности? "
                                       f"({strategy.get('volatility_enabled', 'yes')}/no): ")
            if volatility_enabled.lower() == 'yes':
                strategy['volatility_enabled'] = 'yes'
                min_volatility = float(input(f"Введите минимальное значение волатильности "
                                             f"({strategy.get('min_volatility', 0.5)}): "))
                max_volatility = float(input(f"Введите максимальное значение волатильности "
                                             f"({strategy.get('max_volatility', 2.0)}): "))
                strategy['min_volatility'] = str(min_volatility)
                strategy['max_volatility'] = str(max_volatility)
            else:
                strategy['volatility_enabled'] = 'no'

            # Выбор таймфрейма
            timeframe = input(f"Выберите таймфрейм для анализа ({strategy.get('timeframe', '5m')}): ")
            strategy['timeframe'] = timeframe

            # Сохранение стратегии в файл
            strategy.save_strategy()

            # Добавление опции очистки лог-файла
            clear_log_button = input("Очистить лог-файл перед запуском? (yes/no): ")
            if clear_log_button.lower() == 'yes':
                strategy.clear_logfile()

            tasks = [binance.kline_listener(symbol, loop, on_kline) for symbol in white_list]
            tasks.append(save_trade_data({'test': 'data'}))
            await asyncio.gather(*tasks)

    except KeyboardInterrupt:
        logging.info('Программа прервана.')
    finally:
        await binance.close_binance_async()

# Запуск программы
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()

        # Добавление кнопки "Старт"
        start_button = input("Для начала работы введите 'start': ")
        if start_button.lower() != 'start':
            logging.info("Работа программы отменена.")
        else:
            loop.run_until_complete(main())

    except KeyboardInterrupt:
        logging.info('Программа прервана.')
    finally:
        loop.run_until_complete(binance.close_binance_async())
