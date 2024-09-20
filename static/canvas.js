let canvas = document.getElementById('draw_canvas')
let ctx = canvas.getContext('2d')
let isDrawing = false

canvas.width = 600
canvas.height = 600

const gridsize = 20
const grid_width = canvas.width / gridsize
const grid_height = canvas.height / gridsize

console.log('gridsize', gridsize)
console.log('grid_width', grid_width)
console.log('grid_height', grid_height)

let gridArray = new Array(gridsize ** 2).fill(0)

function drawGrid() {
  ctx.lineWidth = 1
  ctx.strokeStyle = '#0ff'

  for (let i = 0; i <= gridsize; i++) {
    ctx.beginPath()
    ctx.moveTo(0, canvas.height/gridsize * i)
    ctx.lineTo(canvas.width, canvas.height/gridsize * i)
    ctx.stroke()
    ctx.closePath()

    ctx.beginPath()
    ctx.moveTo(canvas.width/gridsize * i, 0)
    ctx.lineTo(canvas.width/gridsize * i, canvas.height)
    ctx.stroke()
    ctx.closePath()
  }
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  drawGrid()
  gridArray = new Array(gridsize ** 2).fill(0)
}

function fillAll(color) {
  ctx.fillStyle = color
  ctx.fillRect(0, 0, canvas.width, canvas.height)
}

canvas.addEventListener('contextmenu', event => event.preventDefault())

canvas.addEventListener('mouseup', () => isDrawing = false)

canvas.addEventListener('mousedown', event => {
  if (event.button == 0) {
    isDrawing = true
  }
  else if (event.button == 2) {
    clearCanvas()
  }
})

function drawRect(clientX, clientY) {
  const rect = canvas.getBoundingClientRect()
  const x = clientX - rect.left
  const y = clientY - rect.top
  const x1 = x - (x % grid_width)
  const y1 = y - (y % grid_height)

  const gridX = x1 / grid_width
  const gridY = y1 / grid_height
  const index = gridY * gridsize + gridX


  ctx.fillStyle = '#0ff'
  ctx.fillRect(x1, y1, grid_width, grid_height)
  gridArray[index] = 1
}

canvas.addEventListener('mousemove', event => {
  if (isDrawing) drawRect(event.clientX, event.clientY)
})

drawGrid()

let text = document.getElementById('valnum')

function actionButton(num) {
  text.textContent = num
}

function sendButton() {
  let num = +text.textContent

  if (!Number.isInteger(num)) {
    alert('Please, select a number first')
    return
  }

  const dataToSend = {
    gridState: gridArray,
    selectedNumber: num
  }

  fetch('/endpoint', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataToSend)
  })
  .then(response => {
    if (!response.ok)
      throw new Error()
    return response.json()
  })
  .then(data => {
    fillAll('#0a0')
    setTimeout(clearCanvas, 80)
  })
  .catch(error => {
    fillAll('#a00')
    setTimeout(clearCanvas, 80)
  })

}

document.addEventListener('keydown', event => {
  if (event.key == 'Enter')
    sendButton()
  else if (Number.isInteger(+event.key))
    if (+event.key != 0)
      actionButton(+event.key)
})

