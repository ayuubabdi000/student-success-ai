# Student Success Prediction System - React UI

## Project Structure

```text
student-success-ui/
│
├── src/
│   ├── components/
│   │   ├── StudentForm.jsx
│   │   ├── ResultCard.jsx
│   │   ├── FeatureInput.jsx
│   │   └── LoadingSpinner.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
│
├── public/
│
├── package.json
│
└── vite.config.js
```

---

# Step 1 Install React

```bash
npm create vite@latest student-success-ui -- --template react

cd student-success-ui

npm install

npm install axios
```

---

# Step 2 Create API Service

**File**

```text
src/services/api.js
```

```javascript
import axios from "axios";

const api = axios.create({

    baseURL: "http://localhost:8000"

});

export default api;
```

---

# Step 3 App Component

**File**

```text
src/App.jsx
```

```jsx
import StudentForm from "./components/StudentForm";

import "./App.css";

function App() {

    return (

        <div className="container">

            <h1>

                Student Success Prediction

            </h1>

            <StudentForm/>

        </div>

    );

}

export default App;
```

---

# Step 4 StudentForm Component

**File**

```text
src/components/StudentForm.jsx
```

Responsibilities

- Display all input fields
- Store user input
- Send data to FastAPI
- Display results

Flow

```text
User Types Data

↓

React State

↓

Axios POST Request

↓

FastAPI

↓

Prediction

↓

Display Result
```

---

# Step 5 FeatureInput Component

Instead of writing 20 inputs manually, create one reusable component.

**File**

```text
src/components/FeatureInput.jsx
```

Props

```text
label

name

value

onChange
```

This component creates

```text
Label

[ Number Input ]
```

---

# Step 6 ResultCard Component

**File**

```text
src/components/ResultCard.jsx
```

Displays

```text
Prediction

Probability

Student Cluster
```

Example

```text
Prediction

Completed

Probability

92%

Student Cluster

Cluster 3
```

---

# Step 7 Loading Spinner

**File**

```text
src/components/LoadingSpinner.jsx
```

Show while waiting for FastAPI.

```
Loading...

⏳
```

---

# Step 8 React State

```javascript
const [form,setForm]=useState({});
```

Stores every feature.

Example

```javascript
{

Login_Frequency:20,

Average_Session_Duration_Min:35,

Video_Completion_Rate:85

}
```

---

# Step 9 Model Selection

Allow users to choose a model.

```
Select Model

▼ Random Forest

▼ Logistic Regression
```

React State

```javascript
const [model,setModel]=useState("random_forest");
```

---

# Step 10 Submit Button

```
+----------------------+

Analyze Student

+----------------------+
```

On click

```
Collect Form

↓

POST

↓

FastAPI

↓

Receive Response

↓

Show Result
```

---

# Step 11 API Request

Endpoint

```text
POST /analyze
```

Body

```json
{
    "Login_Frequency":20,
    "Average_Session_Duration_Min":30,
    "Video_Completion_Rate":90,
    "...":"..."
}
```

Response

```json
{
    "prediction":1,
    "probability":0.92,
    "cluster":3
}
```

---

# Step 12 Result Card

Display

```
Prediction

Completed

Probability

92%

Student Cluster

3
```

---

# Step 13 UI Layout

```text
+----------------------------------------------------+

Student Success Prediction

+----------------------------------------------------+

Model

▼ Random Forest

----------------------------------------------

Student Engagement

Login Frequency

[________]

Average Session Duration

[________]

Video Completion Rate

[________]

Discussion Participation

[________]

----------------------------------------------

Assignments

Assignments Submitted

[________]

Assignments Missed

[________]

Quiz Attempts

[________]

Quiz Score

[________]

----------------------------------------------

Activity

Time Spent

[________]

Notifications Checked

[________]

Peer Interaction

[________]

Rewatch Count

[________]

----------------------------------------------

Learning Metrics

Learning Engagement

[________]

Learning Efficiency

[________]

Assignment Discipline

[________]

Inactivity Risk

[________]

----------------------------------------------

Analyze Student

----------------------------------------------

Prediction

Completed

Probability

91%

Student Cluster

Cluster 3

+----------------------------------------------------+
```

---

# Step 14 Component Tree

```text
App

│

└── StudentForm

      │

      ├── FeatureInput

      ├── FeatureInput

      ├── FeatureInput

      ├── FeatureInput

      ├── FeatureInput

      ├── LoadingSpinner

      └── ResultCard
```

---

# Step 15 React → FastAPI Flow

```text
React UI

↓

Axios

↓

POST /analyze

↓

FastAPI

↓

Random Forest

↓

KMeans

↓

JSON Response

↓

React

↓

Result Card
```

---

# Step 16 Final Features

- ✅ Responsive Design
- ✅ Model Selection
- ✅ Automatic Feature Inputs
- ✅ Loading Spinner
- ✅ Error Messages
- ✅ Prediction Probability
- ✅ Student Cluster
- ✅ Clean Dashboard
- ✅ Easy React Components
- ✅ Connects to FastAPI with Axios

---

# Step 17 Future Improvements

- Add Charts (Chart.js)
- Cluster Description Cards
- Feature Importance Visualization
- Prediction History
- Export Results to PDF
- Dark/Light Mode
- Student Profile Summary
- Batch CSV Prediction
- Authentication (Login)
- MongoDB Result Storage