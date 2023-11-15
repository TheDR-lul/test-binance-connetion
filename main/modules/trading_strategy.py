import json
import logging
from datetime import datetime

class TradingStrategy:
    def __init__(self, binance_client):
        self.binance_client = binance_client
        self.strategy = {}

    async def load_strategy(self):
        try:
            with open('strategy.json', 'r') as file:
                self.strategy = json.load(file)
        except FileNotFoundError:
            logging.info("Файл стратегии не найден. Используется стратегия по умолчанию.")
            self.strategy = self.default_strategy()
            await self.save_strategy()

    async def save_strategy(self):
        try:
            with open('strategy.json', 'w') as file:
                json.dump(self.strategy, file, indent=4)
        except Exception as e:
            logging.info(f"Ошибка при сохранении стратегии: {e}")

    def default_strategy(self):
        return {
            'rsi_period': 14,
            'rsi_overbought': 70,
            'rsi_oversold': 30,
            'profit_target_percent': 1.0,
            'commission_rate': 0.0004,
            'default_rsi_period': 14,
            'volatility_enabled': 'yes',
            'min_volatility': 0.5,
            'max_volatility': 2.0,
            'timeframe': '5m'
        }

    async def set_strategy_param(self, param_name, param_value):
        try:
            self.strategy[param_name] = param_value
            await self.save_strategy()
            logging.info(f"Параметр {param_name} установлен в значение {param_value}.")
        except Exception as e:
            logging.info(f"Ошибка при установке параметра стратегии: {e}")

    async def get_strategy_param(self, param_name):
        return self.strategy.get(param_name)

    async def clear_logfile(self):
        try:
            open('trading_log.txt', 'w').close()
            logging.info("Лог-файл успешно очищен.")
        except Exception as e:
            logging.info(f"Ошибка при очистке лог-файла: {e}")

    async def set_trading_symbol(self, symbol):
        try:
            self.strategy['trading_symbol'] = symbol
            await self.save_strategy()
            logging.info(f"Установлен символ для торговли: {symbol}.")
        except Exception as e:
            logging.info(f"Ошибка при установке символа для торговли: {e}")

    async def get_trading_symbol(self):
        return self.strategy.get('trading_symbol')

    async def get_strategy(self):
        return self.strategy

    async def update_strategy(self, new_strategy):
        try:
            self.strategy.update(new_strategy)
            await self.save_strategy()
            logging.info("Стратегия успешно обновлена.")
        except Exception as e:
            logging.info(f"Ошибка при обновлении стратегии: {e}")

    async def is_volatility_enabled(self):
        return self.strategy.get('volatility_enabled') == 'yes'
    