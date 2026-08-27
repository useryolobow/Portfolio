class Cell {
  constructor(mapWidth,mapHeight,position) {
    this.mapSize = createVector(mapWidth,mapHeight);
    this.currentPosition = createVector(position.x,position.y);
    this.multiply = false;
    this.dead = false;
    this.health = 5;
  }
  move(map,cellarray) {
    let pos = this.currentPosition;
    let newPosition = createVector(pos.x,pos.y);
    for (let i = 0; i < cellarray; i++) {
        if (map[pos.y][pos.x] < map[pos.y-1][pos.x] && map[pos.y-1][pos.x] < 0.9) {
            newPosition.x = pos.x;
            newPosition.y = pos.y-1;
        } else if (map[pos.y][pos.x] < map[pos.y+1][pos.x] && map[pos.y+1][pos.x] < 0.9) {
            newPosition.x = pos.x;
            newPosition.y = pos.y+1;
        } else if (map[pos.y][pos.x] < map[pos.y][pos.x-1] && map[pos.y][pos.x-1] < 0.9) {
            newPosition.x = pos.x-1;
            newPosition.y = pos.y;
        } else if (map[pos.y][pos.x] < map[pos.y][pos.x+1] && map[pos.y][pos.x+1] < 0.9) {
            newPosition.x = pos.x+1;
            newPosition.y = pos.y;
        }
        if (cellarray[i].currentPosition.x == newPosition.x && cellarray[i].currentPosition.y == newPosition.y) {
            newPosition.x = pos.x;
            newPosition.y = pos.y;
        }
    }
    this.currentPosition = newPosition;
  }
  update(map,cellarray) {
    let cells = cellarray;
    let pos = this.currentPosition;
    if (pos.y >= map.length-2 || pos.x <= 2) {
        return;
    }
    if (pos.x >= map[0].length-2 || pos.x <= 2) {
        return;
    }
    map[pos.y][pos.x] += 0.04;
    if (map[pos.y][pos.x] > 0.7 && map[pos.y][pos.x] < 0.9) {
        let possible = false;
        let stopped = 0;
        for (let i = 0; i < cellarray.length; i++) {
            let cellpos = cellarray[i].currentPosition;
            if (pos.x + 1 == cellpos.x && pos.y == cellpos.y) {
                stopped += 1;
            } else if (pos.x - 1 == cellpos.x && pos.y == cellpos.y) {
                stopped += 1;
                
            } else if (pos.x == cellpos.x && pos.y + 1 == cellpos.y) {
                stopped += 1
            } else if (pos.x == cellpos.x && pos.y - 1 == cellpos.y) {
                stopped += 1;
            }

        }
        if (stopped < 3) {
            possible = true;
        }
        if (possible == true) {
            this.multiply = true;
            this.health -= 1;
            map[pos.y][pos.x] += 0.1;
        }
    } else {
        this.health -= 1;
    }
    if (this.health <= 0) {
        this.dead = true;
    }
    if (map[pos.y-1][pos.x] < 0.7) {
        map[pos.y-1][pos.x] += 0.01;
    }
    if (map[pos.y+1][pos.x] < 0.7) {
        map[pos.y+1][pos.x] += 0.01;
    }
    if (map[pos.y][pos.x-1] < 0.7) {
        map[pos.y][pos.x+1] += 0.01;
    }
    if (map[pos.y][pos.x-1] < 0.7) {
        map[pos.y][pos.x-1] += 0.01;
    }
    let distance = createVector(99,99);
    for (let i = 0; i < cells.length; i++) {
        let cellpos = cells[i].currentPosition;
        distance.x = max(cellpos.x,pos.x) - min(cellpos.x,pos.y);
        distance.y = max(cellpos.y,pos.y) - min(cellpos.y, pos.y);
    }
    if (distance < 3 && this.health < 5) {
        this.health += 1;
    }
    this.move();
  }
}