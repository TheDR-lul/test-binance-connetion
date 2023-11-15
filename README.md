# ccxt
simple_rsi_v4.2.py

Этот скрипт реализует стратегию торговли на основе индикатора RSI на бирже Binance с использованием библиотеки ccxt.

Структура кода:
1. Импорт библиотек и установка параметров
2. Определение функций
    2.1. on_kline - обработка свечей
    2.2. calculate_rsi - вычисление RSI
    2.3. check_and_set_leverage - проверка и установка плеча
    2.4. execute_buy_order - выполнение покупки
    2.5. calculate_trade_metrics - расчет торговых параметров
    2.6. calculate_and_export_statistics - расчет и экспорт статистики после покупки
    2.7. calculate_and_export_statistics_after_sell - расчет и экспорт статистики после продажи
    2.8. kline_listener - слушатель свечей
    2.9. main - основная функция программы
3. Запуск программы

Параметры скрипта:
- `white_list` (список): Белый список торговых пар, на которых будет выполняться стратегия.
- `leverage` (float): Уровень плеча для торговли.
- `profit_target_percent` (float): Процент цели прибыли для закрытия сделки.
- `rsi_period` (int): Период расчета RSI.
- `rsi_overbought` (int): Уровень RSI, при достижении которого считается, что актив может быть перекуплен.
- `rsi_oversold` (int): Уровень RSI, при достижении которого считается, что актив может быть перепродан.
- `volatility_enabled` (str): Включение/выключение ограничителя по волатильности ('yes'/'no').
- `min_volatility` (float): Минимальное значение волатильности.
- `max_volatility` (float): Максимальное значение волатильности.
- `timeframe` (str): Таймфрейм для анализа свечей (например, '5m').

Логика работы функций:
1. **on_kline(symbol, close_price)**:
    - Обработка свечи для определенного символа.
    - Вычисление RSI.
    - Проверка условий для выполнения покупки или продажи.
    - Запись статистики после завершения сделки.

2. **calculate_rsi(symbol, close_price)**:
    - Вычисление RSI для заданного символа.

3. **check_and_set_leverage(symbol)**:
    - Проверка и установка уровня плеча в соответствии с максимально допустимым значением для пары.

4. **execute_buy_order(trade)**:
    - Выполнение покупки на основе переданных данных о сделке.

5. **calculate_trade_metrics(entry_price, exit_price, buy_quantity, commission_rate, is_sell)**:
    - Расчет торговых параметров (чистая прибыль, комиссия).

6. **calculate_and_export_statistics(trade)**:
    - Расчет и экспорт статистики после покупки.

7. **calculate_and_export_statistics_after_sell(trade)**:
    - Расчет и экспорт статистики после продажи.

8. **kline_listener(symbol, loop)**:
    - Бесконечный цикл прослушивания изменений в данных свечей.

9. **main()**:
    - Основная функция программы, запускающая слушателя свечей и другие задачи.

Запуск программы:
- Сначала необходимо ввести "start" для начала работы программы.
- Затем программа загрузит стратегию из файла, установит параметры и начнет слушать изменения в данных свечей.

Примечания:
- Рекомендуется тестировать стратегию на демонстрационном счете перед использованием в реальных условиях.
"""






# Инструкция по заполнению текстовых документов для скрипта simple_rsi
## 1. Стратегия (strategy.txt)

В этом документе вы указываете параметры вашей торговой стратегии.

Пример:

```
{
  "rsi_period": 14,
  "rsi_overbought": 70,
  "rsi_oversold": 30,
  "volatility_enabled": "yes",
  "min_volatility": 0.5,
  "max_volatility": 2.0,
  "timeframe": "5m"
}
```
2. Белый список (whitelist.txt)
В этом документе вы перечисляете символы (торговые пары), на которых будет работать стратегия.

```
BTC/USDT
ETH/USDT
BNB/USDT
```


3.  Хранилище ключей (api_keys.txt)
   Вам нужно создать файл api_keys.txt в том же каталоге, где находится ваш скрипт, и добавить в него свои ключи API в формате:


```
API_KEY=ваш_ключ
API_SECRET=ваш_секретный_ключ
```
позаботьтесь о вашей безопастности, ключи пока в открытом виде! 
