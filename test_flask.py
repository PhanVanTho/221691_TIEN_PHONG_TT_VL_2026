from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "FLASK DANG CHAY OK"

@app.route("/tao-giao-trinh")
def tao():
    chu_de = request.args.get("chu_de", "Chua co")
    return f"Chu de: {chu_de}"

if __name__ == "__main__":
    app.run(debug=True)
