document.querySelector('#graphTitle').innerHTML = `${graph.lesson.name}<br>${graph.lesson.title}`
document.querySelector('#graphCode').innerHTML = graph.lesson.code.replace(/\\r\\n/g, "<br>")



const minSize = 6
const curve = 0.1
let selectedNode = ""

function boundingBox() {
  let radius
  let curr_node
  for (curr_node of nodes) {
    radius = Math.sqrt(curr_node.appearances) || minSize
    curr_node.x = Math.max(radius + margin.left, Math.min(width - radius - margin.right, curr_node.x));
    curr_node.y = Math.max(radius + margin.top, Math.min(height - radius - margin.bottom, curr_node.y));
  }
}

function setClick(obj, d) {
  obj.onclick = () => {
    selectedNode = d.name
    document.querySelector("#nodeInfo").style.backgroundColor = fadedColor(d)
    document.querySelector("#nodeName").textContent = `Name: ${d.name}`
    document.querySelector("#nodeDistance").textContent = `Distance: ${d.distance}`
    const correct = Math.round(d.score * 100)
    if (correct >= 0 && correct <= 100) {
      document.querySelector("#nodeCorrect").textContent = `Correct: ${Math.round(d.score * 100)}%`
    } else if (correct > 100) {
      document.querySelector("#nodeCorrect").textContent = "Correct Answer"
    } else {
      document.querySelector("#nodeCorrect").textContent = ""
    }
    document.querySelector("#nodeAppearances").textContent = `Appearances: ${d.appearances}`
    simulation.restart()
  };
  if (d.name == "Start") {
    selectedNode = d.name
    document.querySelector("#nodeInfo").style.backgroundColor = fadedColor(d)
    document.querySelector("#nodeName").textContent = `Name: ${d.name}`
    document.querySelector("#nodeDistance").textContent = `Distance: ${d.distance}`
    document.querySelector("#nodeCorrect").textContent = `Correct: ${Math.round(d.score * 100)}%`
    document.querySelector("#nodeAppearances").textContent = `Appearances: ${d.appearances}`
  }
}

function displayDot(d) {
  if (selectedNode == d.name) {
    return "visible"
  } else {
    return "hidden"
  }
}

function boldLine(d) {
  if (selectedNode == d.source.name || selectedNode == d.target.name) {
    d3.select(this)
      .attr("stroke", "#000")
      .attr("stroke-opacity", "0.75")
  } else {
    d3.select(this)
      .attr("stroke", "#999")
      .attr("stroke-opacity", "0.6")
  }
}

function radius(d) {
  return d.appearances ** 0.7 + minSize
}

function color(d) {
  if (d.name == "GaveUp") {
    return "#ff00ff"
  }
  if (d.distance == "No completions") {
    return "#ff0000"
  }
  if (d.distance == 0) {
    return "#00ffff"
  }
  const goodness = (maxDistance - (d.distance - 1) ** 0.7) / (maxDistance)
  return `rgb(${Math.min(255, Math.floor(510 * (1 - goodness)))}, ${Math.min(Math.floor(510 * goodness), 255)}, 0)`
}

function fadedColor(d) {
  if (d.name == "GaveUp") {
    return "#ffB0ff"
  }
  if (d.distance == "No completions") {
    return "#ffB0B0"
  }
  if (d.distance == 0) {
    return "#B0ffff"
  }
  const goodness = (maxDistance - (d.distance - 1) ** 0.7) / (maxDistance)
  return `rgb(${Math.min(255, Math.floor(158 * (2.114 - goodness)))}, ${Math.min(Math.floor(158 * goodness + 176), 255)}, 176)`
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
  .force("charge", d3.forceManyBody().strength(-180))
  .force("yVal", d3.forceY(function (d) {
    return d.height * (height - margin.top - margin.bottom) + margin.top
  }).strength(1))
  .force("bBox", boundingBox)

// append the svg object to the body of the page
const svg = d3.select("#lessonGraph")
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
  .attr("stroke-opacity", 0.6)
  .attr("fill", "none")
  .attr("stroke", "#999")
  .selectAll("path")
  .data(links)
  .enter()
  .append("path")
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

const center = node.append("circle")
  .attr("r", minSize - 2)
  .attr("visibility", displayDot)
  .attr("stroke-width", 0)

// .call(drag(simulation));



//Labels
// node.append("text")
//   .attr("dx", 12)
//   .attr("stroke", "#000")
//   .text(d => d.name)
// node.append("text")
//   .attr("dy", 16)
//   .attr("dx", -12)
//   .attr("stroke", "#000")
//   .text(d => d.distance)
simulation.on("tick", () => {
  node
    .attr("transform", d => `translate(${d.x}, ${d.y})`)

  center
    .attr("visibility", displayDot)

  link
    .attr("d", d => {
      const angle = Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x)
      const adjRad = radius(d.target) + 6 + minSize
      const targetX = d.target.x - Math.cos(angle) * adjRad
      const targetY = d.target.y - Math.sin(angle) * adjRad
      const distance = Math.sqrt((targetX - d.source.x) ** 2 + (targetY - d.source.y) ** 2)
      const rightAngle = angle + Math.PI / 2
      const middleX = (targetX + d.source.x) / 2 + Math.cos(rightAngle) * curve * distance
      const middleY = (targetY + d.source.y) / 2 + Math.sin(rightAngle) * curve * distance
      return `M ${d.source.x} ${d.source.y} Q ${middleX} ${middleY} ${targetX + Math.cos(rightAngle) * curve * 20} ${targetY + Math.sin(rightAngle) * curve * 20}`
    })
    .each(boldLine)
});