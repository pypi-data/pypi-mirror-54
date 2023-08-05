# keylimepy
Python tools to run and analyse LIME models.

## Installation

```bash
git clone git@gitlab.com:SmirnGreg/keylimepie.git
cd keylimepie
python setup.py develop
sed 's/.\{4\}$//' <<< `which lime`  # get path to lime 
cp keylime /path/to/lime  # your path to lime is probably different. 
```

It will create symbolic links of the library into your python distribution. Additionally, 
you will have to copy `keylime` executable to the LIME installation folder. 
`keylime` creates an empty folder `LIME_IS_COMPILING` that prevents another instance of 
LIME to mess with it. 

## Update

```bash
cd keylimepie
git pull
```

## Usage

As an entrypoint, check `keylimepie.cluster.slurm.run`. 
We also provide `skeylimepie` slurm batch script that 
runs [`fire`](https://google.github.io/python-fire/)
interface to `keylimepie`.

Example of `skeylimepie`:
```
sbatch skeylimepie --molecule=HCO+ --transitions='[2,3,4]' --incl_deg='[0,20,60]' --name_suffix="
test"
```
Requires `HCO+_structure.h` in working directory, generates files `HCO+_test_...fits` for transitions 3-2, 4-3, 5-4 and 
inclinations 0, 20, 60 degrees. 

Do not Ctrl-C while `keylime` is running! If `keylime` shows 
`If you don't run other instances of lime, remove  /path/to/lime/LIME_IS_COMPILING manually`, 
do the following:

```bash
cd /path/to/lime
make clean && rm -rf LIME_IS_COMPILING   
```

## Notes
Please take into account that the following README was written for the obsolete version of
`limepy`. Currently, the modified version of `limepy`, namely `keylimepie`
is introduced. The main feature set is a modified `lime` executable `keylime` which 
locks the lime folder during the compilation. Thus `keylimepie` works fine with
clusters ~~not really~~. 

## Input
Requires a header file readable by C containing (at least) the arrays named
`c1arr`, `c2arr`, `dens`, `temp` and `abund` where the first two are either the
cylindrical coordinates (r, z) or polar coordinates (r, theta). A third
dimension can be added with `c3arr`, which is the azimuthal angle. With this,
`limepy` will write the necessary `model.c` files and execute them.


## Running
A standard call will be something like:

```python
from keylimepie import run_model

run_model(headerfile='header.h',
          name='filenames',
          moldatfile='13co.dat',
          transitions=[1, 2, 3],
          incl=[0.4], # in radians!
          )
```

Most of the variables from LIME are able to be included. If lists of
transitions, inclinations or position angles, all permutations will be made.


In order to increase the signal to noise of the data, one can run several
models and then average over them using the `nmodels` keyword.

## Authors

Richard Teague.
Grigorii V. Smirnov-Pinchukov.