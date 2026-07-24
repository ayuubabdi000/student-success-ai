# Student Success Classifier Frontend (React + Vite)

A simple frontend for your FastAPI API.

---

# Tech Stack

- React
- Vite
- Axios
- CSS

---

# Folder Structure

```text
student-success-frontend/
│
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── PredictionForm.jsx
│   │   ├── ClusterForm.jsx
│   │   ├── ResultCard.jsx
│   │   └── Loader.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── features.js
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
│
├── package.json
└── vite.config.js
```

---

# Install

```bash
npm create vite@latest student-success-frontend -- --template react

cd student-success-frontend

npm install

npm install axios
```

---

# API

Create

```text
src/services/api.js
```

```javascript
import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000"
});

export const predict = (model, data) =>
    api.post(`/predict?model=${model}`, data);

export const cluster = (data) =>
    api.post("/cluster", data);

export default api;
```

---

# Features

Create

```text
src/features.js
```

```javascript
export const predictionFeatures = [
    "Login_Frequency",
    "Average_Session_Duration_Min",
    "Video_Completion_Rate",
    "Discussion_Participation",
    "Time_Spent_Hours",
    "Days_Since_Last_Login",
    "Assignments_Submitted",
    "Assignments_Missed",
    "Quiz_Score_Avg",
    "Progress_Percentage"
];

export const clusterFeatures = predictionFeatures;
```

---

# App.jsx

```javascript
import Header from "./components/Header";
import PredictionForm from "./components/PredictionForm";
import ClusterForm from "./components/ClusterForm";
import "./App.css";

function App() {

  return (
    <div className="container">

      <Header />

      <PredictionForm />

      <ClusterForm />

    </div>
  );

}

export default App;
```

---

# Header.jsx

```javascript
function Header() {

    return (

        <header>

            <h1>Student Success Classifier</h1>

            <p>FastAPI + React Demo</p>

        </header>

    );

}

export default Header;
```

---

# PredictionForm.jsx

```javascript
import { useState } from "react";
import { predictionFeatures } from "../features";
import { predict } from "../services/api";
import ResultCard from "./ResultCard";

function PredictionForm() {

    const initial = {};

    predictionFeatures.forEach(f => initial[f] = "");

    const [form, setForm] = useState(initial);

    const [model, setModel] = useState("rf");

    const [result, setResult] = useState(null);

    const submit = async () => {

        const payload = {};

        for (const key in form)
            payload[key] = Number(form[key]);

        const res = await predict(model, payload);

        setResult(res.data);

    };

    return (

        <div className="card">

            <h2>Prediction</h2>

            <select
                value={model}
                onChange={(e)=>setModel(e.target.value)}
            >

                <option value="rf">
                    Random Forest
                </option>

                <option value="lr">
                    Logistic Regression
                </option>

            </select>

            {
                predictionFeatures.map(feature=>

                    <input

                        key={feature}

                        placeholder={feature}

                        type="number"

                        value={form[feature]}

                        onChange={(e)=>

                            setForm({

                                ...form,

                                [feature]:e.target.value

                            })

                        }

                    />

                )
            }

            <button onClick={submit}>

                Predict

            </button>

            {result && <ResultCard result={result}/>}

        </div>

    );

}

export default PredictionForm;
```

---

# ResultCard.jsx

```javascript
function ResultCard({result}){

    return(

        <div className="result">

            <h3>Prediction Result</h3>

            <p>

                Label:

                {result.label}

            </p>

            <p>

                Confidence:

                {result.confidence}

            </p>

            <p>

                Model:

                {result.model}

            </p>

        </div>

    );

}

export default ResultCard;
```

---

# ClusterForm.jsx

```javascript
import {useState} from "react";
import {clusterFeatures} from "../features";
import {cluster} from "../services/api";

function ClusterForm(){

    const init={};

    clusterFeatures.forEach(f=>init[f]="");

    const [form,setForm]=useState(init);

    const [result,setResult]=useState(null);

    const submit=async()=>{

        const payload={};

        for(const k in form)
            payload[k]=Number(form[k]);

        const res=await cluster(payload);

        setResult(res.data);

    };

    return(

        <div className="card">

            <h2>Cluster Analysis</h2>

            {
                clusterFeatures.map(feature=>

                    <input

                        key={feature}

                        type="number"

                        placeholder={feature}

                        value={form[feature]}

                        onChange={(e)=>

                            setForm({

                                ...form,

                                [feature]:e.target.value

                            })

                        }

                    />

                )
            }

            <button onClick={submit}>

                Analyze Cluster

            </button>

            {

                result &&

                <div className="result">

                    <h3>

                        Cluster {result.cluster}

                    </h3>

                    <pre>

                        {JSON.stringify(result.profile,null,2)}

                    </pre>

                </div>

            }

        </div>

    );

}

export default ClusterForm;
```

---

# App.css

```css
body{

    margin:0;

    font-family:Arial;

    background:#f5f5f5;

}

.container{

    width:900px;

    margin:auto;

    padding:30px;

}

.card{

    background:white;

    padding:20px;

    border-radius:10px;

    margin-bottom:30px;

    box-shadow:0 2px 10px rgba(0,0,0,.1);

}

input,
select{

    width:100%;

    margin:6px 0;

    padding:10px;

}

button{

    width:100%;

    padding:12px;

    background:#2563eb;

    color:white;

    border:none;

    cursor:pointer;

}

button:hover{

    background:#1d4ed8;

}

.result{

    margin-top:20px;

    background:#eef6ff;

    padding:15px;

}
```

---

# Run

```bash
npm run dev
```

---

# Backend

Run FastAPI

```bash
uvicorn main:app --reload
```

---

# API Endpoints Used

```http
GET /

POST /predict?model=rf

POST /predict?model=lr

POST /cluster
```

---

# Final UI

```text
------------------------------------------

Student Success Classifier

Prediction

Model
[Random Forest ▼]

Login Frequency
[________]

Average Session Duration
[________]

...

[ Predict ]

Prediction Result

Completed

Confidence : 0.93

------------------------------------------

Cluster Analysis

Login Frequency
[________]

...

[ Analyze Cluster ]

Cluster : 2

Profile:
Highly Engaged Students

------------------------------------------
```