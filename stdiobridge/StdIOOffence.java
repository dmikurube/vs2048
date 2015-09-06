package stdiobridge;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

import main.Offence;


public class StdIOOffence {
    public static void main(String[] args) throws ClassNotFoundException,
                                                  InstantiationException,
                                                  IllegalAccessException,
                                                  IOException {
        if (args.length < 1) { return; }
        Offence o = Offence.class.cast(Class.forName(args[0]).newInstance());

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
            int position = o.offend(field, 0);
            System.out.printf("%d %d %d\n",
                              position % 4,
                              position % 16 / 4,
                              (position / 16 + 1) * 2);
            System.out.flush();
        }
    }
}
