import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000"
});

export const predict = (model, data) =>
    api.post(`/predict?model=${model}`, data);

export const cluster = (data) =>
    api.post("/cluster", data);

export default api;
