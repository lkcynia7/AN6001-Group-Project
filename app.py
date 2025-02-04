from flask import Flask
from flask import render_template, request
import textblob
import google.generativeai as genai
import os
import news_sentiment

api = os.getenv("makersuite")
genai.configure(api_key = api)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
@app.route("/", methods = ["GET", "POST"])
def index():
    return (render_template("index.html"))

@app.route("/main", methods = ["GET", "POST"])
def main():
    name = request.form.get("q")
    return (render_template("main.html"))

@app.route('/NS', methods=['GET', 'POST'])
def NS():
    if request.method == 'POST':
        ticker = request.form.get("ticker")
        
        # 如果用户没有输入股票代码，返回错误信息
        if not ticker:
            return render_template("NS.html", error="Please enter a valid ticker")
        
        ticker = ticker.upper()  # 将股票代码转换为大写
        news_items = news_sentiment.get_news_data(ticker)
        df = news_sentiment.process_news_data(news_items, ticker)
        
        if df.empty:
            return render_template("NS.html", error="No news found for " + ticker)
        
        plot_url = news_sentiment.plot_scores(df)  # 获取情绪与相关性散点图的 URL
        return render_template("NS.html", ticker=ticker, news=df.to_dict(orient="records"), plot_url=plot_url)

    # GET 请求时直接渲染空的输入页面
    return render_template("NS.html")

@app.route("/genAI", methods = ["GET", "POST"])
def genAI():
    return (render_template("genAI.html"))

@app.route("/genAI_result", methods = ["GET", "POST"])
def genAI_result():
    q = request.form.get("q")
    r = model.generate_content(q)
    return (render_template("genAI_result.html", r=r.candidates[0].content.parts[0].text))

@app.route("/paynow", methods = ["GET", "POST"])
def paynow():
    return (render_template("paynow.html"))

if __name__ == "__main__":
    app.run()