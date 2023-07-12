import sqlite3
import pandas as pd

#【search data】
# data format = 
# ["datetime", opening_price, closing_price, lowest_price, highest_price, trading_volume, 0, 
# MACD, DIF, DEA]
import pandas as pd


# .ewm() = 指數加權移動平均值(Exponential Weighted Moving Average)，在股市中，是一種平滑技術，舉一個例子：
# 你記錄下近 5 天騎車前往公司的時速，越接近
def calculate_ema(data, n):
    ema = data["closing_price"].ewm(span=n, adjust=False).mean()
    return ema

def calculate_dif(data, short_period, long_period):
    ema_short = calculate_ema(data, short_period)
    ema_long = calculate_ema(data, long_period)
    dif = ema_short - ema_long
    return dif

def calculate_dea(data, dif_period, dea_period):
    dif = calculate_dif(data, dif_period, dea_period)
    dea = dif.ewm(span=dea_period, adjust=False).mean()
    return dea

def calculate_macd(data, dif_period, dea_period):
    dif = calculate_dif(data, dif_period, dea_period)
    dea = calculate_dea(data, dif_period, dea_period)
    macd = 2 * (dif - dea)
    return macd

def create_new_data(stock_id):

    db_name = "twse.db"
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute(f'''
                SELECT 
                    date, opening_price, closing_price, lowest_price, highest_price, Trading_volume, 0                
                FROM
                    stock_data
                WHERE
                    stock_num = {stock_id}
                ''')

    results = cur.fetchall()

    echarts_data = []

    for data in results:
        echarts_data.append(list(data))

    data = pd.DataFrame(echarts_data, 
                        columns=['datetime', 'opening_price', 'closing_price', 'lowest_price', 'highest_price', 'trading_volume', '1/0'])

    # # 計算 EMA、DIF、DEA、MACD
    # # data['EMA'] = calculate_ema(data, 12)  # 使用 12 天作為 EMA 的天數
    data['MACD'] = calculate_macd(data, 12, 26)  # 使用 12 天和 26 天作為 MACD 的 DIF 和 DEA 的天數
    data['DIF'] = calculate_dif(data, 12, 26)  # 使用 12 天和 26 天作為 DIF 的短期和長期天數
    data['DEA'] = calculate_dea(data, 12, 26)  # 使用 12 天和 26 天作為 DEA 的 DIF 和 DEA 的天數

    # 輸出結果
    # print(data)
    visualize_data = []

    for data_list in data.values:
        data_list = data_list.tolist()
        visualize_data.append(data_list)
        
    return (visualize_data)

if __name__ == "__main__":
    pass
    # echarts_data = create_new_data("2330")
    # print(echarts_data)