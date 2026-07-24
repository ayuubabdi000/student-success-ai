import { useState } from "react";
import { clusterFeatures } from "./features";
import { cluster } from "./services/api";
import "./PredictionForm.css";

function ClusterForm() {

    const init = {};

    clusterFeatures.forEach(f => init[f] = "");

    const [form, setForm] = useState(init);

    const [result, setResult] = useState(null);


    const submit = async () => {

        const payload = {};

        for (const k in form)
            payload[k] = Number(form[k]);


        const res = await cluster(payload);

        setResult(res.data);

    };


    return (

        <div className="section">


            {/* Cluster Input Form */}

            <div className="card">

                <h2>Cluster Analysis</h2>


                {
                    clusterFeatures.map(feature =>

                        <input

                            key={feature}

                            type="number"

                            placeholder={feature}

                            value={form[feature]}

                            onChange={(e)=>

                                setForm({

                                    ...form,

                                    [feature]: e.target.value

                                })

                            }

                        />

                    )
                }


                <button onClick={submit}>

                    Analyze Cluster

                </button>


            </div>



            {/* Cluster Result */}

            <div className="card result-area">

                <h2>Student Result</h2>


                {

                    result ?

                    <div className="result">

                        <h3>
                            Cluster {result.cluster}
                        </h3>


                        {

                        result.cluster === 0 ?

                        <p>
                            Student is in Low Engagement Group
                        </p>

                        :

                        result.cluster === 1 ?

                        <p>
                            Student is in Active Learning Group
                        </p>

                        :

                        <p>
                            Student belongs to Cluster {result.cluster}
                        </p>

                        }


                    </div>

                    :

                    <p>
                        No cluster analysis yet
                    </p>

                }


            </div>


        </div>

    );

}

export default ClusterForm;