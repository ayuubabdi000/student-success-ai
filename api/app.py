import os
import joblib
import pandas as pd
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import create_model

# =========================
# APP INITIALIZATION
# =========================

app = FastAPI(title="Student Success Prediction API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://student-success-ai-71cy-.*-ayub8\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# PATHS & ARTIFACT LOADING
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load Classification Artifacts
MODEL_PATH = os.path.join(MODEL_DIR, "student_success_model.joblib")
MODEL = joblib.load(MODEL_PATH)
FEATURES: List[str] = joblib.load(
    os.path.join(MODEL_DIR, "classification_features.pkl")
)

# Load Cluster Artifacts
CLUSTER_MODEL = joblib.load(os.path.join(MODEL_DIR, "student_cluster_model.pkl"))
CLUSTER_SCALER = joblib.load(os.path.join(MODEL_DIR, "student_scaler.pkl"))
CLUSTER_FEATURES: List[str] = joblib.load(
    os.path.join(MODEL_DIR, "cluster_features.pkl")
)
CLUSTER_PROFILES = pd.read_csv(os.path.join(MODEL_DIR, "cluster_profiles.csv"))
CLUSTER_NAMES = {
    0: "Excellent Student",
    1: "At Risk Student",
    2: "Average Student",
    3: "Active Student",
    4: "Low Engagement Student",
}
print("Classification Features Loaded:", len(FEATURES))
print("Cluster Features Loaded:", len(CLUSTER_FEATURES))

# =========================
# DYNAMIC PYDANTIC MODELS
# =========================
# This dynamically generates request bodies based on your pkl feature lists
PredictRequest = create_model(
    "PredictRequest", **{feat: (Any, ...) for feat in FEATURES}
)

ClusterRequest = create_model(
    "ClusterRequest", **{feat: (Any, ...) for feat in CLUSTER_FEATURES}
)

# =========================
# ENDPOINTS
# =========================


@app.get("/")
def home():
    return {
        "message": "Student Success Prediction API",
        "model": "best_model",
        "endpoints": ["/api/predict", "/api/cluster"],
    }


@app.post("/api/predict")
async def predict(payload: PredictRequest):
    try:
        # Convert Pydantic model to DataFrame using specified feature order
        data_dict = payload.model_dump()
        x = pd.DataFrame([data_dict])[FEATURES]

        prediction = int(MODEL.predict(x)[0])
        label = "Completed" if prediction == 1 else "Not Completed"

        response: Dict[str, Any] = {"prediction": prediction, "label": label}

        if hasattr(MODEL, "predict_proba"):
            probability = MODEL.predict_proba(x)[0]
            response["confidence"] = round(float(probability[prediction]), 3)

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/api/cluster")
async def cluster(payload: ClusterRequest):
    try:
        data_dict = payload.model_dump()
        x = pd.DataFrame([data_dict])[CLUSTER_FEATURES]

        x_scaled = CLUSTER_SCALER.transform(x)
        cluster_id = int(CLUSTER_MODEL.predict(x_scaled)[0])

        profile = CLUSTER_PROFILES[CLUSTER_PROFILES["Cluster"] == cluster_id]

        return {
            "cluster": cluster_id,
            "student_type": CLUSTER_NAMES[cluster_id],
            "profile": profile.to_dict(orient="records"),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
