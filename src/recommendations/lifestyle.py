"""
Lifestyle Recommendation Engine
Generates personalized lifestyle recommendations based on disease risk
"""

def get_lifestyle_recommendations(disease, risk_level, health_data):
    """
    Get personalized lifestyle recommendations
    
    Args:
        disease: Disease type (diabetes, heart_disease, etc.)
        risk_level: Risk level (Low, Moderate, High)
        health_data: Dictionary of health parameters
    
    Returns:
        Dictionary of recommendations by category
    """
    if disease == "diabetes":
        return get_diabetes_recommendations(risk_level, health_data)
    elif disease == "heart_disease":
        return get_heart_disease_recommendations(risk_level, health_data)
    elif disease == "pneumonia":
        return get_pneumonia_recommendations(risk_level, health_data)
    elif disease == "brain_tumor":
        return get_brain_tumor_recommendations(risk_level, health_data)
    else:
        return get_general_recommendations(risk_level)

def get_diabetes_recommendations(risk_level, health_data):
    """Generate diabetes-specific recommendations"""
    
    recommendations = {
        'Diet': [],
        'Exercise': [],
        'Sleep': [],
        'Stress': []
    }
    
    # Diet recommendations
    if risk_level in ['Moderate', 'High']:
        recommendations['Diet'].extend([
            "Reduce sugar and refined carbohydrate intake",
            "Focus on low glycemic index foods (whole grains, legumes)",
            "Include more fiber-rich vegetables in every meal",
            "Control portion sizes and eat at regular intervals",
            "Limit processed foods and sugary beverages"
        ])
    else:
        recommendations['Diet'].extend([
            "Maintain a balanced diet with adequate fiber",
            "Monitor carbohydrate intake moderately",
            "Include complex carbohydrates over simple sugars"
        ])
    
    # Exercise recommendations
    if risk_level == 'High':
        recommendations['Exercise'].extend([
            "Start with 20-30 minutes of walking daily",
            "Gradually increase to 150 minutes of moderate activity per week",
            "Include resistance training 2-3 times per week",
            "Monitor blood glucose before and after exercise"
        ])
    else:
        recommendations['Exercise'].extend([
            "Maintain at least 30 minutes of physical activity daily",
            "Include both aerobic and strength training exercises",
            "Stay active throughout the day, avoid prolonged sitting"
        ])
    
    # Sleep recommendations
    recommendations['Sleep'].extend([
        "Aim for 7-9 hours of quality sleep nightly",
        "Maintain consistent sleep schedule",
        "Poor sleep can affect blood sugar regulation"
    ])
    
    # Stress management
    recommendations['Stress'].extend([
        "Practice stress-reduction techniques (meditation, yoga)",
        "Stress hormones can increase blood sugar levels",
        "Consider mindfulness or breathing exercises daily"
    ])
    
    return recommendations

def get_heart_disease_recommendations(risk_level, health_data):
    """Generate heart disease-specific recommendations"""
    
    recommendations = {
        'Diet': [],
        'Exercise': [],
        'Sleep': [],
        'Stress': []
    }
    
    # Diet recommendations
    if risk_level in ['Moderate', 'High']:
        recommendations['Diet'].extend([
            "Follow heart-healthy diet (Mediterranean or DASH diet)",
            "Reduce sodium intake to less than 2,300mg daily",
            "Limit saturated and trans fats",
            "Increase omega-3 fatty acids (fish, nuts, seeds)",
            "Eat more fruits, vegetables, and whole grains",
            "Limit alcohol consumption"
        ])
    else:
        recommendations['Diet'].extend([
            "Maintain heart-healthy eating patterns",
            "Monitor sodium and fat intake",
            "Include plenty of fruits and vegetables"
        ])
    
    # Exercise recommendations
    if risk_level == 'High':
        recommendations['Exercise'].extend([
            "Consult doctor before starting exercise program",
            "Start with light activities like walking",
            "Gradually build to 150 minutes of moderate aerobic activity weekly",
            "Avoid sudden strenuous activities"
        ])
    else:
        recommendations['Exercise'].extend([
            "Engage in regular aerobic exercise (walking, swimming, cycling)",
            "Aim for 150-300 minutes of moderate activity per week",
            "Include strength training exercises twice weekly"
        ])
    
    # Sleep recommendations
    recommendations['Sleep'].extend([
        "Get 7-9 hours of sleep per night",
        "Poor sleep linked to high blood pressure and heart disease",
        "Address sleep apnea if present"
    ])
    
    # Stress management
    recommendations['Stress'].extend([
        "Manage stress through relaxation techniques",
        "Chronic stress can increase heart disease risk",
        "Consider yoga, meditation, or tai chi",
        "Maintain social connections and support network"
    ])
    
    return recommendations

def get_pneumonia_recommendations(risk_level, health_data):
    """Generate pneumonia/respiratory recommendations"""
    
    recommendations = {
        'Diet': [],
        'Exercise': [],
        'Sleep': [],
        'Stress': []
    }
    
    recommendations['Diet'].extend([
        "Stay well-hydrated (8-10 glasses of water daily)",
        "Consume nutrient-rich foods to support immune system",
        "Include vitamin C-rich foods (citrus, berries)",
        "Adequate protein intake for tissue repair"
    ])
    
    recommendations['Exercise'].extend([
        "Rest adequately during recovery",
        "Gentle breathing exercises can help lung capacity",
        "Gradually return to normal activity as symptoms improve",
        "Avoid strenuous exercise until fully recovered"
    ])
    
    recommendations['Sleep'].extend([
        "Get plenty of rest to support immune function",
        "Sleep with head elevated if breathing is difficult",
        "Maintain good air quality in sleeping area"
    ])
    
    recommendations['Stress'].extend([
        "Reduce stress to support immune system",
        "Practice deep breathing exercises",
        "Ensure adequate rest and recovery time"
    ])
    
    return recommendations

def get_brain_tumor_recommendations(risk_level, health_data):
    """Generate brain tumor/neurological recommendations"""
    
    recommendations = {
        'Diet': [],
        'Exercise': [],
        'Sleep': [],
        'Stress': []
    }
    
    recommendations['Diet'].extend([
        "Maintain balanced, nutrient-rich diet",
        "Stay well-hydrated",
        "Avoid excessive caffeine which may trigger symptoms",
        "Consider anti-inflammatory foods"
    ])
    
    recommendations['Exercise'].extend([
        "Engage in gentle, low-impact activities",
        "Avoid activities with fall risk if balance is affected",
        "Practice coordination exercises if needed",
        "Rest when experiencing symptoms"
    ])
    
    recommendations['Sleep'].extend([
        "Maintain regular sleep schedule",
        "Ensure adequate sleep for brain health",
        "Address sleep disturbances with healthcare provider"
    ])
    
    recommendations['Stress'].extend([
        "Practice stress reduction techniques",
        "Consider meditation or mindfulness",
        "Seek support from family, friends, or support groups",
        "Manage symptoms-related anxiety"
    ])
    
    return recommendations

def get_general_recommendations(risk_level):
    """Generate general health recommendations"""
    
    recommendations = {
        'Diet': [
            "Eat a balanced diet with variety of nutrients",
            "Include fruits and vegetables in every meal",
            "Stay hydrated throughout the day"
        ],
        'Exercise': [
            "Aim for at least 150 minutes of moderate activity weekly",
            "Include both cardio and strength training",
            "Stay active throughout the day"
        ],
        'Sleep': [
            "Get 7-9 hours of quality sleep nightly",
            "Maintain consistent sleep schedule",
            "Create a restful sleep environment"
        ],
        'Stress': [
            "Practice stress management techniques",
            "Maintain work-life balance",
            "Stay connected with loved ones"
        ]
    }
    
    return recommendations

def get_smoking_cessation_advice():
    """Recommendations for smoking cessation"""
    return [
        "Quitting smoking is the single most important step for heart and lung health",
        "Consider nicotine replacement therapy or medications",
        "Seek support from healthcare provider or cessation programs",
        "Identify and avoid smoking triggers",
        "Join a support group for encouragement"
    ]

def get_weight_management_advice(bmi):
    """Weight management recommendations based on BMI"""
    if bmi < 18.5:
        return [
            "BMI indicates underweight - focus on healthy weight gain",
            "Increase caloric intake with nutrient-dense foods",
            "Consider consulting a nutritionist"
        ]
    elif 18.5 <= bmi < 25:
        return [
            "BMI is in healthy range - maintain current weight",
            "Continue balanced diet and regular exercise"
        ]
    elif 25 <= bmi < 30:
        return [
            "BMI indicates overweight - aim for gradual weight loss",
            "Focus on portion control and increased physical activity",
            "Target 1-2 pounds weight loss per week"
        ]
    else:  # BMI >= 30
        return [
            "BMI indicates obesity - weight loss is important for health",
            "Consult healthcare provider for personalized weight loss plan",
            "Combine dietary changes with regular physical activity",
            "Consider medical weight management programs if needed"
        ]
