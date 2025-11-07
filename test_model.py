"""
Stroke Prediction Model - Testing Script
This script loads the saved model and demonstrates how to make predictions
"""

import joblib
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt

def load_model():
    """Load the saved model package"""
    print("=" * 80)
    print("LOADING MODEL PACKAGE")
    print("=" * 80)
    
    model_package = joblib.load('stroke_prediction_model.pkl')
    
    print(f"\n✅ Model loaded successfully!")
    print(f"   Model type: {model_package['metadata']['model_type']}")
    print(f"   Trained on: {model_package['metadata']['train_date']}")
    print(f"   Optimal threshold: {model_package['optimal_threshold']:.4f}")
    print(f"\n📊 Performance Metrics:")
    for metric, value in model_package['performance'].items():
        print(f"   {metric}: {value:.4f}")
    
    return model_package


def predict_stroke(model_package, patient_data):
    """
    Make stroke prediction for a patient
    
    Parameters:
    -----------
    model_package : dict
        Loaded model package
    patient_data : pd.DataFrame
        Patient data with required features
        
    Returns:
    --------
    prediction : int
        0 = Low risk, 1 = High risk
    probability : float
        Probability of stroke (0-1)
    """
    model = model_package['model']
    optimal_threshold = model_package['optimal_threshold']
    
    # Remove excluded features if present (e.g., 'id')
    excluded_features = model_package['feature_columns'].get('excluded_features', [])
    patient_data = patient_data.drop(columns=excluded_features, errors='ignore')
    
    # Handle optional features - fill with median/mode if missing
    optional_features = model_package['feature_columns'].get('optional_features', [])
    for feature in optional_features:
        if feature not in patient_data.columns:
            # Use a default value for missing optional features
            if feature == 'avg_glucose_level':
                patient_data[feature] = 106.0  # Median value from training
    
    # Get probability predictions
    proba = model.predict_proba(patient_data)[:, 1]
    
    # Apply optimal threshold
    prediction = (proba >= optimal_threshold).astype(int)
    
    return prediction[0], proba[0]


def get_shap_explanation(model_package, patient_data):
    """
    Generate SHAP explanation for the prediction
    
    Parameters:
    -----------
    model_package : dict
        Loaded model package
    patient_data : pd.DataFrame
        Patient data
        
    Returns:
    --------
    shap_values : shap.Explanation
        SHAP values for the prediction
    """
    model = model_package['model']
    explainer = model_package['explainer']
    
    # Remove excluded features if present (e.g., 'id')
    excluded_features = model_package['feature_columns'].get('excluded_features', [])
    patient_data = patient_data.drop(columns=excluded_features, errors='ignore')
    
    # Handle optional features
    optional_features = model_package['feature_columns'].get('optional_features', [])
    for feature in optional_features:
        if feature not in patient_data.columns:
            if feature == 'avg_glucose_level':
                patient_data[feature] = 106.0
    
    # Transform patient data
    X_transformed = model.named_steps['preprocessor'].transform(patient_data)
    
    # Calculate SHAP values
    shap_values = explainer(X_transformed)
    
    return shap_values


def create_test_patient(case='high_risk'):
    """
    Create test patient data
    
    Parameters:
    -----------
    case : str
        'high_risk' or 'low_risk'
        
    Returns:
    --------
    pd.DataFrame
        Patient data
    """
    if case == 'high_risk':
        # High risk patient: old age, hypertension, high glucose, smoker
        patient = pd.DataFrame({
            'age': [67],
            'hypertension': [1],
            'heart_disease': [0],
            'avg_glucose_level': [228.5],
            'bmi': [36.6],
            'gender': ['Male'],
            'ever_married': ['Yes'],
            'work_type': ['Private'],
            'Residence_type': ['Urban'],
            'smoking_status': ['smokes']
        })
    else:
        # Low risk patient: young, healthy
        patient = pd.DataFrame({
            'age': [25],
            'hypertension': [0],
            'heart_disease': [0],
            'avg_glucose_level': [85.0],
            'bmi': [22.5],
            'gender': ['Female'],
            'ever_married': ['No'],
            'work_type': ['Private'],
            'Residence_type': ['Urban'],
            'smoking_status': ['never smoked']
        })
    
    return patient


def main():
    """Main testing function"""
    
    # Load model
    model_package = load_model()
    
    print("\n" + "=" * 80)
    print("TEST CASE 1: HIGH RISK PATIENT")
    print("=" * 80)
    
    # Create high risk patient
    high_risk_patient = create_test_patient('high_risk')
    print("\n📋 Patient Information:")
    for col in high_risk_patient.columns:
        print(f"   {col:20s}: {high_risk_patient[col].values[0]}")
    
    # Make prediction
    prediction, probability = predict_stroke(model_package, high_risk_patient)
    
    print(f"\n🎯 PREDICTION RESULTS:")
    print(f"   Stroke Probability: {probability:.2%}")
    print(f"   Risk Level: {'⚠️  HIGH RISK' if prediction == 1 else '✅ LOW RISK'}")
    print(f"   Classification: {prediction} (using threshold {model_package['optimal_threshold']:.4f})")
    
    # Get SHAP explanation
    print(f"\n🔍 Feature Importance (SHAP):")
    shap_values = get_shap_explanation(model_package, high_risk_patient)
    feature_names = model_package['feature_columns']['all_features']
    
    # Get top 5 contributing features
    shap_array = shap_values.values[0]
    top_indices = np.argsort(np.abs(shap_array))[-5:][::-1]
    
    for idx in top_indices:
        feature = feature_names[idx]
        value = shap_array[idx]
        direction = "↑" if value > 0 else "↓"
        print(f"   {direction} {feature:30s}: {value:+.4f}")
    
    print("\n" + "=" * 80)
    print("TEST CASE 2: LOW RISK PATIENT")
    print("=" * 80)
    
    # Create low risk patient
    low_risk_patient = create_test_patient('low_risk')
    print("\n📋 Patient Information:")
    for col in low_risk_patient.columns:
        print(f"   {col:20s}: {low_risk_patient[col].values[0]}")
    
    # Make prediction
    prediction, probability = predict_stroke(model_package, low_risk_patient)
    
    print(f"\n🎯 PREDICTION RESULTS:")
    print(f"   Stroke Probability: {probability:.2%}")
    print(f"   Risk Level: {'⚠️  HIGH RISK' if prediction == 1 else '✅ LOW RISK'}")
    print(f"   Classification: {prediction} (using threshold {model_package['optimal_threshold']:.4f})")
    
    # Get SHAP explanation
    print(f"\n🔍 Feature Importance (SHAP):")
    shap_values = get_shap_explanation(model_package, low_risk_patient)
    
    # Get top 5 contributing features
    shap_array = shap_values.values[0]
    top_indices = np.argsort(np.abs(shap_array))[-5:][::-1]
    
    for idx in top_indices:
        feature = feature_names[idx]
        value = shap_array[idx]
        direction = "↑" if value > 0 else "↓"
        print(f"   {direction} {feature:30s}: {value:+.4f}")
    
    print("\n" + "=" * 80)
    print("TEST CASE 3: CUSTOM PATIENT")
    print("=" * 80)
    
    # Create custom patient
    custom_patient = pd.DataFrame({
        'age': [52],
        'hypertension': [1],
        'heart_disease': [0],
        'avg_glucose_level': [195.0],
        'bmi': [28.5],
        'gender': ['Male'],
        'ever_married': ['Yes'],
        'work_type': ['Self-employed'],
        'Residence_type': ['Rural'],
        'smoking_status': ['formerly smoked']
    })
    
    print("\n📋 Patient Information:")
    for col in custom_patient.columns:
        print(f"   {col:20s}: {custom_patient[col].values[0]}")
    
    # Make prediction
    prediction, probability = predict_stroke(model_package, custom_patient)
    
    print(f"\n🎯 PREDICTION RESULTS:")
    print(f"   Stroke Probability: {probability:.2%}")
    print(f"   Risk Level: {'⚠️  HIGH RISK' if prediction == 1 else '✅ LOW RISK'}")
    print(f"   Classification: {prediction} (using threshold {model_package['optimal_threshold']:.4f})")
    
    # Get SHAP explanation
    print(f"\n🔍 Feature Importance (SHAP):")
    shap_values = get_shap_explanation(model_package, custom_patient)
    
    # Get top 5 contributing features
    shap_array = shap_values.values[0]
    top_indices = np.argsort(np.abs(shap_array))[-5:][::-1]
    
    for idx in top_indices:
        feature = feature_names[idx]
        value = shap_array[idx]
        direction = "↑" if value > 0 else "↓"
        print(f"   {direction} {feature:30s}: {value:+.4f}")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 80)
    
    # Summary
    print("\n💡 Model Input/Output Summary:")
    print("\n📥 INPUT FORMAT:")
    print("   Required columns: age, hypertension, heart_disease, bmi,")
    print("                     gender, ever_married, work_type, Residence_type, smoking_status")
    print("   Optional columns: avg_glucose_level (default: 106.0 if missing)")
    print("   Excluded columns: id (automatically removed if present)")
    print("\n📤 OUTPUT FORMAT:")
    print("   - probability: float (0.0 to 1.0) - probability of stroke")
    print("   - prediction: int (0 or 1) - 0=Low Risk, 1=High Risk")
    print("   - SHAP values: feature contributions to the prediction")


if __name__ == "__main__":
    main()
