import pandas as pd

# standard 2024 rules dictionary
DEFAULT_RULES = {
    'personal_allowance': 12570,
    'basic_band_width': 37700,
    'higher_band_limit': 125140,
    'ni_primary_threshold': 12570,
    'ni_upper_limit': 50270,
    'basic_rate': 0.20,
    'higher_rate': 0.40,
    'add_rate': 0.45,
    'ni_main_rate': 0.08,
    'ni_upper_rate': 0.02
}

def calculate_breakdown(income, rules=DEFAULT_RULES):
    tax = 0
    personal_allowance = rules['personal_allowance']
    
    # 60% tax trap logic
    if income > 100000:
        reduction = (income - 100000) / 2
        personal_allowance = max(0, personal_allowance - reduction)
        
    taxable_income = max(0, income - personal_allowance)
    
    basic_band_width = rules['basic_band_width']
    higher_band_limit = rules['higher_band_limit']

    # basic rate calculation
    tax += min(taxable_income, basic_band_width) * rules['basic_rate']
    
    # higher rate calculation
    if taxable_income > basic_band_width:
        taxable_at_40 = max(0, min(income, higher_band_limit) - (personal_allowance + basic_band_width))
        tax += taxable_at_40 * rules['higher_rate']

    # additional rate
    if income > higher_band_limit:
        tax += (income - higher_band_limit) * rules['add_rate']

    ni = 0
    ni_primary_threshold = rules['ni_primary_threshold']
    ni_upper_limit = rules['ni_upper_limit']
    
    # ni calculation
    if income > ni_primary_threshold:
        ni_band_income = min(income, ni_upper_limit) - ni_primary_threshold
        ni += ni_band_income * rules['ni_main_rate']
        
    if income > ni_upper_limit:
        ni += (income - ni_upper_limit) * rules['ni_upper_rate']

    return pd.Series([tax, ni, income - tax - ni])

# UPDATED HELPER: Returns separate values (tax, ni) instead of just the total
def calculate_tax(income, rules=DEFAULT_RULES):
    results = calculate_breakdown(income, rules)
    return results[0], results[1] # returns (tax, ni)

if __name__ == "__main__":
    # Test data to verify the logic still works
    data = [
        {'person_id': 1, 'gross_income': 12000, 'name': 'Low Earner'},
        {'person_id': 2, 'gross_income': 25000, 'name': 'Basic Rate'},
        {'person_id': 3, 'gross_income': 50270, 'name': 'Threshold'},
        {'person_id': 4, 'gross_income': 80000, 'name': 'Higher Rate'},
        {'person_id': 5, 'gross_income': 150000, 'name': 'Add. Rate'}
    ]

    df = pd.DataFrame(data)
    df[['income_tax', 'national_insurance', 'net_income']] = df['gross_income'].apply(calculate_breakdown)

    print("--- 2024/25 ACCURATE SIMULATION ---")
    print(df)