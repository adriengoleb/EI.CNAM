package net.cnam.inf330;

import javax.swing.*;
import java.awt.*;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


public class Fenetremenu extends JFrame implements ActionListener {

    public Fenetremenu() {

        this.setTitle("Menu");
        this.setSize(800, 600);

        // Ajout du panel constitué de l'image
        JPanel panel = new JPanel()
        {
            protected void paintComponent(Graphics g)
            {
                super.paintComponent(g);
                //recupère le repertoire courant
                String pwd = System.getProperty("user.dir");
                pwd = pwd.replace("\\", "/");
                ImageIcon m = new ImageIcon(pwd + "/src/net/cnam/inf330/images/imagemenu2.jpg");
                Image monImage = m.getImage();
                g.drawImage(monImage,getX(),getY(),this);


            }
        };

        //Implémentation d'un menu

        JMenuBar barreMenu = new JMenuBar();
        JMenu menuFichier = new JMenu("Menu");
        JMenu menuAide = new JMenu("Aide");

        //Implémentation des items
        JMenuItem itemQuitter = new JMenuItem("Quitter");
        itemQuitter.addActionListener(e -> System.exit(0));
        JMenuItem itemAPropos = new JMenuItem("À propos...");
        itemAPropos.addActionListener(e -> JOptionPane.showMessageDialog(this, "Touche directionnel du clavier pour se diriger, touche \"A\" pour attaquer l'ennemi, \"R\" pour se soigner ", "Aide",
                JOptionPane.INFORMATION_MESSAGE));

        //Ajout des items dans le menu
        menuFichier.add(itemQuitter);
        menuAide.add(itemAPropos);
        barreMenu.add(menuFichier);
        barreMenu.add(menuAide);

        //Ajout des boutons dans la fenetre de lancement du jeu
        JButton jouer = new JButton("Nouvelle partie");
        jouer.addActionListener(this);
        JButton quitter = new JButton("Quitter");
        quitter.addActionListener(e -> System.exit(0));
        panel.add(jouer);
        panel.add(quitter);
        this.setContentPane(panel);

        //ajout du menu dans la fenêtre de lancement du jeu
        this.setJMenuBar(barreMenu);
        this.setLocationRelativeTo(null);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {

        //Du menu vers le choix du guerrier
        if (((JButton)e.getSource()).getText()=="Nouvelle partie") {
            System.out.println("toto");
            FenetreChoixGuerrier j = new FenetreChoixGuerrier();
            this.setVisible(false);
        }
    }
}


