import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie wyników strategii i danych historycznych
df = pd.read_csv("historical_dataSOL.csv")
trades = pd.read_csv("trade_results.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])
trades["timestamp"] = pd.to_datetime(trades["timestamp"])

# Wykres cenowy
plt.figure(figsize=(14, 7))
plt.plot(df["timestamp"], df["close"], label="Cena zamknięcia", color="black", alpha=0.6)

# Rysowanie średnich kroczących
plt.plot(df["timestamp"], df["short_ma"], label="Krótkoterminowa MA (50)", color="blue", linestyle="dashed")
plt.plot(df["timestamp"], df["long_ma"], label="Długoterminowa MA (100)", color="red", linestyle="dashed")

# Oznaczenie sygnałów BUY (zielone strzałki)
buy_signals = trades[trades["action"] == "BUY"]
plt.scatter(buy_signals["timestamp"], buy_signals["price"], marker="^", color="green", label="BUY", zorder=3)

# Oznaczenie sygnałów SELL (czerwone strzałki)
sell_signals = trades[trades["action"] == "SELL"]
plt.scatter(sell_signals["timestamp"], sell_signals["price"], marker="v", color="red", label="SELL", zorder=3)

# Oznaczenie Stop-Loss (czerwone punkty) i Take-Profit (zielone punkty)
stop_loss_hits = trades[trades["action"] == "STOP-LOSS"]
take_profit_hits = trades[trades["action"] == "TAKE-PROFIT"]

plt.scatter(stop_loss_hits["timestamp"], stop_loss_hits["price"], color="red", label="STOP-LOSS", marker="x", zorder=3)
plt.scatter(take_profit_hits["timestamp"], take_profit_hits["price"], color="green", label="TAKE-PROFIT", marker="o", zorder=3)

# Konfiguracja wykresu
plt.xlabel("Czas")
plt.ylabel("Cena SOL/USDT")
plt.title("Strategia przecięcia średnich kroczących – Sygnały BUY/SELL")
plt.legend()
plt.grid()

# Wyświetlenie wykresu
plt.show()
