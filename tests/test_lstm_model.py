import unittest
import numpy as np
from models.lstm_model import AdPricingLSTM

class TestLSTMModel(unittest.TestCase):
    def setUp(self):
        self.input_shape = (10, 5)  # 10 time steps, 5 features
        self.output_shape = 1
        self.model = AdPricingLSTM(self.input_shape, self.output_shape)

    def test_model_creation(self):
        self.assertIsInstance(self.model, AdPricingLSTM)
        self.assertEqual(self.model.model.input_shape[1:], self.input_shape)
        self.assertEqual(self.model.model.output_shape[1], self.output_shape)

    def test_model_prediction(self):
        X = np.random.rand(1, *self.input_shape)
        prediction = self.model.predict(X)
        self.assertEqual(prediction.shape, (1, self.output_shape))

    def test_model_training(self):
        X = np.random.rand(100, *self.input_shape)
        y = np.random.rand(100, self.output_shape)
        history = self.model.train(X, y, epochs=1, batch_size=32, validation_split=0.2)
        self.assertIn('loss', history.history)
        self.assertIn('val_loss', history.history)

if __name__ == '__main__':
    unittest.main()