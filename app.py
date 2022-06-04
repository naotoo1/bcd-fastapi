# -*- coding: utf-8 -*-
"""
Created on Wed june 02 2020
@author: win10
"""

# import libraries
import uvicorn
from fastapi import FastAPI
from breastcancer import BreastCancer
import pickle
from prosemble import Hybrid
import numpy as np

# 2. Create the app object
app = FastAPI()
pickle_in1 = open("svc.pkl", "rb")
pickle_in2 = open("knn.pkl", "rb")
pickle_in3 = open("dtc.pkl", "rb")

svc = pickle.load(pickle_in1)
knn = pickle.load(pickle_in2)
dtc = pickle.load(pickle_in3)


def get_posterior(x, y_, z_):
    """

    :param x: Input data
    :param y_: prediction
    :param z_: model
    :return: prediction probabilities
    """
    z1 = z_.predict_proba(x)
    certainties = [np.max(i) for i in z1]
    cert = np.array(certainties).flatten()
    cert = cert.reshape(len(cert), 1)
    y_ = y_.reshape(len(y_), 1)
    labels_with_certainty = np.concatenate((y_, cert), axis=1)
    return np.round(labels_with_certainty, 4)


# classes labels
proto_classes = np.array([0, 1])

# object of Hybrid class from prosemble
ensemble = Hybrid(model_prototypes=None, proto_classes=proto_classes, mm=2, omega_matrix=None, matrix='n')


# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'model to classify breast cancer'}


# 4. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted cancer with the confidence
@app.post('/predict')
def predict_BreastCancer(data: BreastCancer):
    data = data.dict()
    Radius_mean = data['Radius_mean']
    Radius_texture = data['Radius_texture']
    Method = data['Method']

    # prediction using the svc,knn and dtc models
    pred1 = svc.predict([[Radius_mean, Radius_texture]])
    pred2 = knn.predict([[Radius_mean, Radius_texture]])
    pred3 = dtc.predict([[Radius_mean, Radius_texture]])

    # confidence of prediction using the svc,knn and dtc models respectively
    sec1 = get_posterior(x=[[Radius_mean, Radius_texture]], y_=pred1, z_=svc)
    sec2 = get_posterior(x=[[Radius_mean, Radius_texture]], y_=pred2, z_=knn)
    sec3 = get_posterior(x=[[Radius_mean, Radius_texture]], y_=pred3, z_=dtc)
    all_pred = [pred1, pred2, pred3]
    all_sec = [sec1, sec2, sec3]
    # prediction from the ensemble using hard voting
    prediction1 = ensemble.pred_prob([[Radius_mean, Radius_texture]], all_pred)
    # prediction from the ensemble using soft voting
    prediction2 = ensemble.pred_sprob([[Radius_mean, Radius_texture]], all_sec)
    # confidence of the prediction using hard voting
    hard_prob = ensemble.prob([[Radius_mean, Radius_texture]], all_pred)
    # confidence of the prediction using soft voting
    soft_prob = ensemble.sprob([[Radius_mean, Radius_texture]], all_sec)
    if Method == 'soft':
        if prediction2[0] > 0.5:
            prediction2 = "WDBC-Benign {}"
        else:
            prediction2 = "WDBC-Malignant {}"
        return {
            'prediction': prediction2.format(soft_prob[0]),

        }
    if Method == 'hard':
        if prediction1[0] > 0.5:
            prediction1 = "WDBC-Benign {}"
        else:
            prediction1 = "WDBC-Malignant {}"
        return {
            'prediction': prediction1.format(hard_prob[0])
        }


# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

# uvicorn app:app --reload
