# ippr-tax-model-prep
Preparation logic for Family Resources Survey microsimulation (Python &amp; Stata)

Author: Paul Andy
Date: December 2025

Context prep for family resources survey frs analysis

Overview
This repo has some early logic for simulating uk personal tax and benefits
The aim is to match the 2024 2025 uk tax rules
Standard personal allowance and the taper when income is over 100k
Basic higher and additional rate income tax
National insurance class 1 calculations

Files
tax_simulation py python script using pandas for vectorised tax calculations
frs_tax_simulation do stata script tested on stata 19 5 for data generation and analysis

Usage
Both scripts make a small mock dataset with n equals 5 so i can check the logic works before running it on the secure frs dataset
