import Sidebar from "./Sidebar"
import Topbar from "./Topbar"

function Layout({ children }) {
  return (
    <div className=" bg-cyan-900 flex h-screen overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Topbar />
        <main className="flex-1 overflow-hidden">
          {children}
        </main>
      </div>
    </div>
  )
}

export default Layout