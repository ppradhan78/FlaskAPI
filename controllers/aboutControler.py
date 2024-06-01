from app import app

@app.route("/about/index")
def index():
    return "Welcome to about."