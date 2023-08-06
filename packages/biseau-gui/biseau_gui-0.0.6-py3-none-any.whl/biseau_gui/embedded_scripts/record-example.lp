% Example of a node a that will be transformed as a dot record
%  using vocabulary introduced by record.py biseau script.
node(a).
record(a,"Animal").
record(a,1,"+ name : string").  % at level 1
record(a,1,"+ age : int").      % at level 1
record(a,2,"+ die() : void").   % at level 2
