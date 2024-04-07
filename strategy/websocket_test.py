import websocket
import json

proxy_host = "127.0.0.1"
proxy_port = 7890
target_url = "wss://stream.binance.com:443"


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    # 在建立连接时，向服务器发送订阅请求
    subscribe_request = {
        "method": "SUBSCRIBE",
        "params":
            [
                "btcusdt@miniTicker",  # 订阅 BTC/USDT 的实时行情数据
            ],
        "id": 1
    }
    ws.send(json.dumps(subscribe_request))


if __name__ == "__main__":
    websocket.enableTrace(True)

    websocket.setdefaulttimeout(5)
    ws = websocket.WebSocketApp(target_url + "/stream",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open

    ws.run_forever(http_proxy_host=proxy_host, http_proxy_port=proxy_port)
