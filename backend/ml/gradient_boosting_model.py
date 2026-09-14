from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

class LoanApprovalModel:
    def __init__(self):
        self.model = XGBClassifier(
            n_estimators=100,
            max_depth=7,
            learning_rate=0.1,
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        self.scaler = StandardScaler()
    
    def train(self, X_train, y_train):
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_train_scaled, y_train)
    
    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)[0] 
        probability = self.model.predict_proba(X_scaled)[0] 
        
        return {
            "decision": "APPROVED" if prediction == 1 else "DENIED",
            "confidence": float(probability[1]),
            "feature_importance": self._get_important_features()
        }
    
    def _get_important_features(self):
      
        pass
    
    def save(self, path):
        pickle.dump((self.model, self.scaler), open(path, 'wb'))
    
    def load(self, path):
        self.model, self.scaler = pickle.load(open(path, 'rb'))