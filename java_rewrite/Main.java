package java_rewrite;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Map grid = new Map(10, 10);
        boolean running = true;
        Scanner scan = new Scanner(System.in);

        Game_Object player = new Game_Object(0, 0, "P", grid);

        while (running) {
            grid.draw(player.x, player.y, player.i);
            grid.display();
            String userInput = scan.nextLine();
            switch(userInput) {
                case "w":
                    player.changePos(0, -1);
                    break;
                case "a":
                    player.changePos(-1, 0);
                    break;
                case "s":
                    player.changePos(0, 1);
                    break;
                case "d":
                    player.changePos(1, 0);
                    break;
            }
            grid.clear();
        }
        scan.close();
    }
}