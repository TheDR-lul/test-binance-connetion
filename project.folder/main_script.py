from modules import binance_module, strategy_module, statistics_module, utils_module

async def main():
    try:
        loop = asyncio.get_event_loop()

        start_button = input("Для начала работы введите 'start': ")
        if start_button.lower() != 'start':
            logging.info("Работа программы отменена.")
        else:
            strategy = await strategy_module.read_strategy()
            rsi_period = strategy_module.get_rsi_period(strategy)

            volatility_enabled = input(f"Включить ограничитель по волатильности? "
                                       f"({strategy_module.get_volatility_enabled(strategy)}/no): ")
            strategy_module.set_volatility_options(strategy, volatility_enabled)

            timeframe = input(f"Выберите таймфрейм для анализа ({strategy_module.get_timeframe(strategy)}): ")
            strategy_module.set_timeframe(strategy, timeframe)

            await strategy_module.save_strategy(strategy)

            clear_log_button = input("Очистить лог-файл перед запуском? (yes/no): ")
            if clear_log_button.lower() == 'yes':
                utils_module.clear_logfile()

            tasks = [binance_module.kline_listener(symbol, loop) for symbol in binance_module.white_list]
            tasks.append(utils_module.save_trade_data({'test': 'data'}))
            await asyncio.gather(*tasks)

    except KeyboardInterrupt:
        logging.info('Программа прервана.')
    finally:
        await utils_module.close_binance_async()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()

        start_button = input("Для начала работы введите 'start': ")
        if start_button.lower() != 'start':
            logging.info("Работа программы отменена.")
        else:
            loop.run_until_complete(main())

    except KeyboardInterrupt:
        logging.info('Программа прервана.')
    finally:
        loop.run_until_complete(utils_module.close_binance_async())
        