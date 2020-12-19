from flask import Flask, jsonify ,request
DB_HOST = ""
DB_NAME = "banks"
DB_USER = "postgres"
DB_PASS = "root"
DB_PORT = "5555"

import psycopg2
import json

def query_db(query, args=(), one=False):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute(query)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    conn.commit()
    cur.close()
    conn.close()
    return (r[0] if r else None) if one else r




#print (json_output)


app = Flask(__name__)
@app.route('/')
def hello_world():
    return("Hi please pass the parameters like /api/branches/<q>")
@app.route("/api/branches/autocomplete",methods=["GET"])
def getData():
    branch = request.args['q']
    limit = request.args['limit']
    offset = request.args['offset']
    if (offset == None):
        offset=0
    branch.upper()
    myquery = query_db(f"select * from branches where branch like '%{branch}%' limit  {limit} offset {offset}")
    json_output = json.dumps(myquery)
    return json_output
   
@app.route("/api/branches",methods=["GET"])
def getData_all():
    myquery = query_db("select * from branches")
    json_output = json.dumps(myquery)
    # return json_output
    return request.args['q'] + "" + request.args['limit'] + "" + request.args['offset']
    # return request.args['q']+""+request.args['limit']+""+request.args['offset']
if __name__ == "__main__":
    app.run(debug=True)

