document.querySelector('#graphTitle').innerHTML = `${graph.lesson.name}<br>${graph.lesson.title}`
document.querySelector('#graphCode').innerHTML = graph.lesson.code.replace(/\\r\\n/g, "<br>")
const filter = {}
//users that are checked
filter.checkBoxUsers = []
//users in ranked "goodness" order
filter.sliderUsers = []
//users that should be represent by opaqueness in graph (updated each tick)
filter.allowedUsers = []
Object.entries(graph.data.users).forEach((user) => {
  filter.sliderUsers.push(user[0])
})
filter.sliderUsers.sort((a, b) => {
  return graph.data.users[b].attempts - graph.data.users[a].attempts
})
const minSize = 6
const curve = 0.1
let selectedNode = ""

const drag = d3.drag()
  .on("start", function (d) {
    if (!d3.event.active) simulation.alphaTarget(0.2).restart();
    d.fx = d.x
    d.fy = d.y
  })
  .on("drag", function (d) {
    d.fx = d3.event.x
    d.fy = d3.event.y
  })
  .on("end", function (d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  });

//force for the simulation
function boundingBox() {
  let radius
  let curr_node
  for (curr_node of nodes) {
    radius = Math.sqrt(curr_node.appearances) || minSize
    curr_node.x = Math.max(radius + margin.left, Math.min(width - radius - margin.right, curr_node.x));
    curr_node.y = Math.max(radius + margin.top, Math.min(height - radius - margin.bottom, curr_node.y));
  }
}

//called each tick
function updateAllowedUsers() {
  //only users represented in distance slider
  filter.allowedUsers = filter.sliderUsers.slice(0, Math.ceil(document.querySelector("#filterSlider").value ** 2.5 / Object.entries(graph.data.users).length ** 1.5))
  //now by checkbox
  if(filter.checkBoxUsers.length) {
    const acceptedUsers = []
    for(let user of filter.checkBoxUsers) {
      if(filter.allowedUsers.includes(user)) {
        acceptedUsers.push(user)
      }
    }
    filter.allowedUsers = acceptedUsers
  }
}

//returns the user list that the filter accepts
function filteredUsers(d) {
  allowedUsers = []
  for(let user of d.users) {
    if(filter.allowedUsers.includes(user)) {
      allowedUsers.push(user)
    }
  }
  return allowedUsers
}

function setClick(obj, d) {
  obj.onclick = () => {
    selectedNode = d.name
    document.querySelector("#nodeInfo").style.backgroundColor = fadedColor(d)
    document.querySelector("#nodeName").textContent = `Name: ${d.name}`
    document.querySelector("#nodeDistance").textContent = `Distance: ${d.distance}`
    const correct = Math.round(d.score * 100)
    if (correct >= 0 && correct <= 100) {
      //incorrect ans
      document.querySelector("#nodeCorrect").textContent = `Correct: ${Math.round(d.score * 100)}%`
    } else if (correct > 100) {
      //correct ans
      document.querySelector("#nodeDistance").textContent = `Distance: Correct`
      document.querySelector("#nodeCorrect").textContent = "Correct Answer"
    } else {
      //gave up
      document.querySelector("#nodeCorrect").textContent = "Correct: N/A"
    }
    document.querySelector("#nodeAppearances").textContent = `Appearances: ${d.appearances}`
    updateUserList(d)
    simulation.restart()
  };
  if (d.name == "Start") {
    obj.onclick()
  }
}

function initializeUserList() {
  //set up buttons
  document.querySelector("#selectClear").onclick = () => {
    setAllUserChecks(false)
  }
  document.querySelector("#selectAll").onclick = () => {
    setAllUserChecks(true)
  }
  let userString = ""
  for (let user of Object.entries(graph.data.users)) {
    userString += `<div><input type="checkbox" id="${user[0]}">
        <label for="${user[0]}" style="display: block"></label></div>`
  }
  document.querySelector("#userList").innerHTML = userString.substring(0, userString.length - 6)
  document.querySelectorAll("#userList input").forEach((element) => element.onclick = setUserFilter)
}

function updateUserList(d) {
  const inputs = document.querySelectorAll("#userList input")
  inputs.forEach((element) => {
    element.style.display = "none"
  })
  document.querySelectorAll("#userList label").forEach((element) => {
    element.style.display = "none"
  })
  //count users
  let userMap = new Map()
  for (let user of d.users) {
    if (!userMap.has(user)) {
      userMap.set(user, 1)
    } else {
      userMap.set(user, userMap.get(user) + 1)
    }
  }
  inputs.forEach((element) => {
    for (let user of userMap) {
      if (user[0] === element.id) {
        //show!
        element.style.display = "initial"
        const label = document.querySelector(`#userList label[for="${element.id}"]`)
        label.style.display = "initial"
        //handle multiple occurrences
        if (user[1] > 1) {
          label.textContent = `${graph.data.users[user[0]].name} (${user[1]})`
        } else {
          label.textContent = graph.data.users[user[0]].name
        }
        return
      }
    }
  })
}

function initializeSlider() {
  const slider = document.querySelector("#filterSlider")
  filterSlider.min = 1
  filterSlider.value = filterSlider.max = Object.entries(graph.data.users).length
  filterSlider.oninput = () => {
    simulation.restart()
  }
}

function setAllUserChecks(value) {
  document.querySelectorAll("#userList input").forEach((element) => {
    if (element.style.display != "none") {
      element.checked = value
    }
  })
  setUserFilter()
}

function setUserFilter() {
  filter.checkBoxUsers = []
  document.querySelectorAll("#userList input").forEach((element) => {
    if (element.checked) {
      filter.checkBoxUsers.push(element.id)
    }
  })
  simulation.restart()
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
  } else {
    d3.select(this)
      .attr("stroke", "#999")
  }
}

function manageOpaqueLink(d) {
  const users = filteredUsers(d).length
  if (users > 0) {
    d3.select(this)
      .attr("stroke-width", users ** 0.6 + 1)
      .attr("marker-end", "url(#OpaqueTriangle")
  } else {
    d3.select(this)
      .attr("stroke-width", 0)
      .attr("marker-end", "url(#TranslucentTriangle")
  }
}

function radius(d) {
  return radiusHelper(d.appearances)
}

function radiusHelper(appearances) {
  if (appearances <= 0) {
    return 0
  }
  return appearances ** 0.7 + minSize
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


//Initialize page
initializeUserList()
initializeSlider()
// set the dimensions of graph, data
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
      //normal case
      if (Number.parseFloat(b.distance) - Number.parseFloat(a.distance) != 0) {
        return Number.parseFloat(b.distance) - Number.parseFloat(a.distance)
      } else {
        //Tied in distance, make more often nodes lower
        return a.appearances - b.appearances
      }
    }
    //b is a no completions, "infinite" distance
    return 1
  }
  //a is no completions
  if (!Number.isNaN(Number.parseFloat(b.distance))) {
    return -1
  }
  //Both are no completions, make more often nodes lower
  return a.appearances - b.appearances
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
  .force("charge", d3.forceManyBody().strength(-120))
  .force("yVal", d3.forceY(function (d) {
    return d.height * (height - margin.top - margin.bottom) + margin.top
  }).strength(1))
  .force("xVal", d3.forceX(width / 2).strength(0.005))
  .force("bBox", boundingBox)

// append the svg object to the body of the page
const svg = d3.select("#lessonGraph")
  .attr("viewBox", [0, 0, width, height])
  .style("border", "solid 1px black")


const opaqueMarker = d3.select("svg")
  .append('defs')
  .append('marker')
  .attr("id", "OpaqueTriangle")
  .attr("refX", 3)
  .attr("refY", 4)
  .attr("markerUnits", 'userSpaceOnUse')
  .attr("markerWidth", 12)
  .attr("markerHeight", 8)
  .attr("orient", 'auto')
  .append('path')
  .style("fill", "#000000")
  .attr("d", 'M 0 0 12 4 0 8 3 4');

const translucentMarker = d3.select("svg")
  .append('defs')
  .append('marker')
  .attr("id", "TranslucentTriangle")
  .attr("refX", 3)
  .attr("refY", 4)
  .attr("markerUnits", 'userSpaceOnUse')
  .attr("markerWidth", 12)
  .attr("markerHeight", 8)
  .attr("orient", 'auto')
  .append('path')
  .style("fill", "#000000")
  .attr("d", 'M 0 0 12 4 0 8 3 4')
  .attr("opacity", 0.1)

const link = svg.selectAll(".link")
  .data(links)
  .enter()
  .append("g")
  .attr("fill", "none")
  .attr("class", "link")
  .attr("stroke", "#999")

link
  .append("path")
  .attr("class", "translucent")
  .attr("stroke-width", d => d.size ** 0.6 + 1)
  .attr("opacity", 0.1)

link
  .append("path")
  .attr("class", "opaque")

const node = svg.selectAll(".node")
  .data(nodes)
  .enter()
  .append("g")
  .attr("class", "node")
  .attr("style", "cursor: pointer;")
  .each(function (d) {
    setClick(this, d)
  })
  .call(drag)

node.append("circle")
  .attr("r", radius)
  .attr("fill", color)
  .attr("opacity", 0.1)
  .attr("class", "translucent")

node.append("circle")
  .attr("r", radius)
  .attr("fill", color)
  .attr("class", "opaque")



const center = node.append("circle")
  .attr("r", minSize - 2)
  .attr("stroke-width", 0)

simulation.on("tick", () => {
  updateAllowedUsers()

  node
    .attr("transform", d => `translate(${d.x}, ${d.y})`)
    .selectAll(".opaque")
    .attr("r", d => radiusHelper(filteredUsers(d).length))

  center
    .attr("visibility", displayDot)

  link
    .selectAll("path")
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
    // .attr("opacity", mainFilter)
    .each(boldLine)

  link
    .selectAll(".opaque")
    .each(manageOpaqueLink)
})