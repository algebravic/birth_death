A Birth-Death Process in Binary Trees
=====================================

In Kochman-Miller ("A Birth Death process in binary trees") the
following Markov Chain is considered:

The states are all rooted binary trees, plus the empty tree.
Each node of the tree has two "slots" which are either empty
or filled.  The transitions are as follows:

For each node that has 0 or 1 children, independently, with
probability $p$, each empty slot will then become the root of a tree
with two children.  However, if a node with 0 children fails to fill
in both slots it then "dies", freeing up the slot that it lives in.
We are interested in the long term behavior of this Markov Chain.

There are three possible behavior: *positive recurrent*, *null
recurrent*, or *transient*.  We Recall the definitions: If $M$ is a
countable Markov Chain started in state `$s_0$`, we can define a
random variable $T$ which is the time (number of steps) that it takes
for $M$ to return to state `$s_0$`. The chain $M$ is *recurrent* if
$\lim_{k \rightarrow \infty}\Pr(T \le k) = 1$ (i.e. $M$ almost surely
returns to `$s_0$`). It is *positive recurrent* if $E(T) < \infty$,
and *null recurrent* otherwise. If it is not recurrent, it is said to
be *transient*.
