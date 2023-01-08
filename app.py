from flask import Flask, render_template,  request, flash, session,  current_app
from flask_session import Session
from pymongo import MongoClient
from flask_pymongo import PyMongo
from IA.nlp import*
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = "zozo"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MONGO_URI'] = f"mongodb+srv://Manuel:pwd@cluster0.ntszcrx.mongodb.net/Manuel"
#app.config['MONGO_URI'] = f"mongodb+srv://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@cluster0.ntszcrx.mongodb.net/{os.environ['MONGODB_DATABASE']}"
mongo = PyMongo(app)
db = mongo.db.Jobs
ident = mongo.db.ids
Session(app)
tech_terms = ['python', 'r', 'sql', 'hadoop', 'spark', 'java', 'sas', 'tableau',
              'hive', 'scala', 'aws', 'c', 'c++', 'matlab', 'tensorflow', 'excel',
              'nosql', 'linux', 'azure', 'scikit', 'machine learning', 'statistic',
              'analysis', 'computer science', 'visual', 'ai', 'deep learning',
              'nlp', 'natural language processing', 'neural network', 'mathematic',
              'database', 'oop', 'blockchain',
              'html', 'css', 'javascript', 'jquery', 'git', 'photoshop', 'illustrator',
              'word press', 'seo', 'responsive design', 'php', 'mobile', 'design', 'react',
              'security', 'ruby', 'fireworks', 'json', 'node', 'express', 'redux', 'ajax',
              'java', 'api', 'state management',
              'wireframe', 'ui prototype', 'ux writing', 'interactive design',
              'metric', 'analytic', 'ux research', 'empathy', 'collaborate', 'mockup', 
              'prototype', 'test', 'ideate', 'usability', 'high-fidelity design',
              'framework',
              'swift', 'xcode', 'spatial reasoning', 'human interface', 'core data',
              'grand central', 'network', 'objective-c', 'foundation', 'uikit', 
              'cocoatouch', 'spritekit', 'scenekit', 'opengl', 'metal', 'api', 'iot',
              'karma']
global client
client = []
@app.route('/')
def main():
    return render_template('login.html')

@app.route('/redirect')
def redirect():
    return render_template('signup.html')

@app.route('/login',methods=['POST'])
def signin():   
    password = request.form['pswd']
    email = request.form['email']
    session['my_var'] = email
    val = ident.find({"Email":email}).next()
    if val:
        if val['Password'] == password:
            nom = val['Nom']
            flash("Hello "+nom+"!")
            session['client'] = pd.DataFrame(list(db.find())).drop("_id",axis=1).to_dict()
            return render_template('index.html',skills = tech_terms)
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
    val = ident.find_one({"Email":email}) 
    if val!=None :
        flash('Email address already exists go to login page',"error")
        return render_template('signup.html')
    else :
        ident.insert_one(dico)
        return render_template('login.html')
  
    

@app.route('/pred', methods=['POST'])
def clt():
    """em = session.get('my_var', None)
    name = ident.find_one({'Email':em}).next()['Nom']"""
    client = pd.DataFrame(session['client'])
    data1 = request.form['Job'].lower()
    data2 = request.form['Location'].lower()
    data3 = request.form['Skill1'].lower()
    data4 = request.form['Skill2'].lower()
    data5 = request.form['Skill3'].lower()
    skillset = data3+" "+data4+" "+data5
    jober = {"Job":data1,"Location":data2,"skills":skillset}
    #processus de matching
    dummies,vectorizer = init(client)
    pred = match(jober,0.8,client,dummies,vectorizer)
    result = pred[['job_title','description','location','company','high_salary']]
    return render_template('after.html', tables=[result.to_html(classes='data')], titles=result.columns.values)

if __name__ == "__main__":
    app.run(debug=True,port=5000)