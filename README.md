# ippr-tax-model-prep
Preparation logic for Family Resources Survey microsimulation (Python & Stata)

Author: Paul Andy
Date: December 2025

Context prep for family resources survey frs analysis

Overview
This repo has early logic for simulating uk personal tax and benefits
The aim is to match the 2024 2025 uk tax rules
Standard personal allowance and the taper when income is over 100k
Basic higher and additional rate income tax
National insurance class 1 calculations
Added a gui sandbox so users can test policy changes dynamically

Files
tax_simulation py python script using pandas for vectorised tax calculations
tax_app py wxpython gui app for interactive policy testing with sliders
frs_tax_simulation do stata script tested on stata 19 5 for data generation and analysis

Usage
Both scripts make a small mock dataset with n equals 5 so i can check the logic works before running it on the secure frs dataset
Run tax_app py to open the policy sandbox window

Quality Assurance
Using stata as the control model to validate the python logic
frs_tax_simulation do sets the benchmark figures
tax_simulation py matches it perfectly e.g. 150k earner gets 91286.40 net in both models
