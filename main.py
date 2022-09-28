import sys
import math

class Entity:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y =y
    def properties (self, x, y, state, value):
        self.x = x
        self.y = y
        self.state = state
        self.value = value
        self.esvisible = True
    def distancia (self, point):
        return math.hypot((self.x, self.y)[0]-point[0], (self.x, self.y)[1]-point[1]) 

class Buster(Entity):
    def __init__(self, id, x, y, entity_type, state, value):
        super().__init__ (id, x, y)
        self.teamid = entity_type
        self.myteam = entity_type == player.myteamid
        self.lleva = state == 1
        self.lleva_ghostid = value
        self.ir = (-1, -1)
    def properties (self, x, y, state, value):
        super().properties(x, y)
        self.lleva = state == 1
        self.lleva_ghostid = value
        self.nolleva = value
    def move (self, point):
        print (f"MOVE {point[0]}{point[1]}")
    def bust (self, ghostid):
        print(f"BUST {ghostid}")
    def release (self):
        print ("RELEASE")
    def closesghost (self):
        ghosts = sorted([ghost for ghost in player.ghosts.values() if not ghost.inbase], key=lambda ghost: ghost.distancia (self.x, self.y) )
        for ghost in ghosts:
            closebuster = ghost.closesghost()
            if closebuster:
                if closebuster.id == self.id:
                    return ghost
        return None
    def action (self):
        if self.lleva:
            if self.distancia(player.base) < 1600:
                player.ghosts[self.lleva_ghostid].inbase = True
                self.release
                print(f'{self.id} released {self.lleva_ghostid} ghost', file=sys.stderr, flush=True)
            else: 
                self.move(player.base)
                print(f'{self.id}')
        else:
            nghost = self.closesghost()
            if nghost:
                print(f'{nghost.id} esta en myteam base: {nghost.inbase}')
                if self.distancia(nghost.position) <= 1760 and self.distancia(nghost.position) >= 900:
                    self.bust(nghost.id)
                    print(f'{self.id} busted {nghost.id} ghost', file=sys.stderr, flush=True)
                else:
                    self.move(nghost.position)
                    print(f'{self.id} ir hacia {nghost.id} ghost', file=sys.stderr, flush=True)
    def __str__(self):
        return f"id: {self.id} posicion: {self.position} {'MIO' if self.myteam else 'ENEMIGO'} {f'lleva: {self.lleva_ghostid}' if self.lleva else ' '}"

class Ghost(Entity):
    def __init__(self, id, x, y, state, value):
        super().__init__(id, x, y)
        self.state = state
        self.getghost = value
        self.inbase = False
    def properties(self, x, y, state, value):
        super().properties(x, y)
        self.state = state
        self.getghost = value
def closesbuster (self):
    busters = sorted ([buster for buster  in player.busters.values() if buster.inbase], key=lambda buster: self.distancia (buster.posicion))
    for buster in busters:
        if buster.lleva:
            if buster.nolleva != 1:
                return buster
    return None
def __str__ (self):
    return f"id: {self.id} posicion: {self.posicion} getghost: {self.getghost}"

class Player: 
    def __init__(self, bustersB, ghostcount, myteamid):
        self.bustersB = bustersB
        self.ghostcount = ghostcount
        self.myteamid = myteamid
        self.base = (0, 0) if myteamid == 0 else (16001, 9001)
        self.baseenemiga = (0, 0) if myteamid == 1 else (16001, 9001)
        self.busters = {}
        self.ghosts = {}  
    def main (self):
        for ghost in self.ghosts.values():
            ghost.esvisible = False
        for buster in self.busters.values():
            buster.esvisible = False
bustersB = int(input())
ghostcount = int(input())
myteamid = int(input())

player = Player (bustersB, ghostcount, myteamid)
while True: 
    entities = int (input())
    for i in range(entities):
        # entity_id: buster id or ghost id
        # y: position of this buster / ghost
        # entity_type: the team id if it is a buster, -1 if it is a ghost.
        # state: For busters: 0=idle, 1=carrying a ghost. For ghosts: remaining stamina points.
        # value: For busters: Ghost id being carried/busted or number of turns left when stunned. For ghosts: number of busters attempting to trap this ghost.        
        entity_id, x, y, entity_type, state, value = [int(j) for j in input().split()]
        if entity_type == -1:
            ghost = player.ghosts.get(entity_id, Ghost(entity_id, x, y, state, value))
            player.ghosts[entity_id] = ghost
            ghost.properties(x, y, state, value)
            print (ghost)
        else: 
            buster = player.busters.get(entity_id, Buster(entity_id, x, y, entity_type, state, value))
            player.busters[entity_id] = buster
            buster.properties(x, y, state, value)
            print(buster)
    for busterid in player.busters:
        buster = player.busters[busterid]
        if buster.myteam:
            buster.action()
    
    player.main()