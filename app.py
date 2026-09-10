from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello Nandhu! CI/CD Automation is 100% SUCCESS! 🔥</h1>"

if __name__ == '__main__':
    # 0.0.0.0 pota thaan velila irunthu access panna mudiyum
    app.run(host='0.0.0.0', port=5000)
