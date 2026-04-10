import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    
    # 1. Feature Engineering (if any, for now just basic encoding)
    
    # Drop IDs
    X = df.drop(['student_id', 'placement_timeline', 'actual_salary', 'placement_risk_score'], axis=1)
    
    # Labels
    y_timeline = df['placement_timeline']
    y_salary = df['actual_salary']
    
    # 2. Encoding Categorical Variables
    le_timeline = LabelEncoder()
    y_timeline_encoded = le_timeline.fit_transform(y_timeline)
    
    # Save encoders for later use
    os.makedirs('models', exist_ok=True)
    joblib.dump(le_timeline, 'models/le_timeline.pkl')
    
    # Identify categorical columns for X
    cat_cols = X.select_dtypes(include=['object']).columns
    X_encoded = pd.get_dummies(X, columns=cat_cols)
    
    # 3. Splitting
    X_train, X_test, y_t_train, y_t_test, y_s_train, y_s_test = train_test_split(
        X_encoded, y_timeline_encoded, y_salary, test_size=0.2, random_state=42
    )
    
    # 4. Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    joblib.dump(scaler, 'models/scaler.pkl')
    # Save feature names for inference
    joblib.dump(X_encoded.columns.tolist(), 'models/feature_names.pkl')
    
    # Save processed data
    output_dir = 'data/processed'
    os.makedirs(output_dir, exist_ok=True)
    
    np.save(f'{output_dir}/X_train.npy', X_train_scaled)
    np.save(f'{output_dir}/X_test.npy', X_test_scaled)
    np.save(f'{output_dir}/y_t_train.npy', y_t_train)
    np.save(f'{output_dir}/y_t_test.npy', y_t_test)
    np.save(f'{output_dir}/y_s_train.npy', y_s_train.values)
    np.save(f'{output_dir}/y_s_test.npy', y_s_test.values)
    
    print("Preprocessing complete. Files saved in 'data/processed/' and encoders in 'models/'")

if __name__ == "__main__":
    preprocess_data('data/student_data.csv')
