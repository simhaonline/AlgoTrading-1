import alpaca_trade_api as alpaca
import json
import threading as thread
import websocket


class AlpacaListener:
    def __init__(self):
        self.ws = None
        self.listener = None
        self.acc_data = {"key_id": "PKF4MUFXNRXC6NGBUCWM", "secret_key": "kCsBXWdZJGDbpV54ZEAnApUs9bTojB7jHFw1DsI2"}
        self.trading_api = alpaca.REST(self.acc_data["key_id"], self.acc_data["secret_key"],
                                       base_url="https://paper-api.alpaca.markets")
        self.data_api = alpaca.REST(self.acc_data["key_id"], self.acc_data["secret_key"],
                                    base_url="https://data.alpaca.markets/v1")
        self.account = self.trading_api.get_account()

    def start_listener(self, open_cb=None, close_cb=None, error_cb=None, msg_cb=None):
        # Initiate the web socket connection with the appropriate callback
        self.ws = websocket.WebSocketApp("wss://data.alpaca.markets/stream", on_open=open_cb, on_close=close_cb,
                                         on_error=error_cb, on_message=msg_cb)
        self.listener = thread.Thread(target=self.ws.run_forever)
        self.listener.daemon = True
        self.listener.start()

        return self.ws.sock.connected

    def listener_active(self):
        return self.listener.is_alive()

    def account_info(self):
        return self.account

    def stream_subscribe(self, ticker, type):
        listen_payload = {"action": "listen", "data": {"streams": ["T.AAPL"]}}
        self.ws.send(json.dumps(listen_payload))
