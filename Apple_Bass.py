import numpy as np
import pandas as pd

class AAPL_BASS(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 14)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.AddEquity("SPY", Resolution.Daily)
        self.AddEquity("AAPL", Resolution.Daily)


    # def OnData(self, data):
        
        
    def OnEndOfAlgorithm(self):
        # call historical data from QC database
        history_spy = self.History(self.Symbol("SPY"), 30, Resolution.Daily)
        # extract all the close prices and convert it to a list 
        history_spy = history_spy["close"].tolist()
        # calculate absolute return of SPY
        spy_abs_return = (history_spy[-1] - history_spy[0]) / history_spy[0]
        # [-1] index gives the last value in the list
        
        # do the same by for AAPL
        history_AAPL = self.History(self.Symbol("AAPL"), 30, Resolution.Daily)
        history_AAPL = history_AAPL["close"].tolist()
        AAPL_abs_return = (history_AAPL[-1] - history_AAPL[0]) / history_AAPL[0]
        
        # make a dataframe for visual and calculations
        df = pd.DataFrame()
        df["SPY_Price"] = history_spy
        df["AAPL_Price"] = history_AAPL
        
        # store the SPY and AAPL prices into the dataframe
        df["SPY_returns"] = df["SPY_Price"].pct_change()
        df["AAPL_returns"] = df["AAPL_Price"].pct_change()
        #self.Debug(df)


        ##### Values for BAS Calculations #####
        # Mean of Daily Returns
        spy_daily_ret = df["SPY_returns"].mean()
        AAPL_daily_ret = df["AAPL_returns"].mean()
        
        # Variance
        spy_var = df["SPY_returns"].var()
        AAPL_var = df["AAPL_returns"].var()
        
        # Covariance
        covariance = df["SPY_returns"].cov(df["AAPL_returns"])
        
        # Correlation
        correlation = df["SPY_returns"].corr(df["AAPL_returns"])
        self.Debug('Correlation: {}'.format(correlation))
        
        
        ##### BASS Calculation #####
        # Standard Diviation
        spy_std = df["SPY_returns"].std()
        AAPL_std = df["AAPL_returns"].std()
        self.Debug('Std Deviation of AAPL: {}'.format(AAPL_std))
        
        # AAPL Beta
        AAPL_beta = covariance / spy_var
        self.Debug('AAPL Beta: {}'.format(AAPL_beta))
        
        # AAPL Alpha
        AAPL_alpha = AAPL_abs_return - AAPL_beta * spy_abs_return 
        #uses annualized mean returns
        self.Debug('AAPL Alpha: {}'.format(AAPL_alpha))
        
        # AAPL Sharpe
        AAPL_SR = AAPL_daily_ret / AAPL_std * (180**0.5)
        self.Debug('AAPL Sharpe Ratio: {}'.format(AAPL_SR))
        