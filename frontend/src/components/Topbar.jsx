function Topbar() {
  return (
    <div className="h-12  bg-white border-b border-gray-200 flex items-center px-6 gap-4">
      <span className="text-sm font-extrabold text-black flex-1">
        Live social graph monitor
      </span>
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
        <span className="text-xs text-red-800 font-medium">Live</span>
      </div>
    </div>
  )
}

export default Topbar