package net.cnam.inf330;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class FenetreChoixGuerrier extends JFrame implements ActionListener {

    boolean choix; //entre le héros 1 et le héros 2

    public FenetreChoixGuerrier() {
        this.setTitle("Choix du personnage");
        this.setSize(800, 600);
        this.setLocationRelativeTo(null);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        JLabel titre = new JLabel("Choisis ton personnage");
        titre.setHorizontalAlignment(JLabel.CENTER);
        JSplitPane sp = new JSplitPane(JSplitPane.VERTICAL_SPLIT);

        // côté gauche de la fenêtre

        //Ajout des caractères
        JPanel panneauRacine = new JPanel(new GridLayout(6, 2));
        JLabel Caract1 = new JLabel("Vélocité 1 : 50");
        Caract1.setHorizontalAlignment(JLabel.CENTER);
        JLabel Caract2 = new JLabel("Attaque 2 : 50");
        Caract2.setHorizontalAlignment(JLabel.CENTER);
        JLabel Caract3 = new JLabel("Energie : 100");
        Caract3.setHorizontalAlignment(JLabel.CENTER);
        JLabel Caract4 = new JLabel("Aptitude : nager");
        Caract4.setHorizontalAlignment(JLabel.CENTER);

        //Ajout du boutton 1
        JButton choisir1 = new JButton("Choisir le personnage 1");
        choisir1.addActionListener(this);

        //Récupération de l'image
        String pwd = System.getProperty("user.dir");
        pwd = pwd.replace("\\", "/");
        Icon img = new ImageIcon(pwd + "/src/net/cnam/inf330/images/Hero1.png");
        JLabel hero = new JLabel();
        hero.setHorizontalAlignment(JLabel.CENTER);
        hero.setIcon(img);

        //Côté droit de la fenêtre

        //Ajout des caractères
        JLabel Caract1d = new JLabel("Vélocité : 50");
        Caract1d.setHorizontalAlignment(JLabel.CENTER);
        JLabel Caract2d = new JLabel("Attaque : 50");
        Caract2d.setHorizontalAlignment(JLabel.CENTER);
        JLabel Caract3d = new JLabel("Energie : 100");
        Caract3d.setHorizontalAlignment(JLabel.CENTER);
        JLabel Caract4d = new JLabel("Aptitude : voler");
        Caract4d.setHorizontalAlignment(JLabel.CENTER);

        //Ajout du boutton 2
        JButton choisir2 = new JButton("Choisir le personnage 2");
        choisir2.addActionListener(this);

        //Récupération de l'image
        Icon imgd = new ImageIcon(pwd + "/src/net/cnam/inf330/images/Hero2.png");
        JLabel herod = new JLabel();
        herod.setHorizontalAlignment(JLabel.CENTER);
        herod.setIcon(imgd);

        // Ajout des deux images + texte + boutons dans le jpannel
        panneauRacine.add(hero);
        panneauRacine.add(herod);
        panneauRacine.add(Caract1);
        panneauRacine.add(Caract1d);
        panneauRacine.add(Caract2);
        panneauRacine.add(Caract2d);
        panneauRacine.add(Caract3);
        panneauRacine.add(Caract3d);
        panneauRacine.add(Caract4);
        panneauRacine.add(Caract4d);
        panneauRacine.add(choisir1);
        panneauRacine.add(choisir2);

        // Ajout du jpannel et du titre dans le split pane
        sp.add(titre);
        sp.add(panneauRacine);

        // Ajout dans le conteneur
        this.setContentPane(sp);
        this.setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {


        //Du choix du guerrier 1 vers le jeu
        if (((JButton) e.getSource()).getText() == "Choisir le personnage 1") {
            choix = false;
            net.cnam.inf330.Fenetrejeu j = new net.cnam.inf330.Fenetrejeu(choix);
            this.setVisible(false);
        }

        //Du choix du guerrier 2 vers le jeu
        if (((JButton) e.getSource()).getText() == "Choisir le personnage 2") {
            choix = true;
            net.cnam.inf330.Fenetrejeu j = new net.cnam.inf330.Fenetrejeu(choix);
            this.setVisible(false);

        }
    }

}
