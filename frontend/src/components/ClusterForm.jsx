import { useState, useRef } from "react";
import { clusterFeatures, randomStudent } from "./features";
import { cluster } from "../components/services/api";
import "./PredictionForm.css";

function ClusterForm() {

    const initial = {};

    clusterFeatures.forEach(feature => {
        initial[feature] = "";
    });

    const [form, setForm] = useState(initial);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [missingFields, setMissingFields] = useState([]);


    const inputRefs = useRef({});
    const handleEnter = (e, index) => {

        if (e.key === "Enter") {

            e.preventDefault();

            const next =
                inputRefs.current[
                clusterFeatures[index + 1]
                ];

            if (next) {
                next.focus();
            } else {
                submit();
            }
        }
    };
    const fillRandom = () => {

        setForm(randomStudent);

    };


    const submit = async () => {

        const missing = clusterFeatures.filter(
            feature => form[feature] === ""
        );

        if (missing.length > 0) {

            setMissingFields(missing);

            inputRefs.current[missing[0]]?.focus();

            return;
        }

        setMissingFields([]);

        try {

            setLoading(true);

            const payload = {};

            for (const key in form) {
                payload[key] = Number(form[key]);
            }

            const res = await cluster(payload);

            setResult(res.data);

        } catch (error) {

            console.error(error);

            alert("Failed to analyze cluster.");

        } finally {

            setLoading(false);

        }
    };
    const clearForm = () => {

        const emptyForm = {};

        clusterFeatures.forEach(feature => {
            emptyForm[feature] = "";
        });

        setForm(emptyForm);
        setResult(null);
        setMissingFields([]);

    };

    return (

        <div className="section">

            <div className="card">

                <h2>Student Cluster Type Analysis</h2>

                {
                    clusterFeatures.map((feature, index) => (

                        <input

                            key={feature}

                            ref={(el) =>
                                inputRefs.current[feature] = el
                            }

                            className={
                                missingFields.includes(feature)
                                    ? "input-error"
                                    : ""
                            }

                            type="number"

                            placeholder={feature}

                            value={form[feature]}

                            onKeyDown={(e) =>
                                handleEnter(e, index)
                            }

                            onChange={(e) => {

                                setForm({

                                    ...form,

                                    [feature]: e.target.value

                                });

                                setMissingFields(
                                    missingFields.filter(
                                        item => item !== feature
                                    )
                                );

                            }}

                        />

                    ))
                }

                <button

                    onClick={submit}

                    disabled={loading}

                >

                    {
                        loading
                            ? "Analyzing..."
                            : "Analyze Cluster"
                    }

                </button>
                <button onClick={fillRandom}>
                    Random Student
                </button>
                <button onClick={clearForm}>
                    Clear Form
                </button>

            </div>

            <div className="card result-area">

                <h2>Result</h2>

                {

                    result

                        ?

                        <div className="result">

                            <div className="result">

                                <h3>
                                    {result.student_type}
                                </h3>

                                <p>
                                    Cluster ID: {result.cluster}
                                </p>

                            </div>

                        </div>

                        :

                        <p>

                            No analysis yet

                        </p>

                }

            </div>

        </div>

    );

}

export default ClusterForm;



