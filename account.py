import math

# This class simulates basic buying and selling of stocks

class Account:
    def __init__(self):
        self.cash = 0
        self.daytrading_active = False
        self.total_daytrades = 0
        self.start_value = 0
        self.shares_holding = 0  # Total number of shares held across all stocks
        self.position_active = False  # Indicates if there is at least one position being held of any stock
        self.open_positions = []  # List of dictionaries for each position being held
        self.closed_positions = []  # List of dictionaries for each position previously held
        self.buys = 0
        self.sells = 0

    def init_session(self, cash, daytrading=False):
        # Method to initialize an account session
        self.daytrading_active = daytrading  # Sets if daytrading should be enforced
        self.__set_cash(cash)
        self.start_value = self.get_cash()

    def __set_cash(self, cash_value):
        """
        This method sets the cash value for the account. Default implementation assigns cash_value to self.cash.

        :param cash_value: the starting cash value
        :type cash_value: float
        :return:
        :rtype:
        """
        self.cash = cash_value

    def get_cash(self):
        """
        This method returns the cash value that the account currently has.

        :return: cash
        :rtype: float
        """
        return self.cash

    def buy_stock(self, ticker, price, shares):
        """
        This method implements the logic required to buy a certain number of shares in a stock.
        The default implementation does nothing. Each child class must implement this method.

        :param price: the price to buy the stock at
        :type price: float
        :param shares: the total number of shares to buy
        :type shares: int
        :return shares_holding: the number of shares
        :rtype:
        """
        pass

    def sell_stock(self, ticker, price, shares):
        """
        This method implements the logic required to sell a certain number of shares in a stock.
        The default implementation does nothing. Each child class must implement this method.

        :param price: the price to sell the stock at
        :type price: float
        :param shares: the total number of shares to sell
        :type shares: int
        :return shares_holding: the total number of shares held in the stock after selling
        :rtype: int
        """
        pass

    def any_position_active(self):
        """
        This method returns if the account has any active position or not.

        :return: position_active
        :rtype: bool
        """
        if self.open_positions:
            self.position_active = True
        else:
            self.position_active = False
        return self.position_active

    def get_profit_loss(self):
        """
        This method returns the total profit gain or loss since the account was initialized.

        :return:
        :rtype: float
        """
        return self.cash - self.start_value

    def get_total_transactions(self):
        """
        This method returns the total number of buys and sells.
        :return: buys, sells
        :rtype: int, int
        """
        return self.buys, self.sells

