from load_data import load_data
from data_preprocessing import preprocess_data

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from xgboost import XGBRegressor
import joblib


# Step 1: Load data
data = load_data()

print("Dataset Loaded")
print(data.head())


# Step 2: Preprocess data
X, y = preprocess_data(data)


# Step 3: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# -------------------------------
# Step 4: Train Random Forest
# -------------------------------

rf_model = RandomForestRegressor()

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

rf_error = mean_absolute_error(y_test, rf_predictions)

print("Random Forest MAE:", rf_error)


# -------------------------------
# Step 5: Train XGBoost
# -------------------------------

xgb_model = XGBRegressor()

xgb_model.fit(X_train, y_train)

xgb_predictions = xgb_model.predict(X_test)

xgb_error = mean_absolute_error(y_test, xgb_predictions)

print("XGBoost MAE:", xgb_error)


# -------------------------------
# Step 6: Choose Best Model
# -------------------------------

if xgb_error < rf_error:
    best_model = xgb_model
    model_name = "XGBoost"
else:
    best_model = rf_model
    model_name = "RandomForest"


print("Best Model:", model_name)


# -------------------------------
# Step 7: Save Model
# -------------------------------

joblib.dump(best_model, "hospital_prediction_model.pkl")

print("Model saved successfully")