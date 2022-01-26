package net.cnam.inf330;

public class Objects {



    public  int id;
    public int posx;
    public int posy;
    public int casex;
    public int casey;



    public Objects(int posx, int posy) {
        this.posx = posx;
        this.posy = posy;
        this.casex = posx/32;
        this.casey = posy/32;

    }

    //getters
    public int getposx() { return posx; }
    public int getposy() { return posy; }

    public int getId() {
        return id;
    }

    public int getCasex() {
        return casex;
    }

    public int getCasey() {
        return casey;
    }
}
