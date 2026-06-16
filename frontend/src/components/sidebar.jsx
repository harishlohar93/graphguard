import { Link } from "react-router-dom"

function Sidebar() {
  return (
    <div className="w-48 min-h-screen  bg-white border-r border-gray-200 flex flex-col py-4">
      <div className="flex items-center gap-2 px-4 mb-6">
        <div className="w-3 h-3 rounded-full bg-red-500"></div>
        <span className="text-sm font-extrabold text-gray-900">GraphGuard</span>
      </div>
      <nav className="flex flex-col gap-1 px-2">
        <Link to="/" className="px-3 py-2 text-sm text-gray-700 rounded-lg hover:bg-gray-300">
          Live Graph
        </Link>
        <Link to="/alerts" className="px-3 py-2 text-sm text-gray-700 rounded-lg hover:bg-gray-300">
          Alerts
        </Link>
        <Link to="/clusters" className="px-3 py-2 text-sm text-gray-700 rounded-lg hover:bg-gray-300">
          Clusters
        </Link>
      </nav>
    </div>
  )
}

export default Sidebar