# 导入所需的库
import websocket
import json
import ccxt

# 定义币安现货和合约交易所
exchange_spot = ccxt.binance({
    'apiKey': 'eFB7692qkk1KOExLrE0PM05aEIqODSvSn7Ny5pFHHGk9t7IE8YpeHwUimQkcvjr7',
    'secret': 'S7TJ8QHTT7BsX2shd8MBQItszVRxaVQpGNhLXRsD1eLn671HBntalSvNvOsS2NSY',
    'enableRateLimit': True,  # 启用币安的速率限制
})

exchange_futures = ccxt.binance({
    'apiKey': 'eFB7692qkk1KOExLrE0PM05aEIqODSvSn7Ny5pFHHGk9t7IE8YpeHwUimQkcvjr7',
    'secret': 'S7TJ8QHTT7BsX2shd8MBQItszVRxaVQpGNhLXRsD1eLn671HBntalSvNvOsS2NSY',
    'enableRateLimit': True,  # 启用币安的速率限制
    'urls': {
        'api': 'https://fapi.binance.com/api/v3',
        'fapi': 'https://fapi.binance.com/fapi/v1',
    }
})

# 定义交易对和套利参数
symbol = 'ETHUSDT'
spread = 0.01  # 套利价格差异阈值


# 定义websocket回调函数
def on_open(ws):
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [f"{symbol}@kline_1m"],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    try:
        data = json.loads(message)
        if 'k' in data and symbol in data['k']:
            # 获取现货和合约的最新价格
            spot_price = exchange_spot.fetch_ticker(symbol)['last']
            futures_price = exchange_futures.fetch_ticker(symbol)['last']

            # 计算价格差异
            price_difference = spot_price - futures_price

            # 如果价格差异大于阈值，则执行套利交易
            if abs(price_difference) > spread:
                if price_difference > 0:
                    # 现货价格高于合约，买入合约卖出现货
                    print(f"现货价格高于合约价格, 套利机会: 现货价格 {spot_price}, 合约价格 {futures_price}")
                    # 这里添加买入合约和卖出现货的代码
                else:
                    # 现货价格低于合约，买入现货卖出合约
                    print(f"现货价格低于合约价格, 套利机会: 现货价格 {spot_price}, 合约价格 {futures_price}")
                    # 这里添加买入现货和卖出合约的代码
    except Exception as e:
        print("Error handling message:", e)


# 定义币安websocket连接的URL
binance_websocket_url = "wss://stream.binance.com:9443/ws"

# 创建websocket实例
ws = websocket.WebSocketApp(
    binance_websocket_url,
    on_open=on_open,
    on_message=on_message,
    on_error=lambda ws, error: print("Error:", error),
    on_close=lambda ws: print("Connection closed"),
)

if __name__ == '__main__':
    # 运行websocket客户端
    ws.run_forever()
