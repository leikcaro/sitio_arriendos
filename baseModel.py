#consultas RAW 
from django.db import connection

class BaseModel:
    
    def ExecuteQuery(sql,params=None):
        cursor = connection.cursor()
        cursor.execute(sql,params if params is not None else [])

        print(cursor.description)#data
        #recorrer la data
        #retornar un list[dicc]
        return []

    def Execute(sql,params=None):
        cursor = connection.cursor()
        cursor.execute(sql,params if params is not None else [])
        try:
            queryRow = cursor.fetchone()
            if queryRow is not None:
                return queryRow
            else:
                return []
        except Exception as e:
            print("error:", e)
            return []