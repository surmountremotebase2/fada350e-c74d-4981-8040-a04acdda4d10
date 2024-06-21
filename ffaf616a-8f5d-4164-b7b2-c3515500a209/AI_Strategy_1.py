from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Definire i ticker di interesse: SPY per l'ETF S&P 500, SHY per l'ETF Treasury Bond a 1-3 anni
        self.tickers = ["SPY", "SHY", "TQQQ"]

    @property
    def interval(self):
        # Intervallo settimanale per il calcolo dell'RSI
        return "1day"

    @property
    def assets(self):
        # Asset coinvolti nella strategia di trading
        return self.tickers

    @property
    def data(self):
        # Nessun dato aggiuntivo richiesto oltre a quello fornito di default
        return []

    def run(self, data):
        # Calcolare l'RSI settimanale per TQQQ
        tqqq_rsi = RSI("TQQQ", data["ohlcv"], 10)  # Utilizzando un periodo di 10 settimane per l'RSI

        # Inizializzare allocation_dict con nessuna allocazione
        allocation_dict = {"SPY": 1.0, "SHY": 0.0}

        if tqqq_rsi is not None and len(tqqq_rsi) > 0:
            current_rsi = tqqq_rsi[-1]  # Ottenere il valore RSI più recente

            # Se RSI > 80, spostare il 100% a SHY
            if current_rsi > 80:
                allocation_dict["SHY"] = 1.0
                allocation_dict["SPY"] = 0.0
            # Se RSI < 40, spostare il 100% a SPY
            elif current_rsi < 40:
                allocation_dict["SPY"] = 1.0
                allocation_dict["SHY"] = 0.0

        return TargetAllocation(allocation_dict)


        return TargetAllocation(allocation_dict)