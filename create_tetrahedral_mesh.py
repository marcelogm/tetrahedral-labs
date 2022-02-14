import pyvista as pv
import tetgen
import numpy as np
import meshio

sphere = pv.read('objects/pipe_12v.obj')
tet = tetgen.TetGen(sphere)
tet.tetrahedralize(order=1, mindihedral=2, minratio=1.5)
grid = tet.grid
grid.save('pipe_12v.vtk')

mesh = meshio.read('pipe_12v.vtk')
meshio.write('pipe_12v.node', mesh)