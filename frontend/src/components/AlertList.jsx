function getBadgeStyle(label) {
  if (label === "bot") return "background:#ef444420;color:#f87171;border:1px solid #ef4444"
  if (label === "suspect") return "background:#f59e0b20;color:#fbbf24;border:1px solid #f59e0b"
  return "background:#22c55e20;color:#4ade80;border:1px solid #22c55e"
}

function AlertList({ alerts }) {
  return (
    <div className="w-64 shrink-0 flex flex-col overflow-hidden" style={{background: "#0f172a", borderLeft: "1px solid #1e293b"}}>
      <div className="px-3 py-2 text-xs font-medium text-slate-400" style={{borderBottom: "1px solid #1e293b"}}>
        Alerts
      </div>
      <div className="flex-1 overflow-y-auto">
        {alerts.map((alert) => (
          <div key={alert.id} className="px-3 py-2 hover:bg-slate-800 cursor-pointer" style={{borderBottom: "1px solid #1e293b"}}>
            <div className="flex justify-between items-center mb-1">
              <span className="text-xs font-mono text-slate-300">
                {alert.account}
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full font-medium" style={Object.fromEntries(getBadgeStyle(alert.label).split(";").map(s => s.split(":")))}>
                {alert.label}
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Score: {alert.score?.toFixed(2)} · {alert.status}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default AlertList