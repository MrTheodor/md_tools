"""
Copyright (C) 2015 Jakub Krajniak <jkrajniak@gmail.com>

This file is distributed under free software licence:
you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import h5py
import numpy as np

from matplotlib import pyplot as plt


def _args():
    parser = argparse.ArgumentParser(description='Plots observables from H5MD file.')
    parser.add_argument('h5file')
    parser.add_argument('-b', '--begin', help='Begin frame', default=0, type=int)
    parser.add_argument('-e', '--end', help='End frame', default=-1, type=int)

    return parser.parse_args()


def _print_observables(observables):
    print('Observables:')
    for i, key in enumerate(observables, 1):
        print('{} - {}'.format(i, key))

    print('\n0 - Exit')


def _show_observable(names, h5file, time_begin, time_end):
    plt.xlabel('Step')
    for name in names:
        values = h5file['observables/{}/value'.format(name)][time_begin:time_end]

        print('=== {} ==='.format(name))
        print('Number of frames: {}'.format(len(values)))
        print('Avg of {}: {}'.format(name, np.average(values)))
        print('Std of {}: {}'.format(name, np.std(values)))

        plt.plot(values, label=name)

    plt.legend()
    plt.show()


def main():
    args = _args()

    h5file = h5py.File(args.h5file)

    observables = h5file['observables'].keys()
    _print_observables(observables)
    ans = raw_input('Select: ')
    while ans != '0':
        try:
            ans_index = map(int, ans.split())
        except ValueError:
            ans = raw_input('Select: ')
            continue
        obs_names = set([observables[x-1] for x in ans_index])
        _show_observable(obs_names, h5file, args.begin, args.end)
        ans = raw_input('Select: ')


if __name__ == '__main__':
    main()
