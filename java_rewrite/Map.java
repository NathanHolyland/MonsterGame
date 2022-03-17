package java_rewrite;
import java.util.ArrayList;
import java.util.Random;
import java.lang.Math;

public class Map {
    String[][] map;
    String[][] permanents;
    int xBound;
    int yBound;
    public Map(int width, int height) {
        String[][] map = new String[width][height];
        for (int i = 0; i < map.length; i++) {
            for (int j = 0; j < map[i].length; j++) {
                map[i][j] = "_";
            }
        }
        this.map = map;
        this.xBound = width-1;
        this.yBound = height-1;
    }

    public void draw(int x, int y, String i) {
        map[y][x] = i;
    }

    public void clear() {
        for (int i = 0; i < this.map.length; i++) {
            for (int j = 0; j < this.map[0].length; j++) {
                this.map[i][j] = this.permanents[i][j];
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

    public void generateMaze() {
        ArrayList<int[]> nodes = new ArrayList<>();
        for (int r = 0; r < this.map.length; r++) {
            for (int c = 0; c < this.map[0].length; c++) {
                if (r%2 == 1 && c%2 == 1) {
                    map[r][c] = "_";
                    int[] node = new int[2];
                    node[0] = r;
                    node[1] = c;
                    nodes.add(node);
                    continue;
                }
                map[r][c] = "#";
            }
        }
        Random rand = new Random();
        int randomIndex = rand.nextInt(nodes.size());
        ArrayList<int[]> visited = new ArrayList<>();
        int[] current = nodes.get(randomIndex);
        visited.add(current);

        while (visited.size() < nodes.size()) {
            System.out.println("Loop");
            ArrayList<int[]> nextNodes = new ArrayList<>();
            for (int dx = -2; dx <= 2; dx += 2) {
                for (int dy = -2; dy <= 2; dy += 2) {
                    int[] next_node = new int[2];
                    next_node[0] = current[0]+dx;
                    next_node[1] = current[1]+dy;
                    System.out.println(String.valueOf(next_node[0])+" "+String.valueOf(next_node[1]));
                    if (Math.abs(dy) == Math.abs(dx)) {
                        continue;
                    }
                    if (next_node[0] < 0 || next_node[0] > this.xBound || next_node[1] < 0 || next_node[1] > this.yBound) {
                        continue;
                    }
                    if (visited.contains(next_node)) {
                        continue;
                    }
                    nextNodes.add(next_node);
                }
            }
            if (nextNodes.size() == 0) {
                current = visited.get(visited.indexOf(current)-1);
                continue;
            }
            randomIndex = rand.nextInt(nextNodes.size());
            int[] choice = nextNodes.get(randomIndex);
            int dx = choice[0] - current[0];
            int dy = choice[1] - current[1];
            int[] wall = {current[0] + dx/2, current[1] + dy/2};
            this.map[wall[1]][wall[0]] = "_";
            current = choice;
            visited.add(current);
        }
        this.permanents = map.clone();
    }
}