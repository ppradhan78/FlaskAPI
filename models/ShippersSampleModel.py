import json
import pyodbc
from flask import make_response
from datetime import datetime, timedelta
import jwt
# from configs.config import dbconfig

class ShippersSampleModel():

    def __init__(self):
           
           with open('configuration.json','r') as fh:
               config = json.load(fh)

           self.driver = config['driver']
           self.server = config['server']
           self.database = config['database']    
           #connStr="Driver=SQL Server;Server=home\\SQLEXPRESS;Database=Northwind;Trusted_Connection=yes;"
           connStr=f"Driver={self.driver};Server={self.server};Database={self.database};Trusted_Connection=yes;"
           conn = pyodbc.connect(connStr)
           conn.autocommit=True
           self.cur = conn.cursor()
    
    def getAllShippers(self):
        self.cur.execute('select  * from Shippers')
        result = self.cur.fetchall()
        results = [tuple(row) for row in result]
        if len(results)>0:
            res=make_response({"payload":results},200)
            res.headers['Access-Control-Allow-Origin']="*"
            return res
        else:
            return make_response({"message":"No Records are found."},204)
        
    def getShippersById(self,id):
        self.cur.execute('select  * from Shippers where ShipperID='+id)
        result = self.cur.fetchall()
        results = [tuple(row) for row in result]
        if len(results)>0:
            res=make_response({"payload":results},200)
            res.headers['Access-Control-Allow-Origin']="*"
            return res
        else:
            return make_response({"message":"No Records are found."},204)
        
    def addShippers(self,data):
        print(data)
        CompanyName=data['CompanyName']
        Phone=data['Phone']
        self.cur.execute(f"INSERT INTO Shippers(CompanyName,Phone)VALUES('{CompanyName}','{Phone}')")
        return make_response({"message":"Shippers information Save Successfully."},201)
    
    def updateShippers(self,data):
        CompanyName=data['CompanyName']
        Phone=data['Phone']
        ShipperID=data['ShipperID']
        self.cur.execute(f"UPDATE Shippers SET CompanyName='{CompanyName}' , Phone='{Phone}' WHERE ShipperID={ShipperID}")
        if self.cur.rowcount>0:
             return make_response({"message":"Shippers information Updated Successfully."},204)
        else:
             return make_response({"message":"Nothing to Update Shippers information."},202)
        
    def deleteShippers(self,id):
        self.cur.execute(f"DELETE FROM Shippers WHERE ShipperID={id}")
        if self.cur.rowcount>0:
             return make_response( {"message":"Shippers information Deleted Successfully."},200)
        else:
             return make_response({"message":"Nothing Deleted Shippers information."},202)    
        
    def patchShippers(self,data,id):
        # query=f"UPDATE Shippers SET CompanyName='{CompanyName}' , Phone='{Phone}' WHERE ShipperID={ShipperID}"
        query="UPDATE Shippers SET "
        for key in data:
             query += f"{key}='{data[key]}',"
        
        query = query[:-1] + f" WHERE ShipperID={id}"     
        print(query)
        self.cur.execute(query)
        if self.cur.rowcount>0:
             return make_response( {"message":"Shippers information Updated Successfully."},200)
        else:
             return make_response({"message":"Nothing Updated Shippers information."},202)        
        
    def getPaginationShippers(self,Between,Id):
        Between=int(Between)
        Id=int(Id)
        start=(Id*Between)-Between
        query=f"select  * from Shippers WHERE ShipperID Between {Between} and {start}"
        print(query)
        self.cur.execute(query)
        result = self.cur.fetchall()
        results = [tuple(row) for row in result]
        if len(results)>0:
            res=make_response({"payload":results,"page_no":Id,"limit":Between},200)
            res.headers['Access-Control-Allow-Origin']="*"
            return res
        else:
            return make_response({"message":"No Records are found."},204)
        
    def uploadShippersAvatar(self, uid, db_path):
        self.cur.execute(f"UPDATE Shippers SET avatar='{db_path}' WHERE ShipperID={uid}")
        if self.cur.rowcount>0:
            return make_response({"message":"FILE_UPLOADED_SUCCESSFULLY", "path":db_path},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)   
        
    def user_login_model(self, username, password):
        self.cur.execute(f"SELECT id, roleid, avatar, email, name, phone from users WHERE email='{username}' and password='{password}'")
        result = self.cur.fetchall()
        if len(result)==1:
            exptime = datetime.now() + timedelta(minutes=15)
            exp_epoc_time = exptime.timestamp()
            data = {
                "payload":result[0],
                "exp":int(exp_epoc_time)
            }
            print(int(exp_epoc_time))
            jwt_token = jwt.encode(data, "Sagar@123", algorithm="HS256")
            return make_response({"token":jwt_token}, 200)
        else:
            return make_response({"message":"NO SUCH USER"}, 204)
                

    def add_multiple_users_model(self, data):
        # Generating query for multiple inserts
        qry = "INSERT INTO users(name, email, phone, roleid, password) VALUES "
        for userdata in data:
            qry += f" ('{userdata['name']}', '{userdata['email']}', '{userdata['phone']}', {userdata['roleid']},'{userdata['password']}'),"
        finalqry = qry.rstrip(",")
        self.cur.execute(finalqry)
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)            