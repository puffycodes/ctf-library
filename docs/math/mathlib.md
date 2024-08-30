# Documentation for MathLib

## Class MathLib

1. Some common math functions implemented using algorithms found on the Internet. (See [Reference](#references))

## Usage

```
from ctf_library.math.mathlib import MathLib
```

## Functions

1. MathLib.gcd(a, b): Returns the greatest common divisor (GCD) of a and b.
1. MathLib.xgcd(a, b): Returns g, x and y where g = gcd(a, b) and g = ax + by.
1. MathLib.lcm(a, b): Returns the least common muliple (LCM) of a and b.
1. MathLib.pow(x, n): Returns x ** n for a positive integer n where n >= 0.
    - [Known Issue](../known_issues.md#known-issues): x must be an integer. 

## Python Native Implementation

Python has native implementations for many of these functions.

1. MathLib.gcd(a, b): Use math.gcd(a, b) for Python 3.5 and above.
1. MathLib.lcd(a, b): Use math.lcm(a, b) for Python 3.9.0 and above.
1. MathLib.pow(x, n): Use Python built-in function pow(x, n).

## References

1. References are listed in the [source code](../../ctf_library/math/mathlib.py).

***
*Updated on 30 August 2024*
