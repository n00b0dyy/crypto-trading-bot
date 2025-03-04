import ccxt
import pandas as pd
import time

# Inicjalizacja Binance API
exchange = ccxt.binance()

# Parametry pobierania danych
symbol = "BNB/USDT"  # Para walutowa
timeframe = "5m"  # Można zmienić na '15m', '4h', '1d'
limit_per_request = 1000  # Maksymalna liczba świec na jedno zapytanie
max_candles = 333000  # Ile świec chcesz pobrać?
all_candles = []  # Lista do przechowywania świec

# Ustawienie początkowego timestampa
since = exchange.parse8601("2021-01-01T00:00:00Z") 

# Pobieranie danych w pętli
while len(all_candles) < max_candles:
    print(f"Pobieranie świec... {len(all_candles)}/{max_candles}")

    # Pobieranie świec
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit_per_request)

    if not bars:
        print("Brak nowych danych, kończenie pobierania.")
        break  # Przerwanie, jeśli Binance nie zwraca więcej danych

    all_candles.extend(bars)

    # Aktualizacja "since" na ostatnią pobraną świecę + 1 ms
    since = bars[-1][0] + 1

    # Krótkie opóźnienie, aby uniknąć limitów API
    time.sleep(0.5)

# Tworzenie DataFrame
df = pd.DataFrame(all_candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# Zapis do CSV
df.to_csv("historical_dataBNB.csv", index=False)

print(f"Pobrano {len(df)} świec.")
print(df.head())
