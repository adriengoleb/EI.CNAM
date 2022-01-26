package net.cnam.inf330;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.event.*;
import java.io.FileNotFoundException;
import java.io.IOException;

import static java.awt.image.BufferedImage.TYPE_INT_ARGB;

public class Fenetrejeu extends JFrame{


    public Fenetrejeu(boolean choix){
        this.setTitle("JEU");
        this.setSize(960,640);
        this.setLocationRelativeTo(null);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        Map m = new Map(choix, this);
        // ajout du listener pour le clavier
        m.addKeyListener(m);
        m.setFocusable(true);
        // ajout de la map
        this.add(m);
        // Rendre visible le tout
        this.setVisible(true);
    }


}

