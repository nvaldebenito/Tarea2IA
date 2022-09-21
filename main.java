import java.util.Scanner;
import java.util.ArrayList;
import java.util.List;
class Player {
	public static final int MAPAX = 16001;  
	public static final int MAPAY = 9001;   
	public static final int BUSTA = 1760;   
	public static final int BUSTB = 900;
	public static final int RELEASEA = 1600;  
	public static final int RANGOVISION = 2200; 
	public static Entity base; 
	public static Entity BaseEnemiga;  
	public static int bustersB;
	public static List<Buster> busters; 
	public static List<Entity> enemigos;   
	public static List<Entity> ghosts; 
	public static List<Buster> bustersEnemigo;   
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        bustersB = sc.nextInt(); 
        int ghostCount = sc.nextInt(); 
        int myTeamId = sc.nextInt(); 
        int TeamEnemigoId = myTeamId == 0?1: 0;

        bustersEnemigo = new ArrayList<>();
        busters = initBustersList(myTeamId, bustersB);
        enemigos = initEntitiesList(bustersB, TeamEnemigoId);
        ghosts = initEntitiesList(ghostCount, -1);
        base = confiBase(myTeamId);
        BaseEnemiga = confiBase(TeamEnemigoId);

        while (true) {
            int entities = sc.nextInt(); 
            resetVisibilidad(enemigos);
            resetVisibilidad(ghosts);
            for (int i = 0; i < entities; i++) {
                int entityId = sc.nextInt();
                int x = sc.nextInt();
                int y = sc.nextInt();
                int entityType = sc.nextInt();
                int state = sc.nextInt();
                int value = sc.nextInt();
                setupEntity(myTeamId, TeamEnemigoId, entityId, x, y, entityType, state, value);
            } 
            refrescarBusters(busters, TeamEnemigoId);
            for (int i = 0; i < bustersB; i++) {
            	Buster currentBuster = busters.get(i);
            	Action action = getAction(currentBuster);
            	action.print();
            }

        }
    }
    private static void refrescarBusters(List<Buster> busters, int TeamEnemigoId) {
    	for (Buster b : busters) {
    		b.refresh(BaseEnemiga);
    		b.BaseEnemiga = BaseEnemiga(TeamEnemigoId, b);
    		System.err.println("Buster : " + b.id + " BaseEnemiga : " + b.BaseEnemiga + " Hola Mundo: " + bustersEnemigo.contains(b));
    		if (b.BaseEnemiga) {
    			if (!bustersEnemigo.contains(b)) bustersEnemigo.add(b);
    		} else {
    			int index = bustersEnemigo.indexOf(b);
    			if (index != -1)  {
    				System.err.println("VENDETA: " + index);
    				bustersEnemigo.remove(index);
    			}
            }}}
    	
    public static Entity confiBase(int myTeamId) {
		Entity base = new Entity(-1);
		if (myTeamId == 0) {
			base.x = 0;
			base.y = 0;
		} else {
			base.x = 16001;
			base.y = 9001;
		}
		return base;
	}
	public static boolean BaseEnemiga(int TeamEnemigoId, Buster b) {
		int enX=(int)Math.abs(BaseEnemiga.x-RELEASEA*2);
		int enY=(int)Math.abs(BaseEnemiga.y-RELEASEA*2);
		if (TeamEnemigoId == 0) {
			return b.x<=enX&&b.y<=enY;
		} else {
			return b.x>=enX&&b.y>=enY;
		}
	}
    
    public static void resetVisibilidad(List<Entity> entities) {
    	for (Entity e : entities) {
    		e.EsVisible = false;
    	}
	}
	
	public static void setupEntity(int myTeamId, int TeamEnemigoId, int entityId, int x, int y, int entityType, int state, int value) {
		Entity e = null;
		if (entityType == -1) {
			System.err.println(" Xao Mundo" + entityId);
			e = ghosts.get(entityId);
		} else {
		    if (entityType == myTeamId) {
		    	e = busters.get(getIdNormalizado(myTeamId, entityId));
		    } else {
		    	e = enemigos.get(getIdNormalizado(TeamEnemigoId, entityId));
		    }
		}
		e.setProperties(x, y, entityType, state, value);
	}
    public static int getIdNormalizado(int teamId, int entityId) {
    	int IdNormalizado = teamId == 0 ? entityId : entityId - bustersB;
    	return IdNormalizado;
	}
	public static List<Buster> initBustersList(int MiTeamId,
			int nbBusters) {
		List<Buster> bustersList = new ArrayList<>(nbBusters);
		for (int i = 0; i < nbBusters; i++) {
			int id = MiTeamId == 0 ? i : i + nbBusters;
			int IdNormalizado = MiTeamId == 0 ? id : id - nbBusters;
			Buster b = new Buster(id, IdNormalizado);
			bustersList.add(b);
		}
		return bustersList;
	}
	public static List<Entity> initEntitiesList(int nbEntities, int teamId) {
		List<Entity> entities = new ArrayList<>(nbEntities);
		for (int i = 0; i < nbEntities; i++) {
			int id = i;
			if (teamId != -1) {
				
				id = teamId == 0 ? i : i + nbEntities;
			}
			Entity b = new Entity(id);
			entities.add(b);
		}
		return entities;
	}
	public static Action getAction(Buster currentBuster) {
		Action a = null;
		if (currentBuster.state == 1) {
			Boolean RealeasePosible = RealeasePosible(currentBuster, base);
			if (RealeasePosible) {
				return new Action("RELEASE");
			}
			return new Action("MOVE", base.x, base.y);
        }
		a = getEnemy(currentBuster, enemigos, ghosts);
		if (a == null) {
			a = getGhost(currentBuster, ghosts);
			if (a == null) {
				return DescubirMapa(currentBuster);
			}
		}

		return a;
	}
	
	private static Action getEnemy(Buster currentBuster, List<Entity> enemigos2, List<Entity> ghosts2) {
		return null;
	}

	public static Action getGhost(Entity currentBuster, List<Entity> ghosts) {
		if (!ghosts.isEmpty()) {
			Entity closestGhost = getClosestGhost(currentBuster, ghosts);
			if (closestGhost == null) {
				return null;
			}
			Boolean BustingPosible = BustingPosible(currentBuster, closestGhost);
			if (BustingPosible) {
				return new Action("BUST", closestGhost.id);
			}
			return new Action("MOVE", closestGhost.x, closestGhost.y);
		}

		return null;
	}
	public static Action DescubirMapa(Buster buster) {

		double ZonaX = MAPAX / bustersB;
		double ZonaY = MAPAY / bustersB;
		int posXDiagonal=(int)((ZonaX*(buster.IdNormalizado+1))-(ZonaX/2));
		int posYDiagonal=MAPAY-(int)((ZonaY*(buster.IdNormalizado+1))-(ZonaY/2));

		if (buster.samePosX(posXDiagonal)&&buster.samePosY(posYDiagonal)) {
			buster.isDiagonalCheck=true;
		}
		if (buster.isDiagonalCheck){
			int nbBusterBaseEnemiga = bustersEnemigo.size();
			int index=bustersEnemigo.indexOf(buster);
			if (index==-1) {
				index=nbBusterBaseEnemiga;
				nbBusterBaseEnemiga++;
			}
			double angleRange = 90.0 / nbBusterBaseEnemiga;
			double angle = (angleRange * (index + 1)) - (angleRange / 2.0);
			posXDiagonal = Math.abs((int) (BaseEnemiga.x - RELEASEA * Math.cos(Math.toRadians(angle))));
			posYDiagonal = Math.abs((int) (BaseEnemiga.y - RELEASEA * Math.sin(Math.toRadians(angle))));
		}
		return new Action ("MOVE", posXDiagonal, posYDiagonal);
	}
	public static Entity getClosestGhost(Entity buster, List<Entity> ghosts) {
		double Distanciaminima = Double.MAX_VALUE;
		Entity closestEntity = null;
		for (Entity ghost : ghosts) {
			if (ghost.EsVisible) {
				double distancia = getdistancia(buster, ghost);
				if (distancia > RANGOVISION*2||ghost.state>= 50);
				if (distancia < Distanciaminima) {
					closestEntity = ghost;
					Distanciaminima = distancia;
				}
			}
		}
		return closestEntity;
	}
	public static List<Entity> getobjetivos(Entity buster, List<Entity> enemies) {
		List<Entity> objetivos = new ArrayList<>();
		for (Entity enemy : enemies) {
			if (enemy.EsVisible) {
				double distancia = getdistancia(buster, enemy);
				if (distancia <= BUSTA) {
					objetivos.add(enemy);
				}
			}
		}
		return objetivos;
	}
	public static double getdistancia(Entity a, Entity b) {
		double d = Math.pow(Math.abs(a.x - b.x), 2) + Math.pow(Math.abs(a.y - b.y), 2);
		return Math.sqrt(d);
	}
	public static Boolean BustingPosible(Entity currentBuster,
			Entity closestGhost) {
		double distancia = getdistancia(currentBuster, closestGhost);
		return (distancia < BUSTA && distancia > BUSTB);
	}
	public static Boolean RealeasePosible(Entity currentBuster, Entity base) {
		double distancia = getdistancia(currentBuster, base);
		return distancia < RELEASEA;
	}
}
class Entity {

	public int id;
	public int x;
	public int y;
	public int type;
    public int state;
    public int value;
    public boolean EsVisible = false;

	public void setProperties(int x, int y, int entityType, int state,int value) {
		this.x = x;
		this.y = y;
		this.type = entityType;
		this.state = state;
		this.value = value;
		this.EsVisible = true;
	}

	public Entity(int id) {
		this.id = id;
    }
	
	public boolean equals(Object obj) {
		if (this == obj) {
			return true;
		}
		if (obj == null) {
			return false;
		}
		if (getClass() != obj.getClass()) {
			return false;
		}
		Entity otros = (Entity) obj;
		if (id != otros.id) {
			return false;
		}
		return true;
	}
}
class Buster extends Entity {

	int targetId = -1;
	int IdNormalizado;
	boolean isDiagonalCheck = false;
	boolean BaseEnemiga = false;
	int idAtEnnemyBase = 0;

	public Buster(int id) {
		super(id);
	}

	public void refresh(Entity baseEnemiga) {
	}

	public boolean samePosX(int posXDiagonal) {
		int differencia = Math.abs(this.x - posXDiagonal);
		return differencia <= 20;
	}

	public boolean samePosY(int posYDiagonal) {
		int differencia = Math.abs(this.y - posYDiagonal);
		return differencia <= 20;
	}

	public Buster(int id, int IdNormalizado) {
		super(id);
		this.IdNormalizado = IdNormalizado;
	}

}
class Action {

	public String name;
	public List<Integer> parametros = new ArrayList<>();

	public Action(String name) {
		this.name = name;
	}

	public Action(String name, int... parametros) {
		this.name = name;
		for (int param : parametros) {
			this.parametros.add(param);
		}
	}

	public void print() {
		System.out.print(this.name);
		for (int param : this.parametros) {
			System.out.print(" " + param);
		}
		System.out.print(System.getProperty("line.separator"));
	}
}