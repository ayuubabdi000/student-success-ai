import { useState, useRef } from "react";
import { predictionFeatures, randomStudent } from "./features";
import { predict } from "./services/api";
import ResultCard from "./ResultCard";
import "./PredictionForm.css";

function PredictionForm() {


    const initial = {};


    predictionFeatures.forEach(
        feature => initial[feature] = ""
    );



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
                predictionFeatures[index + 1]
                ];

            if (next) {

                next.focus();

            }
            else {

                submit();

            }

        }

    };
    const fillRandom = () => {

        setForm(randomStudent);

    };

    const submit = async () => {


        const missing = predictionFeatures.filter(
            feature => form[feature] === ""
        );


        if (missing.length > 0) {


            setMissingFields(missing);


            inputRefs.current[missing[0]].focus();


            return;

        }



        setMissingFields([]);



        try {


            setLoading(true);



            const payload = {};



            for (const key in form) {


                payload[key] = Number(form[key]);


            }



            const res = await predict(payload);



            setResult(res.data);



        } catch (error) {


            console.log(error);


        }
        finally {


            setLoading(false);


        }


    };
    const clearForm = () => {

        const emptyForm = {};

        predictionFeatures.forEach(feature => {
            emptyForm[feature] = "";
        });

        setForm(emptyForm);
        setResult(null);
        setMissingFields([]);

    };




    return (

        <div className="section">



            <div className="card">


                <h2>
                    Student Success Prediction
                </h2>



                {
                    predictionFeatures.map(feature => (


                        <input

                            key={feature}

                            ref={(el) =>
                                inputRefs.current[feature] = el
                            }

                            className={
                                missingFields.includes(feature)
                                    ?
                                    "input-error"
                                    :
                                    ""
                            }

                            placeholder={feature}

                            type="number"

                            value={form[feature]}

                            onKeyDown={(e) =>
                                handleEnter(
                                    e,
                                    predictionFeatures.indexOf(feature)
                                )
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
                            ?
                            "Predicting..."
                            :
                            "Predict"
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


                <h2>
                    Result
                </h2>



                {

                    result

                        ?

                        <ResultCard result={result} />


                        :

                        <p>
                            No prediction yet
                        </p>

                }



            </div>




        </div>

    );


}


export default PredictionForm;