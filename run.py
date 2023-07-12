from flask import Flask, render_template, request

from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route("/")

def index():
    return "hello!!"

@app.route('/submit', methods=['GET', 'POST'])

def submit():
    return render_template('professional_kline_chart.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)