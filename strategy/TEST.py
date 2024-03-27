import pandas as pd
import pandas_ta as ta

# 假设df是一个包含股票价格历史数据的DataFrame，其中'close'是收盘价列
df = pd.DataFrame({
    'close': [1.2, 1.3, 1.4, 1.5, 1.5, 1.6, 1.7, 1.6, 1.5, 1.4]
})

# 计算10期简单移动平均线
df['SMA_10'] = ta.sma(df['close'], length=3)

print(df)