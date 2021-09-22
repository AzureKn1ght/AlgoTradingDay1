import numpy as np
import pandas as pd

class SPY_BASS(QCAlgorithm):

    def Initialize(self):
        self.UniverseSettings.Resolution = Resolution.Daily
        self.SetStartDate(2021, 1, 1)   # Set Start Date
        self.SetCash(100000)            # Set Strategy Cash
        
        # Add all stocks in S&P 500
        self.AddUniverse(self.Universe.QC500)
        

    # def OnData(self, data):
        
        
    def OnEndOfAlgorithm(self):
        # Get all the symbols in S&P500
        symbol_list = []
        for universe in self.UniverseManager.Values:
            symbols = universe.Members.Keys       
            for symbol in symbols:
                symbol_list.append(symbol)

        
        # Calculate the vaules for all the symbols using loop
        for symbol in symbol_list:
            # create a new symbol for the S&P market index
            self.spy = Symbol.Create('SPY', SecurityType.Equity, Market.USA) 
            
            # calculate absolute return of SPY
            history_spy = self.History(self.spy, 30, Resolution.Daily)
            history_spy = history_spy["close"].tolist()
            spy_abs_return = (history_spy[-1] - history_spy[0]) / history_spy[0]

            # same for item
            history = self.History(symbol, 30, Resolution.Daily)
            self.Debug("-----")
            self.Debug(symbol.Value)
            history = history["close"].tolist()
            abs_return = (history[-1] - history[0]) / history[0]
        
            # make a dataframe for visual and calculations
            df = pd.DataFrame()
            df["SPY_Price"] = history_spy
            df["Price"] = history
        
            # store the percentage change
            df["SPY_returns"] = df["SPY_Price"].pct_change()
            df["returns"] = df["Price"].pct_change()
           

            ##### Values for BAS Calculations #####
            # Mean of Daily Returns
            spy_daily_ret = df["SPY_returns"].mean()
            daily_ret = df["returns"].mean()
        
            # Variance
            spy_var = df["SPY_returns"].var()
            var = df["returns"].var()
        
            # Covariance
            covariance = df["SPY_returns"].cov(df["returns"])
        
            # Correlation
            correlation = df["SPY_returns"].corr(df["returns"])
            self.Debug('Correlation: {}'.format(correlation))
        
        
            ##### BASS Calculation #####
            # Standard Diviation
            spy_std = df["SPY_returns"].std()
            std = df["returns"].std()
            self.Debug('Std Deviation: {}'.format(std))
        
            # Beta
            beta = covariance / spy_var
            self.Debug('Beta: {}'.format(beta))
        
            # Alpha
            alpha = abs_return - beta * spy_abs_return 
            #uses annualized mean returns
            self.Debug('Alpha: {}'.format(alpha))
        
            # Sharpe
            SR = daily_ret / std * (252**0.5)
            self.Debug('Sharpe Ratio: {}'.format(SR))