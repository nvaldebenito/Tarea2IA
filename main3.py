import math

MAPAX = 16001
MAPAY = 9001
BUSTA = 1760
BUSTB = 900
RELEASEA = 1600
RANGOVISION = 2200
base = []
BaseEnemiga = []
bustersB = 0
busters = []
enemigos = []
ghosts = []
bustersEnemigo = []


def refrescarBusters(busters, TeamEnemigoId):
    for b in busters:
        b.refresh(BaseEnemiga)
        b.BaseEnemiga = BaseEnemiga(TeamEnemigoId, b)
        print("Buster : " + str(b.id) + " BaseEnemiga : " +
              str(b.BaseEnemiga) + " Hola Mundo: " +
              str(bustersEnemigo.contains(b)))
        if (b.BaseEnemiga):
            if (not bustersEnemigo.contains(b)):
                bustersEnemigo.add(b)
        else:
            index = bustersEnemigo.indexOf(b)
            if (index != -1):
                print("VENDETA: " + str(index))
                bustersEnemigo.remove(index)


def confiBase(myTeamId, Entity):
    base = Entity(-1)
    if (myTeamId == 0):
        base.x = 0
        base.y = 0
    else:
        base.x = 16001
        base.y = 9001
    return base


def BaseEnemiga(TeamEnemigoId, b):
    enX = int(abs(BaseEnemiga.x - RELEASEA * 2))
    enY = int(abs(BaseEnemiga.y - RELEASEA * 2))
    if (TeamEnemigoId == 0):
        return b.x <= enX and b.y <= enY
    else:
        return b.x >= enX and b.y >= enY


def resetVisibilidad(entities):
    for e in entities:
        e.EsVisible = False


def setupEntity(myTeamId, TeamEnemigoId, entityId, x, y, entityType, state,
                value):
    e = None
    if (entityType == -1):
        print(" Xao Mundo" + str(entityId))
        e = ghosts.get(entityId)
    else:
        if (entityType == myTeamId):
            e = busters.get(getIdNormalizado(myTeamId, entityId))
        else:
            e = enemigos.get(getIdNormalizado(TeamEnemigoId, entityId))
    e.setProperties(x, y, entityType, state, value)


def getIdNormalizado(teamId, entityId):
    IdNormalizado = entityId if teamId == 0 else entityId - bustersB
    return IdNormalizado


def initBustersList(MiTeamId, nbBusters):
    bustersList = []
    i = 0
    while (i < nbBusters):
        id = i if MiTeamId == 0 else i + nbBusters
        IdNormalizado = id if MiTeamId == 0 else id - nbBusters
        b = nbBusters(id, IdNormalizado)
        bustersList.add(b)
        i += 1
    return bustersList


def initEntitiesList(nbEntities, teamId, Entity):
    entities = []
    i = 0
    while (i < nbEntities):
        id = i
        if (teamId != -1):
            id = i if teamId == 0 else i + nbEntities
        b = Entity(id)
        entities.add(b)
        i += 1
    return entities


def getAction(currentBuster, Action):
    a = None
    if (currentBuster.state == 1):
        RealeasePosible = RealeasePosible(currentBuster, base)
        if (RealeasePosible):
            return Action("RELEASE")
        return Action("MOVE", base.x, base.y)
    a = getEnemy(currentBuster, enemigos, ghosts)
    if (a == None):
        a = getGhost(currentBuster, ghosts)
        if (a == None):
            return DescubirMapa(currentBuster)
    return a


def getEnemy(currentBuster, enemigos2, ghosts2):
    return None


def getGhost(currentBuster, ghosts, Action):
    if (not ghosts.isEmpty()):
        closestGhost = getClosestGhost(currentBuster, ghosts)
        if (closestGhost == None):
            return None
        BustingPosible = BustingPosible(currentBuster, closestGhost)
        if (BustingPosible):
            return Action("BUST", closestGhost.id)
        return Action("MOVE", closestGhost.x, closestGhost.y)
    return None


def DescubirMapa(buster, Action):
    ZonaX = int(MAPAX / bustersB)
    ZonaY = int(MAPAY / bustersB)
    posXDiagonal = int(((ZonaX * (buster.IdNormalizado + 1)) - (ZonaX / 2)))
    posYDiagonal = MAPAY - int(
        ((ZonaY * (buster.IdNormalizado + 1)) - (ZonaY / 2)))
    if (buster.samePosX(posXDiagonal) and buster.samePosY(posYDiagonal)):
        buster.isDiagonalCheck = True
    if (buster.isDiagonalCheck):
        nbBusterBaseEnemiga = bustersEnemigo.size()
        index = bustersEnemigo.indexOf(buster)
        if (index == -1):
            index = nbBusterBaseEnemiga
            nbBusterBaseEnemiga += 1
        angleRange = 90.0 / nbBusterBaseEnemiga
        angle = (angleRange * (index + 1)) - (angleRange / 2.0)
        posXDiagonal = abs(
            int((BaseEnemiga.x - RELEASEA * math.cos(math.toRadians(angle)))))
        posYDiagonal = abs(
            int((BaseEnemiga.y - RELEASEA * math.sin(math.toRadians(angle)))))
    return Action("MOVE", posXDiagonal, posYDiagonal)


def getClosestGhost(buster, ghosts):
    Distanciaminima = 1.7976931348623157E308
    closestEntity = None
    for ghost in ghosts:
        if (ghost.EsVisible):
            distancia = getdistancia(buster, ghost)
            if (distancia > RANGOVISION * 2 or ghost.state >= 50):
                if (distancia < Distanciaminima):
                    closestEntity = ghost
                    Distanciaminima = distancia
    return closestEntity


def getobjetivos(buster, enemies):
    objetivos = []
    for enemy in enemies:
        if (enemy.EsVisible):
            distancia = getdistancia(buster, enemy)
            if (distancia <= BUSTA):
                objetivos.add(enemy)
    return objetivos


def getdistancia(a, b):
    d = math.sqrt(math.pow(abs(a.x - b.x), 2) + math.pow(abs(a.y - b.y), 2))
    return d


def BustingPosible(currentBuster, closestGhost):
    distancia = getdistancia(currentBuster, closestGhost)
    return (distancia < BUSTA and distancia > BUSTB)


def RealeasePosible(currentBuster, base):
    distancia = getdistancia(currentBuster, base)
    return distancia < RELEASEA


class Entity:
    id = 0
    x = 0
    y = 0
    type = 0
    state = 0
    value = 0
    EsVisible = False

    def setProperties(self, x, y, entityType, state, value):
        self.x = x
        self.y = y
        self.type = entityType
        self.state = state
        self.value = value
        self.EsVisible = True

    def __init__(self, id):
        self.id = id

    def equals(self, obj):
        if (self.this == obj):
            return True
        if (obj == None):
            return False
        if (self.getClass() != type(obj)):
            return False
        otros = Entity(obj)
        if (self.id != otros.id):
            return False
        return True


class Buster(Entity):
    targetId = -1
    IdNormalizado = 0
    isDiagonalCheck = False
    BaseEnemiga = False
    idAtEnnemyBase = 0

    def __init__(self, id):
        self.id = id

    def refresh(self, baseEnemiga):
        self.baseEnemiga = baseEnemiga

    def samePosX(self, posXDiagonal):
        differencia = abs(self.x - posXDiagonal)
        return differencia <= 20

    def samePosY(self, posYDiagonal):
        differencia = abs(self.y - posYDiagonal)
        return differencia <= 20

    def __init__(self, id, IdNormalizado):
        self.IdNormalizado = IdNormalizado


class Action:
    name = None
    parametros = []

    def __init__(self, name):
        self.name = name

    def __init__(self, name, parametros):
        self.name = name
        for param in parametros:
            self.parametros.add(param)

    def print(self):
        print(self.name, end="")
        for param in self.parametros:
            print(" " + str(param), end="")


if __name__ == "__main__":

    def main(arg):
        bustersB = input()
        ghostCount = input()
        myTeamId = input()
        TeamEnemigoId = 1 if myTeamId == 0 else 0
        bustersEnemigo = []
        busters = initBustersList(myTeamId, bustersB)
        enemigos = initEntitiesList(bustersB, TeamEnemigoId)
        ghosts = initEntitiesList(ghostCount, -1)
        base = confiBase(myTeamId)
        BaseEnemiga = confiBase(TeamEnemigoId)
        while (True):
            entities = input()
            resetVisibilidad(enemigos)
            resetVisibilidad(ghosts)
            i = 0
            while (i < entities):
                entityId = input()
                x = input()
                y = input()
                entityType = input()
                state = input()
                value = input()
                setupEntity(myTeamId, TeamEnemigoId, entityId, x, y,
                            entityType, state, value)
                i += 1
            refrescarBusters(busters, TeamEnemigoId)
            i = 0
            while (i < bustersB):
                currentBuster = busters.get(i)
                action = getAction(currentBuster)
                action.print()
                i += 1
