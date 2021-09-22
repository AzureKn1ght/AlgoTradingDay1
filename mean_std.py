import numpy as np

class MeanStd(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 12, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 31)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.AddEquity("TSLA", Resolution.Daily)
        self.prices = []


    def OnData(self, data):
        close_price = (data["TSLA"].Close)
        self.prices.append(close_price)
        # if not self.Portfolio.Invested:
        #    self.SetHoldings("SPY", 1)
        
        
    def OnEndOfAlgorithm(self):
        self.Debug(" The prices are: " + str(self.prices))
        self.Debug(" Number of data points: " + str(len(self.prices)))
        mean = np.mean(self.prices)
        std_dev = np.std(self.prices)
        self.Debug(" The mean is: " + str(mean))
        self.Debug(" The standard deviation is: " + str(std_dev))
        