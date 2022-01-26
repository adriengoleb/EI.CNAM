package net.cnam.inf330;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Random;

public class Map extends JPanel implements KeyListener {
//Implémentation de l'interface pour la gestion clavier

    //Type d'image utilisé
    public BufferedImage imageSable;
    public BufferedImage imageGrass;
    public BufferedImage imageEau;
    public BufferedImage imageHero ;
    public BufferedImage imageForet;
    public BufferedImage imageBrickWall;
    public BufferedImage imageBouee;
    public BufferedImage imageBateau;
    public BufferedImage imageEnnemi;

    //Récupération des images
    public URL ressourceSable = getClass().getResource("images/solsable.png");
    public URL ressourceGrass = getClass().getResource("images/Grass.png");
    public URL ressourceEau = getClass().getResource("images/eau.png");
    public URL ressourceForet = getClass().getResource("images/foret.png");
    public URL ressourceHero1d = getClass().getResource("images/HeroTile1d.png");
    public URL ressourceHero2d = getClass().getResource("images/HeroTile2d.png");
    public URL ressourceHero1g = getClass().getResource("images/HeroTile1g.png");
    public URL ressourceHero2g = getClass().getResource("images/HeroTile2g.png");
    public URL ressourceBrickWall = getClass().getResource("images/BrickWall.png");
    public URL ressourceBouee = getClass().getResource("images/bouee.png");
    public URL ressourceBateau = getClass().getResource("images/bateau.png");
    public URL ressourceEnnemi = getClass().getResource("images/aviond.png");


    Fenetrejeu j;
    Hero hero;

    // Initialisation de la position de déplacement du héro et de la jauge compteur coup
    int casex = 0;
    int casey= 0;
    int compteurcoup = 100;


    //Implémentation listes Objects + ennemis
    ArrayList<Objects> listeObjet = new ArrayList<Objects>();
    ArrayList<Ennemi> listeEnnemis = new ArrayList<>();

    // Initialisation de la position des objets dans la carte (non aléatoire)
    Objects foret1 = new Foret(128,128);
    Objects foret2 = new Foret(128,160);
    Objects foret3 = new Foret(128,192);
    Objects foret4 = new Foret(160,128);
    Objects foret5 = new Foret(160,160);
    Objects foret6 = new Foret(160,192);
    Objects foret7 = new Foret(640,128);
    Objects foret8 = new Foret(640,160);
    Objects foret9 = new Foret(640,192);
    Objects foret10 = new Foret(672,128);
    Objects foret11 = new Foret(672,160);
    Objects foret12 = new Foret(672,192);
    Objects bricksWall1 = new BricksWall(256,256);
    Objects bricksWall2 = new BricksWall(256,288 );
    Objects bricksWall3 = new BricksWall(256,320);
    Objects bricksWall4 = new BricksWall(224,320 );
    Objects bricksWall5 = new BricksWall(192,320 );
    Objects bricksWall6 = new BricksWall(640,256);
    Objects bricksWall7 = new BricksWall(640,288 );
    Objects bricksWall8 = new BricksWall(640,320);
    Objects bricksWall9 = new BricksWall(608,320 );
    Objects bricksWall10 = new BricksWall(576,320 );
    Objects bouee1 = new Bouee(480,480);
    Objects bouee2 = new Bouee(320, 480);
    Objects bateau1 = new Bateau(448,448);
    Objects bateau2 = new Bateau(544,544);
    Ennemi ennemi1 = new Ennemi(320,320);
    Ennemi ennemi2 = new Ennemi(384,384);
    Ennemi ennemi3 = new Ennemi(512,480);

    //Constructeur Map - Choix du héro
    public Map(boolean choix, Fenetrejeu j) {
        hero = new Hero(50,50,choix,true);
        try {
            if (!this.hero.fly) {
                this.imageHero = ImageIO.read(ressourceHero1d);
            } else {
                this.imageHero = ImageIO.read(ressourceHero2d);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        setListeEnnemis(listeEnnemis);
        setListeObjet(listeObjet);
        this.j=j;
    }

    // Nombre de cases vertes + Nb de case horizontakes pour faciliter l'affichage
    public int getnbcasevert(){
        return (this.getWidth()/32);
    }
    public int getnbcasehoriz(){
        return (this.getHeight()/32);
    }

    //Ajout des objets dans leur liste respective
    public void setListeObjet(ArrayList<Objects> listeObjet) {
        listeObjet.add(foret1);
        listeObjet.add(foret2);
        listeObjet.add(foret3);
        listeObjet.add(foret4);
        listeObjet.add(foret5);
        listeObjet.add(foret6);
        listeObjet.add(foret7);
        listeObjet.add(foret8);
        listeObjet.add(foret9);
        listeObjet.add(foret10);
        listeObjet.add(foret11);
        listeObjet.add(foret12);
        listeObjet.add(bouee1);
        listeObjet.add(bouee2);
        listeObjet.add(bricksWall1);
        listeObjet.add(bricksWall2);
        listeObjet.add(bricksWall3);
        listeObjet.add(bricksWall4);
        listeObjet.add(bricksWall5);
        listeObjet.add(bricksWall6);
        listeObjet.add(bricksWall7);
        listeObjet.add(bricksWall8);
        listeObjet.add(bricksWall9);
        listeObjet.add(bricksWall10);
        listeObjet.add(bateau1);
        listeObjet.add(bateau2);
        this.listeObjet = listeObjet;
    }

    //Setter associé à la liste ennemi
    public void setListeEnnemis(ArrayList<Ennemi> listeEnnemis) {
        listeEnnemis.add(ennemi1);
        listeEnnemis.add(ennemi2);
        listeEnnemis.add(ennemi3);
        this.listeEnnemis = listeEnnemis;
    }


    // Méthodes de l'interfaces KeyListener

    public void keyTyped(KeyEvent e) {}

    // Méthode pour gérer les actions du héro/ennemi lorsque le joueur clic sur la souris
    public void keyPressed(KeyEvent e) {


        switch(e.getKeyCode()){

            /* déplacement à gauche */
            case KeyEvent.VK_LEFT: //touche clavier direction gauche
                if (!depasseBorduregauche(casex)) {
                    if (this.hero.isFly() || !isobstacle(this.casex-1,this.casey)) { // si le perso vole ou si pas d'obstacles
                        System.out.println("left"); //affichage dans la console

                        System.out.println("Cases : " + (this.casex - 1) + " " + this.casey);  //affichage dans la console

                        this.hero.posX -= 32;  // position d'affichage du héro
                        this.casex -= 1; //Position de déplacement du héro
                        this.hero.energie -= 5;  // Perte d'énergie -5 à chaque déplacement
                        try {
                            if (!this.hero.fly) {  // En fonction du héro 1 ou du héro 2
                                this.imageHero = ImageIO.read(ressourceHero1g);
                            } else {
                                this.imageHero = ImageIO.read(ressourceHero2g);
                            }
                        } catch (IOException ex) {
                            ex.printStackTrace();
                        }
                    }
                }
                break;


            /* déplacement à droite */
            case KeyEvent.VK_RIGHT: //touche clavier direction droite
                if (!depasseBorduredroite(casex)){
                    // si le perso vole ou si pas d'obstacles
                    if (this.hero.isFly() || !isobstacle(this.casex+1,this.casey)) {
                        System.out.println("right");
                        System.out.println("Cases : " + (this.casex + 1) + " " + this.casey);

                        this.hero.posX += 32;
                        this.casex += 1;
                        this.hero.energie -= 5;
                        try {
                            if (!this.hero.fly) {
                                this.imageHero = ImageIO.read(ressourceHero1d);
                            } else {
                                this.imageHero = ImageIO.read(ressourceHero2d);
                            }
                        } catch (IOException ex) {
                            ex.printStackTrace();
                        }
                    }

                }
                break;
            /*déplacement en haut */
            case KeyEvent.VK_UP:  //touche clavier direction haute
                if (!depasseBordurehaut(casey)) {
                    if (this.hero.isFly() || !isobstacle(this.casex, this.casey - 1)) {
                        System.out.println("up");
                        System.out.println("Cases : " + this.casex + " " + (this.casey - 1));
                        this.hero.posY -= 32;
                        this.casey -= 1;
                        this.hero.energie -= 5;
                    }
                }

                break;

            /* deplacement en bas */
            case KeyEvent.VK_DOWN:  //touche clavier direction bas
                if (!depasseBordurebas(casey)) {
                    if (this.hero.isFly() || !isobstacle(this.casex, this.casey + 1)) {
                        System.out.println("down");
                        System.out.println("Cases : " + this.casex + " " + (this.casey + 1));
                        this.hero.posY += 32;
                        this.casey += 1;
                        this.hero.energie -= 5;
                    }
                }
                break;

            /* permet de se soigner */
            case KeyEvent.VK_R: //touche clavier lettre "R"
                System.out.println("r"); //affichage dans la console
                this.hero.energie+=10;   // +10 pour l'énergie du héros
                break;

            //attaquer
            case KeyEvent.VK_A:  //touche clavier lettre "A"
                System.out.println("a");
                Attaque(this.casex, this.casey);
                break;

        }
        //Dans tous les cas, à la fin de chaque touche préssée, l'ennemi se déplace et contre attaque si il peut
        ActionEnnemi();
        this.repaint();
        compteurcoup -=1;  //compteur diminue à chaque attaque (subie ou lancée)

        //on vérifie les conditions de défaites
        if (compteurcoup == 0 || this.hero.energie <=0){
            //fenêtre game over
            System.out.println("Défaite");
            Fenetregameover f = new Fenetregameover();
            j.setVisible(false);
        }


    }

    //attaque du héros
    void Attaque(int x, int y){
        boolean att = false;
        int i = x-1;
        while(i<=x+1 && !att){
            int j = y-1;
            while(j<=y+1 && !att) {
                for (Ennemi e : listeEnnemis) {
                    att = (i == e.getCasex() && j == e.getCasey()); // le héro se trouve sur la même case que l'énnemi ou à une case d'écart
                    if (att) {  // si c'est vrai
                        ActionAttaque(e); //il attaque
                        break;
                    }
                }
                j += 1;
            }
            i+=1;
        }
    }

    //Gestion de la santé de l'ennemi et de la victoire du héro
    private void ActionAttaque(Ennemi e) {
        e.sante -= this.hero.getAttaque();  //Perte de santé pour l'ennemi suite à l'attaque du héro
        this.hero.energie += this.hero.getAttaque();  // ce qui permet .... gain d'energie du héro suite à son attaque dévastatrice
        //si l'ennemi n'a plus de vie, il disparait
        if (e.sante<=0) {
            this.listeEnnemis.remove(e);
        }
        //si plus d'ennemie -> victoire
        if (listeEnnemis.isEmpty()){
            System.out.println("VICTOIRE");
            FenetreVictoire fv = new FenetreVictoire();
            j.setVisible(false);
        }

    }


    public void riposteEnnemi(Ennemi e){
        boolean rep = false;
        int distancex = this.casex - e.getCasex(); //calcul de la distance x entre le héro et l'ennemi
        int distancey = this.casey - e.getCasey(); //calcul de la distance y entre le héro et l'ennemi
        if (distancex < 3 && distancex > -3 && distancey < 3 && distancey > -3){ // Attaque de l'avion lorsque le héro se trouve à moins de 3 cases
            this.hero.energie -= e.getAttaque();  // Perte d'énergie du héro car trop proche de l'ennemi (à moins de 3 cases)
        }
    }

    public void keyReleased(KeyEvent e) {

    }

    // Gestion des collisions et obstacles
    boolean isobstacle(int x, int y) {
        boolean collision = false;
        for (Objects obj : listeObjet) { //on parcourt les objets
            collision = (x == obj.getCasex() && y == obj.getCasey()); //héro dans la case de l'obstacle
            if (collision){break;} // si collision, sortie au premier obstacle
        }
        return collision;
    }

    //Gestion des bordures de la map
    boolean depasseBorduredroite(int x){
        return (x+1>getnbcasevert());
    }
    boolean depasseBorduregauche(int x){
        return (x-1<0);
    }
    boolean depasseBordurehaut(int y){
        return (y -1 <0);
    }
    boolean depasseBordurebas(int y){
        return (y +1 >getnbcasehoriz());
    }

    //Génère un nombre aleatoire
    private static int getRandomNumberInRange(int min, int max) {

        if (min >= max) {
            throw new IllegalArgumentException("max must be greater than min");
        }

        Random r = new Random();
        return r.nextInt((max - min) + 1) + min;
    }

    //Gestion des déplacements des ennemis
    public void ActionEnnemi(){
        for (Ennemi e : listeEnnemis){
            //l'ennemi attaque avant de s'être déplacé
            riposteEnnemi(e);
            //on propose un deplacement aléatoire : soit + 1 soit -1 soit 0 (pas de déplacement) par rapport au déplacement du héro
            int propx = getRandomNumberInRange(-1, 1);
            int propy = getRandomNumberInRange(-1, 1);
            if (propx != 0 && propy != 0){
                int casextempo = e.casex + propx;
                int caseytempo = e.casey + propy;
                if (!depasseBorduregauche(casextempo) && !depasseBordurehaut(casextempo)){ //si ne dépasse pas les bordures de gauche et de droite
                    e.casex = casextempo;
                    e.posx += propx * 32; //mise à jour de la position de l'ennemi - on multiplie par la taille de la tuile
                }
                if (!depasseBordurebas(caseytempo) && !depasseBordurehaut(caseytempo)){ //si ne dépasse pas les bordures du haut et du bas
                    e.casey = caseytempo;
                    e.posy += propy * 32;
                }
            }
        }


    }

    //Gestion de l'affichage des éléments de la carte
    public void paintComponent(Graphics g){

        //Récupération des images
        try {
            imageSable = ImageIO.read(ressourceSable);
            imageGrass = ImageIO.read(ressourceGrass);
            imageEau = ImageIO.read(ressourceEau);
            imageForet = ImageIO.read(ressourceForet);
            imageBrickWall = ImageIO.read(ressourceBrickWall);
            imageBouee = ImageIO.read(ressourceBouee);
            imageBateau = ImageIO.read(ressourceBateau);
            imageEnnemi = ImageIO.read(ressourceEnnemi);



        } catch (Exception e) {
            e.printStackTrace();
        }

        //Draw des surfaces


        //Herbe


        for (int i = 0; i <= 11; i +=1) {
            for (int j = 0; j <= getnbcasevert(); j += 1) {
                g.drawImage(imageGrass, j*32, i*32, 32, 32, this);
            }
        }




        //sable

        for (int i = 10; i <= 12; i +=1) {
            for (int j = 0; j <= getnbcasevert(); j += 1) {
                g.drawImage(imageSable, j*32, i*32, 32, 32, this);
            }
        }

        //eau
        for (int i = 13; i <= getnbcasehoriz(); i += 1) {
            for (int j = 0; j <= getnbcasevert(); j += 1) {
                g.drawImage(imageEau, j*32, i*32, 32, 32, this);
            }
        }






        // draw des objets

        for (Objects obj : this.listeObjet) {
            //System.out.println(obj.getCasex() + " " + obj.getCasey());
            if (obj.getId() == 1) {
                g.drawImage(this.imageBouee, obj.getposx(), obj.getposy(), this);
            }
            if (obj.getId() == 2) {
                g.drawImage(this.imageForet, obj.getposx(), obj.getposy(), this);
            }
            if (obj.getId() == 3) {
                g.drawImage(this.imageBrickWall, obj.getposx(), obj.getposy(), this);
            }
            if (obj.getId() == 4) {
                g.drawImage(this.imageBateau, obj.getposx(), obj.getposy(), this);
            }
        }


        //dessin des ennemis

        for (Ennemi e : listeEnnemis) {
            g.drawImage(this.imageEnnemi, e.getPosx(), e.getPosy(), this);
            g.setColor(new Color(255,0,0));
            g.drawString("" + e.getSante(), e.getPosx(), e.getPosy() +32);
        }




        // Draw du Hero
        g.drawImage(this.imageHero, this.hero.getPosX(), this.hero.getPosY(), this);
        g.setColor(new Color(255,255,255));
        g.setFont(new Font("TimesRoman", Font.PLAIN, 15));
        g.drawString("Energie :" + this.hero.getEnergie(), 0, 32);
        g.drawString("Coups restant :" + compteurcoup, 0, 64);

    }
}