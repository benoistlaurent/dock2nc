=======
dock2nc
=======

A package to convert ASCII docking files to NetCDF files.

It merges the 2 PDB files and the docking data file into a single binary NetCDF
file. It reduces the number of I/O operation required to analyze docking
results.

dock2nc allows to convert docking files one at the time or entire archives
all at once (see the `Example usage`_ section).

dock2nc expects Protein Data Bank (PDB) files to be provided as a tar
archive (tarball).
See section `Input archives`_ for details and command-line examples to create
those input tarballs.


Dependencies
------------

- netcdf4
- numpy
- `mollib`_ 
  

Input archives
--------------

dock2nc can read tarballs.
It is important to known that when a tarball is given in input, dock2nc
expects the files to be at the root of the tarball.

As an example, this is how one would create an input tarball containing PDB
files::

    $ cd /path/to/pdbfiles/directory
    $ tar cf archive.tar *.pdb

The same prevails for docking files.


Example usage
-------------

* Single docking file convertion::

    $ dock2nc GATMA--1ZET_A--reformatted.dat.bz2 pdbfiles.tar

* Convert an archive full of docking files:

    $ dock2nc dockingfiles.tar pdbfiles.tar


.. _mollib: https://bitbucket.org/lvamparys/mollib