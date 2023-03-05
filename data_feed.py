from backtrader.feeds import PandasData
import pandas as pd
class MyDataFeed(PandasData):
    params = (
        ("datetime", None),
        ("open", "Open"),
        ("high", "High"),
        ("low", "Low"),
        ("close", "Close"),
        ("volume", "Volume_(BTC)"),
        ("openinterest", None),
    )

    def __init__(self):
        df = pd.read_csv("1min_data.csv", parse_dates=True, index_col="Timestamp")
        df.dropna(inplace=True)

        # Convert the open, high, low, close columns to float
        df["Open"] = df["Open"].astype(float) 
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume_(BTC)"] = df["Volume_(BTC)"].astype(float)
        df["Volume_(Currency)"] = df["Volume_(Currency)"].astype(float)
        df["Weighted_Price"] = df["Weighted_Price"].astype(float)

        super(MyDataFeed, self).__init__(dataname=df)
        
        if not hasattr(self, "dataname"):
            raise ValueError("dataname not set in superclass constructor")

        self.datetime = self.dataname.index[0]
        self.open = self.dataname["Open"]
        self.high = self.dataname["High"]
        self.low = self.dataname["Low"]
        self.close = self.dataname["Close"]
