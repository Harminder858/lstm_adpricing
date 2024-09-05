import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import MinMaxScaler

class AdPricingLSTM:
    def __init__(self, input_shape, output_shape):
        self.model = self._build_model(input_shape, output_shape)
        self.scaler = MinMaxScaler()

    def _build_model(self, input_shape, output_shape):
        model = Sequential([
            Bidirectional(LSTM(128, return_sequences=True), input_shape=input_shape),
            BatchNormalization(),
            Dropout(0.3),
            Bidirectional(LSTM(64, return_sequences=True)),
            BatchNormalization(),
            Dropout(0.3),
            Bidirectional(LSTM(32)),
            BatchNormalization(),
            Dropout(0.3),
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            Dense(output_shape)
        ])
        
        optimizer = Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        return model

    def preprocess_data(self, X, y=None):
        X_scaled = self.scaler.fit_transform(X)
        if y is not None:
            y_scaled = self.scaler.transform(y.reshape(-1, 1))
            return X_scaled, y_scaled.ravel()
        return X_scaled

    def inverse_transform(self, data):
        return self.scaler.inverse_transform(data.reshape(-1, 1)).ravel()

    def train(self, X_train, y_train, epochs=200, batch_size=32, validation_split=0.2):
        X_scaled, y_scaled = self.preprocess_data(X_train, y_train)
        
        early_stopping = EarlyStopping(patience=20, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(factor=0.2, patience=10, min_lr=0.0001)
        
        history = self.model.fit(
            X_scaled, y_scaled,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stopping, reduce_lr]
        )
        return history

    def predict(self, X):
        X_scaled = self.preprocess_data(X)
        predictions = self.model.predict(X_scaled)
        return self.inverse_transform(predictions)

    def evaluate(self, X_test, y_test):
        X_scaled, y_scaled = self.preprocess_data(X_test, y_test)
        return self.model.evaluate(X_scaled, y_scaled)

    def save(self, filepath):
        self.model.save(filepath)

    @classmethod
    def load(cls, filepath):
        model = tf.keras.models.load_model(filepath)
        instance = cls(model.input_shape[1:], model.output_shape[1])
        instance.model = model
        return instance

    def feature_importance(self, X):
        X_scaled = self.preprocess_data(X)
        baseline_prediction = self.model.predict(X_scaled)
        feature_importance = []

        for i in range(X_scaled.shape[1]):
            perturbed_X = X_scaled.copy()
            perturbed_X[:, i] = np.random.permutation(perturbed_X[:, i])
            perturbed_prediction = self.model.predict(perturbed_X)
            importance = np.mean(np.abs(baseline_prediction - perturbed_prediction))
            feature_importance.append(importance)

        return feature_importance