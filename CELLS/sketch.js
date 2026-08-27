let cells = [];
let board = [];
let size;
let pause = false;
function createCells(amount) {
  for (let i = 0; i < amount; i++) {
    cells.push(new Cell(width/size.x,height/size.y,createVector(floor(random(0,width/size.x)),floor(random(0,height/size.y)))));
  }
}
function decOneRound(value,decimals) {
  let result = Math.round(value * 10**decimals) / 10**decimals;
  return result
}
function updateMap() {
  let next = [];

  for (let i = 0; i < board.length; i++) {
    next[i] = [];
    for (let j = 0; j < board[i].length; j++) {
      next[i][j] = board[i][j];
    }
  }

  for (let i = 1; i < board.length - 1; i++) {
    for (let j = 1; j < board[i].length - 1; j++) {
      let current = board[i][j];

      let neighbors = [
        board[i-1][j],
        board[i+1][j],
        board[i][j-1],
        board[i][j+1]
      ];

      for (let n = 0; n < neighbors.length; n++) {
        let diff = (current - neighbors[n]) * 0.01;
        next[i][j] -= diff;
        next[i + (n===0?-1:n===1?1:0)]
            [j + (n===2?-1:n===3?1:0)] += diff;
      }
    }
  }

  board = next;
}

function createMap(sx,sy) {
  for (let i = 0; i < height/sy; i++) {
    board.push([])
    for (let j = 0; j < width/sx; j++) {
      board[i].push(decOneRound(random(0,1),2));
    }
  }
}
function setup() {
  createCanvas(windowWidth, windowHeight);
  size = createVector(floor(width/80),floor(height/80));
  createMap(size.x,size.y);
  createCells(30);
}

function draw() {
  background(220);
  if (keyIsDown(CONTROL)) {
    pause = true;
  } else {
    pause = false;
  }
  //frameRate(10);
  
  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j < board[i].length; j++) {
      fill(0+board[i][j]*200,0+board[i][j]*50,0);
      noStroke();
      rect(j*size.x,i*size.y,size.x,size.y);
      //fill(255);
      //text(map[i][j],j*size.x,i*size.y)
      //board[i][j] -= 0.0001;
    }
  }
  for (let i = 0; i < cells.length; i++) {
    fill(105,105,105,200);
    rect(cells[i].currentPosition.x*size.x,cells[i].currentPosition.y*size.y,size.x,size.y);
    if (pause == false) {
      cells[i].update(board,cells);
      if (cells[i].dead == true) {
        cells.splice(i,1);
        continue;
      }
      fill(255,255,255,200);
      rect(cells[i].currentPosition.x*size.x,cells[i].currentPosition.y*size.y,size.x,size.y);
      if (cells[i].multiply == true) {
        cells.push(new Cell(width/size.x,height/size.y,createVector(cells[i].currentPosition.x+floor(random(-1,1)),cells[i].currentPosition.y+floor(random(1,-1)))));
        cells[i].multiply = false;
      }
    }
  }
  if (mouseIsPressed) {
    let mx = floor(map(mouseX,0,width,0,width/size.x));
    let my = floor(map(mouseY,0,height,0,height/size.y));
    let pasteable = true;
    for (let i = 0; i < cells.length; i++) {
      if (cells[i].x == mx && cells[i].y == my) {
        pasteable = false;
      }
    }
    if (pasteable == true) {
      cells.push(new Cell(width/size.x,height/size.y,createVector(mx,my)));
    }
  }
  if (pause == false) {
    updateMap();
  }
}
