from  flask import Flask
app=Flask(__name__)

@app.route("/")
def Welcome():
    return "Welcome to flask..!"

# from app.main.controllers import *
from  controllers import *
 





