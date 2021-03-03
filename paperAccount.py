"""
This class implements inherited methods and also adds new methods
that are specific to a paper trading account.

Created By:     Brandon Jinright
Created On:     02/11/2021
Last Updated:   02/11/2021
"""

import time
import datetime
from account import *
from constants import *
from utils import get_time


class PaperAccount(Account):
    def __init__(self):
        super().__init__()

    def init_session(self, cash, daytrading=False):
        # Method to initialize an account session
        self.daytrading_active = daytrading  # Sets if daytrading should be enforced
        self.__set_cash(cash)

    def __set_cash(self, cash_value):
        self.cash = cash_value
        self.start_value = self.get_cash()

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
        if self.cash < price:
            print("You do not have enough funds to buy at least 1 share!")
            return False

        # If we have an active position in this ticker, retrieve it--if not, create one
        index, stock_info = self.find_position(ticker)
        new_stock = False
        if not stock_info:
            new_stock = True
            stock_info = {"ticker": ticker, "shares": 0}  # Create a new position

        if "open_date" not in stock_info.keys():
            stock_info["open_date"] = get_time()

        if self.cash < (shares*price):
            print("Insufficient funds to buy {0} shares of {1} @ {2}".format(shares, ticker, price))
            return False

        stock_info["shares"] += shares
        print("Shares bought: {0} @ ${1}".format(shares, price))

        self.cash -= shares * price
        self.position_active = True
        self.buys += 1

        if new_stock:
            self.open_positions.append(stock_info)
        else:
            index, info = self.find_position(ticker)
            self.open_positions[index] = stock_info

        return stock_info["shares"]

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

        index, stock_info = self.find_position(ticker)
        if not stock_info:
            print("ERROR: There is not an active position under the ticker ${0}".format(ticker))
            return False

        shares_holding = stock_info["shares"]
        if shares <= 0:
            print("ERROR: Cannot sell 0 or less shares!")
            return False

        sell_amt = 0
        if shares == ALL_SHARES_AVAILABLE:
            sell_amt = stock_info["shares"]
        else:
            sell_amt = shares

        if sell_amt > shares_holding:
            print("ERROR: Short-selling is not a supported feature!")
            return False

        print("Shares sold: {0} @ {1}".format(sell_amt, price))
        self.cash += sell_amt * price
        self.sells += 1
        stock_info["shares"] -= sell_amt
        if stock_info["shares"] == 0:
            # Mark position as closed
            stock_info["closed_date"] = get_time()
            self.closed_positions.append(stock_info)
            self.open_positions.pop(index)
        else:
            # Update position
            self.open_positions[index] = stock_info

        return stock_info["shares"]

    def active_position(self, ticker):
        if not self.find_position(ticker):
            return False
        return True

    def find_position(self, ticker):
        # TODO Search for closed positions too? Maybe introduce this as a flag
        for index, position in enumerate(self.open_positions):
            if position["ticker"] is ticker:
                return index, position

        return -1, None

