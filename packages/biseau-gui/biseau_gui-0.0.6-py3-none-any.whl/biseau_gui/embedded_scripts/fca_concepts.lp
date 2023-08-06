ext(X) :- rel(X,_) ; rel(X,Y): int(Y).
int(Y) :- rel(_,Y) ; rel(X,Y): ext(X).
