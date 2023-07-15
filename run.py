from flask import Flask, render_template, request ,jsonify
from flask_cors import CORS
from create_visualize_data import create_new_data
from visualize import StockApp






app = Flask(__name__)

CORS(app)


@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')


@app.route('/stock', methods=['POST','GET'])

def stock_selector():
    # 獲取 POST 請求中的所有參數
    params = request.form

    # 獲取特定參數的值
    selected_stock = params.get('stock')

    stock_app = StockApp()
    stock_app.set_stock_id(selected_stock)  # 設定 stock_id 屬性的值
    stock_app.split_data(selected_stock)
    stock_app.draw_chart(selected_stock)
    
    return render_template(f'{selected_stock}_kline_chart.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)