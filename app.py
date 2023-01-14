from flask import Flask, render_template,  request, flash, session, jsonify,current_app
from flask_session import Session
from googletrans import Translator
from pymongo import MongoClient
from IA.nlp import prediction
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'u'
app.config['SESSION_TYPE'] = 'filesystem'
def get_db():
    client = MongoClient(host='mongodb',port=27017, username=os.environ.get('MONGO_USERNAME'),password=os.environ.get('MONGO_PASSWORD'),authSource="admin")
    db = client["Sentiment"]
    return db
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/redirect')
def redirect():
    return render_template('signup.html')

@app.route('/login',methods=['POST'])
def signin():   
    password = request.form['pswd']
    email = request.form['email']
    session['my_var'] = email
    ident = get_db().ident
    val = ident.find_one({"Email":email})
    if val:
        if val['Password'] == password:
            nom = val['Nom']
            flash("Hello "+nom+"!")
            #session['client'] = pd.DataFrame(list(db.find())).drop("_id",axis=1).to_dict()
            return render_template('index.html')
        else:
            flash("Wrong password!","error")
            return render_template('login.html')
    else:
        flash("User not found! You must sign up","error")
        return render_template('login.html')



@app.route('/signup',methods=['POST'])
def signup():
    
    name = request.form['name']
    email = request.form['mail']
    password = request.form['pass']
    dico = {"Nom": name,"Email": email, "Password": password}
    ident = get_db().ident
    val = ident.find_one({"Email":email}) 
    if val!=None :
        flash('Email address already exists go to login page',"error")
        return render_template('signup.html')
    else :
        ident.insert_one(dico)
        return render_template('login.html')
    

@app.route('/pred', methods=['POST'])
def clt():
    data1 = request.form['lang'].lower()
    data2 = request.form['sentence'].lower()
    if data1=='french':
        tr = Translator()
        data2 = tr.translate(data2,dest='fr').text
    df = prediction(data2)
    return render_template('after.html',tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == "__main__":
    app.run(debug=True,port=5000)