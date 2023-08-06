c(C) :- ext(C,_).
c(C) :- int(C,_).
smaller(X,Y):- c(X) ; c(Y) ; X!=Y ; ext(X,E): ext(Y,E).
link(X,Z):- smaller(X,Z) ; not link(X,Y): smaller(Y,Z).

annot(upper,X,A):- ext(X,A).
annot(lower,X,B):- int(X,B).
