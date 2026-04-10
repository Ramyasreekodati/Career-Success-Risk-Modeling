import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    
    # 1. Student Academic & Program Information
    courses = ['Engineering', 'MBA', 'Nursing', 'Data Science', 'Finance', 'Arts']
    data = {
        'student_id': range(1, num_samples + 1),
        'course_type': np.random.choice(courses, num_samples),
        'cgpa': np.round(np.random.uniform(6.0, 10.0, num_samples), 2),
        'internships': np.random.randint(0, 4, num_samples),
        'certifications': np.random.randint(0, 6, num_samples),
        'academic_consistency': np.random.choice(['High', 'Medium', 'Low'], num_samples, p=[0.4, 0.4, 0.2]),
    }
    
    # 2. Institute & Program Level Data
    tiers = ['Tier 1', 'Tier 2', 'Tier 3']
    data['institute_tier'] = np.random.choice(tiers, num_samples, p=[0.2, 0.5, 0.3])
    data['placement_cell_activity'] = np.random.choice(['High', 'Medium', 'Low'], num_samples)
    
    # 3. Industry & Labor Market Indicators
    data['industry_demand_index'] = np.random.uniform(0, 1, num_samples) # 0 to 1 scale
    data['regional_job_density'] = np.random.uniform(0, 1, num_samples)
    
    # 4. Student Behavior (Optional but included)
    data['job_portal_activity'] = np.random.uniform(0, 1, num_samples)
    data['mock_interviews_cleared'] = np.random.randint(0, 10, num_samples)

    # 5. Logical Labels Generation (Outcome Labels)
    # Probability of placement depends on CGPA, Internships, Tier, and demand
    base_score = (data['cgpa'] / 10 * 0.3) + \
                 (data['internships'] / 3 * 0.2) + \
                 (data['industry_demand_index'] * 0.2) + \
                 ((3 - np.array([tiers.index(t) for t in data['institute_tier']])) / 3 * 0.2) + \
                 (data['certifications'] / 5 * 0.1)
    
    # Normalize base_score
    base_score = (base_score - base_score.min()) / (base_score.max() - base_score.min())
    
    # Map to placement timeline
    timeline = []
    for score in base_score:
        if score > 0.75:
            timeline.append('Within 3 months')
        elif score > 0.5:
            timeline.append('Within 6 months')
        elif score > 0.3:
            timeline.append('Within 12 months')
        else:
            timeline.append('Delayed / High Risk')
            
    data['placement_timeline'] = timeline
    
    # Salary Estimation (in INR)
    course_base_salary = {
        'Engineering': 500000,
        'MBA': 700000,
        'Nursing': 350000,
        'Data Science': 650000,
        'Finance': 600000,
        'Arts': 300000
    }
    
    tier_multiplier = {'Tier 1': 1.4, 'Tier 2': 1.1, 'Tier 3': 0.85}
    
    salaries = []
    for i in range(num_samples):
        base = course_base_salary[data['course_type'][i]]
        mult = tier_multiplier[data['institute_tier'][i]]
        perf = 0.9 + (base_score[i] * 0.3) # performance boost (90% to 120%)
        noise = np.random.normal(0, 0.03) # 3% noise
        salary = base * mult * perf * (1 + noise)
        salaries.append(int(salary))
        
    data['actual_salary'] = salaries
    
    df = pd.DataFrame(data)
    
    # Risk Score Formulation
    mapping = {'Within 3 months': 0, 'Within 6 months': 1, 'Within 12 months': 2, 'Delayed / High Risk': 3}
    df['placement_risk_score'] = df['placement_timeline'].map(mapping)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/student_data.csv', index=False)
    print(f"Generated {num_samples} samples and saved to 'data/student_data.csv'")

if __name__ == "__main__":
    generate_synthetic_data(2000)
