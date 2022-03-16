package java_rewrite;
public class Game_Object {
    int x;
    int xBound;
    int y;
    int yBound;
    String i;
    public Game_Object(int x, int y, String identifier, Map map) {
        this.x = x;
        this.xBound = map.map[0].length;
        this.y = y;
        this.yBound = map.map.length;
        this.i = identifier;
    }

    public void changePos(int dx, int dy) {
        if (0 <= x+dx && x+dx < xBound) {
            this.x += dx;
        }
        if (0 <= y+dy && y+dy < yBound) {
            this.y += dy;
        }
    }
}
