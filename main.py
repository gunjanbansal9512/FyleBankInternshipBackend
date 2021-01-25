from flask import Flask, jsonify, request
from flask_cors import CORS
DB_HOST = "ec2-54-84-238-74.compute-1.amazonaws.com"
DB_NAME = "degeu1cikkc76v"
DB_USER = "imvqhhchvpvrsw"
DB_PASS = "a58e8ccc9c9ade298bfae086816cce03cfc33273eea8055e95cf60bb0b2297fc"
DB_PORT = "5432"

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
CORS(app)

@app.route('/')
def hello_world():
    return("Hi please pass the parameters like /api/branches/<q>")
@app.route("/api/branches/autocomplete",methods=["GET"])
def getData():
    branch = request.args['q']
    limit = request.args['limit']
    offset = request.args['offset']
    branch.upper()
    myquery = query_db(f"select * from branches where branch like '%{branch}%' limit  {limit} offset {offset}")
    json_output = json.dumps(myquery)
    return json_output
   
@app.route("/api/branches",methods=["GET"])
def getData_all():
    city = request.args['q']
    limit = request.args['limit']
    offset = request.args['offset']
    myquery = query_db(f"select banks.name,banks.id,branches.ifsc,branches.city,branches.district from banks,branches where banks.id = branches.bank_id AND branches.city= '{city}' limit {limit} offset {offset} ")
    json_output = json.dumps(myquery)
    return json_output
    # return request.args['q'] + "" + request.args['limit'] + "" + request.args['offset']
    # return request.args['q']+""+request.args['limit']+""+request.args['offset']
if __name__ == "__main__":
    app.run(debug=True)

