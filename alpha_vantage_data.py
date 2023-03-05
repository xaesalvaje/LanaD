import backtrader as bt
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

class AlphaVantageData(bt.feeds.PandasData):
    params = (
        ('api_key', 'D0XPFM4TVVEVHCLF'),
        ('symbol', 'BTC'),
        ('output_format', 'pandas'),
        ('datatype', 'csv'),
        ('adj_close', True),
        ('fromdate', None),
        ('todate', None),
        ('name', None),
    )

    def __init__(self):
        ts = TimeSeries(key=self.params.api_key, output_format=self.params.output_format)
        data, meta_data = ts.get_daily_adjusted(symbol=self.params.symbol, outputsize='full')

        data = {k: [v] for k, v in data.items()}
        data['datetime'] = meta_data['date']
        data['openinterest'] = 0

        df = pd.DataFrame(data)
        df.set_index('datetime', inplace=True)
        df.index = pd.to_datetime(df.index)

        if self.params.fromdate:
            df = df.loc[self.params.fromdate:]
        if self.params.todate:
            df = df.loc[:self.params.todate]

        super().__init__(dataname=df, name=self.params.name) 

    def _load_data(self, ts):
        raw_data, meta_data = ts.get_daily_adjusted(self.params.dataname, outputsize='full')
        raw_data = raw_data.rename(columns={'1. open': 'open',
                                             '2. high': 'high',
                                             '3. low': 'low',
                                             '4. close': 'close',
                                             '5. adjusted close': 'adj_close',
                                             '6. volume': 'volume',
                                             '7. dividend amount': 'dividend',
                                             '8. split coefficient': 'split_coeff'})

        if self.params.timeframe == bt.TimeFrame.Days and self.params.compression == 1:
            self._frame = raw_data
        else:
            self._frame = self._compress(raw_data)

        self._adjust_columns()

    def _compress(self, data):
        ohlcv_dict = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'adj_close': 'last',
            'volume': 'sum',
            'dividend': 'sum',
            'split_coeff': 'last'
        }
        resampled = data.resample(self.params.timeframe).agg(ohlcv_dict)