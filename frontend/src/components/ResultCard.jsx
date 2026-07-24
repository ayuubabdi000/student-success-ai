import "./ResultCard.css";

function ResultCard({result}){

    return(

        <div className="result">

            <h3>
                Prediction Result
            </h3>


            <div className="result-item">

                <span>Label</span>

                <strong>
                    {result.label}
                </strong>

            </div>


            <div className="result-item">

                <span>Confidence</span>

                <strong>
                    {result.confidence}
                </strong>

            </div>


            <div className="result-item">

                <span>Model</span>

                <strong>
                    {result.model}
                </strong>

            </div>


        </div>

    );

}

export default ResultCard;