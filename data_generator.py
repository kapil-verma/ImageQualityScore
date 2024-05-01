import os
import glob
import numpy as np
import utils
import tensorflow as tf
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array

class DataGenerator(Sequence):
    '''inherits from Keras Sequence base object, allows to use multiprocessing in .fit_generator'''
    def __init__(self, samples, img_dir, batch_size, n_classes, basenet_preprocess, img_load_dims=(256, 256), img_crop_dims=(224, 224), shuffle=True):
        self.samples = samples
        self.img_dir = img_dir
        self.batch_size = batch_size
        self.n_classes = n_classes
        self.basenet_preprocess = basenet_preprocess
        self.img_load_dims = img_load_dims
        self.img_crop_dims = img_crop_dims
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.samples) / self.batch_size))

    def __getitem__(self, index):
        batch_indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        batch_samples = [self.samples[i] for i in batch_indexes]
        X, y = self.__data_generation(batch_samples)
        return X, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.samples))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __data_generation(self, batch_samples):
        X = np.empty((len(batch_samples), *self.img_crop_dims, 3))
        y = np.empty((len(batch_samples), self.n_classes))
        for i, sample in enumerate(batch_samples):
            print(sample['image_id'])
            img_files = glob.glob(os.path.join(self.img_dir, f"*{os.path.basename(sample['image_url']).split('.')[0]}*.jpeg"))
            if img_files:
                print(img_files[0])
                img = image.load_img(img_files[0], target_size=self.img_load_dims)
                img_array = img_to_array(img)
                if img is not None:
                    img_cropped = utils.random_crop(img_array, self.img_crop_dims)
                    img_processed = utils.random_horizontal_flip(img_cropped)
                    X[i, ] = self.basenet_preprocess(img_processed)

                if sample.get('label') is not None:
                    y[i, ] = utils.normalize_labels(sample['label'])
        return X, y