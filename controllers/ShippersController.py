from datetime import datetime
from flask import request
from app import app
from models.ShippersRepository import ShippersRepository
from models.ShippersSampleModel import ShippersSampleModel
from models.ShippersDb import ShippersDb


obj=ShippersSampleModel()
objnew =ShippersDb()
objShippersRepository=ShippersRepository()

@app.route("/Shippers/GetList")
def GetList():
    return objShippersRepository.getAllShippers()
    # return objnew.getAllShippers()
    # return obj.getAllShippers()

@app.route("/Shippers/GetById/<id>")
def GetById(id):
    return obj.getShippersById(id)

@app.route("/Shippers/Save",methods=["POST"])
def Save():
    return obj.addShippers(request.form)

@app.route("/Shippers/Update",methods=["PUT"])
def Update():
    return obj.updateShippers(request.form)

@app.route("/Shippers/Patch/<id>",methods=["PATCH"])
def Patch(id):
    return obj.patchShippers(request.form,id)

@app.route("/Shippers/Delete/<id>",methods=["DELETE"])
def Delete(id):
    return obj.deleteShippers(id)

@app.route("/Shippers/GetList/Between/<Between>/Id/<Id>",methods=["GET"])
def GetPagination(Between,Id):
    return obj.getPaginationShippers(Between,Id)

@app.route("/Shippers/<uid>/avatar/upload", methods=["PATCH"])
def upload_avatar(uid):
    file = request.files['avatar']
    new_filename =  str(datetime.now().timestamp()).replace(".", "") # Generating unique name for the file
    split_filename = file.filename.split(".") # Spliting ORIGINAL filename to seperate extenstion
    ext_pos = len(split_filename)-1 # Canlculating last index of the list got by splitting the filname
    ext = split_filename[ext_pos] # Using last index to get the file extension
    db_path = f"uploads/{new_filename}.{ext}"
    file.save(f"uploads/{new_filename}.{ext}")
    return obj.uploadShippersAvatar(uid, db_path)

@app.route("/user/login")
def user_login():
    auth_data = request.authorization
    return obj.user_login_model(auth_data['username'], auth_data['password'])

@app.route("/user/addmultiple", methods=["POST"])
def add_multiple_users():
    return obj.add_multiple_users_model(request.json)