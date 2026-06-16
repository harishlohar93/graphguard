function StatCard({ label, value, color = "text-gray-900" }) {
  return (
    <div className=" bg-white px-4 py-3 border-r border-gray-200 last:border-r-0">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className={`text-2xl font-medium ${color}`}>{value}</p>
    </div>
  )
}

export default StatCard