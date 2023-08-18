import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

data = pd.read_csv('train.csv')

selected_features = ['MSSubClass', 'MSZoning', 'LotFrontage', 'LotArea', 'Neighborhood', 'OverallQual', 'OverallCond', 'YearBuilt', 'MasVnrArea', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenQual', 'TotRmsAbvGrd', 'Fireplaces', 'GarageCars', 'GarageArea', 'PavedDrive', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'SaleType', 'SaleCondition']

X = data[selected_features]
y = data['SalePrice']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_features = ['MSZoning', 'Neighborhood', 'KitchenQual', 'PavedDrive', 'SaleType', 'SaleCondition']
preprocessor = ColumnTransformer(transformers=[('cat', OneHotEncoder(), categorical_features)], remainder='passthrough')

numerical_features = x_train.columns.difference(categorical_features)
imputer = SimpleImputer(strategy='mean')

pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('imputer', imputer), ('model', LinearRegression())])

pipeline.fit(x_train, y_train)

y_pred = pipeline.predict(x_test)

#Calculate the mean squared error
mse = mean_squared_error(y_test, y_pred)

# Calculate Root Mean Squared Error (RMSE)
rmse = mean_squared_error(y_test, y_pred, squared=False)

# Calculate Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)

# Calculate R-squared (coefficient of determination)
r2 = r2_score(y_test, y_pred)

manual_input = {
    'MSSubClass': 60,
    'MSZoning': 'RL',
    'LotFrontage': 65,
    'LotArea': 8450,
    'Neighborhood': 'CollgCr',
    'OverallQual': 7,
    'OverallCond': 5,
    'YearBuilt': 2003,
    'MasVnrArea': 196,
    'TotalBsmtSF': 856,
    '1stFlrSF': 856,
    '2ndFlrSF': 854,
    'FullBath': 2,
    'HalfBath': 1,
    'BedroomAbvGr': 3,
    'KitchenQual': 'Gd',
    'TotRmsAbvGrd': 8,
    'Fireplaces': 0,
    'GarageCars': 2,
    'GarageArea': 548,
    'PavedDrive': 'Y',
    'WoodDeckSF': 0,
    'OpenPorchSF': 61,
    'EnclosedPorch': 0,
    '3SsnPorch': 0,
    'ScreenPorch': 0,
    'PoolArea': 0,
    'SaleType': 'WD',
    'SaleCondition': 'Normal'
}

# Convert the manual input into a DataFrame
manual_input_df = pd.DataFrame([manual_input])

# Preprocess the manual input using the preprocessor
manual_input_preprocessed = pipeline.named_steps['preprocessor'].transform(manual_input_df)

# Make predictions using the preprocessed input
predicted_sale_price = pipeline.named_steps['model'].predict(manual_input_preprocessed)

print(f"Predicted Sale Price: {predicted_sale_price[0]}")