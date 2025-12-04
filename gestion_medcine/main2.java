main2.java
import javax.swing.*;
import java.awt.*;

public class CorrectionExerciceGridPane extends JFrame {

    public CorrectionExerciceGridPane() {
        setTitle("Exercice supplémentaire - Grilles");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLocationRelativeTo(null);

        // Panel principal divisé en deux (gauche / droite)
        JPanel mainPanel = new JPanel(new GridLayout(1, 2, 10, 10));
        mainPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Partie gauche : 3 grilles empilées
        JPanel leftPanel = new JPanel(new GridLayout(3, 1, 10, 10));
        leftPanel.setBorder(BorderFactory.createTitledBorder("Schémas"));

        // Grille 1 : 2x2
        JPanel grid1 = new JPanel(new GridLayout(2, 2, 5, 5));
        grid1.setBorder(BorderFactory.createTitledBorder("Grille 2x2"));
        for (int i = 1; i <= 4; i++) {
            grid1.add(new JLabel("Cell " + i, SwingConstants.CENTER));
        }

        // Grille 2 : 3x3
        JPanel grid2 = new JPanel(new GridLayout(3, 3, 5, 5));
        grid2.setBorder(BorderFactory.createTitledBorder("Grille 3x3"));
        for (int i = 1; i <= 9; i++) {
            grid2.add(new JLabel("C" + i, SwingConstants.CENTER));
        }

        // Grille 3 : 1x4
        JPanel grid3 = new JPanel(new GridLayout(1, 4, 5, 5));
        grid3.setBorder(BorderFactory.createTitledBorder("Grille 1x4"));
        for (int i = 1; i <= 4; i++) {
            grid3.add(new JLabel("Case " + i, SwingConstants.CENTER));
        }

        leftPanel.add(grid1);
        leftPanel.add(grid2);
        leftPanel.add(grid3);

        // Partie droite : grande grille (fig. à droite)
        JPanel rightPanel = new JPanel(new BorderLayout());
        rightPanel.setBorder(BorderFactory.createTitledBorder("Fenêtre de la figure (Grille principale)"));

        JPanel bigGrid = new JPanel(new GridLayout(4, 4, 5, 5));
        for (int row = 0; row < 4; row++) {
            for (int col = 0; col < 4; col++) {
                JLabel cell = new JLabel("R" + (row + 1) + "C" + (col + 1), SwingConstants.CENTER);
                cell.setBorder(BorderFactory.createLineBorder(Color.BLACK));
                bigGrid.add(cell);
            }
        }

        rightPanel.add(bigGrid, BorderLayout.CENTER);

        // Ajout des deux parties au mainPanel
        mainPanel.add(leftPanel);
        mainPanel.add(rightPanel);

        add(mainPanel);
        setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new CorrectionExerciceGridPane();
        });
    }
}