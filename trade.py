import alpaca_trade_api as alpaca
import json
import time
import threading as thread
import websocket
from listener import *
from backtest import Backtest

# Globals
time_frame = 365  # One year
thread_active = False

def check_status(acc):
    # Check our status
    if acc.status != 'ACTIVE':
        print("Account is not active!")
        return False

    if acc.trading_blocked is True:
        print("Trading is currently blocked!")
        return False

    # Only needed if under $25K in live account
    if acc.daytrade_count == 3:
        print("Reached the maximum amount of day trades!")
        return False

    # Check our cash balance
    if float(acc.cash) <= 0.0:
        print("Not enough cash on hand to trade today!")
        return False
    return True


def on_open(ws):
    global acc_data
    print("Opened web socket!")

    # Authenticate
    payload = {
        "action": "authenticate",
        "data": acc_data
    }
    ws.send(json.dumps(payload))


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    global thread_active
    thread_active = False
    print(error)


def on_close(ws):
    global thread_active
    thread_active = False
    print("Socket has been closed")


"""listener = AlpacaListener()
acc_data = {"key_id": "PKF4MUFXNRXC6NGBUCWM", "secret_key": "kCsBXWdZJGDbpV54ZEAnApUs9bTojB7jHFw1DsI2"}
account = listener.account_info()
if not check_status(account):
    exit(-1)  # We can't trade at the moment

# Success, we can begin trading
print("Cash balance for today: $" + account.cash + " " + account.currency)
symbol = "AMD"

symbol_bars = trading_api.get_barset(symbol, "minute").df.iloc
for bar in symbol_bars:
    print(bar)


listener.start_listener(open_cb=on_open, close_cb=on_close, msg_cb=on_message, error_cb=on_error)
if listener.listener_active():
    print("Thread was started")
    thread_active = True

time.sleep(5)
listener.stream_subscribe("AMD", "T")

# Main thread - handles the logic for the trading algorithm
#while thread_active:
    #pass"""

if __name__ == '__main__':
    backtest = Backtest()
    backtest.set_duration(48)
    backtest.add_symbol("AMD")
    backtest.add_symbol("AAPL")
    backtest.add_symbol("NFLX")
    backtest.add_symbol("FB")
    backtest.add_symbol("PK")
    #backtest.download_data()

    #time.sleep(5)
    #backtest.close_browser()
    #print(backtest.get_files(backtest.get_path()))
    test_path = "C:\\Users\\goodp\\PycharmProjects\\AlgoTrading\\02082021223022"
    backtest.test_strategy("AAPL", test_path)
    watchlist = backtest.get_symbols()

    # TODO could add a callback to test_strategy to add the result to a P/L list
    threads = []
    for symbol in watchlist:
        threads.append(thread.Thread(target=backtest.test_strategy(symbol, test_path)))

    for t in threads:
        t.start()


