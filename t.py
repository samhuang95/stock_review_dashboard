import sqlite3
from get_data import data_range

db_name = "twse.db"
table_name = "stock_data"
stock_id = "2330"
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


date_list = data_range(stock_id, '20200101', '20230701')
# print(date_list)

new_date_list = []
for date in date_list:
    a = str(int(date[:4])-1911) + "/" + date[4:6]
    if a not in check_list:
        a = str(int(a[:3])+1911) + "/" + a[4:6] + "/01"
        new_date_list.append(a)
print(new_date_list)


    


