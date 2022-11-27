from urllib import request
import numpy as np
import pandas as pd
from flask import Flask, jsonify,request
import pickle

app = Flask(__name__)
model = pickle.load(open('blood_donation_model.pkl','rb'))

@app.route('/prediction', methods=["GET"])
def prediction():
    recency = int(request.args.get('recency'))
    frequency = int(request.args.get('frequency'))
    monetary = float(request.args.get('monetary'))
    time = int(request.args.get('time'))
    input_features = list()
    input_features.append(recency/74)
    input_features.append((frequency-1)/49)
    input_features.append((monetary-250)/(12500-250))
    input_features.append((time-2)/(98-2))
    features_value = [np.array(input_features)]
    features_name = ["Recency","Frequency","Monetary","Time"]
    df = pd.DataFrame(features_value,columns=features_name)
    output = model.predict(df)
    return jsonify({
        "Prediction" : str(output[0])
    })

if __name__ == '__main__':
    app.run(debug=True)