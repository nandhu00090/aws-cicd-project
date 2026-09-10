from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello Nandhu! Welcome to your AWS CI/CD Pipeline!</h1>"

if __name__ == '__main__':
    # 0.0.0.0 pota thaan velila irunthu access panna mudiyum
    app.run(host='0.0.0.0', port=5000)
