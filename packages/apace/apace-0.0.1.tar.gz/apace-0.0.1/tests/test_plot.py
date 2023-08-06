import apace as ap
from apace.plot import plot_lattice

import os

dir_name = os.path.dirname(__file__)
file_path = os.path.join(dir_name, 'data', 'lattices', 'FODO-lattice.json')


def test_plot():
    line = ap.read_lattice_file(file_path)
    twiss = ap.Twiss(line)

    plot_lattice(twiss, line, eta_x_scale=1, path=os.path.join(dir_name, '/tmp/out.pdf'))


