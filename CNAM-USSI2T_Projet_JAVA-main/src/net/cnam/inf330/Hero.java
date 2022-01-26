package net.cnam.inf330;


import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.image.ImageObserver;
import java.net.URL;

public class Hero {
    public int velocite;
    public int attaque;
    public int energie = 100;
    public boolean fly;
    public boolean swim;
    public int posX;
    public int posY;

    public BufferedImage ImageHero;


    public Map map;

    public Hero(int velocite, int attaque,  boolean fly, boolean swim) {


        this.velocite = velocite;   //Caractéristique non utilisée
        this.attaque = attaque; // Energie gagnée ou perdue lors d'une attaque lancée ou subie par le héro
        this.energie = 1000;  // Initialisation de l'énergie du héro
        this.fly = fly;   // Booleén, capaciter de voler ou non
        this.swim = swim; // Booleén, capaciter de nager ou non
        this.posX = 0;  // Initialisation de la position x d'affichage du héro
        this.posY = 0;  // Initialisation de la position y d'affichage du héro

    }


    //getters associés
    public int getEnergie() {
        return energie;
    }

    public int getPosX() {
        return posX;
    }

    public int getPosY() {
        return posY;
    }

    public int getVelocite() { return velocite; }

    public boolean isFly() {
        return fly;
    }

    public boolean isSwim() {
        return swim;
    }

    public int getAttaque() {
        return attaque;
    }
}


