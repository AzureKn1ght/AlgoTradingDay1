import numpy as np
import pandas as pd

class BASS_Calc(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 14)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.AddEquity("SPY", Resolution.Daily)
        self.AddEquity("TSLA", Resolution.Daily)


    # def OnData(self, data):
    #     '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
    #         Arguments:
    #             data: Slice object keyed by symbol containing the stock data
    #     '''

    #     # if not self.Portfolio.Invested:
    #     #    self.SetHoldings("SPY", 1)
        
        
    def OnEndOfAlgorithm(self):
        # call historical data from QC database
        history_spy = self.History(self.Symbol("SPY"), 30, Resolution.Daily)
        # extract all the close prices and convert it to a list 
        history_spy = history_spy["close"].tolist()
        # calculate absolute return of SPY
        spy_abs_return = (history_spy[-1] - history_spy[0]) / history_spy[0]
        # [-1] index gives the last value in the list
        
        # do the same by for TSLA
        history_tsla = self.History(self.Symbol("TSLA"), 30, Resolution.Daily)
        history_tsla = history_tsla["close"].tolist()
        tsla_abs_return = (history_tsla[-1] - history_tsla[0]) / history_tsla[0]
        
        # make a dataframe for visual and calculations
        df = pd.DataFrame()
        df["SPY_Price"] = history_spy
        df["TSLA_Price"] = history_tsla
        
        # store the SPY and TSLA prices into the dataframe
        df["SPY_returns"] = df["SPY_Price"].pct_change()
        df["TSLA_returns"] = df["TSLA_Price"].pct_change()
        #self.Debug(df)


        ##### Values for BAS Calculations #####
        # Mean of Daily Returns
        spy_daily_ret = df["SPY_returns"].mean()
        tsla_daily_ret = df["TSLA_returns"].mean()
        
        # Variance
        spy_var = df["SPY_returns"].var()
        tsla_var = df["TSLA_returns"].var()
        
        # Covariance
        covariance = df["SPY_returns"].cov(df["TSLA_returns"])
        
        # Correlation
        correlation = df["SPY_returns"].corr(df["TSLA_returns"])
        self.Debug('Correlation: {}'.format(correlation))
        
        
        ##### BASS Calculation #####
        # Standard Diviation
        spy_std = df["SPY_returns"].std()
        tsla_std = df["TSLA_returns"].std()
        self.Debug('Std Deviation of TSLA: {}'.format(tsla_std))
        
        # TSLA Beta
        TSLA_beta = covariance / spy_var
        self.Debug('TSLA Beta: {}'.format(TSLA_beta))
        
        # TSLA Alpha
        TSLA_alpha = tsla_abs_return - TSLA_beta * spy_abs_return 
        #uses annualized mean returns
        self.Debug('TSLA Alpha: {}'.format(TSLA_alpha))
        
        # TSLA Sharpe
        TSLA_SR = tsla_daily_ret / tsla_std * (252**0.5)
        self.Debug('TSLA Sharpe Ratio: {}'.format(TSLA_SR))
        