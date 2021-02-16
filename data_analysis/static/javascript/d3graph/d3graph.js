function boundingBox() {
  let radius
  let curr_node
  for (curr_node of nodes) {
    radius = Math.sqrt(curr_node.appearances) || 5
    curr_node.x = Math.max(radius + margin.left, Math.min(width - radius - margin.right, curr_node.x));
    curr_node.y = Math.max(radius + margin.top, Math.min(height - radius - margin.bottom, curr_node.y));
  }
}

function setClick(obj, d) {
  obj.onclick = () => console.log(d);
}

function radius(d) {
  return d.appearances ** 0.7 + 4
}

function color(d) {
  if (d.name == "GaveUp") {
    return "#ff00ff"
  }
  if (d.distance == "No completions") {
    return "#ff0000"
  }
  if (d.distance == 0) {
    return "#2222ff"
  }
  const goodness = (maxDistance - (d.distance - 1) ** 0.7) / (maxDistance)
  return `rgb(${Math.min(255, Math.floor(510 * (1 - goodness)))}, ${Math.min(Math.floor(510 * goodness), 255)}, 0)`
}

// set the dimensions of graph, data
const actWidth = 300
const actHeight = 300
const width = 960
const height = 600
const margin = {
  "left": 50,
  "right": 50,
  "top": 50,
  "bottom": 50
}
const links = graph.data.links
//Filter loops
links.forEach((link, index) => {
  if (link.source == link.target) {
    links.splice(index, 1)
  }
})
let nodes = graph.data.nodes
nodes.sort((a, b) => {
  if (!Number.isNaN(Number.parseFloat(a.distance))) {
    if (!Number.isNaN(Number.parseFloat(b.distance))) {
      return Number.parseFloat(b.distance) - Number.parseFloat(a.distance)
    }
    //b is a no completions, "infinite" distance
    return 1
  }
  //a is no completions
  if (!Number.isNaN(Number.parseFloat(b.distance))) {
    return -1
  }
  return 0
})
// Preferred height
const length = nodes.length - 1
let maxDistance = 0
nodes.forEach((node, index) => {
  if (!Number.isNaN(Number.parseFloat(node.distance))) {
    if (Number.parseFloat(node.distance) > maxDistance) {
      maxDistance = Number.parseFloat(node.distance)
    }
  }
  node.height = index / length
  node.y = node.height * (height - margin.top - margin.bottom) + margin.top + (0.5 - Math.random()) * 100
  node.x = width / 2 + (0.5 - Math.random()) * 100
})
maxDistance--
maxDistance = maxDistance ** 0.7
// forces
const simulation = d3.forceSimulation(graph.data.nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(100).strength(0.01))
  .force("charge", d3.forceManyBody().strength(-200))
  .force("yVal", d3.forceY(function (d) {
    return d.height * (height - margin.top - margin.bottom) + margin.top
  }).strength(1))
  .force("bBox", boundingBox)

// append the svg object to the body of the page
const svg = d3.select("#graphDisplay").append("svg")
  .attr("width", actWidth)
  .attr("height", actHeight)
  .attr("viewBox", [0, 0, width, height])
  .style("border", "solid 1px black")


const marker = d3.select("svg")
  .append('defs')
  .append('marker')
  .attr("id", "Triangle")
  .attr("refX", 3)
  .attr("refY", 4)
  .attr("markerUnits", 'userSpaceOnUse')
  .attr("markerWidth", 12)
  .attr("markerHeight", 8)
  .attr("orient", 'auto')
  .append('path')
  .style("fill", "#000000")
  .attr("d", 'M 0 0 12 4 0 8 3 4');

const link = svg.append("g")
  .attr("stroke", "#999")
  .attr("stroke-opacity", 0.6)
  .selectAll("line")
  .data(links)
  .enter()
  .append("line")
  .attr("stroke-width", d => d.size ** 0.6 + 1)
  .attr("marker-end", "url(#Triangle)");

const node = svg.selectAll(".node")
  .data(nodes)
  .enter()
  .append("g")
  .attr("class", "node")
  .attr("stroke", "#fff")
  .attr("stroke-width", 1.5)
  .attr("style", "cursor: pointer;")
  .each(function (d) {
    setClick(this, d)
  })

node.append("circle")
  .attr("r", radius)
  .attr("fill", color)

// .call(drag(simulation));
node.append("text")
  .attr("dx", 12)
  .attr("stroke", "#000")
  .text(d => d.name)
node.append("text")
  .attr("dy", 16)
  .attr("dx", -12)
  .attr("stroke", "#000")
  .text(d => d.distance)

simulation.on("tick", () => {
  node
    .attr("transform", d => `translate(${d.x}, ${d.y})`)

  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x - Math.cos(Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x)) * (radius(d.target) + 11))
    .attr("y2", d => d.target.y - Math.sin(Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x)) * (radius(d.target) + 11))
});