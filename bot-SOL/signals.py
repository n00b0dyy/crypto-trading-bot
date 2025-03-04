def generate_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest  # Poprzednia świeca

    # BUY: gdy krótkoterminowa średnia przecina długoterminową w górę
    if prev["short_ma"] < prev["long_ma"] and latest["short_ma"] > latest["long_ma"]:
        return "BUY"

    # SELL: gdy krótkoterminowa średnia przecina długoterminową w dół
    elif prev["short_ma"] > prev["long_ma"] and latest["short_ma"] < latest["long_ma"]:
        return "SELL"

    return "HOLD"
