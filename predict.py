"""
https://ai.googleblog.com/2017/12/introducing-nima-neural-image-assessment.html
"""
import os
import glob
import json
import pandas as pd
import numpy as np
from utils import calc_mean_score, save_json
from model_builder import Nima
from data_generator import DataGenerator

# Function to read the Excel file and convert it to a list of dictionaries
def excel_to_json(excel_path, url_column='image_urls'):
    df = pd.read_excel(excel_path)
    # Find a column that contains the substring 'image_id'
    image_id_column = next((col for col in df.columns if 'image_id' in col.lower()), None)
    item_id_column = next((col for col in df.columns if 'accommodation_id' in col.lower()), None)
    if image_id_column and item_id_column:
        samples = [{'item_id': row[item_id_column],'image_id': row[image_id_column], 'image_url': row[url_column]} for _, row in df.iterrows()]
    else:
        samples = [{'image_id': os.path.basename(url).split('.')[0], 'image_url': url} for url in df[url_column]]
    return samples

def image_file_to_json(img_path):
    img_dir = os.path.dirname(img_path)
    img_id = os.path.basename(img_path).split('.')[0]

    return img_dir, [{'image_id': img_id}]


def image_dir_to_json(img_dir, img_type='jpg'):
    img_paths = glob.glob(os.path.join(img_dir, '*.'+img_type))

    samples = []
    for img_path in img_paths:
        img_id = os.path.basename(img_path).split('.')[0]
        samples.append({'image_id': img_id})

    return samples


def predict_sequentially(model, data_generator):
    predictions = []
    for batch in data_generator:
        if isinstance(batch, tuple) and len(batch) == 2:
            batch_data = batch[0]
        else:
            batch_data = batch

        batch_predictions = model.predict_on_batch(batch_data)
        predictions.append(batch_predictions)
    # Concatenate all batch predictions
    return np.concatenate(predictions, axis=0)


def main(base_model_name, model_type, image_source,image_dir, predictions_file=None, csv_file=None, retrained=False):
    dirname = os.path.dirname(__file__)
    if retrained:
        weights_file = glob.glob(os.path.join(dirname, f'models/*{model_type}-enhanced*.hdf5'))[0]
    else:
        weights_file = glob.glob(os.path.join(dirname, f'models/*weights_mobilenet_{model_type}*.hdf5'))[0]
    
    if os.path.isfile(image_source) and image_source.endswith(('.xlsx', '.xls')):
        samples = excel_to_json(image_source)
    else:
        image_dir = image_source if os.path.isdir(image_source) else os.path.dirname(image_source)
        samples = image_dir_to_json(image_dir)
    print(samples)
    nima = Nima(base_model_name)
    nima.build()
    nima.nima_model.load_weights(weights_file)
    model = nima.nima_model

    data_generator = DataGenerator(samples, image_dir, batch_size=64, n_classes=10, basenet_preprocess=nima.preprocessing_function())

    predictions = predict_sequentially(model, data_generator)

    for i, sample in enumerate(samples):
        sample[f'{model_type}_mean_score_prediction'] = round(calc_mean_score(predictions[i]), 2)

    result = json.dumps(samples, indent=2)

    if predictions_file:
        save_json(samples, predictions_file)

    if csv_file:
        df = pd.DataFrame(samples)
        df.to_csv(csv_file, index=False)
        print(f"Results saved to {csv_file}")

    return samples


if __name__ == '__main__':
    base_model_name='MobileNet'
    model_types = ['aesthetic','technical']
    image_dir = "/Users/kverma/Downloads/Hackathon/ImageQualityScore/images/sampleimages"

    # for model_type in model_types:
    #     predictions_file = f'predictions_{model_type}-test.json'
    #     main(base_model_name, model_type, 'test_images.xlsx', predictions_file,f'predictions-{model_type}-test.csv')
    main(base_model_name, 'aesthetic', '/Users/kverma/Downloads/Hackathon/all20images.xlsx', image_dir, f'predictions_aesthetic-trinima.json',f'predictions-aesthetic-trinima.csv', retrained=True)

