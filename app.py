# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 20:27:03 2020

@author: Aruna
"""
from flask import session


import numpy as np
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import pickle
import json

app = Flask(__name__)

cors = CORS(app)
app.secret_key = "Secret"

app.config['CORS_HEADERS'] = 'Content-Type'
liver = pickle.load(open('liverRF.pkl', 'rb'))
#hyp = pickle.load(open('hyp3way.pkl', 'rb'))
anemia = pickle.load(open('Anemiafiltered.pkl', 'rb'))
kid= pickle.load(open('kid.pkl', 'rb'))
heart = pickle.load(open('RF.pkl', 'rb'))
dia_both = pickle.load(open('both.pkl', 'rb'))
dia_waist = pickle.load(open('noWaist.pkl', 'rb'))
dia_trig = pickle.load(open('noTrigs983.pkl', 'rb'))
dia_all = pickle.load(open('done.pkl', 'rb'))
#global score1,score2,score3,score4,score5



@app.route('/')
def home():
    return render_template('liver.html')

@app.route('/predictLiverDisease',methods=['POST'])
@cross_origin()
def predict1():
    '''
    For rendering results on HTML GUI
    '''
    if("text" == "M"):
        text = 1
    else:
        text =0
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    
    prediction = liver.predict(final_features)
    prediction=liver.predict_proba(final_features)
    global score1
    alpha=0.80
    beta=0.80
   # finalProb=
    # for i in prediction:
    #  # print("list: i is:",i)
    #   if i[1] > alpha and i[1]> i[0]:
    #     ele =i[1]
    #    # print("positive")
    #     add=1
    #     finalProb=add
    #     #finalLabelProb.append(add)
    
    #   elif i[0]>beta and i[0]>i[1]:
    #    # print("negative")
    #     add=0
    #     finalProb= add
    #     #finalLabelProb.append(add)
    #   else:
    #     #print("abstention incurred")
    #     add=2
    #     ##remove prob with target as 2
    #     finalProb=add
    pos= prediction[0]
    #neg=prediction[1]
    if pos[1]>0.50:
        score=20
    else:
        score=0
        
    output = score
    score1=score
    session['score1']=int(score1)
    # if output==0:
    #     output1='Normal'
    # elif output==1 or output==2:
    #     output1='Liver Disease'
    #output = finalProb
    #also display output from 'prediction' variable

    return render_template('anemia.html', prediction_text='Liver score: {}'.format(score))

#####################anemia model

@app.route('/predictAnemia',methods=['POST'])
@cross_origin()
def predict2():
    '''
    For rendering results on HTML GUI
    '''

    if("text" == "Male"):
        text = 0
    else:
        text =1
    global score2

    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    
   # prediction = model.predict_proba(final_features)
    prediction =  anemia.predict_proba(final_features)
    pos= prediction[0]
    #neg=prediction[1]
    if pos[1]>0.50:
        score=20
    else:
        score=0
        
    output = score
    score2=score
    session['score2']=int(score2)

    # output = prediction[0]
    # if output>0.7:
    #     output1='Normal'
    # elif output==1:
    #     output1='Anemic'


    return render_template('kid.html', prediction_text='Blood Score: {}'.format(output))

##########################KDC

@app.route('/predictKDC',methods=['POST'])
@cross_origin()
def predict3():
    '''
    For rendering results on HTML GUI
    '''

    # if("text" == "M"):
    #     text = 0
    # else:
    #     text =1

    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    
    prediction = kid.predict_proba(final_features)
    #prediction =  kid.predict(final_features)
    pos= prediction[0]
    #neg=prediction[1]
    if pos[1]>0.50:
        score=20
    else:
        score=0
        
    output = score
    # output = prediction[0]
    # if output<0.5:
    #     output1='Normal'
    # elif output>0.5:
    #     output1='Chronic Kidney Disease'
    score3=score
    session['score3']=int(score3)


    return render_template('heart.html', prediction_text='Kidney score {}'.format(output))

######################CHD
    
@app.route('/predictCHD',methods=['POST'])
@cross_origin()
def predict4():
    '''
    For rendering results on HTML GUI
    '''
    global score4

    if("text" == "M"):
        text = 0
    else:
        text =1

    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    
   # prediction = model.predict_proba(final_features)
    prediction =  heart.predict_proba(final_features)
    pos= prediction[0]
    #neg=prediction[1]
    if pos[1]>0.50:
        score=20
    else:
        score=0
        
    output = score
    score4=score
    session['score4']=int(score4)
    # output = prediction[0]
    # if output<0.5:
    #     output1='Normal'
    # elif output>0.5:
    #     output1='10yr CHD risk'


    return render_template('dia.html', prediction_text='Heart score {}'.format(output))


############DIABETES
@app.route('/predictDiabetes',methods=['POST'])
@cross_origin()
def predict5():
    global score5
    '''
    For rendering results on HTML GUI
    '''

    if("text" == "M"):
        text = 0
    else:
        text =1
    int_features1=[]

    int_features = [float(x) for x in request.form.values()]
    for i in int_features:
        #for male, it is zero
        if i != 100:
            int_features1.append(i)
        
    final_features = [np.array(int_features1)]
    
    if int_features[3]==100 and int_features[9]==100:
        prediction = dia_both.predict_proba(final_features)
    elif int_features[9]==100:
        prediction = dia_trig.predict_proba(final_features)
    elif int_features[3]==100:
        prediction = dia_waist.predict_proba(final_features)
    else:
        prediction = dia_all.predict_proba(final_features)
    
    pos= prediction[0]
   #neg=prediction[1]
    if pos[1]>0.50:
        score=20
    else:
        score=0
        
    output = score
    score5=score
    session['score5']=int(score5)


    # output = prediction[0]
    # if output==0:
    #     output1='Normal'
    # elif output==1:
    #     output1='Diabetic'
    # elif output==2:
    #     output1='Pre-Diabetic'

    return render_template('index.html', prediction_text='Sugar level score {}'.format(output))
################################HEALTH SCORE

@app.route('/predictHealthScore',methods=['POST'])
@cross_origin()
def predict():
    '''
    For rendering results on HTML GUI
    '''
    score1=session.get('score1')
    score2=session.get('score2')
    score3=session.get('score3')
    score4=session.get('score4')
    score5=session.get('score5')

    final_score = score1+score2+score3+score4+score5
    if final_score>70:
    
        return render_template('index.html', prediction_text='You are Healthy:) and your health score is {}'.format(final_score))

    else:
        score=0

    

        return render_template('index.html', prediction_text='You need to consult doctor because your health score is {}'.format(final_score))



if __name__ == "__main__":
    app.run(debug=True)
