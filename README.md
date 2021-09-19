# Automated Image Quality Estimation Application
A model for getting automatically learned quality assessment for input images. The model can estimate two type of scores on a scale of 10: Aesthetic and Technical, based on the input. Aesthetic score quantifies semantic level characteristics associated with emotions and beauty in images whereas technical score quantifies quality metrics such as noise, blur, compression etc. <br>
#### Contents
* `data_generator.py` contain functions for preprocessing of images<br>
* `flaskapi.py` is the Flask API without UI
* `losses.py` is the loss function 
* `model_builder.py` loads the Google's NIMA model
* `predict.py` & `utils.py` contain necessary binding functions
* `routes.py` is the Flask API file with UI
* [models](models/) folder contain saved models and their weights, which are deployed in our application
* [templates](templates/) folder contain the frontend of the application 

### Dataset
Aesthetic model is trained on [Aesthetic Visual Analysis (AVA) dataset](https://github.com/mtobeiyf/ava_downloader).<br>
Technical model is trained on [TID2013 test set dataset](https://paperswithcode.com/dataset/tid2013).<br>

### Reference
> * To read about approach and architecture used, go to [this paper](https://arxiv.org/pdf/1709.05424.pdf).
