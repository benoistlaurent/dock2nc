
from numpy.distutils.core import setup, Extension


VERSION = '1.0.0'


def write_version(fname, version):
    with open(fname, 'wt') as f:
        print >> f, "VERSION = '{}'".format(version)


write_version('dock2nc/version.py', VERSION)

core = Extension(name='_core',
                 sources=['src/core.f90'])

setup(name='dock2nc',
      version=VERSION,
      description='Convert ASCII docking files to netCDF.',
      author='Benoist LAURENT',
      author_email='benoist.laurent@gmail.com',
      packages=['dock2nc'],
      scripts=['scripts/dock2nc'],
      license='GPL')
