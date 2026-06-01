"""
Risk Analysis Utilities
Categorizes risk levels and generates explanations
"""

def categorize_risk(probability):
    """
    Categorize risk based on probability
    
    Args:
        probability: Prediction probability (0-100)
    
    Returns:
        Risk level: 'Low', 'Moderate', or 'High'
    """
    if probability < 30:
        return 'Low'
    elif probability < 60:
        return 'Moderate'
    else:
        return 'High'

def generate_explanation(disease, probability, health_data):
    """
    Generate human-readable explanation of prediction
    
    Args:
        disease: Disease type
        probability: Prediction probability
        health_data: Dictionary of health parameters
    
    Returns:
        Explanation string
    """
    risk_level = categorize_risk(probability)
    
    if disease == "diabetes":
        return generate_diabetes_explanation(probability, risk_level, health_data)
    elif disease == "heart_disease":
        return generate_heart_disease_explanation(probability, risk_level, health_data)
    elif disease == "pneumonia":
        return generate_pneumonia_explanation(probability, risk_level, health_data)
    elif disease == "brain_tumor":
        return generate_brain_tumor_explanation(probability, risk_level, health_data)
    else:
        return generate_generic_explanation(probability, risk_level)

def generate_diabetes_explanation(probability, risk_level, health_data):
    """Generate explanation for diabetes risk"""
    
    explanations = []
    
    if risk_level == 'High':
        explanations.append(f"Your diabetes risk assessment indicates a {probability:.1f}% probability, which is considered HIGH risk.")
        
        # Identify contributing factors
        if 'Glucose' in health_data and health_data['Glucose'] > 125:
            explanations.append("Your glucose level is elevated, which is a strong indicator.")
        if 'BMI' in health_data and health_data['BMI'] > 30:
            explanations.append("Your BMI suggests obesity, a significant diabetes risk factor.")
        if 'Age' in health_data and health_data['Age'] > 45:
            explanations.append("Age is a contributing factor to diabetes risk.")
            
        explanations.append("Immediate lifestyle modifications and medical consultation are strongly recommended.")
        
    elif risk_level == 'Moderate':
        explanations.append(f"Your diabetes risk assessment shows a {probability:.1f}% probability, indicating MODERATE risk.")
        explanations.append("Several health parameters suggest you may be at risk for developing diabetes.")
        explanations.append("Proactive lifestyle changes can significantly reduce your risk.")
        
    else:  # Low risk
        explanations.append(f"Your diabetes risk assessment indicates a {probability:.1f}% probability, which is LOW risk.")
        explanations.append("Your current health parameters suggest a lower likelihood of diabetes.")
        explanations.append("Continue maintaining healthy lifestyle habits to keep your risk low.")
    
    return " ".join(explanations)

def generate_heart_disease_explanation(probability, risk_level, health_data):
    """Generate explanation for heart disease risk"""
    
    explanations = []
    
    if risk_level == 'High':
        explanations.append(f"Your cardiovascular risk assessment indicates a {probability:.1f}% probability, which is HIGH risk.")
        
        # Identify contributing factors
        if 'chol' in health_data and health_data['chol'] > 240:
            explanations.append("Your cholesterol level is elevated, increasing heart disease risk.")
        if 'trestbps' in health_data and health_data['trestbps'] > 140:
            explanations.append("Your blood pressure is high, a major risk factor.")
        if 'age' in health_data and health_data['age'] > 55:
            explanations.append("Age increases cardiovascular risk.")
            
        explanations.append("Immediate medical evaluation and lifestyle modifications are crucial.")
        
    elif risk_level == 'Moderate':
        explanations.append(f"Your cardiovascular risk assessment shows a {probability:.1f}% probability, indicating MODERATE risk.")
        explanations.append("Some cardiac parameters suggest elevated risk.")
        explanations.append("Preventive measures and lifestyle changes are recommended.")
        
    else:  # Low risk
        explanations.append(f"Your cardiovascular risk assessment indicates a {probability:.1f}% probability, which is LOW risk.")
        explanations.append("Your cardiac health parameters appear favorable.")
        explanations.append("Maintain heart-healthy habits to preserve cardiovascular health.")
    
    return " ".join(explanations)

def generate_pneumonia_explanation(probability, risk_level, health_data):
    """Generate explanation for pneumonia detection"""
    
    explanations = []
    
    if risk_level == 'High':
        explanations.append(f"The chest X-ray analysis indicates a {probability:.1f}% probability of pneumonia/COVID, which is HIGH.")
        explanations.append("Imaging patterns suggest possible lung infection or inflammation.")
        explanations.append("Immediate medical evaluation is strongly recommended.")
        
    elif risk_level == 'Moderate':
        explanations.append(f"The chest X-ray analysis shows a {probability:.1f}% probability of pneumonia/COVID, indicating MODERATE concern.")
        explanations.append("Some imaging features warrant medical attention.")
        explanations.append("Consult a healthcare provider for further evaluation.")
        
    else:  # Low risk
        explanations.append(f"The chest X-ray analysis indicates a {probability:.1f}% probability of pneumonia/COVID, which is LOW.")
        explanations.append("No significant findings suggesting active infection.")
        explanations.append("Continue monitoring your respiratory health.")
    
    return " ".join(explanations)

def generate_brain_tumor_explanation(probability, risk_level, health_data):
    """Generate explanation for brain tumor detection"""
    
    explanations = []
    
    if risk_level == 'High':
        explanations.append(f"The MRI analysis indicates a {probability:.1f}% probability of abnormality, which is HIGH concern.")
        explanations.append("Imaging patterns suggest possible abnormal tissue or mass.")
        explanations.append("Immediate neurological consultation is essential.")
        
    elif risk_level == 'Moderate':
        explanations.append(f"The MRI analysis shows a {probability:.1f}% probability of abnormality, indicating MODERATE concern.")
        explanations.append("Some imaging features require professional evaluation.")
        explanations.append("Consult a neurologist for comprehensive assessment.")
        
    else:  # Low risk
        explanations.append(f"The MRI analysis indicates a {probability:.1f}% probability of abnormality, which is LOW.")
        explanations.append("No significant findings suggesting tumor or mass.")
        explanations.append("Continue routine health monitoring.")
    
    return " ".join(explanations)

def generate_generic_explanation(probability, risk_level):
    """Generate generic explanation"""
    
    if risk_level == 'High':
        return f"The analysis indicates a {probability:.1f}% probability, suggesting HIGH risk. Medical consultation is recommended."
    elif risk_level == 'Moderate':
        return f"The analysis shows a {probability:.1f}% probability, indicating MODERATE risk. Consider medical evaluation."
    else:
        return f"The analysis indicates a {probability:.1f}% probability, which is LOW risk. Continue healthy practices."

def get_risk_color(risk_level):
    """
    Get color code for risk level
    
    Args:
        risk_level: 'Low', 'Moderate', or 'High'
    
    Returns:
        Hex color code
    """
    colors = {
        'Low': '#28a745',      # Green
        'Moderate': '#ffc107',  # Yellow/Orange
        'High': '#dc3545'       # Red
    }
    return colors.get(risk_level, '#6c757d')  # Default gray

def get_risk_emoji(risk_level):
    """Get emoji for risk level"""
    emojis = {
        'Low': '✅',
        'Moderate': '⚠️',
        'High': '🚨'
    }
    return emojis.get(risk_level, '❓')
