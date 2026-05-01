# Real Estate Investment Advisor

## Project Overview

Real Estate Investment Advisor is a machine learning-based web application that helps users evaluate whether a property is a good investment and predicts its estimated future price after 5 years.

This project combines:
- Classification: predicts whether a property is a `Good Investment`
- Regression: predicts `Future Price after 5 Years`
- EDA: analyzes property trends, price patterns, and location-based insights
- Streamlit Dashboard: provides an interactive user interface for prediction and visualization

## Problem Statement

The objective of this project is to assist real estate investors and buyers in making better property decisions using data-driven insights.

The system should:
- classify whether a property is a good investment
- predict future value after 5 years
- show visual insights from housing data
- help investors compare profitability potential

## Business Use Cases

- Helps investors identify high-potential properties
- Supports buyers in comparing future returns across cities and localities
- Assists real estate companies in automating investment evaluation
- Improves trust through transparent, data-backed predictions

## Dataset

Dataset used:
- `india_housing_prices.csv`

Processed dataset:
- `cleaned_data.csv`

Final enriched dataset generated after training:
- `final_enriched_data.csv`

### Main Features

- `State`
- `City`
- `Locality`
- `Property_Type`
- `BHK`
- `Size_in_SqFt`
- `Price_in_Lakhs`
- `Price_per_SqFt`
- `Year_Built`
- `Furnished_Status`
- `Floor_No`
- `Total_Floors`
- `Age_of_Property`
- `Nearby_Schools`
- `Nearby_Hospitals`
- `Public_Transport_Accessibility`
- `Parking_Space`
- `Security`
- `Amenities`
- `Facing`
- `Owner_Type`
- `Availability_Status`

## Feature Engineering

Additional engineered features used in this project:
- `Property_Age = 2026 - Year_Built`
- `Price_per_BHK = Price_in_Lakhs / BHK`
- `Future_Price_5Y`
- `Good_Investment`

## Target Creation Logic

### 1. Regression Target: `Future_Price_5Y`

Future property price is estimated using a growth-based formula influenced by:
- public transport accessibility
- nearby schools
- nearby hospitals

A small market noise term is also added to simulate realistic variation.

### 2. Classification Target: `Good_Investment`

A property is labeled as a good investment using a rule-based score based on:
- good public transport access
- lower property age
- above-median nearby schools
- above-median nearby hospitals
- price per sqft compared to city median

If the total score crosses a threshold, the property is marked as a good investment.

## Exploratory Data Analysis (EDA)

EDA was performed to understand:
- distribution of property prices
- distribution of property sizes
- average prices by city
- price per sqft by property type
- size vs price relationship
- BHK distribution
- price variation by furnished status
- correlation between numeric features

### EDA Output Charts

Generated charts:
- `price_distribution.png`
- `size_distribution.png`
- `top_cities.png`
- `property_type_price_per_sqft.png`
- `size_vs_price.png`
- `heatmap.png`
- `bhk_distribution.png`
- `furnished_vs_price.png`

## Machine Learning Models

### Classification Model
- `RandomForestClassifier`

Used to predict:
- `Good_Investment`

### Regression Model
- `RandomForestRegressor`

Used to predict:
- `Future_Price_5Y`

## Evaluation Metrics

### Classification Metrics
- Accuracy
- Confusion Matrix
- Classification Report
- Precision
- Recall
- F1-score

### Regression Metrics
- MAE
- RMSE
- R² Score

## Streamlit Dashboard

The project includes an interactive Streamlit dashboard built in:
- `app.py`

### Dashboard Features
- property input form in sidebar
- investment classification result
- confidence score
- future price forecast
- ROI and profit analysis
- city-level charts
- property type distribution
- feature importance
- locality ranking insights

## Project Structure

```text
RealEstateAdvisor/
├── .streamlit/
│   └── config.toml
├── charts/
├── models/
│   ├── classifier.pkl
│   ├── encoders.pkl
│   └── regressor.pkl
├── utils/
├── app.py
├── cleaned_data.csv
├── eda.ipynb
├── eda.py
├── final_enriched_data.csv
├── india_housing_prices.csv
├── README.md
├── requirements.txt
├── test.py
├── train.py
└── watchlist.csv
