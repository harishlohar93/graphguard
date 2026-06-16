import client from "./client"

export const getAccounts = () => client.get("/accounts/")
export const getAlerts = () => client.get("/alerts/")
export const getClusters = () => client.get("/clusters/")
export const getGraph = () => client.get("/graph/")
export const scoreAccount = (id) => client.post(`/score/${id}/`)
export const updateAlert = (id, data) => client.patch(`/alerts/${id}/`, data)