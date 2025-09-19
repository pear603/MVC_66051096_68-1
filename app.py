from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.before_request
def prepare_data():
    # This function runs before each request to prepare necessary data
    pass

@app.route("/")
def home():    
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)