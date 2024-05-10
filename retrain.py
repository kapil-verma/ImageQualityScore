import h5py
import cv2
import glob
import json
import numpy as np
from model_builder import Nima
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from losses import earth_movers_distance
import matplotlib.pyplot as plt

def load_data(scores_path):
    with h5py.File(scores_path, 'r') as h5f:
        scores = h5f['image_scores'][:]
    return scores

def load_scores(scores_path, image_id_path):
    with h5py.File(image_id_path, 'r') as f:
        ids = [i.decode('utf-8') for i in f['train_image_ids'][:]]
    scores = load_data(scores_path)
    
    # Create a dictionary to map ids to scores
    id_score_dict = dict(zip(ids, scores))
    return id_score_dict

def load_files(file_directory, scores_dict):
    """ Function to read images and convert them to acceptable input shape for the model """
    images = []
    scores = [] 
    print(scores_dict)
    for image_id, score in scores_dict.items():
        image_pattern = f"{file_directory}/*{image_id}*jpeg"
        print(image_pattern)
        matching_files = glob.glob(image_pattern)

        if len(matching_files) > 0:
            img_path = matching_files[0]
        else:
            print(f'Warning: No image found for image_id: {image_id} Skipping this image.')
            continue

        img = cv2.imread(img_path)

        if img is None:
            print(f'Warning: Failed reading image at {img_path} Skipping this image.')
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        images.append(img)
        scores.append(score)

    images = np.array(images)
    scores = np.array(scores)

    return images, scores

def retrain_nima_model(model_path, model_type, X_train=None, y_train=None, X_val=None, y_val=None):
    with open(f'models/config_{model_type}_cpu.json', 'r') as config_file:
        config = json.load(config_file)

    learning_rate = config['learning_rate_all']
    decay = config['decay_all']
    batch_size = config['batch_size']
    epochs = config['epochs_train_all']

    nima = Nima('MobileNet')
    nima.build()
    nima.nima_model.load_weights(model_path)
    optimizer = Adam(learning_rate=learning_rate, decay=decay)
    nima.nima_model.compile(optimizer=optimizer, loss=earth_movers_distance)
    if np.any(np.isnan(X_train)):
        print("NaNs found in X_train.")
    if np.any(np.isnan(y_train)):
        print("NaNs found in y_train.")

    history = nima.nima_model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size)
    nima.nima_model.save(f'models/{model_type}-enhanced.hdf5')
    print(nima.nima_model.summary())
    y_pred = nima.nima_model.predict(X_val)
    emd_score = earth_movers_distance(y_val, y_pred)

    print("Earth Mover's Distance on Validation set:", emd_score)
    return nima.nima_model, history, y_pred

def plot_history(history):
    plt.figure(figsize=(12, 6))

    # Plot loss
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train loss')
    plt.plot(history.history['val_loss'], label='Validation loss')
    plt.title('Loss over epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()

def plot_distributions(y_true, y_pred):
    score_classes = y_true.shape[1]  
    # Calculate mean and standard deviation for both actual and predicted scores
    actual_mean = np.mean(y_true, axis=0)
    predicted_mean = np.mean(y_pred, axis=0)
    actual_std = np.std(y_true, axis=0)
    predicted_std = np.std(y_pred, axis=0)
    
    # Prepare histogram plot
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
    axes[0].hist(np.argmax(y_true, axis=1), bins=np.arange(0, score_classes+1)-0.5, alpha=0.7, label='Actual Scores')
    axes[0].hist(np.argmax(y_pred, axis=1), bins=np.arange(0, score_classes+1)-0.5, alpha=0.7, label='Predicted Scores')
    axes[0].set_xlabel('Scores')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Histogram of Actual and Predicted Scores')
    axes[0].set_xticks(np.arange(score_classes))
    axes[0].legend()

    # Prepare error bar plot for mean and standard deviation
    x = np.arange(len(actual_mean))  # the label locations
    width = 0.35  # the width of the bars
    
    axes[1].bar(x - width/2, actual_mean, width, yerr=actual_std, label='Actual Mean and STD', capsize=5, alpha=0.7)
    axes[1].bar(x + width/2, predicted_mean, width, yerr=predicted_std, label='Predicted Mean and STD', capsize=5, alpha=0.7)
    
    axes[1].set_xlabel('Scores')
    axes[1].set_ylabel('probabilities')
    axes[1].set_title('Mean and Standard Deviation of Actual proportion and Predicted probability')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(np.arange(score_classes))
    axes[1].legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # load images and scores 
    good_images, good_scores = load_files('/Users/kverma/Downloads/Hackathon/images/GOD_FM_images', load_scores('features/trainImageScores.h5','features/trainImageIds.h5'))
    bad_images, bad_scores = load_files('/Users/kverma/Downloads/Hackathon/images/badimages', load_scores('features/badImageScores.h5','features/badImageIds.h5'))
    images = np.concatenate([good_images, bad_images])
    
    scores = np.concatenate([good_scores, bad_scores])
    scores_onehot = np.eye(10)[scores.astype('int32')]
    X_train, X_val, y_train, y_val = train_test_split(images, scores_onehot, test_size=0.2, random_state=42)
    print("Shapes - X_train: {}, y_train: {}, X_val: {}, y_val: {}".format(X_train.shape, y_train.shape, X_val.shape, y_val.shape))
    # retrain models
    _, history, y_pred = retrain_nima_model('models/weights_mobilenet_aesthetic_0.07.hdf5','aesthetic', X_train, y_train, X_val, y_val) # 
    plot_history(history)
    plot_distributions(y_val, y_pred)
    #retrain_nima_model('technical', X_train, y_train, X_val, y_val)