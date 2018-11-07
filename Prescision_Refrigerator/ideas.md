**Different convergence methods**

Standard on/off

Hysteretic loop, different for heating than for cooling.

What ever this is, https://docs.sympy.org/0.7.1/modules/mpmath/functions/hypergeometric.html

scipy optimize. minimize?

Use these then compare run times to cool from a temp to another. (relative to room tmp)

**Cooling efficency**

Compare the energy used from the voltage and time to find the exp heat capacity and compare this to a known heat capacity of water.

**Convergence Rate**

https://en.wikipedia.org/wiki/Rate_of_convergence

http://hplgit.github.io/Programming-for-Computations/pub/p4c/._p4c-solarized-Python030.html
```python
def rate(x, x_exact):
    e = [abs(x_ - x_exact) for x_ in x]
    q = [log(e[n+1]/e[n])/log(e[n]/e[n-1])
         for n in range(1, len(e)-1, 1)]
    return q
```

https://en.wikipedia.org/wiki/Rate_of_convergence

Have one them to measure the room tmp as a refference then compare if heating or cooling relative to room tmp.
