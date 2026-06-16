function getBadgeStyle(label) {
  if (label === "bot") return "bg-red-100 text-red-700"
  if (label === "suspect") return "bg-amber-100 text-amber-700"
  return "bg-green-100 text-green-700"
}

function AlertList({ alerts }) {
  return (
    <div className="w-64 shrink-0 border-l border-gray-200  bg-white flex flex-col overflow-hidden">
      <div className="px-3 py-2 border-b border-gray-200 text-xs font-medium text-gray-600">
        Alerts
      </div>
      <div className="flex-1 overflow-y-auto">
        {alerts.map((alert) => (
          <div key={alert.id} className="px-3 py-2 border-b border-gray-100 hover:bg-gray-50">
            <div className="flex justify-between items-center mb-1">
              <span className="text-xs font-mono font-medium">
                {alert.account}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getBadgeStyle(alert.label)}`}>
                {alert.label}
              </span>
            </div>
            <p className="text-xs text-gray-400">
              Score: {alert.score?.toFixed(2)} · {alert.status}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default AlertList