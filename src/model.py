import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class ECGClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()

        # Define class labels
        self.classes = [
            'COVID-19',
            'Myocardial Infarction',
            'Abnormal Heartbeat',
            'History of MI',
            'Normal'
        ]

        # Initialize with sample data matching our feature extractor (9 features)
        sample_features = np.random.rand(500, 9)
        sample_labels = np.random.choice(range(5), size=500)  # 5 classes

        # Fit the model with the correct number of features
        self.model.fit(sample_features, sample_labels)

    def predict(self, features):
        """
        Predict ECG class and return the most probable class with its confidence
        Args:
            features (np.array): Extracted features from ECG
        Returns:
            tuple: (predicted class name, confidence score)
        """
        features = features.reshape(1, -1)
        features_scaled = self.scaler.fit_transform(features)

        # Get probabilities for all classes
        probabilities = self.model.predict_proba(features_scaled)[0]

        # Get the most probable class
        class_index = np.argmax(probabilities)
        confidence = probabilities[class_index]

        return self.classes[class_index], float(confidence)

    def get_class_name(self, class_index):
        """Get class name from index"""
        return self.classes[class_index]