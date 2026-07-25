import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
});

export const predict = (data) =>
    api.post("/predict", data);

export const cluster = (data) =>
    api.post("/cluster", data);


export default api;