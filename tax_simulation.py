import pandas as pd

data = [
    {'person_id': 1, 'gross_income': 12000, 'name': 'Low Earner'},
    {'person_id': 2, 'gross_income': 25000, 'name': 'Basic Rate'},
    {'person_id': 3, 'gross_income': 50270, 'name': 'Threshold'},
    {'person_id': 4, 'gross_income': 80000, 'name': 'Higher Rate'},
    {'person_id': 5, 'gross_income': 150000, 'name': 'Add. Rate'}
]

df = pd.DataFrame(data)

def calculate_take_home_2024(income):
    tax = 0
    personal_allowance = 12570
    
    # this is the 60% tax trap basically cause for every £2 over 100k you lose £1 of tax free allowance
    if income > 100000:
        reduction = (income - 100000) / 2
        personal_allowance = max(0, personal_allowance - reduction)
        
    taxable_income = max(0, income - personal_allowance)
    
    basic_band_width = 37700
    higher_band_limit = 125140 

    tax += min(taxable_income, basic_band_width) * 0.20
    
    # the maths gets messy here cause if the allowance dropped to 0 we gotta make sure we dont double count the basic band
    if taxable_income > basic_band_width:
        taxable_at_40 = max(0, min(income, 125140) - (personal_allowance + basic_band_width))
        tax += taxable_at_40 * 0.40

    if income > 125140:
        tax += (income - 125140) * 0.45

    ni = 0
    ni_primary_threshold = 12570
    ni_upper_limit = 50270
    
    # ni is cheaper now only 8% in the main band used to be higher
    if income > ni_primary_threshold:
        ni_band_income = min(income, ni_upper_limit) - ni_primary_threshold
        ni += ni_band_income * 0.08
        
    if income > ni_upper_limit:
        ni += (income - ni_upper_limit) * 0.02

    # returning this as a series lets pandas split it into columns automatically down below
    return pd.Series([tax, ni, income - tax - ni])

df[['income_tax', 'national_insurance', 'net_income']] = df['gross_income'].apply(calculate_take_home_2024)

print("--- 2024/25 ACCURATE SIMULATION ---")
print(df)