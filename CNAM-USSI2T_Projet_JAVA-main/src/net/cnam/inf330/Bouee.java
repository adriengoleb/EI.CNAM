package net.cnam.inf330;

public class Bouee extends Objects {

    //nombre de point de vie regeneré
    int regen = 20;

    public Bouee(int posx, int posy) {
        super(posx, posy); //récupère les positions
        this.id = 1;
    }

    public int getRegen() {
        return regen;
    }


}
