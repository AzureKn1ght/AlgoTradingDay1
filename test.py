class SGUS(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 9, 1)  # Set Start Date
        # self.SetEndDate(2021, 4, 21)    # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.AddEquity("SPY", Resolution.Hour) # Data for this equity at this resolution
        # self.AddEquity("TSLA", Resolution.Daily) # Data for this equity at this resolution


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''

        # Code starts here
        # Impt: if not invested then buy, if not buy everyday
        
        if not self.Portfolio.Invested:
            self.SetHoldings("SPY", 1)
            self.Debug("Bought!")
            
        x = data["SPY"].Close
        self.Debug(x)
        
        
    def OnEndOfAlgorithm(self):
        self.Debug("Algo Ended")
            