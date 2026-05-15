import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score,root_mean_squared_error
from train_utils import DATA_FILE_PATH, MODEL_FILE_PATH, MODEL_DIR

df = (pd.read_csv(DATA_FILE_PATH)
      .drop(columns=['name','model','edition'])
      .drop_duplicates()
     )
x = df.drop(columns = 'selling_price')
y = df.selling_price.copy()

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=42)
num_cols=x_train.select_dtypes(include='number').columns.tolist()
cat_cols = [col for col in x_train.columns if col not in num_cols]
num_pipe = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_pipe = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore',sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', num_pipe, num_cols),
    ('cat', cat_pipe, cat_cols)
])
regressor = RandomForestRegressor(
    n_estimators=10,max_depth=5 ,random_state=42)

re_model = Pipeline(steps=[
    ('pre', preprocessor),
    ('reg', regressor)
])

re_model.fit(x_train, y_train)

### save the model

os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(re_model, MODEL_FILE_PATH)