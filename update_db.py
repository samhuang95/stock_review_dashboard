import sqlite3
import time
from get_data import get_data, data_range


def insert_data(db_name, table_name, stock_id, date):
    """
    Insert data into the specified database table.

    Args:
        db_name (str): The name of the database.

        table_name (str): The name of the table.

        data (a list include multiple tuples): The data to be inserted. 
                Example:
                [
                ('stock_name(str)', 'stock_num(str)','date(str)',opening_price(float),closing_price(float),Trading_volume(int)),
                ('stock_name(str)', 'stock_num(str)','date(str)',opening_price(float),closing_price(float),Trading_volume(int)),
                ...]
                
            Such as:
            ("台積電", "2330", "112/07/04", 347.00, 348.00, 9693)
    Returns:
        None

    Raises:
        ValueError: If the data is not in the correct format.

    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # 檢查資料是否已存在
    cur.execute(f"SELECT * FROM {table_name} WHERE stock_num=? AND date=?", (stock_id, date))
    existing_data = cur.fetchone()

    if existing_data is None:
        collected_info = get_data(stock_id, date)

        # 將資料整理成需要的格式
        data = []
        for info in collected_info:
            values = (
                info['股票代號'],
                info['日期'],
                float(info['開盤價'].replace(',', '')),
                float(info['收盤價'].replace(',', '')),
                float(info['最高價'].replace(',', '')),
                float(info['最低價'].replace(',', '')),
                int(info['成交筆數'].replace(',', ''))
            )
            data.append(values)

        # 使用參數化的 SQL 語句插入資料
        cur.executemany(f"INSERT OR IGNORE INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)", data)

    con.commit()
    con.close()


if __name__ == '__main__':

    # setting the stock list
    # stock_list = {"台積電":"2330", "聯發科":"2454", "台達電":"2308"}
    # stock_list = {"台達電":"2308"}
    stock_list = {"台積電":"2330"}

    for stock_id in stock_list.values():
        date_list = data_range(stock_id,'20210101','20230701')
        for date in date_list:
            # 執行插入資料的程式
            db_name = "twse.db"
            table_name = "stock_data"         
            insert_data(db_name, table_name, stock_id, date)
            print("successfully inserted", stock_id, date)                      
            time.sleep(20)
    print("update fininsh !")


    




