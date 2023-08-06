% Printing of metabolic networks encoded by reaction/3 atoms.
%  reaction(X,R,Y): metabolite X is reactant of reaction R, which produce Y.
%  reversible(R): reaction R is reversible.
%  seed(S): metabolite S is a seed.
% OUTPUTS:
%  scope(S): metabolite S is in the scope.
%  color/2, link/2, shape/2, obj_property/3, dot_property/4

link(X,Y) :- reaction(_,X,Y).
link(X,Y) :- reaction(X,Y,_).
shape(X,rectangle) :- reaction(_,X,_).


% Arrows on edges
obj_property(edge,arrowhead,none).  % default case
dot_property(R,Y,arrowhead,normal) :- reaction(_,R,Y).
dot_property(X,R,dir,both) :- reaction(X,R,_) ; reversible(R).
dot_property(X,R,arrowtail,normal) :- reaction(X,R,_) ; reversible(R).

% biseau:option: all arrows: print arrows on all edges
dot_property(X,R,arrowhead,normal) :- reaction(X,R,_).
% end option.

% biseau:option: LR: left-right orientation of the graph
obj_property(graph,rankdir,"LR").
% end option.

% COLORING
color(X,green) :- seed(X).
% biseau:option: show scope: color the scope in blue
scope(X) :- seed(X).
scope(R;Y) :- reaction(_,R,Y) ; scope(X): reaction(X,R,_).
color(X,blue) :- scope(X) ; not seed(X).
% else:
%obj_property(node,fillcolor,white).
% end option.
