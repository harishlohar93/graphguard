function StatCard({ label, value, color = "text-white" }) {
  return (
    <div className="px-4 py-3" style={{background: "#0f172a", borderRight: "1px solid #1e293b"}}>
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      <p className={`text-2xl font-medium ${color}`}>{value}</p>
    </div>
  )
}

export default StatCard