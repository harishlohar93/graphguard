import { useEffect, useRef } from "react"
import { useQuery } from "@tanstack/react-query"
import * as d3 from "d3"
import { getGraph } from "../api/endpoints"

function getNodeColor(d) {
  if (d.label === "bot" || d.account_type === "bot") return "#a80303"
  if (d.label === "suspect") return "#e6aa05"
  return "#4ff00a"
}

function getNodeRadius(d) {
  if (d.label === "bot") return 10
  if (d.label === "suspect") return 7
  return 6
}

function GraphPanel() {
  const svgRef = useRef(null)

  const { data, isLoading } = useQuery({
    queryKey: ["graph"],
    queryFn: () => getGraph().then(r => r.data),
    staleTime: 0,
    cacheTime: 0,
  })



  useEffect(() => {
    if (!data || !svgRef.current) return

    const width = svgRef.current.clientWidth
    const height = svgRef.current.clientHeight

    d3.select(svgRef.current).selectAll("*").remove()

    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height)

    const nodes = data.nodes.map(d => ({ ...d }))
    const links = data.edges.map(d => ({ source: d.source, target: d.target }))

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(20))
      .force("charge", d3.forceManyBody().strength(-80))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(8))

    const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke", "#d0deca")
      .attr("stroke-width", 0.8)
      .attr("opacity", 0.15)

    const node = svg.append("g")
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", d => getNodeRadius(d))
    .attr("fill", d => getNodeColor(d))
    .attr("opacity", d => d.account_type === "bot" ? 1 : 0.7)
    .attr("stroke", d => d.label === "bot" ? "#991b1b" : "none")
    .attr("stroke-width", 1)
    .style("cursor", "pointer")



    node.append("title").text(d => `${d.username} (${d.account_type})`)

    const zoom = d3.zoom()
    .scaleExtent([0.3, 5])
    .on("zoom", (event) => {
      svg.selectAll("g").attr("transform", event.transform)
    })

svg.call(zoom)

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y)
      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
    })

    return () => simulation.stop()
  }, [data])

  if (isLoading) {
    return (
      <div className="flex-1 bg-white flex items-center justify-center border-r border-gray-200">
        <p className="text-sm text-gray-400">Loading graph...</p>
      </div>
    )
  }

   

  return (
    <div className="flex-1 flex flex-col overflow-hidden" style={{background: "#0f172a", borderRight: "1px solid #1e293b"}}>
      <div className="px-3 py-2 flex items-center gap-4" style={{borderBottom: "1px solid #1e293b"}}>
        <span className="text-xs font-medium text-slate-300">Force-directed graph</span>
        <div className="flex items-center gap-3 ml-auto">
          <span className="flex items-center gap-1 text-xs text-slate-400">
            <span className="w-2 h-2 rounded-full bg-green-500 inline-block"></span>Normal
          </span>
          <span className="flex items-center gap-1 text-xs text-slate-400">
            <span className="w-2 h-2 rounded-full bg-amber-400 inline-block"></span>Suspect
          </span>
          <span className="flex items-center gap-1 text-xs text-slate-400">
            <span className="w-2 h-2 rounded-full bg-red-500 inline-block"></span>Bot
          </span>
        </div>
      </div>
      <svg ref={svgRef} className="flex-1 w-full h-full" style={{background: "#0f172a"}}></svg>
    </div>
  )
}

export default GraphPanel