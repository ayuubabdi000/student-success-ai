import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.API_URL ||"http://localhost:8000"
});

export const predict = (data) =>
    api.post("/predict", data);

export const cluster = (data) =>
    api.post("/cluster", data);

export default api;