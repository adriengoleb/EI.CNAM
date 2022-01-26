package net.cnam.inf330;

import javax.swing.*;
import java.awt.*;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Fenetregameover extends JFrame implements ActionListener {
    public Fenetregameover(){


        this.setTitle("Game Over");
        this.setSize(800, 600);
        this.setLocationRelativeTo(null);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        //Récupération de l'image
        JPanel panelgameover = new JPanel()
        {
            protected void paintComponent(Graphics g)
            {
                super.paintComponent(g);
                //recupère le repertoire courant
                String pwd = System.getProperty("user.dir");
                pwd = pwd.replace("\\", "/");
                ImageIcon m = new ImageIcon(pwd + "/src/net/cnam/inf330/images/gameover.jpg");
                Image monImage = m.getImage();
                g.drawImage(monImage,getX(),getY(),this);

            }
        };

        //Ajout du bouton dans la fenetre de lancement du jeu
        JButton gameover = new JButton("Retente ta chance");
        gameover.addActionListener(this);
        panelgameover.add(gameover);
        this.add(panelgameover);
        this.setContentPane(panelgameover);
        this.setVisible(true);

    }
    //Retour au menu
    public void actionPerformed(ActionEvent e) {
        Fenetremenu f = new Fenetremenu();
        this.setVisible(false);
    }
}
