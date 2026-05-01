import math

def calculate_emi(principal, annual_rate=8.5, years=20):
    r = annual_rate / 12 / 100
    n = years * 12

    emi = principal * r * ((1+r)**n) / (((1+r)**n)-1)
    return round(emi,2)

def rental_yield(monthly_rent, property_price_lakhs):
    annual_rent = monthly_rent * 12
    property_price = property_price_lakhs * 100000
    yield_percent = (annual_rent / property_price) * 100
    return round(yield_percent,2)