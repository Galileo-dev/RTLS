
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/spacex/25254688767/in/photostream/" title="Falcon Heavy Demo Mission"><img src="https://farm5.staticflickr.com/4654/25254688767_83c0563d06_b.jpg" width="800" height="534" alt="Falcon Heavy Demo Mission"></a>

# G-FOLD Python
### Guidance for Fuel Optimal Landing Diverts (GFOLD)

This code reimplements GFOLD algorithm in Python with use of the fantastic cvxpy utility. The algorithm was defined by a number of papers, but chiefly [this paper by Ackimese, Carson, and Blackmore at JPL.](http://www.larsblackmore.com/iee_tcst13.pdf)

### What you can do with GFOLD-Python

- Calculate fuel optimal spacecraft landing trajectories
- Generate embeddable C code for real-time trajectory calculation (~0.3 second calculation time 1x 2.4GHz)
- [Autonomous landing of Kerbal Space Program rockets](https://www.youtube.com/watch?v=7skZHu9i7Fg)

### What you can't do with GFOLD-Python

- Attitude control
- Robust control
- Control of any kind (this is a guidance algorithm!)

### How to use it

- If you wish to do a static calculation (not generating C code)
  1. Define your vehicle and environment in GFOLD_Static_Parms
    - All notation follows conventions laid out in the [original paper](http://www.larsblackmore.com/iee_tcst13.pdf)
  2. Comment / Uncomment the constraints you wish to have in GFOLD_Static
  3. Run `python GFOLD_Static.py` *(requires scipy)*
  4. View the "evil" plots *(this name is just a joke btw)*


- If you wish to do C code generation
    1. Set `test = 0` at the top of `GFOLD_Generate.py`
    3. Run `python GFOLD_Generate.py` *(requires cvxpy_codegen)*
    3. Fix some of the known-bugs cvxpy_codegen creates
      - See issues page of the repo
      - Attempt to compile, and solve each error as they come
    4. Compile the generated C code
    5. *(Optional:)* Install the compiled CPython code into your Python distribution with setup.py if you wish to use the compiled code from Python
      - Be aware that the Python2.7 Windows Compiler provided by Microsoft will not work because it has a pathetically tiny stack heap size. Recommend using MinGW on Windows!

### Documentation

- Since this is a pre-alpha research project, the main documentation is found in `#code comments`, and in the content of the [paper](http://www.larsblackmore.com/iee_tcst13.pdf) itself.

### Requirements

  - Python 2.7 *(I'm sorry about still using python 2, Mr. Guido, but cvxpy_codegen is the constraint here...)*
  - scipy (for static solutions)
  - cvxpy (for static solutions)
  - cvxpy_codegen (for code generation)

### License
GPLv3, copyleft license.

Chose this license because I spent way too many late nights and heartbeats working on this - and want to see what people do with it and have changes propagated forward!
