# -*- coding: utf-8 -*-
import sys
import ccxt
import json
import talib
import pandas as pd
from datetime import datetime
import asyncio
import atexit
import logging
from logging.handlers import RotatingFileHandler
import os

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Очистка лог-файла
def clear_logfile():  
    try:
        with open('logfile.log', 'w'):
            pass
        logging.info("Лог-файл очищен.")
    except Exception as e:
        logging.error(f"Ошибка при очистке лог-файла: {e}")

# Установка кодировки для обработчика
class UTF8RotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding='utf-8', delay=0):
        super(UTF8RotatingFileHandler, self).__init__(filename, mode, maxBytes, backupCount, delay=delay)
        self.encoding = encoding

# Создание логгера
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Установка обработчика с явной кодировкой
log_handler = UTF8RotatingFileHandler('logfile.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)


# Асинхронная функция для сохранения данных о сделках в файл
async def save_trade_data(trade):
    try:
        with open('trade_data.json', 'a') as file:
            json.dump(trade, file)
            file.write('\n')
        logging.info(f"Данные о сделке сохранены: {trade}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных о сделке: {e}")


# Функция для чтения API-ключей из файла

def read_api_keys(filename='api_keys.txt'):
    try:
        with open(filename, 'r') as file:
            api_keys = {}
            for line in file:
                key, value = line.strip().split('=')
                api_keys[key] = value
            return api_keys
    except FileNotFoundError:
        logging.info(f"Файл {filename} не найден. Убедитесь, что создали файл с вашими ключами API.")
        raise
    except Exception as e:
        logging.info(f"Ошибка при чтении ключей API из {filename}: {e}")
        raise


# Чтение API-ключей
def read_api_keys(filename='api_keys.txt'):
    try:
        with open(filename, 'r') as file:
            api_keys = {}
            for line in file:
                key, value = line.strip().split('=')
                api_keys[key] = value
            return api_keys
    except FileNotFoundError:
        logging.error(f"Файл {filename} не найден. Убедитесь, что создали файл с вашими ключами API.")
        raise
    except Exception as e:
        logging.error(f"Ошибка при чтении ключей API из {filename}: {e}")
        raise

api_keys = read_api_keys()
api_key = api_keys.get('API_KEY')
api_secret = api_keys.get('API_SECRET')


# Функция для чтения белого списка из файла
def read_white_list(filename='white_list.txt'):
    with open(filename) as f:
        return [line.strip() for line in f]

if not api_key or not api_secret: # Проверка наличия ключей
    raise ValueError("Не найдены ключи API. Убедитесь, что в файле api_keys.txt указаны правильные API_KEY и API_SECRET.")

white_list = read_white_list() # Чтение белого списка

async def read_strategy(filename='strategy.txt'): # Чтение параметров стратегии из файла
    try:
        with open(filename, 'r') as file:
            strategy = {}
            for line in file:
                key, value = line.strip().split('=')
                strategy[key] = value
            return strategy
    except FileNotFoundError:
        logging.warning(f"Файл стратегии {filename} не найден. Используются значения по умолчанию.")
        return {}
    except Exception as e:
        logging.error(f"Ошибка при загрузке стратегии из {filename}: {e}")
        return {}

async def calculate_rsi(symbol: str, close_price: float):
    pass

async def save_strategy(strategy, filename='strategy.txt'):
    try:
        with open(filename, 'w') as file:
            for key, value in strategy.items():
                file.write(f"{key}={value}\n")
        logging.info(f"Стратегия сохранена в файл {filename}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении стратегии в файл {filename}: {e}")

# Глобальные переменные
buy_usdt_amount = 0
max_active_pairs = 0
active_pairs_count = 0
strategy_filename = 'strategy.txt'


# Чтение параметров стратегии из файла
async def read_strategy(filename='strategy.txt'):
    try:
        with open(filename, 'r') as file:
            strategy = {}
            for line in file:
                key, value = line.strip().split('=')
                strategy[key] = value
            return strategy
    except FileNotFoundError:
        logging.warning(f"Файл стратегии {filename} не найден. Используются значения по умолчанию.")
        return {}
    except Exception as e:
        logging.error(f"Ошибка при загрузке стратегии из {filename}: {e}")
        return {}



# Чтение параметров стратегии
async def main():
    strategy = await read_strategy()

    # Извлечение параметров RSI из стратегии
    rsi_period = int(strategy.get('rsi_period', 14))
    rsi_overbought = int(strategy.get('rsi_overbought', 70))
    rsi_oversold = int(strategy.get('rsi_oversold', 30))


    # Установка параметров RSI
    logging.info(f"RSI Period: {rsi_period}, Overbought: {rsi_overbought}, Oversold: {rsi_oversold}")

    rsi_period = int(strategy.get('rsi_period', 14))
    rsi_overbought = int(strategy.get('rsi_overbought', 70))
    rsi_oversold = int(strategy.get('rsi_oversold', 30))

    # Чтение параметров стратегии
    async def main():
        strategy = await read_strategy()

        # Извлечение параметров RSI из стратегии
        rsi_period = int(strategy.get('rsi_period', 14))
        rsi_overbought = int(strategy.get('rsi_overbought', 70))
        rsi_oversold = int(strategy.get('rsi_oversold', 30))

        # Установка параметров RSI
        logging.info(f"RSI Period: {rsi_period}, Overbought: {rsi_overbought}, Oversold: {rsi_oversold}")

    asyncio.run(main())
# Загрузка стратегии из файла
strategy = read_strategy()
default_rsi_period = 14  # Замените 14 на значение по умолчанию или другое, которое вы хотите использовать
rsi_period = strategy.get('rsi_period', default_rsi_period)

# Определение переменной "strategy"
rsi_overbought = int(strategy.get('rsi_overbought', 70))
rsi_oversold = int(strategy.get('rsi_oversold', 30))

# Установка параметров RSI
logging.info(f"RSI Period: {rsi_period}, Overbought: {rsi_overbought}, Oversold: {rsi_oversold}")

# Функция для чтения торгового депозита из файла
def read_trading_deposit(filename='trading_deposit.txt'):
    global buy_usdt_amount, max_active_pairs  # Объявляем как глобальные переменные

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            # Извлекаем числовое значение из первой строки
            trading_deposit = float(lines[0].split('\t')[0].strip())

            # Извлекаем числовое значение из второй строки
            max_active_pairs = int(lines[1].split('\t')[0].strip())

            # Обновляем переменные buy_usdt_amount и max_active_pairs
            buy_usdt_amount = trading_deposit

            return trading_deposit, max_active_pairs
    except FileNotFoundError:
        logging.info(f"Файл {filename} не найден. Обязательно создайте файл с торговым депозитом.")
        raise
    except ValueError as ve:
        logging.info(f"Ошибка при считывании торгового депозита из {filename}: {ve}")
        raise
    except Exception as e:
        logging.info(f"Другая ошибка при считывании торгового депозита из {filename}: {e}")
        raise


trading_deposit, max_active_pairs = read_trading_deposit()

buy_usdt_amount = trading_deposit
active_pairs_count = 0

# Установите уровень фиксации прибыли (в процентах) - сейчас 1%
profit_target_percent = 1.0

# Установите уровень плеча - сейчас x20
leverage = 20

# Инициализация ключей с binance
binance = ccxt.binance({    
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'future': True,
})

# Переменные для отслеживания торговых пар
active_pairs = set()
current_trades = {}


# Регистрация функции для закрытия соединения с биржей при завершении программы
@atexit.register
def close_binance():
    asyncio.run(close_binance_async())

async def close_binance_async():
    # Вы можете добавить сюда логику очистки, если это необходимо
    logging.info("Закрытие соединения с Binance.")

    global buy_usdt_amount, max_active_pairs  # Объявляем как глобальные переменные
    buy_usdt_amount = trading_deposit

# Создание DataFrame для хранения статистики
columns = ['Pair', 'Entry Time', 'Exit Time', 'Candle Count', 'Net Profit (USDT)', 'Exchange Fee (USDT)', 'RSI Entry', 'RSI Exit']
statistics_df = pd.DataFrame(columns=columns)

async def close_trade(symbol):
    try:
        position = await binance.fapiPrivateGetPositionRisk({'symbol': symbol})
        if position['positionAmt'] == '0':
            return
        side = 'SELL' if float(position['positionAmt']) > 0 else 'BUY'
        await binance.fapiPrivatePostOrder({
            'symbol': symbol,
            'type': 'MARKET',
            'side': side,
            'quantity': abs(float(position['positionAmt'])),
            'reduceOnly': True
        })
    except Exception as e:
        logging.info(f'Error closing trade for {symbol}: {e}')
        # Логирование ошибки, можно добавить дополнительную обработку по необходимости
        pass

async def on_kline(msg):
    logging.info(f"Получены данные о свече: {msg}")
    global current_trades, active_pairs_count

    try:
        kline_data = json.loads(msg)
        kline = kline_data['k']
        close_price = float(kline[4])  # Изменено: использование числового индекса

        symbol = kline_data['s']

        logging.info(f"Обработка свечи для {symbol}. Цена закрытия: {close_price}")

        if not symbol or symbol not in white_list or symbol not in current_trades or active_pairs_count >= max_active_pairs:
            return

        rsi = await calculate_rsi(symbol, close_price)

        if rsi < rsi_oversold and symbol not in current_trades and active_pairs_count < max_active_pairs:
            entry_time = datetime.now().strftime('%d,%m %H:%M:%S')
            logging.info(f"Сигнал на покупку для {symbol}. RSI: {rsi}")
            current_trade = {
                'symbol': symbol,
                'entry_time': entry_time,
                'entry_price': close_price,
                'rsi_entry': rsi,
                'buy_quantity': buy_usdt_amount / close_price,
                'profit_target_price': close_price * (1 + profit_target_percent / 100)
            }
            await check_and_set_leverage(symbol)
            active_pairs_count += 1
            await execute_buy_order(current_trade)

        elif symbol in current_trades and close_price >= current_trades[symbol]['profit_target_price']:
            exit_time = datetime.now().strftime('%d,%m %H:%M:%S')
            logging.info(f"Цель по прибыли достигнута для {symbol}. RSI: {rsi}")
            current_trades[symbol]['exit_time'] = exit_time
            current_trades[symbol]['exit_price'] = close_price
            current_trades[symbol]['rsi_exit'] = rsi
            await calculate_and_export_statistics(current_trades[symbol])
            del current_trades[symbol]
            active_pairs_count -= 1

        logging.info(f"Символ: {symbol}, Цена закрытия: {close_price}, RSI: {rsi}")
    except Exception as e:
        logging.info(f"Ошибка при обработке свечи: {e}")

async def calculate_rsi(symbol, close_price): # Вычисление RSI
    try:
        klines = await binance.fapiPublic_klines(symbol=symbol, interval='5m')      # Получение данных потоковых свечей для futures веб-сокета

        closes = [float(x[4]) for x in klines]  # индекс для получения цены закрытия

    
        rsi = talib.RSI(closes, timeperiod=int(rsi_period))     # Вычисление RSI

        return rsi[-1]  # Вернуть последнее значение RSI
       
    except Exception as e:
        logging.info(f"Ошибка при расчете RSI для {symbol}: {e}")
        return None

async def check_and_set_leverage(symbol): # Проверка и установка плеча
    try:
        symbol_info = await binance.fapiPublic_get_symbol(symbol=symbol)  # Получить информацию о плече для пары
        max_leverage = symbol_info['leverage']  # Получить максимальное кредитное плечо для пары

        global leverage # Объявляем как глобальную переменную
        if leverage > max_leverage: # Если установленное плечо больше максимального, установить максимальное
            logging.info(f"установленное плечо {leverage} для {symbol} превышает максимально допустимое значение. Установить максимальное кредитное плечо: {max_leverage}.")
            leverage = max_leverage
    except Exception as e:
        logging.info(f"Error checking and setting leverage: {e}")

async def execute_buy_order(trade): # Выполнение покупки
    try:
        order = await binance.fapiPrivate_post_order({      
            'symbol': trade['symbol'],
            'side': 'BUY',
            'type': 'MARKET',
            'quantity': trade['buy_quantity'],
            'leverage': leverage  # Устанавливаем плечо x20
        })
        logging.info(f"Successfully bought {trade['buy_quantity']} {trade['symbol']}. Order: {order}")
        current_trades[trade['symbol']] = trade
        current_trades[trade['symbol']]['profit_target_price'] = trade['entry_price'] * (1 + profit_target_percent / 100)
        active_pairs.add(trade['symbol'])  # Добавляем в множество активных пар
    except Exception as e:
        logging.info(f"Error buying: {e}")
        await close_trade(trade['symbol'])         # Если произошла ошибка при покупке, закрываем сделку

    finally:
        active_pairs.remove(trade['symbol'])  # Удаляем из множества активных пар после покупки


async def calculate_trade_metrics(entry_price, exit_price, buy_quantity, commission_rate, is_sell):     # Расчет торговых параметров
    try:
        # Рассчитываем комиссию в зависимости от типа операции (BUY или SELL)
        commission_fee = exit_price * buy_quantity * commission_rate if is_sell else entry_price * buy_quantity * commission_rate

        # Рассчитываем чистую прибыль с учетом комиссии
        net_profit = (exit_price - entry_price) * buy_quantity - commission_fee

        return net_profit, commission_fee
    except Exception as e:
        logging.info(f"Ошибка при расчете торговых параметров: {e}")
        return None, None

async def calculate_and_export_statistics(trade):
    try:
        entry_price = trade['entry_price']
        exit_price = trade['exit_price']
        symbol = trade['symbol']

        position_info = await binance.fapiPrivateGetPositionRisk({'symbol': symbol})
        commission_rate = float(position_info.get('commissionRate', 0.0004))

        klines = await binance.fapiPublic_klines(symbol=symbol, interval='5m')
        candle_count = len(klines)

        is_sell = trade['rsi_exit'] is not None

        # Рассчитываем комиссию в зависимости от типа операции (BUY или SELL)
        buy_quantity = trade['buy_quantity']
        if is_sell:
            commission_fee = exit_price * buy_quantity * commission_rate
        else:
            commission_fee = entry_price * buy_quantity * commission_rate

        net_profit = (exit_price - entry_price) * buy_quantity - commission_fee

        # Записываем статистику в DataFrame
        statistics_df.loc[len(statistics_df)] = [
            symbol, trade['entry_time'], trade['exit_time'], candle_count,
            net_profit, commission_fee, trade['rsi_entry'], trade['rsi_exit']
        ]

        # Экспортируем статистику в текстовый файл
        filename = 'trading_statistics.txt'
        with open(filename, 'a') as file:
            file.write(f"Symbol: {symbol}, Commission Fee: {commission_fee}\n")
        statistics_df.to_csv(filename, sep='\t', index=False)

    except Exception as e:
        logging.info(f"Ошибка при расчете и экспорте статистики: {e}")
    finally:
        active_pairs.remove(symbol)  # Удаляем из множества активных пар после продажи


async def calculate_and_export_statistics_after_sell(trade):
    try:
        entry_price = trade['entry_price']
        exit_price = trade['exit_price']
        symbol = trade['symbol']

        position_info = await binance.fapiPrivateGetPositionRisk({'symbol': symbol})  # Получаем информацию о позиции для расчета комиссии
        commission_rate = float(position_info.get('commissionRate', 0.0004))

        klines = await binance.fapiPublic_klines(symbol=symbol, interval='5m')  # Получаем информацию о свечах для расчета количества свечей
        candle_count = len(klines)

        is_sell = trade['rsi_exit'] is not None  # Определяем, является ли это продажей

        # Рассчитываем комиссию в зависимости от типа операции (BUY или SELL)
        buy_quantity = trade['buy_quantity']
        if trade['rsi_exit'] is not None:
            commission_fee = exit_price * buy_quantity * commission_rate  # Если есть информация о выходе из сделки, рассчитываем комиссию для продажи
        else:
            commission_fee = entry_price * buy_quantity * commission_rate  # Иначе рассчитываем комиссию для покупки

        net_profit = (exit_price - entry_price) * buy_quantity - commission_fee  # Рассчитываем чистую прибыль с учетом комиссии

        # Записываем статистику в DataFrame
        statistics_df.loc[len(statistics_df)] = [
            symbol, trade['entry_time'], trade['exit_time'], candle_count,
            net_profit, commission_fee, trade['rsi_entry'], trade['rsi_exit']
        ]

        # Экспортируем статистику в текстовый файл
        filename = 'trading_statistics.txt'
        with open(filename, 'a') as file:
            file.write(f"Symbol: {symbol}, Commission Fee: {commission_fee}\n")  # Записываем статистику в текстовый файл
        statistics_df.to_csv(filename, sep='\t', index=False)

    except Exception as e:  # Логирование ошибки, можно добавить дополнительную обработку по необходимости
        logging.info(f"Ошибка при расчете и экспорте статистики: {e}")
    finally:
        active_pairs.remove(symbol)  # Удаляем из множества активных пар после продажи



async def kline_listener(symbol, loop):
    while True:
        try:
            klines = await binance.fapiPublic_klines(symbol=symbol, interval='5m')
            for kline in klines:
                await on_kline(json.dumps({'k': kline, 's': symbol}))
            await asyncio.sleep(1)
        except ccxt.NetworkError as e:
            logging.info(f'Сетевая ошибка: {e}')
            await asyncio.sleep(5)  # При возникновении ошибки сети ждем 5 секунд и повторяем
        except KeyboardInterrupt:
            logging.info(f'Прерывание с клавиатуры. Завершение программы.')
            await close_binance_async()
            sys.exit(0)
        except Exception as e:
            logging.info(f'Ошибка: {e}')
            if symbol in current_trades:
                await close_trade(symbol)

async def main():
    try:
        loop = asyncio.get_event_loop()

        # Добавление кнопки "Старт"
        start_button = input("Для начала работы введите 'start': ")
        if start_button.lower() != 'start':
            logging.info("Работа программы отменена.")
        else:
            # Загрузка стратегии из файла
            strategy = await read_strategy()
            rsi_period = strategy.get('rsi_period', default_rsi_period)

            # Включение/выключение ограничителя по волатильности
            volatility_enabled = input(f"Включить ограничитель по волатильности? ({strategy.get('volatility_enabled', 'yes')}/no): ")
            if volatility_enabled.lower() == 'yes':
                strategy['volatility_enabled'] = 'yes'
                min_volatility = float(input(f"Введите минимальное значение волатильности ({strategy.get('min_volatility', 0.5)}): "))
                max_volatility = float(input(f"Введите максимальное значение волатильности ({strategy.get('max_volatility', 2.0)}): "))
                strategy['min_volatility'] = str(min_volatility)
                strategy['max_volatility'] = str(max_volatility)
            else:
                strategy['volatility_enabled'] = 'no'

            # Выбор таймфрейма
            timeframe = input(f"Выберите таймфрейм для анализа ({strategy.get('timeframe', '5m')}): ")
            strategy['timeframe'] = timeframe

            # Сохранение стратегии в файл
            await save_strategy(strategy)

            # Добавление опции очистки лог-файла
            clear_log_button = input("Очистить лог-файл перед запуском? (yes/no): ")
            if clear_log_button.lower() == 'yes':
                clear_logfile()

            tasks = [kline_listener(symbol, loop) for symbol in white_list]
            tasks.append(save_trade_data({'test': 'data'}))
            await asyncio.gather(*tasks)

    except KeyboardInterrupt:
        logging.info('Программа прервана.')
    finally:
        await close_binance_async()

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
        loop.run_until_complete(close_binance_async())
