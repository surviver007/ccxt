import ccxt
import time

# 创建币安交易所实例
exchange = ccxt.binance({
    'apiKey': 'eFB7692qkk1KOExLrE0PM05aEIqODSvSn7Ny5pFHHGk9t7IE8YpeHwUimQkcvjr7',
    'secret': 'S7TJ8QHTT7BsX2shd8MBQItszVRxaVQpGNhLXRsD1eLn671HBntalSvNvOsS2NSY',
})

# 创建币安合约交易所实例
futures_exchange = ccxt.binance({
    'apiKey': 'eFB7692qkk1KOExLrE0PM05aEIqODSvSn7Ny5pFHHGk9t7IE8YpeHwUimQkcvjr7',
    'secret': 'S7TJ8QHTT7BsX2shd8MBQItszVRxaVQpGNhLXRsD1eLn671HBntalSvNvOsS2NSY',
    'options': {'defaultType': 'future'},
})


# 定义套利函数
def arbitrage(symbol, amount, threshold):
    # 获取现货市场深度
    spot_orderbook = exchange.fetch_order_book(symbol)
    spot_price = spot_orderbook['bids'][0][0]
    print(spot_price)

    # 获取合约市场深度
    futures_orderbook = futures_exchange.fetch_order_book(symbol)
    futures_price = futures_orderbook['bids'][0][0]
    print(futures_price)

    # 计算价格差异
    price_diff = spot_price - futures_price

    print(price_diff)

    # # 检查是否满足进场条件
    # if price_diff > threshold:
    #     print(f"套利机会: 现货价格 {spot_price}, 合约价格 {futures_price}, 价格差异 {price_diff}")
    #
    #     # 执行套利交易
    #     try:
    #         # 在现货市场买入,合约市场卖出
    #         spot_buy_order = exchange.create_market_buy_order(symbol, amount)
    #         futures_sell_order = futures_exchange.create_market_sell_order(symbol, amount)
    #         print(f"现货买入订单: {spot_buy_order}")
    #         print(f"合约卖出订单: {futures_sell_order}")
    #     except Exception as e:
    #         print(f"交易失败: {e}")
    # else:
    #     print("没有满足进场条件的套利机会.")
    #
    # # 检查是否满足平仓条件
    # if spot_price >= futures_price:  # 现货价格大于等于合约价格时平仓
    #     try:
    #         # 平掉现货买入和合约卖出的仓位
    #         spot_sell_order = exchange.create_market_sell_order(symbol, amount)
    #         futures_buy_order = futures_exchange.create_market_buy_order(symbol, amount)
    #         print(f"现货平仓卖出订单: {spot_sell_order}")
    #         print(f"合约平仓买入订单: {futures_buy_order}")
    #     except Exception as e:
    #         print(f"平仓失败: {e}")


if __name__ == '__main__':
    # 套利交易对、数量和价格差异阈值
    symbol = 'ETH/USDT'
    amount = 0.01
    threshold = 5  # 价格差异阈值,单位为币安的最小价格变动单位

    # 循环执行套利策略
    while True:
        try:
            arbitrage(symbol, amount, threshold)
        except Exception as e:
            print(f"发生错误: {e}")

        # 暂停一段时间再进行下一次套利检查
        time.sleep(5)
