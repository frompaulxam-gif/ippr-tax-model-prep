clear all
set more off

set obs 5
gen person_id = _n

gen income = .
replace income = 12000 in 1
replace income = 25000 in 2
replace income = 50270 in 3
replace income = 80000 in 4
replace income = 150000 in 5

gen str15 name = ""
replace name = "Low Earner" in 1
replace name = "Basic Rate" in 2
replace name = "Threshold" in 3
replace name = "Higher Rate" in 4
replace name = "Add. Rate" in 5

gen personal_allowance = 12570

* this is the 60% tax trap basically cause for every £2 over 100k you lose £1 of tax free allowance
replace personal_allowance = max(0, 12570 - (income - 100000)/2) if income > 100000

gen taxable_income = max(0, income - personal_allowance)

gen tax_due = 0

* first 37700 of taxable income is taxed at 20%
replace tax_due = min(taxable_income, 37700) * 0.20 if taxable_income > 0

* now we check for the 40% band which is anything between 37700 and the top band
replace tax_due = tax_due + (min(taxable_income, 125140 - personal_allowance) - 37700) * 0.40 if taxable_income > 37700

* everything over 125140 gross gets hit with the 45% rate
replace tax_due = tax_due + (income - 125140) * 0.45 if income > 125140

gen ni_due = 0

* ni is cheaper now only 8% in the main band used to be higher
replace ni_due = (min(income, 50270) - 12570) * 0.08 if income > 12570

* rich people pay 2% on everything over the upper limit
replace ni_due = ni_due + (income - 50270) * 0.02 if income > 50270

gen net_income = income - tax_due - ni_due

format income tax_due ni_due net_income %9.2f

list name income tax_due ni_due net_income, separator(5)
