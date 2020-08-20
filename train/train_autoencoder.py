import glob
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow.keras.backend as K
from tf.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Flatten, Conv2DTranspose, Reshape
from tensorflow.keras.models import Model

from pylab import rcParams
rcParams['figure.figsize'] = 20, 20

INPUT_SHAPE = [2036, 1012, 3]
BATCH_SIZE = 1
MODEL_SAVE_PATH = 'model.h5'


def make_autoencoder():
    # Slightly larger than the autoencoder written by Francois Chollet
    # here https://blog.keras.io/building-autoencoders-in-keras.html

    input_img = Input(shape=INPUT_SHAPE)

    x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(x){{}}
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)

    x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(16, (3, 3), activation='relu')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(32, (3, 3), activation='relu')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    autoencoder = Model(input_img, decoded)
    autoencoder.compile(optimizer='adam', loss='mse')

    return autoencoder


def read_img(img_path):
    img_str = tf.io.read_file(img_path)
    img = tf.image.decode_png(img_str, channels=3)
    img = tf.image.resize(img, INPUT_SHAPE[:2])
    img = tf.cast(img, tf.float32) * 1 / 255.0
    return img, img


if __name__ = '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir', type=str, help='path to train images')
    args = parser.parse_args()

    img_paths = glob.glob(f'{args.train_dir}/*.png')

    train_ds = tf.data.Dataset.from_tensor_slices(img_paths)
    train_ds = train_ds.map(read_img, num_parallel_calls=1)
                        .shuffle(420)
                        .batch(BATCH_SIZE)
                        .repeat()

    cp = ModelCheckpoint(filepath=MODEL_SAVE_PATH,
                        monitor='mse',
                        save_best_only=True,
                        save_weights_only=False,
                        verbose=1)
    
    autoencoder = make_autoencoder()

    autoencoder.fit(train_ds,
                    epochs=50,
                    batch_size=BATCH_SIZE,
                    steps_per_epoch=int(
                        np.ceil(len(img_paths) / float(BATCH_SIZE))),
                    shuffle=True,
                    callbacks=[cp])
