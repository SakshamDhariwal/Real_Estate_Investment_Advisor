def generate_summary(city, bhk, pred_price, roi, rating):

    return f"""
This {bhk} BHK property in {city} has an estimated future value of ₹{pred_price:.1f} Lakhs.
Projected ROI is {roi:.1f}%.
Overall recommendation: {rating}.
"""