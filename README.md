vs2048
======

    % ./vs2048.py [-v] -o (offender command line) -d (defender command line)

E.g.

    % ./vs2048.py -v -o python offender.py -d python defender.py


stdiobridge
-----------

Java classes under stdiobridge/ bridge players of the original 2048 battle into this vs2048.

E.g.

    % javac -cp .:(original/2048/src) stdiobridge/*

    % ./vs2048.py -v -o java -cp .:(original/2048/src) stdiobridge.StdIOOffence sample.MinimaxOffence -d java -cp .:(original/2048/src) stdiobridge.StdIODefence sample.GreedyDefence
