from surmount.base_class import Strategy, TargetAllocation
from surmount.data import ohlcv

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ"]  # Utilizzare ETF azionari statunitensi preferiti
        self.data_list = []

    @property
    def interval(self):
        return "1day"  # Analisi su base giornaliera

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def calculate_ibs(self, data):
        """Calcola l'Internal Bar Strength (IBS) per un ticker."""
        low = data['low']
        high = data['high']
        close = data['close']
        # Formula IBS = (Chiusura - Min) / (Max - Min)
        return (close - low) / (high - low) if (high - low) > 0 else 0.5

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            daily_data = data["ohlcv"][-1][ticker]  # Ultimi dati disponibili

            # Calcola l'IBS
            ibs = self.calculate_ibs(daily_data)

            # Strategia di allocazione in base all'IBS
            # Valori IBS bassi (<0.3) indicano un potenziale acquisto (reversione alla media prevista)
            # Valori IBS alti (>0.7) suggeriscono di evitare acquisti o eventualmente vendere
            if ibs < 0.3:
                allocation_dict[ticker] = 1 / len(self.tickers)  # Allocazione equa
            elif ibs > 0.7:
                allocation_dict[ticker] = 0  # Nessuna allocazione
            else:
                allocation_dict[ticker] = 0.5 / len(self.tickers)  # Allocatione neutrale

        return TargetAllocation(allocation_value=allocation_dict)

    @property
    def metadata(self):
        # Metadata per identificare i giorni della settimana e adattare la strategia
        # soprattutto concentrarsi su lunedì o in periodi ad alta volatilità
        return {"include_weekdays": [1], "volatility_threshold": None}