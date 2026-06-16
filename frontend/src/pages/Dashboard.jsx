import { useQuery } from "@tanstack/react-query"
import { getAccounts, getAlerts, getClusters } from "../api/endpoints"
import StatCard from "../components/StatCard"
import AlertList from "../components/AlertList"
import GraphPanel from "../components/GraphPanel"

function Dashboard() {
  const { data: accounts } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => getAccounts().then(r => r.data),
  })

  const { data: alerts } = useQuery({
    queryKey: ["alerts"],
    queryFn: () => getAlerts().then(r => r.data),
  })

  const { data: clusters } = useQuery({
    queryKey: ["clusters"],
    queryFn: () => getClusters().then(r => r.data),
  })

  const flagged = alerts?.filter(a => a.label !== "normal").length || 0
  const reviewed = alerts?.filter(a => a.status === "reviewed").length || 0

  return (
    <div className=" bg-sky-950 flex flex-col h-full gap-0">
      <div className="grid grid-cols-4 border-b border-gray-200">
        <StatCard label="Total accounts" value={accounts?.length || 0} />
        <StatCard label="Flagged" value={flagged} color="text-red-500" />
        <StatCard label="Clusters" value={clusters?.length || 0} color="text-amber-500" />
        <StatCard label="Reviewed" value={reviewed} color="text-green-500" />
      </div>
      <div className="flex flex-1 overflow-hidden">
        <GraphPanel />
        <AlertList alerts={alerts || []} />
      </div>
    </div>
  )
}

export default Dashboard