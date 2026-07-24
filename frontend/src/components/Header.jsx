import { NavLink } from "react-router-dom";
import "./Header.css";


function Header(){

    return (

        <header>

            <div>

                <h1>
                    Student Success AI
                </h1>

                <p>
                    Predict student outcomes and discover learning patterns
                </p>

            </div>


            <nav>

                <NavLink to="/">
                    Prediction
                </NavLink>


                <NavLink to="/cluster">
                    Cluster Analysis
                </NavLink>

            </nav>


        </header>

    );

}


export default Header;