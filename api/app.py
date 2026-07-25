import os
import joblib
import pandas as pd


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# =========================
# APP
# =========================

app = FastAPI(title="Student Success Prediction API", version="1.0")


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
# LOAD CLASSIFICATION MODEL
# =========================


MODEL_PATH = os.path.join(MODEL_DIR, "student_success_model.joblib")


MODEL = joblib.load(MODEL_PATH)


FEATURES = joblib.load(os.path.join(MODEL_DIR, "classification_features.pkl"))


# =========================
# LOAD CLUSTER MODEL
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
        "message": "Student Success Prediction API",
        "model": "best_model",
        "endpoints": ["/predict", "/cluster"],
    }


# =========================
# CLASSIFICATION
# =========================


@app.post("/predict")
async def predict(request: Request):

    try:

        data = await request.json()

    except:

        return JSONResponse(status_code=400, content={"error": "Invalid JSON"})

    # Check features

    missing = [f for f in FEATURES if f not in data]

    if missing:

        return JSONResponse(status_code=400, content={"missing_features": missing})

    try:

        x = pd.DataFrame([data])


        x = x[FEATURES]

        prediction = int(MODEL.predict(x)[0])

        label = "Completed" if prediction == 1 else "Not Completed"

        response = {"prediction": prediction, "label": label}

        if hasattr(MODEL, "predict_proba"):

            probability = MODEL.predict_proba(x)[0]

            response["confidence"] = round(float(probability[prediction]), 3)

        return response

    except Exception as e:

        return JSONResponse(status_code=500, content={"error": str(e)})


# =========================
# CLUSTERING
# =========================


@app.post("/cluster")
async def cluster(request: Request):

    try:

        data = await request.json()

        missing = [f for f in CLUSTER_FEATURES if f not in data]

        if missing:

            return JSONResponse(status_code=400, content={"missing_features": missing})

        x = pd.DataFrame([data])

        x = x[CLUSTER_FEATURES]

        x_scaled = CLUSTER_SCALER.transform(x)

        cluster_id = int(CLUSTER_MODEL.predict(x_scaled)[0])

        profile = CLUSTER_PROFILES[CLUSTER_PROFILES["Cluster"] == cluster_id]

        return {"cluster": cluster_id, "profile": profile.to_dict(orient="records")}

    except Exception as e:

        return JSONResponse(status_code=500, content={"error": str(e)})




print("Classification Features:", FEATURES)
