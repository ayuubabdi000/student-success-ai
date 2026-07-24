import { useState } from "react";
import { predictionFeatures } from "./features";
import { predict } from "./services/api";
import ResultCard from "./ResultCard";
import './PredictionForm.css'

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

        <div className="section">


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
                    predictionFeatures.map(feature =>

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

            </div>


            <div className="card result-area">

                <h2>Student Result</h2>

                {
                    result 
                    ? <ResultCard result={result}/>
                    : <p>No prediction yet</p>
                }

            </div>


        </div>

    );

}

export default PredictionForm;
