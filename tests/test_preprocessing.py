import unittest

import pandas as pd

from src.feature_engineering import split_features_target
from src.preprocessing import build_preprocessor, get_feature_columns


class PreprocessingTests(unittest.TestCase):
    def setUp(self):
        self.features = pd.DataFrame(
            {
                "Age": [20, None, 24],
                "Gender": ["Female", "Male", None],
            }
        )

    def test_identifies_numeric_and_categorical_columns(self):
        numeric, categorical = get_feature_columns(self.features)

        self.assertEqual(numeric, ["Age"])
        self.assertEqual(categorical, ["Gender"])

    def test_preprocessor_handles_missing_and_unseen_values(self):
        preprocessor = build_preprocessor(self.features)
        transformed = preprocessor.fit_transform(self.features)
        unseen = preprocessor.transform(
            pd.DataFrame({"Age": [22], "Gender": ["Unseen"]})
        )

        self.assertEqual(transformed.shape, (3, 3))
        self.assertEqual(unseen.shape, (1, 3))

    def test_target_split_drops_exported_index(self):
        data = self.features.assign(
            **{"Unnamed: 0": [0, 1, 2], "Mental_Health_Score": [6.0, 7.0, 8.0]}
        )

        features, target = split_features_target(data)

        self.assertNotIn("Unnamed: 0", features.columns)
        self.assertEqual(target.name, "Mental_Health_Score")
        self.assertEqual(len(features), len(target))


if __name__ == "__main__":
    unittest.main()
