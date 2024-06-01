from flask import make_response
from models.GenericRepository import GenericRepository

class ShippersRepository:
  def __init__(self):
    self.shippersRepository = GenericRepository()

  def getAllShippers(self):
    result=self.shippersRepository.list("Shippers")
    results = [tuple(row) for row in result]
    if len(results)>0:
            res=make_response({"payload":results},200)
            res.headers['Access-Control-Allow-Origin']="*"
            self.shippersRepository.close()
            return res
    else:
            self.shippersRepository.close()
            return make_response({"message":"No Records are found."},204)  