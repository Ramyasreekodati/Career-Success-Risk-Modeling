import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import calculate_stress_test

class TestRiskLogic(unittest.TestCase):

    def test_emi_calculation(self):
        # Case: $1M loan, 12% annual interest (1% monthly), 10 years (120 months)
        loan_info = {
            "loan_amount": 1000000.0,
            "interest_rate": 12.0,
            "tenure_years": 10
        }
        salary = 1200000 # Annual salary
        timeline = "Within 3 months"
        
        results = calculate_stress_test(salary, timeline, loan_info)
        
        # Expected EMI simplified: P*r / (1 - (1+r)^-n)
        # 1,000,000 * 0.01 / (1 - (1.01)^-120) ~= 14,347.09
        self.assertAlmostEqual(results['monthly_emi'], 14347.09, delta=1.0)
        
    def test_stress_profile_high(self):
        # High DTI and delay
        loan_info = {"loan_amount": 2000000, "interest_rate": 15, "tenure_years": 5}
        salary = 400000 # Low salary
        timeline = "Delayed / High Risk"
        
        results = calculate_stress_test(salary, timeline, loan_info)
        self.assertEqual(results['stress_profile'], "High")

    def test_stress_profile_low(self):
        # Low DTI and quick placement
        loan_info = {"loan_amount": 100000, "interest_rate": 5, "tenure_years": 10}
        salary = 2000000 # High salary
        timeline = "Within 3 months"
        
        results = calculate_stress_test(salary, timeline, loan_info)
        self.assertEqual(results['stress_profile'], "Low")

if __name__ == '__main__':
    unittest.main()
