import backtrader as bt
from my_strategy import MyStrategy
from data_feed import MyDataFeed
import pandas as pd

if __name__ == '__main__':
    # define parameters
    start_cash = 10000.0 
    commission_rate = 0.002
    stop_loss_pct = 0.05
    trailing_stop_loss_pct = 0.02

    # Create an instance of Cerebro
    cerebro = bt.Cerebro()

    # Add data feed to Cerebro
    data = MyDataFeed()
    cerebro.adddata(data)

    # Add strategy to Cerebro
    cerebro.addstrategy(
        MyStrategy,
        fromdate=pd.Timestamp('2015-01-01'),
        todate=pd.Timestamp('2021-03-31'),
        rsi_period=14,
        rsi_upper=70,
        rsi_lower=30,
        macd_fast=12,
        macd_slow=26,
        macd_signal=9,
        stop_loss_pct=stop_loss_pct,
        trailing_stop_loss_pct=trailing_stop_loss_pct
    )

    # Set broker parameters
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=commission_rate)

    # Run the backtest
    cerebro.run()

    # Print final results
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - start_cash
    print('Final Portfolio Value: ${}'.format(portvalue))
    print('P/L: ${}'.format(pnl))

    # Save results
    cerebro.broker.save()

    # Plot the results
    cerebro.plot(style='candlestick', barup='green', bardown='red')
