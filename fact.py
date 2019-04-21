# fact.py
from random import randint
import curses as c
import datetime as dt

class Land:
    GROUND = 0
    COAL = 1
    IRON = 2
    MACHINE = 10
    CONNECTOR = 15
    WASTE = 20
    ENERGIZER = 30
    DIGGER = 40
    GATE = 50
    GO = 51
    
    CHARDICT = {
        GROUND: " ",
        COAL: ".",
        IRON: "!",
        MACHINE: "&",
        WASTE: "#",
        CONNECTOR: "~",
        ENERGIZER: "$",
        DIGGER: "+",
        GATE: "*",
        GO: "^",
    }
    COLORDICT = {
        GROUND: 2,
        COAL: 4,
        IRON: 3,
        MACHINE: 5,
        WASTE: 6,
        CONNECTOR: 7,
        ENERGIZER: 1,
        DIGGER: 8,
        GATE: 9,
        GO: 10,
    }
    
    def __init__(self,xsize,ysize,maplist,percent):
        self.t1 = dt.datetime.now()
        self.t3 = self.t1
        self.td = "DAY"
        self.gmap = []
        self.width = xsize
        self.height = ysize
        self.is_gate = []
        if (maplist == []):
            for i in range(xsize):
                self.gmap.append([])
                for j in range(ysize):
                    if (randint(0,100) < percent):
                        self.gmap[i].append(randint(0,2))
                    else:
                        self.gmap[i].append(0)
        else:
            self.gmap = []


    def mine(self,player,x,y):
        if (self.gmap[x][y] == self.COAL):
            player.coal += 4
            player.energy -= 5
        if (self.gmap[x][y] == self.IRON):
            player.iron += 2
            player.energy -= 5
        if (self.gmap[x][y] == self.WASTE):
            player.energy -= 5

        self.gmap[x][y] = self.GROUND

    def build(self,player,x,y,msg):
        if (self.gmap[x][y] == self.GROUND and player.iron >= 5):
            self.gmap[x][y] = self.MACHINE
            player.energy -= 5
            player.iron -= 5
            return msg
        else:
            return "Iron"
    
    def connector(self,player,x,y,msg):
        if (self.gmap[x][y] == self.GROUND and player.iron >= 1 and player.coal >= 1):
            self.gmap[x][y] = self.CONNECTOR
            player.energy -= 2
            player.iron -= 1
            player.coal -= 1
            return msg
        else:
            return "Iron + Coal"
        
            
    def energizer(self,player,x,y,msg):
        if (self.gmap[x][y] == self.GROUND and player.iron >= 1 and player.coal >= 1):
            self.gmap[x][y] = self.ENERGIZER
            player.energy -= 10
            player.iron -= 1
            player.coal -= 1
            return msg
        else:
            return "Iron + Coal"
        
    def digger(self,player,x,y,msg):
        if (self.gmap[x][y] == self.GROUND and player.iron >= 40 and player.pix >= 200):
            self.gmap[x][y] = self.DIGGER
            player.energy -= 20
            player.iron -= 40
            player.pix -= 200
            return msg
        else:
            return "Iron + Pix"
        
    def gate(self,player,x,y,msg):
        if (self.gmap[x][y] == self.GROUND and player.pix >= 500):
            self.gmap[x][y] = self.GATE
            player.energy -= 5
            player.pix -= 500
            return msg
        else:
            return "Pix"
            
    def curses_draw(self,cwin):
        for i in range(self.width):
            for j in range(self.height):
                cwin.addstr(j+1,i,self.CHARDICT[self.gmap[i][j]],c.color_pair(self.COLORDICT[self.gmap[i][j]]))
            
    def count_energizer(self):
        count = 0
        for i in self.gmap:
            for j in i:
                if j == self.ENERGIZER:
                    count += 1
        return count
    
    def count_machine(self):
        count = 0
        for i in self.gmap:
            for j in i:
                if j == self.MACHINE:
                    count += 1
        return count
    
    def count_digger(self):
        count = 0
        for i in self.gmap:
            for j in i:
                if j == self.DIGGER:
                    count += 1
        return count
    
    def gates(self):
        tot_gates = []
        for i in range(self.width):
            for j in range(self.height):
                if self.gmap[i][j] == self.GATE:
                    tot_gates.append([i,j])
        return tot_gates
        
    
    def update(self,player):
        t2 = dt.datetime.now()
        s = (t2-self.t1).total_seconds()
        if (s >= 5):
            e = self.count_energizer()
            for i in range(e):
                if (player.coal - 3 >= 0):
                    player.coal -= 3
                    player.energy += 10
            e = self.count_machine()
            for i in range(e):
                if (player.coal - 2 >= 0):
                    player.coal -= 2
                    player.pix += 10
            e = self.count_digger()
            for i in range(e):
                player.coal += randint(2,5)
                player.iron += randint(1,4)
                    
                    
            if (self.td == "DAY"):
                player.energy -= 5
            else:
                player.energy -= 20
            self.t1 = t2
            
        s = (t2-self.t3).total_seconds()
        if (s >= 120):
            self.t3 = t2
            if self.td == "NIGHT":
                self.td = "DAY"
            else:
                self.td = "NIGHT"
            if (len(self.is_gate) > 0):
                for g in self.is_gate:
                    self.gmap[g[0]][g[1]] = self.GO
            self.is_gate = self.gates()
                
            
            
class Player:
    def __init__(self,x,y):
        self.score = 0
        self.coal = 0
        self.iron = 0
        self.energy = 100
        self.pix = 0
        self.x = x
        self.y = y
        self.level = 1
        
    def has_iron(self):
        if self.iron > 0:
            return True
        return False
    
    def is_dead(self):
        if self.energy >= 0:
            return False
        return True
    
    def has_coal(self):
        if self.coal > 0:
            return True
        return False
    
    def move(self,land,dx,dy):
        if (self.x + dx < land.width and self.x + dx >= 0 and dx != 0):
            self.x += dx
            if (land.gmap[self.x][self.y] != land.CONNECTOR):
                self.energy -= 1
        if (self.y + dy < land.height and self.y + dy >= 0 and dy != 0):
            self.y += dy
            if (land.gmap[self.x][self.y] != land.CONNECTOR):            
                self.energy -= 1 
            
