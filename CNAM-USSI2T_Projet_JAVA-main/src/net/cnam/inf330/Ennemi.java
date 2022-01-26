package net.cnam.inf330;

public class Ennemi {
    int sante = 100;  // Initialisation de la santé de l'ennemi
    int attaque = 75 ; // Dégat causé au héro (-75) à chaque attaque de l'ennemi
    int posx;  // Position x d'affichage de l'ennemi
    int posy; // Position y d'affichage de l'ennemi
    int casex; // Position x de déplacement de l'ennemi
    int casey;  // Position y de déplacement de l'ennemi

    public Ennemi(int posx, int posy) {
        this.posx = posx;
        this.posy = posy;
        this.casex = posx/32;
        this.casey = posy/32;
    }

    //getters associés
    public int getCasex() {
        return casex;
    }

    public int getCasey() {
        return casey;
    }

    public int getPosx() {
        return posx;
    }

    public int getPosy() {
        return posy;
    }

    public int getSante() {
        return sante;
    }

    public int getAttaque() {
        return attaque;
    }
}
