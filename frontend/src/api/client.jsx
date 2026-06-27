import axios from "axios"

const client = axios.create({
  bbaseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
})

export default client