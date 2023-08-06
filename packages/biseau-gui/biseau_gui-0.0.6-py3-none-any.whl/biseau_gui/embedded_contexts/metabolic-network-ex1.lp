reaction(z,r0,(a;b;c)).
reaction((a;b;c),r1,(d;e;f)). reversible(r1).
reaction((d;e;f),r2,(g;h)).
reaction(g,r3,i).
reaction(i,r4,j).
reaction(j,r5,g).
reaction(h,r6,k).
reaction(k,r7,l).
reaction(l,r8,h).
reaction((j;k),r9,m).
