import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Load Data
df = pd.read_csv("cleaned_sleep_health_data.csv")
df = df.dropna(subset=["Sleep Disorder"])  # Remove rows with no target label

# Feature & Target
X = df.drop(columns=["Sleep Disorder"])
y = df["Sleep Disorder"]

# Pipeline
num_cols = ["Age", "Sleep Duration", "Quality of Sleep", "Physical Activity Level", "Stress Level",
            "Heart Rate", "Daily Steps", "Systolic_BP", "Diastolic_BP"]

cat_cols = ["Gender", "Occupation", "BMI Category"]

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, num_cols),
        ("cat", categorical_transformer, cat_cols)
    ]
)

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(random_state=42))
])

# Train & Save
pipeline.fit(X, y)

with open("app/model.pkl", "wb") as f:
    pickle.dump(pipeline, f)
with open("app/preprocessor.pkl", "wb") as f:
    pickle.dump(preprocessor, f)
