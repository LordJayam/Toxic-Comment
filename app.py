from flask import request,jsonify
from flask import Flask
from fastai.text import *
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jayamkavan'
app.config['MYSQL_DB'] = 'JUHack'

mysql = MySQL(app)


path = Path("")
learn = load_learner(path,"export.pkl")

@app.route('/api/threat_classification', methods=['POST'])
def get_text_prediction():
    json = request.get_json()
    #print("data")
    data = json["data"]
    a  = classify(data)
    return a


def classify(data):
        losses = learn.predict(data)
        return   '{"ans": "' + str(losses[0]) + '"}'

@app.route('/api/feedback',methods = ['POST'])
def put_feedback():
    #get_data("abc",0,0,0,0,0,0)
    json = request.get_json()
    data = json["data"]
    text = data["text"]
    flags = json["data"]["flag"]

    get_data(text,flags["toxic"],flags["severe_toxic"],flags["obscene"],flags["threat"],flags["insult"],flags["identity_hate"])
    return "True"

def get_data(text,toxic,severe_toxic,obscene,threat,insult,identity_hate):
        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO `user_data`
        ( `text`, `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`)
        VALUES (%s,%s,%s,%s,%s,%s,%s) """, (text,toxic,severe_toxic,obscene,threat,insult,identity_hate))
        mysql.connection.commit()
        cur.close()
        #train_data()

def train_data():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM user_data WHERE flag = 0 """)
    data = cur.fetchall()

    df = pd.DataFrame(columns = ["text","toxic","severe_toxic","obscene","threat","insult","identity_hate"])

    count = 0
    for i in data:
        df.loc[count] = {"text":i[1],"toxic":i[2],"severe_toxic":i[3],"obscene":i[4],"threat":i[5],"insult":i[6],"identity_hate":i[7]}
        count+=1
    #if(count >=100):
    print(df)


if __name__ == '__main__':
    app.run("localhost",2190)
