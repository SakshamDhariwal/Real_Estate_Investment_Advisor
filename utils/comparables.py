import pandas as pd

def get_similar_properties(df, city, bhk, sqft, price):
    data = df.copy()

    filtered = data[
        (data["City"] == city) &
        (data["BHK"].between(bhk-1, bhk+1)) &
        (data["Size_in_SqFt"].between(sqft-300, sqft+300)) &
        (data["Price_in_Lakhs"].between(price*0.7, price*1.3))
    ]

    return filtered[
        ["City","Property_Type","BHK","Size_in_SqFt","Price_in_Lakhs"]
    ].head(5)