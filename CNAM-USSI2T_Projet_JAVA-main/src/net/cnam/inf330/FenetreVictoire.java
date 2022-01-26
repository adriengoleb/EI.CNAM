package net.cnam.inf330;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.event.*;
import java.io.FileNotFoundException;
import java.io.IOException;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class FenetreVictoire extends JFrame implements ActionListener {

    public FenetreVictoire() {
        this.setTitle("Victoire");
        this.setSize(800, 600);
        this.setLocationRelativeTo(null);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setVisible(true);

        //Récupération de l'image
        JPanel pannelvictoire = new JPanel() {
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                //recupère le repertoire courant
                String pwd = System.getProperty("user.dir");
                pwd = pwd.replace("\\", "/");
                ImageIcon m = new ImageIcon(pwd + "/src/net/cnam/inf330/images/imagevictoire.jpg");
                Image monImage = m.getImage();
                g.drawImage(monImage, getX(), getY(), this);
            }};

            //Ajout du bouton dans la fenetre de lancement du jeu
            JButton victoire = new JButton("Rééssaye avec un autre personnage");
            victoire.addActionListener(this);
            pannelvictoire.add(victoire);
            this.add(pannelvictoire);
            this.setContentPane(pannelvictoire);
            this.setVisible(true);

        }

        //Retour au menu
        public void actionPerformed (ActionEvent actionEvent){
            Fenetremenu f = new Fenetremenu();
            this.setVisible(false);
        }
    }
