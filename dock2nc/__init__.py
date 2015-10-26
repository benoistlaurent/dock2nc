
"""
Create docking file in netCDF format.

netCDF file will contain both PDB data as well as docking data.
"""


from __future__ import print_function
import mollib
import netCDF4
import numpy as np
import os
import tarfile
import time

import version
__version__ = version.VERSION


def create_variable(name, type, dims, root, data, **kwargs):
    dim_names = tuple(dim.name for dim in dims)
    var = root.createVariable(name, type, dim_names, **kwargs)
    if type.startswith('S') and len(dims) > 1:
        data = strlist_to_netcdf(data, dims)
    var[:] = data


def strlist_to_netcdf(a, dim=None):
    """Convert a list of strings to a netCDF4 chararray.

    Arguments:
        a: a list of strings
        dim (optionnal): netCDF4 dimensions

    Returns:
        netCDF4 chararray
    """
    if dim is None:
        dim = (len(a), max(len(s) for s in a))
    else:
        dim = tuple(len(d) for d in dim)
    array = np.chararray(dim)
    array[:] = [list(s.ljust(dim[1])) for s in a]
    return netCDF4.stringtochar(array)


def dockingfile_to_nc(dockingfilename, ncfile, groupname):
    data = mollib.pdbbuilder.DockingList(dockingfilename)
    group = ncfile.createGroup(groupname)
    dim_npositions = group.createDimension('Npositions', data.Npositions)
    dim_rotation = group.createDimension('Rotation_dim', 6)

    comp_opts = {'zlib': True, 'complevel': 9}

    create_variable('Npos', 'i4', (dim_npositions, ), root=group,
                    data=data.Npos, **comp_opts)
    create_variable('Nrot', 'i4', (dim_npositions, ), root=group,
                    data=data.Nrot, **comp_opts)
    create_variable('Elj', 'f4', (dim_npositions, ), root=group,
                    data=data.Elj, **comp_opts)
    create_variable('Ecoul', 'f4', (dim_npositions, ), root=group,
                    data=data.Ecoul, **comp_opts)
    create_variable('Etot', 'f4', (dim_npositions, ), root=group,
                    data=data.Etot, **comp_opts)
    create_variable('New_position', 'f4', (dim_npositions, dim_rotation), root=group,
                    data=data.New_position, **comp_opts)

    group['Elj'].description = 'Lennard-Jones energy'
    group['Ecoul'].description = 'Coulomb energy'
    group['Etot'].description = 'Total energy'
    group['Elj'].units = 'kcal/mol'
    group['Ecoul'].units = 'kcal/mol'
    group['Etot'].units = 'kcal/mol'


def mol_to_nc(mol, ncfile, groupname):
    group = ncfile.createGroup(groupname)

    dim_spatial = group.createDimension('Dim3D', 3)
    dim_natoms = group.createDimension('Natoms', len(mol))
    dim_record = group.createDimension('LenRecord', 6)
    dim_atomname = group.createDimension('LenAtomName', 4)
    dim_resname = group.createDimension('LenResName', 3)
    dim_element = group.createDimension('LenElementName', 2)

    comp_opts = {'zlib': True, 'complevel': 9}

    create_variable('record', 'S1', (dim_natoms, dim_record), root=group,
                    data=[a.rec for a in mol], **comp_opts)

    create_variable('name', 'S1', (dim_natoms, dim_atomname), root=group,
                    data=[a.name for a in mol], **comp_opts)

    create_variable('resname', 'S1', (dim_natoms, dim_resname), root=group,
                    data=[a.resname for a in mol], **comp_opts)

    create_variable('element', 'S1', (dim_natoms, dim_element), root=group,
                    data=[a.element for a in mol], **comp_opts)

    create_variable('chain', 'S1', (dim_natoms, ), root=group,
                    data=[a.chain for a in mol], **comp_opts)

    create_variable('altloc', 'S1', (dim_natoms, ), root=group,
                    data=[a.altloc for a in mol], **comp_opts)

    create_variable('icode', 'S1', (dim_natoms, ), root=group,
                    data=[a.icode for a in mol], **comp_opts)

    create_variable('resid', 'i4', (dim_natoms, ), root=group,
                    data=[a.resid for a in mol], **comp_opts)

    create_variable('atomid', 'i4', (dim_natoms, ), root=group,
                    data=[a.index for a in mol], **comp_opts)

    create_variable('bfactor', 'f4', (dim_natoms, ), root=group,
                    data=[a.b for a in mol], **comp_opts)

    create_variable('occupancy', 'f4', (dim_natoms, ), root=group,
                    data=[a.occ for a in mol], **comp_opts)

    create_variable('xyz', 'f4', (dim_natoms, dim_spatial), root=group,
                    data=[(a.x, a.y, a.z) for a in mol], **comp_opts)

    group['record'].description = 'record (ATOM or HETATM)'
    group['name'].description = 'atom name'
    group['resname'].description = 'residue name'
    group['element'].description = 'element symbol'
    group['chain'].description = 'chain identifier'
    group['altloc'].description = 'alternate location indicator'
    group['icode'].description = 'chain identifiers'
    group['resid'].description = 'chain identifiers'
    group['atomid'].description = 'code for insertion of residues'
    group['bfactor'].description = 'temperature factor'
    group['occupancy'].description = 'occupancy'
    group['xyz'].description = '3d coordinates'


def read_pdb_from_tar(pdbid, tar):
    pdbname = '{}.pdb'.format(pdbid)
    stream = tar.extractfile(pdbname)
    return mollib.mymolecule.read_pdb(stream, name=pdbname)


def today():
    """Return formatted current date and time."""
    return time.strftime('%Y-%m-%d %H:%M:%S')


def convert(dockingfilename, pdbfilestarname, outputdir):
    """Convert an old docking file to a new docking file.

    New docking file is in netCDF 4 format.
    It includes both PDB files and old docking file data.

    Arguments:
        dockingfilename: path to input docking file
        pdbfilestarname: path to tarball containing all PDB files
    """
    prefix = os.path.basename(dockingfilename).split('.')[0]
    pdbid1, pdbid2 = prefix.split('--')[:2]

    tar = tarfile.open(pdbfilestarname, 'r')

    # Open output netCDF file.
    fname = '{}--{}.nc'.format(pdbid1, pdbid2)
    fname = os.path.join(outputdir, fname)
    ncfile = netCDF4.Dataset(fname, mode='w', format='NETCDF4')
    ncfile.history = 'Created on {}'.format(today())

    # Save molecule 1 to nc.
    mol1 = read_pdb_from_tar(pdbid1, tar)
    mol_to_nc(mol1, ncfile, groupname='pdb1')

    # Save molecule 2 to nc.
    mol2 = read_pdb_from_tar(pdbid2, tar)
    mol_to_nc(mol2, ncfile, groupname='pdb2')

    # Save docking file to nc.
    dockingfile_to_nc(dockingfilename, ncfile, groupname='dockingfile')

    # Close files.
    ncfile.close()
    tar.close()


def main():
    convert('test/GATMA--1ZET_A--reformatted.dat',
            'test/pdbfiles.tar',
            '.')


if __name__ == '__main__':
    main()
