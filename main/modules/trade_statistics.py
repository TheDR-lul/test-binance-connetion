import pandas as pd
import logging
import json

class TradeStatistics:
    def __init__(self):
        self.statistics_df = pd.DataFrame(columns=['Symbol', 'Entry Time', 'Exit Time', 'Candle Count', 'Net Profit',
                                                   'Commission Fee', 'RSI Entry', 'RSI Exit'])

    async def calculate_and_export_statistics_after_sell(self, trade):
        try:
            entry_price = trade['entry_price']
            exit_price = trade['exit_price']
            buy_quantity = trade['buy_quantity']
            symbol = trade['symbol']

            position_info = await self.binance_client.fapiPrivateGetPositionRisk({'symbol': symbol})
            commission_rate = float(position_info.get('commissionRate', 0.0004))

            commission_fee = exit_price * buy_quantity * commission_rate
            net_profit = (exit_price - entry_price) * buy_quantity - commission_fee

            self.statistics_df = self.statistics_df.append({
                'Symbol': symbol,
                'Entry Time': trade['entry_time'],
                'Exit Time': trade['exit_time'],
                'Candle Count': trade['candle_count'],
                'Net Profit': net_profit,
                'Commission Fee': commission_fee,
                'RSI Entry': trade['rsi_entry'],
                'RSI Exit': trade['rsi_exit']
            }, ignore_index=True)

            await self.export_statistics_to_file(trade)
        except Exception as e:
            logging.info(f"Ошибка при расчете и экспорте статистики: {e}")
            raise

    async def export_statistics_to_file(self, trade):
        try:
            filename = 'trading_statistics.txt'
            with open(filename, 'a') as file:
                file.write(f"Symbol: {trade['symbol']}, Commission Fee: {trade['commission_fee']}\n")
            self.statistics_df.to_csv(filename, sep='\t', index=False)
        except Exception as e:
            logging.info(f"Ошибка при экспорте статистики в файл: {e}")
            raise
        