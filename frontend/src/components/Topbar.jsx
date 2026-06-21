function Topbar() {
  return (
    <div className="h-12 flex items-center px-6 gap-4" style={{background: "#0f172a", borderBottom: "1px solid #1e293b"}}>
      <span className="text-sm font-medium text-white flex-1">
        Live social graph monitor
      </span>
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
        <span className="text-xs text-red-400 font-medium">Live</span>
      </div>
    </div>
  )
}

export default Topbar