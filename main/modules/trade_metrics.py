import ccxt
import logging

class TradeMetrics:
    def __init__(self):
        self.binance_client = ccxt.binance()  # Используем ccxt для взаимодействия с Binance

    async def calculate_trade_metrics(self, trade):
        try:
            entry_price = trade['entry_price']
            exit_price = trade['exit_price']
            buy_quantity = trade['buy_quantity']
            symbol = trade['symbol']

            position_info = await self.binance_client.fapiPrivateGetPositionRisk({'symbol': symbol})
            commission_rate = float(position_info.get('commissionRate', 0.0004))

            commission_fee = exit_price * buy_quantity * commission_rate
            net_profit = (exit_price - entry_price) * buy_quantity - commission_fee

            return {
                'symbol': symbol,
                'entry_time': trade['entry_time'],
                'exit_time': trade['exit_time'],
                'candle_count': trade['candle_count'],
                'net_profit': net_profit,
                'commission_fee': commission_fee,
                'rsi_entry': trade['rsi_entry'],
                'rsi_exit': trade['rsi_exit']
            }
        except Exception as e:
            logging.info(f"Ошибка при расчете метрик сделки: {e}")
            raise
        