 
import json
from flask import make_response
import pyodbc

class ShippersDb():
      def __init__(self):

        with open('configuration.json','r') as fh:
            config = json.load(fh)

        self.driver = config['driver']
        self.server = config['server']
        self.database = config['database']
        connection =f"Driver={self.driver};Server={self.server};Database={self.database};Trusted_Connection=yes;"
        print(connection)
        conn = pyodbc.connect(connection)
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

