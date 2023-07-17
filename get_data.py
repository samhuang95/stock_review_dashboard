import requests
from datetime import datetime
import sqlite3
import os  # 加入這一行



TWSE_URL = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json'


def get_web_content(stock_id, current_date):
    resp = requests.get(TWSE_URL + '&date=' + current_date + '&stockNo=' + stock_id)
    if resp.status_code != 200:
        return None
    else:
        return resp.json()
    

def get_data(stock_id, current_date):
    info = list()
    resp = get_web_content(stock_id, current_date)
    if resp is None:
        return None
    else:
        if resp['data']:
            for data in resp['data']:
                record = {
                    '股票代號' : stock_id,
                    '日期': data[0],
                    '開盤價': data[3],
                    '收盤價': data[6],
                    '最高價': data[4],
                    '最低價': data[5],
                    '成交筆數': data[8]
                }
                info.append(record)
        return info
    

# def main(stock_id, current_date):
#     # current_year = current_date[:4]
#     # current_month = current_date[4:6]
#     # print(f'Processing data for {stock_id} {current_year} {current_month}')
#     collected_info = get_data(stock_id, current_date)
#     return collected_info


# create search date range
def data_range(stock_id, start_date:str, end_date:str):

    date_format = "%Y%m%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    
    date_list = []
    while start <= end:
        date_list.append(start.strftime("%Y%m01"))
        next_month = start.month + 1 if start.month < 12 else 1
        next_year = start.year + 1 if start.month == 12 else start.year
        start = start.replace(year=next_year, month=next_month, day=1)
    
    # 下方程式碼是為了確認資料是否已存在資料庫中，不會不存在才會進行 API 操作
    # 不然全部都更新資料會太耗時，也有被抓的疑慮
    
    # 使用 crontab
    # os.chdir("/mnt/d/Program_project/stock_review_dashboard")
    db_name = "/mnt/d/Program_project/stock_review_dashboard/twse.db"
    # db_name = "twse.db"

    table_name = "stock_data"
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute(f"SELECT date FROM {table_name} WHERE stock_num={stock_id}")
    existing_data = cur.fetchall()

    check_list = []
    for date in existing_data:
        if date[0][:6] not in check_list:
            check_list.append(date[0][:6])
        else:
            pass

    new_date_list = []
    for date in date_list:
        a = str(int(date[:4])-1911) + "/" + date[4:6]
        if a not in check_list:
            a = str(int(a[:3])+1911) +a[4:6] + "01"
            new_date_list.append(a)
    new_date_list.append(end_date)

    return new_date_list


if __name__ == '__main__':

    # setting the stock list
    # stock_list = {"台積電":"2330", "聯發科":"2454", "台達電":"2308"}
    stock_list = {"台積電":"2330"}    

    # for stock_id in stock_list.values():
    #     date_list = data_range(stock_id, '20210101','20230701')
    #     for date in date_list:
    #         a = get_data(stock_id, date)
    #         print(a)             
    #         time.sleep(1)
    
    for stock_id in stock_list.values():
        date_list = data_range('2308', '20210101','20230712')
        print(date_list)