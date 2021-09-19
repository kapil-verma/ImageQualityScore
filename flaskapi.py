#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 03:37:01 2021

@author: kapilverma
"""
from predict import main
from flask import Flask,request

app = Flask(__name__)

    
@app.route('/predict')
def predict():
    """
    Main API function which takes path of image from local storage as params with request 
    and uses function main for estimation 
    and covert the result to JSON format
    """
    print(""""give params for model_type and path as:
    predict?model_type=aesthetic&path=/path/to/file""")
    
    base_model_name='MobileNet'
    model_type = request.args.get('model_type')
    path = request.args.get('path')

    result = main(base_model_name,model_type,path,None)
    
    return result

if __name__ == '__main__':
    #example
    #http://127.0.0.1:5000/predict?model_type=aesthetic&path=/Users/kapilverma/Downloads/Hotel_recognition/Hotels-50K/hotels50k_snapshot/images/test/
    
    #ssl_context='adhoc'
    app.run()