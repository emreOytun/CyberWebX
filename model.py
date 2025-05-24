# model.py
import pickle
import pandas as pd
import numpy as np

class MalwareModel:
    def __init__(self, model_path: str, scaler_path: str):
        self.model = pickle.load(open(model_path, 'rb'))
        self.scaler = pickle.load(open(scaler_path, 'rb'))

    def predict_from_features(self, features, columns):
        df = pd.DataFrame([features], columns=columns)
        df["legitimate"] = 0  # dummy label
        X = df.drop(["Name", "md5", "legitimate"], axis=1)
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)[0]
        label = "malicious" if prediction == 0 else "legitimate"
        return label
