import os
import joblib
import pandas as pd


from sklearn.model_selection import train_test_split


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier


from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

# ===============================
# CONFIG
# ===============================

DATA_PATH = "../dataset/clean_Student.csv"

MODEL_DIR = "../models"

RANDOM_STATE = 42


os.makedirs(MODEL_DIR, exist_ok=True)


# ===============================
# LOAD DATA
# ===============================


df = pd.read_csv(DATA_PATH)


print("Dataset shape:", df.shape)


# ===============================
# FEATURES / TARGET
# ===============================


X = df.drop(columns=["Completed"])


y = df["Completed"]


# Save feature order for API

FEATURES = X.columns.tolist()


joblib.dump(FEATURES, f"{MODEL_DIR}/classification_features.pkl")


# ===============================
# TRAIN TEST SPLIT
# ===============================


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)


print("\nTrain:", X_train.shape)

print("Test :", X_test.shape)


# ===============================
# MODELS
# ===============================


models = {
    "logistic_regression": Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=3000, random_state=RANDOM_STATE)),
        ]
    ),
    "random_forest": RandomForestClassifier(
        n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1
    ),
    "gradient_boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
}


# ===============================
# TRAIN + EVALUATE
# ===============================


results = {}


for name, model in models.items():

    print("\n======================")

    print(name)

    print("======================")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(y_test, predictions)

    recall = recall_score(y_test, predictions)

    f1 = f1_score(y_test, predictions)

    auc = roc_auc_score(y_test, probabilities)

    print("Accuracy:", round(accuracy, 3))

    print("Precision:", round(precision, 3))

    print("Recall:", round(recall, 3))

    print("F1:", round(f1, 3))

    print("ROC-AUC:", round(auc, 3))

    print("\nConfusion Matrix")

    print(confusion_matrix(y_test, predictions))

    print(classification_report(y_test, predictions))

    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "ROC-AUC": auc,
    }


# ===============================
# MODEL COMPARISON TABLE
# ===============================


results_df = pd.DataFrame(results).T


print("\n======================")

print("MODEL COMPARISON")

print("======================")


print(results_df)




# ===============================
# SELECT BEST MODEL
# F1 SCORE RULE
# ===============================


best_model_name = results_df["F1"].idxmax()


print("\nBest Model:", best_model_name)


best_model = models[best_model_name]


# ===============================
# SAVE ONLY WINNER
# ===============================


joblib.dump(best_model, f"{MODEL_DIR}/student_success_model.joblib")


print("\nBest model saved")


# ===============================
# FEATURE IMPORTANCE
# RANDOM FOREST ONLY
# ===============================


rf = models["random_forest"]


importance = pd.DataFrame({"Feature": FEATURES, "Importance": rf.feature_importances_})


importance = importance.sort_values(by="Importance", ascending=False)


print("\nFeature Importance")


print(importance)


importance.to_csv(f"{MODEL_DIR}/feature_importance.csv", index=False)


# ===============================
# SANITY CHECKS
# ===============================


print("\n======================")

print("SANITY CHECKS")

print("======================")


loaded_model = joblib.load(f"{MODEL_DIR}/student_success_model.joblib")


samples = X_test.head(3)


for index, row in samples.iterrows():

    prediction = loaded_model.predict([row])[0]

    probability = loaded_model.predict_proba([row])[0][1]

    print("\nINPUT")

    print(row)

    print("Prediction:", "Completed" if prediction == 1 else "Not Completed")

    print("Probability:", round(probability, 3))


print("\nTraining completed successfully")
