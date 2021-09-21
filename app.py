import os
from predict import main
from flask import Flask,request,render_template
from keras import backend as K

app = Flask(__name__)

    
@app.route('/')
def home():
    """
    Renders a HTML page which allows us to input an image.
    
    """
    return render_template('index.html',title='Home')

@app.route('/predict' ,methods=['POST'])
def predict():
    """
    Main API function which takes path of image from local storage as params with request 
    and uses function main for estimation 
    and covert the result to JSON format
    """
    base_model_name='MobileNet'
    
        
    if request.method == 'POST':
        model_type = request.form.get('scr_select')
        # if request.form['text']=='1':
        #     model_type = 'aesthetic'
        # else:
        #     model_type = 'technical'
    # check if the post request has the file part
        if 'file' not in request.files:
            print(request.files)
            return 'No file found'
    user_file = request.files['file']
    if user_file.filename == '':
        return 'file name not found …'
    else:
        path=os.path.join(os.getcwd(),user_file.filename)
        print(path)
        #user_file.save(path)
        K.clear_session() 
        result = main(base_model_name,model_type,path,None,path.split(".")[-1])
        K.clear_session() 
        
        prediction ={
        f"{model_type} Score Prediction":str(round(eval(result)[0]['mean_score_prediction'],2))+'/10'
        }
    return render_template('result.html',prediction = prediction)

if __name__ == '__main__':
    #ssl_context='adhoc'
    app.run()
            

   




            
           
          


