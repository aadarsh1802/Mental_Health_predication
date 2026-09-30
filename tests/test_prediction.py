import unittest

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.predict import predict_scores
from src.train import train_model


class PredictionTests(unittest.TestCase):
    def setUp(self):
        self.features = pd.DataFrame(
            {
                "Age": [18, 20, 22, 24],
                "Gender": ["Female", "Male", "Female", "Male"],
            }
        )
        target = pd.Series([5.0, 6.0, 7.0, 8.0], name="Mental_Health_Score")
        self.model = train_model(
            self.features,
            target,
            RandomForestRegressor(n_estimators=5, random_state=42),
        )

    def test_predicts_a_single_record(self):
        prediction = predict_scores(
            self.model, {"Age": 21, "Gender": "Other"}
        )

        self.assertEqual(len(prediction), 1)
        self.assertIsInstance(prediction[0], float)

    def test_rejects_feature_schema_mismatch(self):
        with self.assertRaisesRegex(ValueError, "schema mismatch"):
            predict_scores(self.model, {"Age": 21, "Unknown": "value"})


if __name__ == "__main__":
    unittest.main()
