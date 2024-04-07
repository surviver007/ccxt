# 导入所需的库
import websocket
import json

# 定义币安websocket连接的URL
binance_websocket_url = "wss://stream.binance.com:9443/ws"

proxy_host = "127.0.0.1"
proxy_port = 7890

# 定义交易对的通道
btc_usd_websocket_channel = "btcusdt@ticker"
eth_usd_websocket_channel = "ethusdt@kline_1m"


def on_open(ws):
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [btc_usd_websocket_channel, eth_usd_websocket_channel],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    # 当接收到消息时，打印实时交易数据
    # print("Received message:", message)
    close = json.loads(message)['k']['c']
    print('close:', close)


def on_error(ws, error):
    # 当发生错误时，打印错误信息
    print("Error:", error)


def on_close(ws):
    # 当连接关闭时，打印关闭信息
    print("Connection closed")


if __name__ == '__main__':
    # 创建websocket实例
    ws = websocket.WebSocketApp(
        binance_websocket_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # 开始运行websocket客户端
    ws.run_forever(http_proxy_host=proxy_host, http_proxy_port=proxy_port)
