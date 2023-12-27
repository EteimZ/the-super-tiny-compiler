[![The Super Tiny Compiler](https://cloud.githubusercontent.com/assets/952783/21579290/5755288a-cf75-11e6-90e0-029529a44a38.png)](the_super_tiny_compiler.py)

***Welcome to The Super Tiny Compiler!***

This is the python implementation of [the-super-tiny-compiler](https://github.com/jamiebuilds/the-super-tiny-compiler) by [Jamie builds](https://github.com/jamiebuilds).

Head over to his repo to learn how compilers work. If you are interested in getting to build compilers in python read through my source code.

## Usage

The compiler only depends on python.

```bash
python main.py
```

The compiler demonstrates how code written in lisp can compiled to python/javascript.

For example the following source code is presented:

```lisp
(add 2 (subtract 4 2))
```

After going through the compiler it becomes:

```python
add(2, subtract(4, 2))
```

**Note**: This isn't a full lisp to python compiler. It only converts functions calls like the above. It serves as an introduction to the inner workings of compilers.
