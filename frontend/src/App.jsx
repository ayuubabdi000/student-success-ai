import { BrowserRouter, Routes, Route } from "react-router-dom";

import PredictionPage from "./pages/PredictionPage";
import ClusterPage from "./pages/ClusterPage";


export default function App(){

    return (

        <BrowserRouter>

            <Routes>

                <Route 
                    path="/" 
                    element={<PredictionPage />}
                />


                <Route 
                    path="/cluster" 
                    element={<ClusterPage />}
                />


            </Routes>

        </BrowserRouter>

    );

}