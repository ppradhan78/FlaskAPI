import json
import pyodbc

class GenericRepository:
  def __init__(self):
    with open('configuration.json','r') as fh:
      config = json.load(fh)

    self.driver = config['driver']
    self.server = config['server']
    self.database = config['database']
    connection_string =f"Driver={self.driver};Server={self.server};Database={self.database};Trusted_Connection=yes;"  

    self.connection_string = connection_string
    self.connect()

  def connect(self):
    self.conn = pyodbc.connect(self.connection_string)
    self.cursor = self.conn.cursor()

  def close(self):
    self.cursor.close()
    self.conn.close()

  def get(self, id, table_name):
    query = f"SELECT * FROM {table_name} WHERE id = %s"
    self.cursor.execute(query, (id,))
    return self.cursor.fetchone()

  def list(self, table_name):
    query = f"SELECT * FROM {table_name}"
    self.cursor.execute(query)
    return self.cursor.fetchall()

  def create(self, table_name, data):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    values = tuple(data.values())
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    self.cursor.execute(query, values)
    self.conn.commit()

  def update(self, id, table_name, data):
    set_clause = ", ".join([f"{key} = %s" for key in data])
    values = tuple(data.values()) + (id,)
    query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"
    self.cursor.execute(query, values)
    self.conn.commit()

  def delete(self, id, table_name):
    query = f"DELETE FROM {table_name} WHERE id = %s"
    self.cursor.execute(query, (id,))
    self.conn.commit()