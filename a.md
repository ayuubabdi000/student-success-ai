# Student Success Classifier API
## FastAPI Deployment Guide

This project deploys trained machine learning models using FastAPI.

The API supports:

- Logistic Regression
- Random Forest
- Student completion prediction
- Prediction confidence
- React frontend integration

---

# Project Structure

```
Student_Project/

│
├── api/
│   │
│   └── main.py
│
├── models/
│   │
│   ├── logistic_regression.pkl
│   ├── random_forest.pkl
│   ├── classification_features.pkl
│   ├── student_cluster_model.pkl
│   ├── student_scaler.pkl
│   └── cluster_features.pkl
│
├── dataset/
│   │
│   └── clean_Student.csv
│
├── training/
│   │
│   ├── train_classification.py
│   └── train_clustering.py
│
└── requirements.txt
```

---

# Installation

Install required packages:

```bash
pip install fastapi uvicorn pandas joblib scikit-learn
```

---

# Model Files

Before starting the API, make sure these files exist:

```
models/

├── logistic_regression.pkl
├── random_forest.pkl
└── classification_features.pkl
```

The API loads these files automatically.

---

# FastAPI Application

Create:

```
api/main.py
```

---

# Import Libraries

```python
import os
import joblib
import pandas as pd


from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
```

---

# Create FastAPI App

```python
app = FastAPI(

    title="Student Success Classifier API",

    version="1.0"

)
```

---

# Enable CORS

Allows React frontend to communicate with FastAPI.

```python
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)
```

---

# Model Configuration

```python
MODEL_DIR = "../models"
```

---

# Load Models

```python
MODELS = {


    "lr":

    joblib.load(

        os.path.join(

            MODEL_DIR,

            "logistic_regression.pkl"

        )

    ),



    "rf":

    joblib.load(

        os.path.join(

            MODEL_DIR,

            "random_forest.pkl"

        )

    )

}
```

---

# Load Feature Names

The model must receive features in the same order used during training.

```python
FEATURES = joblib.load(

    os.path.join(

        MODEL_DIR,

        "classification_features.pkl"

    )

)
```

---

# Home Endpoint

Test if the API is running.

## Request

```
GET /
```

## Code

```python
@app.get("/")
def home():

    return {

        "message":

        "Student Success Classifier API",


        "endpoints": {


            "POST /predict?model=lr|rf":

            {


                "expects_json":

                {

                    feature:"number"

                    for feature in FEATURES

                }


            }


        }

    }
```

---

# Prediction Endpoint

## URL

```
POST /predict?model=lr
```

or

```
POST /predict?model=rf
```

---

# Complete Prediction Function

```python
@app.post("/predict")
async def predict(request: Request):


    # Select model

    choice = request.query_params.get(

        "model",

        "rf"

    ).lower()



    if choice not in MODELS:


        return JSONResponse(

            status_code=400,

            content={

                "error":

                "Unknown model. Use model=lr or model=rf"

            }

        )



    model = MODELS[choice]



    # Read JSON body

    data = await request.json()



    # Check missing fields

    missing = [

        feature

        for feature in FEATURES

        if feature not in data

    ]



    if missing:


        return JSONResponse(

            status_code=400,

            content={

                "error":

                f"Missing fields: {missing}"

            }

        )



    try:


        # Convert input to dataframe

        x_new = pd.DataFrame(

            [data]

        )



        # Same order as training

        x_new = x_new[FEATURES]



        # Prediction

        prediction = int(

            model.predict(

                x_new

            )[0]

        )



        # Convert result to label

        label = (

            "Completed"

            if prediction == 1

            else

            "Not Completed"

        )



        response = {


            "model":

            (

                "logistic_regression"

                if choice == "lr"

                else

                "random_forest"

            ),



            "input":

            data,



            "prediction":

            prediction,



            "label":

            label

        }



        # Confidence

        if hasattr(

            model,

            "predict_proba"

        ):


            probabilities = model.predict_proba(

                x_new

            )[0]



            response["confidence"] = round(

                float(

                    probabilities[prediction]

                ),

                3

            )



        return response



    except Exception as e:


        return JSONResponse(

            status_code=500,

            content={

                "error":

                f"Prediction failed: {str(e)}"

            }

        )
```

---

# Running the API

Move into API folder:

```bash
cd api
```

Start server:

```bash
uvicorn main:app --reload
```

Output:

```
INFO: Application startup complete.
```

---

# API Documentation

FastAPI automatically creates Swagger UI.

Open:

```
http://127.0.0.1:8000/docs
```

---

# Testing API

## Random Forest Prediction

Request:

```
POST

http://127.0.0.1:8000/predict?model=rf
```

---

## Logistic Regression Prediction

Request:

```
POST

http://127.0.0.1:8000/predict?model=lr
```

---

# Example JSON Input

```json
{
    "Login_Frequency":20,
    "Average_Session_Duration_Min":45,
    "Video_Completion_Rate":80,
    "Discussion_Participation":5,
    "Time_Spent_Hours":30,
    "Days_Since_Last_Login":2,
    "Notifications_Checked":20,
    "Peer_Interaction_Score":70,
    "Assignments_Submitted":8,
    "Assignments_Missed":1,
    "Quiz_Attempts":10,
    "Quiz_Score_Avg":80,
    "Project_Grade":85,
    "Rewatch_Count":3,
    "App_Usage_Percentage":90,
    "Reminder_Emails_Clicked":5,
    "Assignment_Discipline":0.9,
    "Learning_Engagement":0.8,
    "Learning_Efficiency":0.85,
    "Inactivity_Risk":0.1
}
```

---

# Example Response

```json
{
    "model":"random_forest",

    "input":{

        "Login_Frequency":20

    },

    "prediction":1,

    "label":"Completed",

    "confidence":0.87
}
```

---

# Response Explanation

| Field | Meaning |
|-|-|
| model | Model used for prediction |
| input | User data sent to API |
| prediction | 0 or 1 result |
| label | Human readable result |
| confidence | Model probability |

---

# React Frontend Request Example

```javascript
fetch(
"http://127.0.0.1:8000/predict?model=rf",
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(studentData)

})
.then(res=>res.json())
.then(data=>console.log(data))
```

---

# API Architecture

```
React Frontend

       |

       |

       ▼

FastAPI

       |

       |

       ├─────────────── Logistic Regression

       |

       └─────────────── Random Forest


       |

       ▼

Prediction JSON

```

---

# Future Endpoints

The same API structure can be extended with:

```
POST /cluster

POST /analyze

GET /feature-importance

GET /cluster-profile
```

for:

- Student clustering
- Complete student analysis
- Feature importance visualization
- Dashboard integration