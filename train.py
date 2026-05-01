import joblib
import numpy as np
import os
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# =====================================================
# PATHS
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "cleaned_data.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODELS_DIR, exist_ok=True)

# MLflow experiment
mlflow.set_experiment("RealEstateAdvisor")

# =====================================================
# LOAD DATA
# =====================================================
def load_data():
    df = pd.read_csv(DATA_PATH)

    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]

    print("Loaded dataset shape:", df.shape)
    print("Duplicates removed:", before - after)

    return df

# =====================================================
# PREPARE NUMERIC COLUMNS
# =====================================================
def prepare_numeric_columns(df):
    df = df.copy()

    numeric_candidates = [
        "BHK",
        "Size_in_SqFt",
        "Price_in_Lakhs",
        "Price_per_SqFt",
        "Year_Built",
        "Floor_No",
        "Total_Floors",
        "Age_of_Property",
        "Nearby_Schools",
        "Nearby_Hospitals",
        "Public_Transport_Accessibility",
    ]

    for col in numeric_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# =====================================================
# FILL MISSING VALUES
# =====================================================
def fill_missing_values(df):
    df = df.copy()

    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(exclude=np.number).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        mode = df[col].mode(dropna=True)
        fill_val = mode.iloc[0] if not mode.empty else "Unknown"
        df[col] = df[col].fillna(fill_val)

    return df

# =====================================================
# FEATURE ENGINEERING
# =====================================================
def engineer_features(df):
    df = df.copy()

    current_year = 2026

    if "Age_of_Property" not in df.columns:
        df["Age_of_Property"] = current_year - df["Year_Built"]

    df["Property_Age"] = current_year - df["Year_Built"]
    df["Price_per_BHK"] = df["Price_in_Lakhs"] / df["BHK"].replace(0, 1)

    if "Price_per_SqFt" not in df.columns:
        safe_sqft = df["Size_in_SqFt"].replace(0, np.nan)
        df["Price_per_SqFt"] = df["Price_in_Lakhs"] / safe_sqft
        df["Price_per_SqFt"] = df["Price_per_SqFt"].fillna(
            df["Price_per_SqFt"].median()
        )

    return df

# =====================================================
# CREATE TARGETS
# =====================================================
def create_targets(df):
    df = df.copy()

    # -------------------------------
    # City-specific growth rates
    # -------------------------------
    city_growth = {
        "Mumbai": 0.11,
        "Delhi": 0.10,
        "Bangalore": 0.10,
        "Hyderabad": 0.095,
        "Pune": 0.09,
        "Chennai": 0.088,
        "Jaipur": 0.082,
        "Lucknow": 0.080,
        "Noida": 0.092,
        "Gurgaon": 0.094
    }

    # default for unknown cities
    df["City_Growth"] = df["City"].map(city_growth).fillna(0.075)

    # -------------------------------
    # Property Type growth premium
    # -------------------------------
    type_growth = {
        "Apartment": 0.010,
        "Villa": 0.018,
        "Independent House": 0.015,
        "Plot": 0.022,
        "Studio": 0.008
    }

    df["Type_Growth"] = df["Property_Type"].map(type_growth).fillna(0.010)

    # -------------------------------
    # Feature-based growth signals
    # -------------------------------
    infra_growth = (
        (df["Public_Transport_Accessibility"] * 0.002)
        + (df["Nearby_Schools"] * 0.0005)
        + (df["Nearby_Hospitals"] * 0.0003)
    )

    # Final growth rate
    growth_rate = (
        df["City_Growth"]
        + df["Type_Growth"]
        + infra_growth
    )

    # realistic market noise
    np.random.seed(42)
    market_noise = np.random.normal(1.0, 0.08, len(df))

    # Future price after 5 years
    df["Future_Price_5Y"] = (
        df["Price_in_Lakhs"] * ((1 + growth_rate) ** 5) * market_noise
    )

    df["Future_Price_5Y"] = pd.to_numeric(
        df["Future_Price_5Y"],
        errors="coerce"
    )

    df["Future_Price_5Y"] = df["Future_Price_5Y"].fillna(
        df["Price_in_Lakhs"] * 1.30
    )

    # -------------------------------
    # Good Investment Classification
    # -------------------------------
    score = (
        (df["Public_Transport_Accessibility"] >= 5).astype(int)
        + (df["Property_Age"] <= 12).astype(int)
        + (df["Nearby_Schools"] >= df["Nearby_Schools"].median()).astype(int)
        + (df["Nearby_Hospitals"] >= df["Nearby_Hospitals"].median()).astype(int)
        + (
            df["Price_per_SqFt"]
            <= df.groupby("City")["Price_per_SqFt"].transform("median")
        ).astype(int)
        + (df["City_Growth"] >= 0.09).astype(int)
    )

    np.random.seed(42)
    noise = np.random.binomial(1, 0.10, len(df))

    df["Good_Investment"] = ((score + noise) >= 4).astype(int)

    return df

# =====================================================
# ENCODE CATEGORICALS
# =====================================================
def encode_categorical_columns(df):
    df = df.copy()
    encoders = {}

    cat_cols = df.select_dtypes(include="object").columns.tolist()

    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    return df, encoders

# =====================================================
# CLASSIFIER
# =====================================================
def train_classifier(df):

    feature_cols = [
        c for c in df.columns
        if c not in ["Good_Investment", "Future_Price_5Y"]
    ]

    X = df[feature_cols]
    y = df["Good_Investment"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=180,
        max_depth=12,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)

    accuracy = accuracy_score(y_test, preds)

    print("\n===== Classification =====")
    print("Accuracy:", round(accuracy, 4))
    print(confusion_matrix(y_test, preds))
    print(classification_report(y_test, preds))

    # Save model
    joblib.dump(clf, os.path.join(MODELS_DIR, "classifier.pkl"))

    # MLflow logs
    mlflow.log_param("classifier", "RandomForestClassifier")
    mlflow.log_param("clf_n_estimators", 180)
    mlflow.log_param("clf_max_depth", 12)

    mlflow.log_metric("classification_accuracy", accuracy)

    mlflow.sklearn.log_model(clf, "classifier_model")

# =====================================================
# REGRESSOR
# =====================================================
def train_regressor(df):

    feature_cols = [
        c for c in df.columns
        if c not in ["Future_Price_5Y", "Good_Investment", "Price_in_Lakhs"]
    ]

    X = df[feature_cols]
    y = df["Future_Price_5Y"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    reg = RandomForestRegressor(
        n_estimators=200,
        max_depth=14,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    reg.fit(X_train, y_train)
    preds = reg.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    print("\n===== Regression =====")
    print("MAE:", round(mae, 4))
    print("RMSE:", round(rmse, 4))
    print("R2 Score:", round(r2, 4))

    # Save model
    joblib.dump(reg, os.path.join(MODELS_DIR, "regressor.pkl"))

    # MLflow logs
    mlflow.log_param("regressor", "RandomForestRegressor")
    mlflow.log_param("reg_n_estimators", 200)
    mlflow.log_param("reg_max_depth", 14)

    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("RMSE", rmse)
    mlflow.log_metric("R2_Score", r2)

    mlflow.sklearn.log_model(reg, "regressor_model")

# =====================================================
# MAIN
# =====================================================
def main():

    df = load_data()
    df = prepare_numeric_columns(df)
    df = fill_missing_values(df)
    df = engineer_features(df)
    df = create_targets(df)

    model_df, encoders = encode_categorical_columns(df)

    joblib.dump(encoders, os.path.join(MODELS_DIR, "encoders.pkl"))

    with mlflow.start_run():

        train_classifier(model_df)
        train_regressor(model_df)

    enriched_path = os.path.join(BASE_DIR, "final_enriched_data.csv")
    df.to_csv(enriched_path, index=False)

    print("\nSaved files:")
    print("- classifier.pkl")
    print("- regressor.pkl")
    print("- encoders.pkl")
    print("- final_enriched_data.csv")
    print("- mlruns/ (MLflow logs)")

# =====================================================
if __name__ == "__main__":
    main()