import unittest
import pandas as pd
import numpy as np
from utils.data_preprocessing import preprocess_data, create_sequences, split_data

class TestDataPreprocessing(unittest.TestCase):
    def setUp(self):
        self.sample_data = pd.DataFrame({
            'date': pd.date_range(start='2024-01-01', periods=10),
            'ad_id': ['AD001'] * 10,
            'platform': ['Facebook', 'Google'] * 5,
            'format': ['Video', 'Display'] * 5,
            'target_audience': ['18-25', '25-34'] * 5,
            'bid_amount': np.random.rand(10),
            'impressions': np.random.randint(1000, 10000, 10),
            'clicks': np.random.randint(10, 1000, 10),
            'conversions': np.random.randint(1, 100, 10),
            'spend': np.random.rand(10) * 1000,
            'revenue': np.random.rand(10) * 1500
        })

    def test_preprocess_data(self):
        preprocessed_data, scaler = preprocess_data(self.sample_data)
        self.assertGreater(preprocessed_data.shape[1], self.sample_data.shape[1])
        self.assertTrue(all(preprocessed_data[['bid_amount', 'impressions', 'clicks', 'conversions', 'spend', 'revenue']].max() <= 1))
        self.assertTrue(all(preprocessed_data[['bid_amount', 'impressions', 'clicks', 'conversions', 'spend', 'revenue']].min() >= 0))

    def test_create_sequences(self):
        data = np.array([i for i in range(10)])
        X, y = create_sequences(data, sequence_length=3)
        self.assertEqual(X.shape, (7, 3))
        self.assertEqual(y.shape, (7,))
        np.testing.assert_array_equal(X[0], [0, 1, 2])
        np.testing.assert_array_equal(y[0], 3)

    def test_split_data(self):
        X = np.array([i for i in range(100)])
        y = np.array([i * 2 for i in range(100)])
        X_train, X_test, y_train, y_test = split_data(X, y, train_ratio=0.8)
        self.assertEqual(len(X_train), 80)
        self.assertEqual(len(X_test), 20)
        self.assertEqual(len(y_train), 80)
        self.assertEqual(len(y_test), 20)

if __name__ == '__main__':
    unittest.main()