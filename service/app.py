from flask import Flask

app = Flask(__name__)

@app.route("/")
def test():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)

# TODO: Switch to using a seperate config file