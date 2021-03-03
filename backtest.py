import datetime as dt
import math
import time
import os
import pandas as pd
import pandas_ta as ta
from constants import *
from paperAccount import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Backtest:
    def __init__(self):
        self.enabled = False
        self.page_loaded = False
        self.watchlist = []
        self.duration = 0
        self.options = webdriver.ChromeOptions()
        self.dir_path = self.__create_directory()
        self.files = []

        # Set the default download directory
        prefs = {
            "download.default_directory": self.dir_path
        }

        self.options.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(chrome_options=self.options)

    def close_browser(self):
        self.browser.close()

    def add_symbol(self, symbol):
        if isinstance(symbol, str):
            print("The symbol " + symbol + " has been added to the watchlist.")
            self.watchlist.append(symbol)
        else:
            print("The symbol could not be added to the watchlist - wrong type.")
        return

    def get_symbols(self):
        return self.watchlist

    def watchlist_contains(self, symbol):
        if symbol not in self.watchlist:
            return False
        return True

    def set_duration(self, duration):
        # Should we specify days only?
        self.duration = duration

    def get_duration(self):
        return self.duration

    def download_data(self):
        # Start downloading csv files
        for symbol in self.watchlist:
            print("Downloading data for symbol " + symbol)
            self.__load_finance_page()

            if self.__is_page_loaded():
                self.__search(str(symbol))
                time.sleep(5)
                self.__load_historical_data()
                time.sleep(5)
                self.__set_time_period()
                time.sleep(5)
                self.__apply_changes()
                time.sleep(5)
                self.__download_csv()

    def is_enabled(self):
        return self.enabled

    def set_enabled(self):
        self.enabled = True

    def set_disabled(self):
        self.enabled = False

    def __load_finance_page(self):
        self.browser.get("http://finance.yahoo.com")
        if "Yahoo Finance" not in self.browser.title:
            self.page_loaded = False
        else:
            self.page_loaded = True

    def __is_page_loaded(self):
        return self.page_loaded

    def __search(self, search_value):
        # Input text into search bar
        search_bar = self.browser.find_element_by_id("yfin-usr-qry")
        search_bar.clear()
        search_bar.send_keys(search_value)

        # Wait for suggestions
        time.sleep(5)

        # Send user input
        search_btn = self.browser.find_element_by_id("header-desktop-search-button")
        search_btn.send_keys(Keys.ENTER)

    def __load_historical_data(self):
        links = self.browser.find_elements_by_tag_name("a")
        historical_btn = None

        for link in links:
            if "history?p" in link.get_property("href"):
                historical_btn = link
                break

        # Wait before clicking a button
        if historical_btn:
            time.sleep(2)
            historical_btn.click()

    def __calculate_date(self):
        date_range = []

        # Calculate the date range
        current_date = dt.date.today()
        past_date = current_date

        # Calculate and set date range difference
        years = math.floor(self.duration / 12)
        months = self.duration % 12
        past_date = past_date.replace(year=(past_date.year - years), month=(past_date.month - months))

        date_range.append(past_date.strftime("%m/%d/%Y"))
        date_range.append(current_date.strftime("%m/%d/%Y"))

        return date_range

    def __set_time_period(self):
        divs = self.browser.find_elements_by_tag_name("div")
        date_dropdown = None

        for div in divs:
            if "dateRangeBtn" in div.get_attribute("class"):
                date_dropdown = div
                break

        # Wait before clicking the dropdown
        if not date_dropdown:
            return

        time.sleep(2)
        date_dropdown.click()
        time.sleep(1)

        date_range = self.__calculate_date()
        startdate_element = self.browser.find_element_by_name("startDate")
        enddate_element = self.browser.find_element_by_name("endDate")
        startdate_element.send_keys(date_range[0])
        enddate_element.send_keys(date_range[1])

        # Find the done button
        spans = self.browser.find_elements_by_tag_name("span")
        done_btn = None

        for span in spans:
            if "Done" in span.text:
                done_btn = span
                break

        if not done_btn:
            return

        done_btn.click()

    def __set_frequency(self, freq):
        valid_frequencies = ["Daily", "Weekly", "Monthly"]
        if freq not in valid_frequencies:
            print("The frequency that was selected is not valid")
            return

        spans = self.browser.find_elements_by_tag_name("span")
        dropdown_btn = None
        for span in spans:
            span_attribute = span.get_attribute("data-test")
            if span_attribute:
                if "historicalFrequency-selected" in span_attribute:
                    dropdown_btn = span
                    break

        if not dropdown_btn:
            return

        dropdown_btn.click()
        time.sleep(5)

        # TODO: Implement selecting a frequency
        """
        spans = self.browser.find_elements_by_tag_name("span")

        selects = []
        for span in spans:
            if freq in span.text:
                selects.append(span)

        print(selects)
        """

    def __apply_changes(self):
        spans = self.browser.find_elements_by_tag_name("span")
        apply_btn = None

        for span in spans:
            if "Apply" in span.text:
                apply_btn = span
                break

        if not apply_btn:
            return

        time.sleep(1)
        apply_btn.click()

    def __download_csv(self):
        links = self.browser.find_elements_by_tag_name("a")
        download_btn = None

        for link in links:
            if "download" in link.get_attribute("href"):
                download_btn = link
                break

        if not download_btn:
            return

        time.sleep(1)
        download_btn.click()
        time.sleep(5)

    def __create_directory(self):
        current_date = time.strftime("%m%d%Y%H%M%S")

        curr_path = os.getcwd()
        path = os.path.join(curr_path, current_date)
        os.mkdir(path)

        return path

    def get_files(self, path):
        for (base, dirs, file_list) in os.walk(path):
            for file in file_list:
                self.files.append(os.path.join(base, file))

        return self.files

    def get_path(self):
        return self.dir_path

    def test_strategy(self, symbol, path):
        if not self.watchlist_contains(symbol):
            print("The selected symbol is not in the watchlist!")
            return

        acc = PaperAccount()
        acc.init_session(10000, False)
        csv_path = os.path.join(path, "{0}.csv".format(symbol))
        df = pd.read_csv(csv_path, sep=",")

        RSIStrategy = ta.Strategy(
            name="RSI",
            description="RSI to measure stock price strength",
            ta=[
                {"kind": "rsi"}
            ]
        )

        shares = 0
        df.ta.strategy(RSIStrategy)

        # Predefined ruleset: buy if RSI_14 less than 35, hold and sell until RSI_14 over 55
        for index, row in df.iterrows():
            if row['RSI_14'] < 35:
                shares = acc.buy_stock(symbol, row['close'], 10)
            if row['RSI_14'] > 50:
                shares = acc.sell_stock(symbol, row['close'], ALL_SHARES_AVAILABLE)

        # Analysis
        result = acc.get_profit_loss()
        if result < 0:
            print("Realized loss:" + str(result))
        else:
            print("Realized gain: " + str(result))

        buys, sells = acc.get_total_transactions()
        print("Total # buys: " + str(buys))
        print("Total # sells: " + str(sells))
