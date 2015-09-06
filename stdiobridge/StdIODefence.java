package stdiobridge;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

import main.Defence;
import main.Direction;


public class StdIODefence {
    public static void main(String[] args) throws ClassNotFoundException,
                                                  InstantiationException,
                                                  IllegalAccessException,
                                                  IOException {
        if (args.length < 1) { return; }
        Defence d = Defence.class.cast(Class.forName(args[0]).newInstance());

        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        while (true) {
            String command = in.readLine();
            if (command.trim().equals("quit")) {
                break;
            }

            int field[] = new int[16];
            int cur = 0;
            for (int i = 0; i < 4; ++i) {
                String[] cells = in.readLine().split(" ");
                for (String cell: cells) {
                    field[cur++] = Integer.parseInt(cell);
                }
            }
            Direction direction = d.defend(field, 0);
            switch (direction) {
            case UP:
                System.out.println("north");
                break;
            case DOWN:
                System.out.println("south");
                break;
            case RIGHT:
                System.out.println("east");
                break;
            case LEFT:
                System.out.println("west");
                break;
            }
            System.out.flush();
        }
    }
}
