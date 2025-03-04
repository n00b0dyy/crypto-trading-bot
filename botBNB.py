import pandas as pd
from indicators import calculate_moving_averages
from signals import generate_signal

# Wczytanie danych historycznych
df = pd.read_csv("historical_dataBNB.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Obliczanie średnich kroczących
df = calculate_moving_averages(df, short_period=50, long_period=100, ma_type="EMA")

# Prowizja Binance (0.10% = 0.001, można zmienić na niższą jeśli używasz BNB)
TRADING_FEE_PERCENT = 0.10 / 100  # 0.10%

# Symulacja handlu
balance = 1000  # Początkowy kapitał w USDT
position = None
trade_history = []
STOP_LOSS_PERCENT = 0.08  # 5% Stop-Loss
TAKE_PROFIT_PERCENT = 0.15  # 10% Take-Profit
INVESTMENT_PERCENT = 0.10  # 10% kapitału na każdą transakcję

# Liczniki trafionych Stop-Loss i Take-Profit
stop_loss_hits = 0
take_profit_hits = 0

# Funkcja do naliczania prowizji
def apply_fee(amount):
    return amount * (1 - TRADING_FEE_PERCENT)

for index, row in df.iterrows():
    price = row["close"]

    if position is not None:
        # Sprawdzamy czy cena osiągnęła Stop-Loss
        if price <= stop_loss:
            balance += apply_fee(position * price)  # Prowizja przy sprzedaży po SL
            position = None
            stop_loss_hits += 1  # Zliczamy trafione SL
            trade_history.append([row["timestamp"], "STOP-LOSS", price, None, None, balance, position])
            print(f"Stop-Loss osiągnięty ({price:.2f}). Zamykam pozycję.")

        # Sprawdzamy czy cena osiągnęła Take-Profit
        elif price >= take_profit:
            balance += apply_fee(position * price)  # Prowizja przy sprzedaży po TP
            position = None
            take_profit_hits += 1  # Zliczamy trafione TP
            trade_history.append([row["timestamp"], "TAKE-PROFIT", price, None, None, balance, position])
            print(f"Take-Profit osiągnięty ({price:.2f}). Zamykam pozycję.")

    # Otwieramy nową pozycję tylko wtedy, gdy NIE mamy aktywnej transakcji
    elif position is None:
        signal = generate_signal(df.iloc[:index+1])  # Pobieramy sygnał
        if signal == "BUY":
            investment_amount = apply_fee(balance * INVESTMENT_PERCENT)  # Uwzględniamy prowizję
            position = investment_amount / price  # Ile BNB kupujemy
            balance -= investment_amount  # Odejmujemy wykorzystany kapitał
            stop_loss = price * (1 - STOP_LOSS_PERCENT)  # SL = 5% poniżej ceny wejścia
            take_profit = price * (1 + TAKE_PROFIT_PERCENT)  # TP = 10% powyżej ceny wejścia
            trade_history.append([row["timestamp"], "BUY", price, stop_loss, take_profit, balance, position])
            print(f"Kupiono {position:.4f} BNB po cenie {price:.2f}. SL: {stop_loss:.2f}, TP: {take_profit:.2f}")

# Zapis wyników do pliku CSV
trade_results = pd.DataFrame(trade_history, columns=["timestamp", "action", "price", "stop_loss", "take_profit", "balance", "position"])
trade_results.to_csv("trade_results.csv", index=False)

# Podsumowanie testu
print("\n========== PODSUMOWANIE TESTU ==========")
print(f"Końcowe saldo: {balance:.2f} USDT")
print(f"Liczba trafionych Stop-Loss: {stop_loss_hits}")
print(f"Liczba trafionych Take-Profit: {take_profit_hits}")
print(f"Całkowita liczba transakcji: {len(trade_history) // 2}")  # Każda transakcja to BUY + SL/TP
