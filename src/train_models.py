import numpy as np
import xgboost as xgb
import lightgbm as lgb
from sklearn.metrics import classification_report, mean_absolute_error, r2_score
import joblib
import os

def train_models():
    # Load data
    data_dir = 'data/processed'
    X_train = np.load(f'{data_dir}/X_train.npy')
    X_test = np.load(f'{data_dir}/X_test.npy')
    y_t_train = np.load(f'{data_dir}/y_t_train.npy')
    y_t_test = np.load(f'{data_dir}/y_t_test.npy')
    y_s_train = np.load(f'{data_dir}/y_s_train.npy')
    y_s_test = np.load(f'{data_dir}/y_s_test.npy')
    
    # 1. Train Classification Model (Timeline)
    print("Training XGBoost Classifier...")
    clf = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    clf.fit(X_train, y_t_train)
    
    y_t_pred = clf.predict(X_test)
    le_timeline = joblib.load('models/le_timeline.pkl')
    print("\nClassification Report (Placement Timeline):")
    print(classification_report(y_t_test, y_t_pred, target_names=le_timeline.classes_))
    
    # 2. Train Regression Model (Salary)
    print("Training LightGBM Regressor...")
    reg = lgb.LGBMRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    reg.fit(X_train, y_s_train)
    
    y_s_pred = reg.predict(X_test)
    print("\nRegression Metrics (Salary):")
    print(f"Mean Absolute Error: {mean_absolute_error(y_s_test, y_s_pred):.2f}")
    print(f"R2 Score: {r2_score(y_s_test, y_s_pred):.4f}")
    
    # 3. Save Models
    os.makedirs('models', exist_ok=True)
    joblib.dump(clf, 'models/clf_timeline.pkl')
    joblib.dump(reg, 'models/reg_salary.pkl')
    print("\nModels saved in 'models/'")

if __name__ == "__main__":
    train_models()
