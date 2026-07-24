import os
import joblib
import pandas as pd

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# =========================
# APP
# =========================

app = FastAPI(title="Student Success Classifier API", version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# PATHS
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


MODEL_DIR = os.path.join(BASE_DIR, "../models")


# =========================
# LOAD MODELS
# =========================

MODELS = {
    "lr": joblib.load(os.path.join(MODEL_DIR, "logistic_regression.joblib")),
    "rf": joblib.load(os.path.join(MODEL_DIR, "random_forest.joblib")),
}


# =========================
# FEATURES
# =========================

FEATURES = joblib.load(os.path.join(MODEL_DIR, "classification_features.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "student_scaler.pkl"))


# =========================
# CLUSTER MODELS
# =========================

CLUSTER_MODEL = joblib.load(os.path.join(MODEL_DIR, "student_cluster_model.pkl"))


CLUSTER_SCALER = joblib.load(os.path.join(MODEL_DIR, "student_scaler.pkl"))


CLUSTER_FEATURES = joblib.load(os.path.join(MODEL_DIR, "cluster_features.pkl"))


CLUSTER_PROFILES = pd.read_csv(os.path.join(MODEL_DIR, "cluster_profiles.csv"))


# =========================
# HOME
# =========================


@app.get("/")
def home():

    return {
        "message": "Student Success Classifier API",
        "models": ["lr", "rf"],
        "endpoint": "POST /predict?model=rf",
    }


# =========================
# PREDICT
# =========================


@app.post("/predict")
async def predict(request: Request):

    # choose model

    choice = request.query_params.get("model", "rf").lower()

    if choice not in MODELS:

        return JSONResponse(
            status_code=400, content={"error": "Use model=lr or model=rf"}
        )

    model = MODELS[choice]

    # safely read json

    try:

        data = await request.json()

    except:

        return JSONResponse(status_code=400, content={"error": "Invalid JSON body"})

    # check features

    missing = [feature for feature in FEATURES if feature not in data]

    if missing:

        return JSONResponse(status_code=400, content={"missing": missing})

    try:

        # dataframe

        x = pd.DataFrame([data])

        # same order as training

        x = x[FEATURES]

        # prediction

        pred = int(model.predict(x)[0])

        label = "Completed" if pred == 1 else "Not Completed"

        response = {
            "model": ("logistic_regression" if choice == "lr" else "random_forest"),
            "prediction": pred,
            "label": label,
        }

        # confidence

        if hasattr(model, "predict_proba"):

            probs = model.predict_proba(x)[0]

            response["confidence"] = round(float(probs[pred]), 3)

        return response

    except Exception as e:

        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/cluster")
async def cluster(request: Request):

    try:

        data = await request.json()

        missing = [f for f in CLUSTER_FEATURES if f not in data]

        if missing:

            return JSONResponse(status_code=400, content={"missing": missing})

        x = pd.DataFrame([data])

        x = x[CLUSTER_FEATURES]

        x_scaled = CLUSTER_SCALER.transform(x)

        cluster_id = int(CLUSTER_MODEL.predict(x_scaled)[0])

        profile = CLUSTER_PROFILES[CLUSTER_PROFILES["Cluster"] == cluster_id]

        return {"cluster": cluster_id, "profile": profile.to_dict(orient="records")}

    except Exception as e:

        return JSONResponse(status_code=500, content={"error": str(e)})
print(FEATURES)