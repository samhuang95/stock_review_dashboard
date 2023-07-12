# 股票觀測儀表板
本功能技術主要分為兩個，<br>
一、資料獲取<br>
二、股市 K 線儀表板建立<br>
接下來會依序介紹，並分享程式碼<br>

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/iMboUJK8vsc/0.jpg)](https://www.youtube.com/watch?v=iMboUJK8vsc)

## 一、資料獲取
1. 建立資料庫、資料表：setting_db_and_table.py<br>
   由於之前不斷的測試資料表的格式，所以有放一個以註解的刪除資料表程式碼，如果有需要使用，可以解開<br>
   
2. 更新資料：update_db.py<br>
   資料獲取是使用 TWSE API 進行提取，<br>
   而設定方面，可以看到下面的 stock_list，如果有需要加入其他監測的股票，就可以透過這一段加入，<br>
   而我的 API 也有設定可以設定區間，但只會依據月份，所以只需要填寫每個月的 1 號就好，舉例：20230201，就會直接抓取 2023 年 2 月份所有的資料<br>
   比較需要注意的是，API 呼叫的限制，所以使用 time.sleep() 的方式限制取用資料的速度，經過測試如果時間低於 15 秒就會被 block，所以建議設定 20 秒<br>
   
3. 資料更新完成後，就可以使用：visualize.py<br>
   這個程式內只要調整你要查閱的股票代號，然後執行這個程式<br>
   就會直接產出一個名為「professional_kline_chart.html」的網頁，在裡面可以直接觀看股票內容了<br>
   
## 二、待更新事項
1. 之後會建立可以查閱多個股票的篩選器，只需要篩選對應的股票 ID 就可以查閱，以此提升使用者便捷<br>
2. 預計使用基礎的程式邏輯，並串接到 LINEBOT 中，系統會依循 MACD 指標提出判斷式，提醒是否買進、賣出<br>
3. 使用「反饋強化學習(RLHF)」進行股市預測，提供投資者對低購買金額，並一樣會有相關通知功能<br>

>本儀表板主要是參考外部開源程式進行數據來源調整，參考文件如下：
https://github.com/pyecharts/pyecharts/issues/1844
