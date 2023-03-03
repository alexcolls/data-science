
from colorama import Fore, Style

import time
print(Fore.BLUE + "\nLoading tensorflow..." + Style.RESET_ALL)
start = time.perf_counter()

from tensorflow.keras import Model, Sequential, layers, regularizers, optimizers
from tensorflow.keras.callbacks import EarlyStopping

end = time.perf_counter()
print(f"\n✅ tensorflow loaded ({round(end - start, 2)} secs)")

from typing import Tuple

import numpy as np


def initialize_model(X: np.ndarray) -> Model:
    """
    Initialize the Neural Network with random weights
    """
    # $CODE_BEGIN
    print(Fore.BLUE + "\nInitialize model..." + Style.RESET_ALL)

    reg = regularizers.l1_l2(l2=0.005)

    model = Sequential()
    model.add(layers.BatchNormalization(input_shape=X.shape[1:]))
    model.add(layers.Dense(100, activation="relu", kernel_regularizer=reg))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(rate=0.1))
    model.add(layers.Dense(50, activation="relu", kernel_regularizer=reg))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(rate=0.1))
    model.add(layers.Dense(10, activation="relu"))
    model.add(layers.BatchNormalization(momentum=0.99))  # use momentum=0 for to only use statistic of the last seen minibatch in inference mode ("short memory"). Use 1 to average statistics of all seen batch during training histories.
    model.add(layers.Dropout(rate=0.1))
    model.add(layers.Dense(1, activation="linear"))
    # $CODE_END

    print("\n✅ model initialized")

    return model


def compile_model(model: Model, learning_rate: float) -> Model:
    """
    Compile the Neural Network
    """
    # $CODE_BEGIN
    optimizer = optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["mae"])
    # $CODE_END

    print("\n✅ model compiled")
    return model


def train_model(model: Model,
                X: np.ndarray,
                y: np.ndarray,
                batch_size=64,
                patience=2,
                validation_split=0.3,
                validation_data=None) -> Tuple[Model, dict]:
    """
    Fit model and return a the tuple (fitted_model, history)
    """

    # $CODE_BEGIN
    print(Fore.BLUE + "\nTrain model..." + Style.RESET_ALL)

    es = EarlyStopping(monitor="val_loss",
                       patience=patience,
                       restore_best_weights=True,
                       verbose=0)

    history = model.fit(X,
                        y,
                        validation_split=validation_split,
                        validation_data=validation_data,
                        epochs=100,
                        batch_size=batch_size,
                        callbacks=[es],
                        verbose=0)
    # $CODE_END

    print(f"\n✅ model trained ({len(X)} rows)")

    return model, history

