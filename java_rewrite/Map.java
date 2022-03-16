package java_rewrite;

public class Map {
    String[][] map;
    public Map(int width, int height) {
        String[][] map = new String[width][height];
        for (int i = 0; i < map.length; i++) {
            for (int j = 0; j < map[i].length; j++) {
                map[i][j] = "_";
            }
        }
        this.map = map;
    }

    public void draw(int x, int y, String i) {
        map[y][x] = i;
    }

    public void clear() {
        for (int i = 0; i < this.map.length; i++) {
            for (int j = 0; j < this.map[i].length; j++) {
                map[i][j] = "_";
            }
        }
    }

    public void display() {
        for (String[] row : this.map) {
            for (String element : row) {
                System.out.printf(" "+element+" ");
            }
            System.out.println();
        }
    }
}