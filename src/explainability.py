import shap
import joblib
import pandas as pd
import numpy as np
import os

def get_risk_explanation(student_features_scaled, student_features_df):
    """
    Returns a natural language summary of why a student was flagged as high risk.
    """
    # Load model and feature names
    clf = joblib.load('models/clf_timeline.pkl')
    feature_names = joblib.load('models/feature_names.pkl')
    le_timeline = joblib.load('models/le_timeline.pkl')
    
    # Calculate SHAP values
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(student_features_scaled)
    
    # Get prediction
    pred_idx = clf.predict(student_features_scaled)[0]
    pred_label = le_timeline.classes_[pred_idx]
    
    # Extract feature importance for this specific prediction
    # shap_values is a list of arrays for multi-class
    if isinstance(shap_values, list):
        sv = shap_values[pred_idx][0]
    else:
        # For recent xgboost versions it might return a single array
        sv = shap_values[0] if len(shap_values.shape) == 2 else shap_values[0, :, pred_idx]

    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'shap_value': sv
    }).sort_values(by='shap_value', ascending=False)
    
    # Generate Summary
    top_pos = feature_importance.head(3)
    top_neg = feature_importance.tail(3)
    
    summary = f"Prediction: {pred_label}. "
    
    if pred_label == 'Delayed / High Risk':
        influencers = top_pos[top_pos['shap_value'] > 0]
        if not influencers.empty:
            reasons = ", ".join(influencers['feature'].tolist())
            summary += f"High risk factors identified: {reasons}."
    else:
        influencers = top_neg[top_neg['shap_value'] < 0]
        if not influencers.empty:
            reasons = ", ".join(influencers['feature'].tolist())
            summary += f"Strengths identified: {reasons}."
            
    return summary, feature_importance.to_dict(orient='records')

if __name__ == "__main__":
    # Test on one sample
    X_test = np.load('data/processed/X_test.npy')
    feature_names = joblib.load('models/feature_names.pkl')
    sample = X_test[0:1]
    
    summary, importance = get_risk_explanation(sample, None)
    print(summary)
