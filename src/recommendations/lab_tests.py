"""
Lab Test Recommendation Engine
Suggests relevant medical tests based on disease risk
"""

def get_lab_test_recommendations(disease):
    """
    Get recommended lab tests for specific disease
    
    Args:
        disease: Disease type (diabetes, heart_disease, etc.)
    
    Returns:
        List of recommended lab tests
    """
    if disease == "diabetes":
        return get_diabetes_tests()
    elif disease == "heart_disease":
        return get_heart_disease_tests()
    elif disease == "pneumonia":
        return get_pneumonia_tests()
    elif disease == "brain_tumor":
        return get_brain_tumor_tests()
    else:
        return get_general_health_tests()

def get_diabetes_tests():
    """Recommended tests for diabetes screening"""
    return [
        "Fasting Blood Glucose (FBG) - Primary diagnostic test",
        "Hemoglobin A1C (HbA1c) - 3-month average blood sugar",
        "Oral Glucose Tolerance Test (OGTT) - If FBG is borderline",
        "Fasting Lipid Profile - Cholesterol and triglycerides",
        "Kidney Function Tests - Creatinine, BUN",
        "Urine Microalbumin - Early kidney damage detection",
        "Thyroid Function Tests (TSH, T3, T4) - Related conditions",
        "Liver Function Tests - Overall metabolic health"
    ]

def get_heart_disease_tests():
    """Recommended tests for heart disease screening"""
    return [
        "Lipid Profile - Total cholesterol, LDL, HDL, triglycerides",
        "Electrocardiogram (ECG/EKG) - Heart rhythm and electrical activity",
        "Echocardiogram - Heart structure and function",
        "Stress Test (Treadmill/Exercise ECG) - Heart under exertion",
        "Blood Pressure Monitoring - 24-hour ambulatory monitoring",
        "C-Reactive Protein (CRP) - Inflammation marker",
        "Troponin Test - Heart muscle damage",
        "BNP/NT-proBNP - Heart failure marker",
        "Coronary Calcium Score (CT scan) - Plaque in arteries",
        "Complete Blood Count (CBC) - Overall health status"
    ]

def get_pneumonia_tests():
    """Recommended tests for pneumonia/respiratory conditions"""
    return [
        "Chest X-Ray - Visualize lung inflammation and infection",
        "Complete Blood Count (CBC) - Check white blood cell count",
        "C-Reactive Protein (CRP) - Inflammation marker",
        "Blood Culture - Identify bacterial infection",
        "Sputum Culture - Identify causative organism",
        "Pulse Oximetry - Blood oxygen saturation",
        "Arterial Blood Gas (ABG) - Oxygen and CO2 levels",
        "COVID-19 RT-PCR Test - Rule out coronavirus",
        "CT Chest - Detailed lung imaging if needed"
    ]

def get_brain_tumor_tests():
    """Recommended tests for brain tumor/neurological conditions"""
    return [
        "Brain MRI with Contrast - Primary diagnostic imaging",
        "CT Scan (Head) - Initial screening or if MRI unavailable",
        "Neurological Examination - Comprehensive nerve function assessment",
        "Vision and Hearing Tests - Cranial nerve function",
        "EEG (Electroencephalogram) - If seizures present",
        "Lumbar Puncture (Spinal Tap) - Cerebrospinal fluid analysis",
        "PET Scan - Metabolic activity of brain tissue",
        "Biopsy - Tissue sample if tumor detected (neurosurgeon)",
        "Blood Tests - Tumor markers, hormone levels"
    ]

def get_general_health_tests():
    """General health screening tests"""
    return [
        "Complete Blood Count (CBC) - Overall health status",
        "Comprehensive Metabolic Panel - Kidney, liver function",
        "Lipid Profile - Cholesterol levels",
        "Blood Pressure Check - Cardiovascular health",
        "Blood Glucose - Diabetes screening",
        "Thyroid Function Tests - Metabolic health",
        "Vitamin D Level - Bone and immune health",
        "Urinalysis - Kidney and urinary tract health"
    ]

def get_preventive_screening_recommendations(age, sex):
    """
    Age and sex-specific preventive screening recommendations
    
    Args:
        age: Patient age
        sex: Patient sex ('M' or 'F')
    
    Returns:
        List of age-appropriate screenings
    """
    screenings = []
    
    # Universal screenings
    if age >= 18:
        screenings.append("Annual physical examination")
        screenings.append("Blood pressure check (every 1-2 years)")
    
    if age >= 20:
        screenings.append("Lipid profile (every 5 years, more if risk factors)")
    
    if age >= 45:
        screenings.append("Diabetes screening (every 3 years)")
        screenings.append("Colorectal cancer screening (colonoscopy every 10 years)")
    
    if age >= 50:
        screenings.append("Annual comprehensive health check")
    
    # Sex-specific screenings
    if sex.upper() == 'F':
        if age >= 21:
            screenings.append("Pap smear (cervical cancer screening every 3 years)")
        if age >= 40:
            screenings.append("Annual mammogram (breast cancer screening)")
        if age >= 65:
            screenings.append("Bone density scan (osteoporosis screening)")
    
    if sex.upper() == 'M':
        if age >= 50:
            screenings.append("PSA test (prostate cancer screening - discuss with doctor)")
        if age >= 65:
            screenings.append("Abdominal aortic aneurysm screening (one-time)")
    
    return screenings

def get_follow_up_recommendations(risk_level, disease):
    """
    Get follow-up consultation recommendations
    
    Args:
        risk_level: Risk level (Low, Moderate, High)
        disease: Disease type
    
    Returns:
        Follow-up recommendations
    """
    recommendations = []
    
    if risk_level == "High":
        recommendations.extend([
            "🚨 Seek immediate medical consultation",
            "Schedule appointment with specialist within 1-2 weeks",
            "Bring all test results to consultation",
            "Do not delay - early intervention is crucial"
        ])
    elif risk_level == "Moderate":
        recommendations.extend([
            "⚠️ Schedule medical consultation within 2-4 weeks",
            "Get recommended lab tests done",
            "Monitor symptoms closely",
            "Consider lifestyle modifications immediately"
        ])
    else:  # Low risk
        recommendations.extend([
            "✓ Schedule routine check-up within 3 months",
            "Continue healthy lifestyle practices",
            "Monitor any changes in health status",
            "Follow preventive care guidelines"
        ])
    
    # Disease-specific recommendations
    if disease == "diabetes":
        recommendations.append("Consider consulting an Endocrinologist")
    elif disease == "heart_disease":
        recommendations.append("Consider consulting a Cardiologist")
    elif disease == "pneumonia":
        recommendations.append("Consider consulting a Pulmonologist")
    elif disease == "brain_tumor":
        recommendations.append("Consider consulting a Neurologist")
    
    return recommendations
