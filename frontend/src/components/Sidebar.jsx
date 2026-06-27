import { Link } from "react-router-dom"

function Sidebar() {
  return (
    <div className="w-48 min-h-screen flex flex-col py-4" style={{background: "#0f172a", borderRight: "1px solid #1e293b"}}>
      <div className="flex items-center gap-2 px-4 mb-6">
        <div className="w-3 h-3 rounded-full bg-red-500"></div>
        <span className="text-sm font-medium text-white">GraphGuard</span>
      </div>
      <nav className="flex flex-col gap-1 px-2">
        <a href="/" className="px-3 py-2 text-sm text-slate-300 rounded-lg hover:bg-slate-800">Live Graph</a>
        <a href="/alerts" className="px-3 py-2 text-sm text-slate-300 rounded-lg hover:bg-slate-800">Alerts</a>
        <a href="/clusters" className="px-3 py-2 text-sm text-slate-300 rounded-lg hover:bg-slate-800">Clusters</a>
      </nav>
    </div>
  )
}

export default Sidebar