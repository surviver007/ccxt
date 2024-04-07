import json
import websocket
import threading
import time

# 定义全局变量
eth_price_binance = 0
eth_price_coinbase = 0
threshold = 0.01  # 价差阈值，可根据需要调整


def on_message_binance(ws, message):
    global eth_price_binance
    data = json.loads(message)
    if "e" in data and data["e"] == "trade" and data["s"] == "ETHUSDT":
        eth_price_binance = float(data["p"])


def on_message_coinbase(ws, message):
    global eth_price_coinbase
    data = json.loads(message)
    if "type" in data and data["type"] == "ticker" and data["product_id"] == "ETH-USD":
        eth_price_coinbase = float(data["price"])


def on_error(ws, error):
    print(error)


def on_close(ws, *args):
    print("WebSocket closed, reconnecting...")
    if ws == ws_binance:
        binance_ws()
    elif ws == ws_coinbase:
        coinbase_ws()


def binance_ws():
    global ws_binance
    ws_binance = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                                        on_message=on_message_binance,
                                        on_error=on_error,
                                        on_close=on_close)
    ws_binance.run_forever(ping_interval=60,
                           http_proxy_host='127.0.0.1',
                           http_proxy_port=7890,
                           proxy_type='http')


def coinbase_ws():
    global ws_coinbase
    ws_coinbase = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com",
                                         on_open=lambda ws: ws.send(json.dumps(
                                             {"type": "subscribe", "product_ids": ["ETH-USD"],
                                              "channels": ["ticker"]})),
                                         on_message=on_message_coinbase,
                                         on_error=on_error,
                                         on_close=on_close)
    ws_coinbase.run_forever(ping_interval=60,
                            http_proxy_host='127.0.0.1',
                            http_proxy_port=7890,
                            proxy_type='http',
                            sslopt={"cert_reqs": ssl.CERT_NONE})


def arbitrage():
    while True:
        if eth_price_binance > 0 and eth_price_coinbase > 0:
            price_diff = eth_price_binance - eth_price_coinbase
            if abs(price_diff) > threshold:
                print(
                    f"Arbitrage opportunity: Binance {eth_price_binance}, Coinbase {eth_price_coinbase}, Difference {price_diff}")
        time.sleep(1)


if __name__ == "__main__":
    binance_thread = threading.Thread(target=binance_ws)
    coinbase_thread = threading.Thread(target=coinbase_ws)
    arbitrage_thread = threading.Thread(target=arbitrage)

    binance_thread.start()
    coinbase_thread.start()
    arbitrage_thread.start()
