import sqlite3

# 【Create db function】
def create_database(db_name):
    con = sqlite3.connect(db_name)
    con.close()

# 【Check db function】
def get_all_databases():
    con = sqlite3.connect(':memory:')  # 連接到一個臨時的記憶體資料庫
    cur = con.cursor()
    cur.execute("ATTACH DATABASE 'twse.db' AS twse")  # 附加 twse.db 資料庫
    cur.execute("PRAGMA database_list")  # 使用 PRAGMA 語句檢索所有資料庫
    databases = cur.fetchall()
    con.close()
    return databases


# 【Check table informations function】
def database_info(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("SELECT * FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    con.close()
    return tables


# 【Create table function】
def create_table():
    # db_name = "/mnt/d/Program_project/stock_review_dashboard/twse.db"
    db_name = "twse.db"
    table_name = "stock_data"

    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                stock_num VARCHAR(10),
                date VARCHAR(20),
                opening_price DECIMAL(5,2),
                closing_price DECIMAL(5,2),
                highest_price DECIMAL(5,2),
                lowest_price DECIMAL(5,2),
                Trading_volume INT,
                CONSTRAINT unique_stock_data UNIQUE (stock_num, date)
                )''')

    con.commit()
    con.close()


# 【Delete table function】
def delete_table(db_name, table_name):

    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    con.commit()
    con.close()


if __name__ == "__main__":
    # databases = get_all_databases()
    # for db in databases:
    #     print(db[1])  # 印出資料庫名稱

    # create_database("twse.db")

    # tables = database_info("twse.db")
    # print(tables)

    # delete_table("twse.db", "stock_data")

    create_table()