import os
import joblib
import pandas as pd


from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ===============================
# CONFIG
# ===============================

DATA_PATH = "../dataset/clean_Student.csv"

MODEL_DIR = "../models"

RANDOM_STATE = 42



os.makedirs(
    MODEL_DIR,
    exist_ok=True
)



# ===============================
# LOAD DATA
# ===============================

df = pd.read_csv(DATA_PATH)


print("Dataset shape:", df.shape)



# ===============================
# SPLIT FEATURES / TARGET
# ===============================


X = df.drop(
    columns=["Completed"]
)


y = df["Completed"]



# Save feature order for API

FEATURES = X.columns.tolist()


joblib.dump(
    FEATURES,
    f"{MODEL_DIR}/classification_features.pkl"
)



# ===============================
# TRAIN TEST SPLIT
# ===============================


X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=RANDOM_STATE,

    stratify=y

)



print("\nTrain:", X_train.shape)
print("Test :", X_test.shape)



# ===============================
# MODELS
# ===============================


models = {


    "logistic_regression":

    LogisticRegression(

        max_iter=3000,

        random_state=RANDOM_STATE

    ),



    "random_forest":

    RandomForestClassifier(

        n_estimators=100,

        random_state=RANDOM_STATE,

        n_jobs=-1

    )

}



# ===============================
# TRAIN + EVALUATE
# ===============================


for name, model in models.items():


    print("\n====================")

    print(name)

    print("====================")


    model.fit(
        X_train,
        y_train
    )


    predictions = model.predict(
        X_test
    )


    probabilities = model.predict_proba(
        X_test
    )[:,1]



    print(
        "Accuracy:",
        round(
            accuracy_score(
                y_test,
                predictions
            ),
            3
        )
    )


    print(
        "Precision:",
        round(
            precision_score(
                y_test,
                predictions
            ),
            3
        )
    )


    print(
        "Recall:",
        round(
            recall_score(
                y_test,
                predictions
            ),
            3
        )
    )


    print(
        "F1:",
        round(
            f1_score(
                y_test,
                predictions
            ),
            3
        )
    )


    print(
        "ROC-AUC:",
        round(
            roc_auc_score(
                y_test,
                probabilities
            ),
            3
        )
    )



    print("\nConfusion Matrix")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )


    print(
        classification_report(
            y_test,
            predictions
        )
    )



    # ===============================
    # SAVE MODEL
    # ===============================


    joblib.dump(

        model,

        f"{MODEL_DIR}/{name}.joblib"

    )


print("\nModels saved successfully")



# ===============================
# RANDOM FOREST IMPORTANCE
# ===============================


rf = models["random_forest"]


importance = pd.DataFrame({

    "Feature": FEATURES,

    "Importance":
    rf.feature_importances_

})


importance = importance.sort_values(

    by="Importance",

    ascending=False

)



print("\nFeature Importance")

print(
    importance
)



importance.to_csv(

    f"{MODEL_DIR}/feature_importance.csv",

    index=False

)