#!/usr/bin/env python3

# Copyright (C) 2020, 2021 University of Rochester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import csv
import glob
import os
import statistics
import sys


#
# Path to the root directory of whole project.
#
root = os.path.abspath(os.path.dirname(sys.argv[0]) + '/..')

#
# Path to the debug directory where we put generated binaries.
#
debug_dir = root + '/debug'

#
# Path to the experiment data directory.
#
data_dir = root + '/data'

#
# List of configurations.
#
configurations = [
    'baseline',
    'ss',
    'sp',
    'cfi',
    'silhouette',
    'invert',
    'sfifull',
]

#
# List of benchmark suites.
#
benchmarks = [
    'beebs',
    'coremark',
    'coremark-pro',
    'pinlock',
    'stm32apps',
]

###############################################################################

#
# Write extracted data to an output file.
#
# @data: the data collection.
# @relative: whether to generate relative numbers for non-baseline
#            configurations.
# @output: path to the output CSV file.
#
def write_data(data, relative, output):
    # Do we have any program that uses average + stdev?
    has_stdev = False
    for prog in data:
        for conf in data[prog]:
            if isinstance(data[prog][conf], list):
                assert len(data[prog][conf]) == 2, 'Not average + stdev list?'
                has_stdev = True

    # Post-process: convert to relative numbers for non-baseline
    if relative:
        for prog in data:
            assert 'baseline' in data[prog], 'Relative to no baseline?'
            baseline = data[prog]['baseline']
            if isinstance(baseline, list):
                baseline = baseline[0]
            baseline = float(baseline)

            for conf in configurations:
                if conf == 'baseline':
                    continue
                if conf in data[prog]:
                    if isinstance(data[prog][conf], list):
                        data[prog][conf][0] /= baseline
                        data[prog][conf][1] /= baseline
                    else:
                        data[prog][conf] /= baseline

    # Post-process: limit floating-point numbers to 3 digits
    for prog in data:
        for conf in data[prog]:
            if isinstance(data[prog][conf], list):
                if isinstance(data[prog][conf][0], float):
                    data[prog][conf][0] = '{0:.3f}'.format(data[prog][conf][0])
                if isinstance(data[prog][conf][1], float):
                    data[prog][conf][1] = '{0:.3f}'.format(data[prog][conf][1])
            elif isinstance(data[prog][conf], float):
                data[prog][conf] = '{0:.3f}'.format(data[prog][conf])

    # Now write to a CSV file
    with open(output, mode='w') as csv_file:
        writer = csv.writer(csv_file)

        # Construct and write the header row
        row = ['#Program']
        for conf in configurations:
            row.append(conf)
            if has_stdev:
                row.append('stdev')
        writer.writerow(row)

        # Construct and write a row for each program
        for prog in data:
            row = [prog]
            for conf in configurations:
                if conf in data[prog]:
                    if isinstance(data[prog][conf], list):
                        row.extend(data[prog][conf])
                    elif has_stdev:
                        row.extend([data[prog][conf], '0'])
                    else:
                        row.append(data[prog][conf])
                elif has_stdev:
                    row.extend(['', ''])
                else:
                    row.append('')
            writer.writerow(row)


#
# Generate a code size CSV file for a specified benchmark suite, assuming
# @debug_dir already contains all the generate binaries needed.
#
# @benchmark: name of the benchmark suite.
# @relative: whether to generate relative numbers for non-baseline
#            configurations.
# @output: path to the output CSV file.
#
def gen_csv_codesize(benchmark, relative, output):
    data = {}
    for conf in configurations:
        new_debug_dir = debug_dir + '/' + benchmark + '-' + conf
        for f in sorted(glob.glob(new_debug_dir + '/*.elf')):
            prog = os.path.splitext(os.path.basename(f))[0]
            prog = prog.replace(conf + '-', '', 1)
            number = 0

            stdout = os.popen('size -A -d ' + f)
            line = stdout.readline()
            while line != '':
                if '.text' in line:
                    number += int(line.split()[1])
                line = stdout.readline()

            if number != 0:
                if prog not in data:
                    data[prog] = {}
                data[prog][conf] = number

    # Write data to CSV
    write_data(data, relative, output)


#
# Generate a performance CSV file for a specified benchmark suite, assuming
# @data_dir already contains all the experiment data needed.
#
# @benchmark: name of the benchmark suite.
# @relative: whether to generate relative numbers for non-baseline
#            configurations.
# @output: path to the output CSV file.
#
def gen_csv_perf(benchmark, relative, output):
    data = {}
    for conf in configurations:
        new_data_dir = data_dir + '/' + benchmark + '-' + conf

        # Process single-number data as is
        for f in sorted(glob.glob(new_data_dir + '/*.stat')):
            prog = os.path.splitext(os.path.basename(f))[0]
            prog = prog.replace(conf + '-', '', 1)
            number = None
            for line in open(f):
                # BEEBS
                if 'Finished' in line:
                    number = int(line.split(' ')[2].lstrip())
                    break
                # CoreMark
                elif 'Total ticks' in line:
                    number = int(line.split(':')[-1].lstrip())
                    break
                # CoreMark-Pro
                elif 'time(ns)' in line:
                    number = int(line.split('=')[-1].lstrip())
                    break
                # PinLock and STM32apps
                elif 'Elapsed time' in line:
                    number = int(line.split(' ')[-2].lstrip())
                    break

            if number is not None:
                if prog not in data:
                    data[prog] = {}
                data[prog][conf] = number

        # Process multi-number data as average and stdev
        for f in sorted(glob.glob(new_data_dir + '/*-stat')):
            prog = os.path.splitext(os.path.basename(f))[0]
            prog = prog.replace(conf + '-', '', 1)
            number = None
            for line in open(f):
                # BEEBS
                if 'Finished' in line:
                    number = int(line.split(' ')[2].lstrip())
                    break
                # CoreMark
                elif 'Total ticks' in line:
                    number = int(line.split(':')[-1].lstrip())
                    break
                # CoreMark-Pro
                elif 'time(ns)' in line:
                    number = int(line.split('=')[-1].lstrip())
                    break
                # PinLock and STM32apps
                elif 'Elapsed time' in line:
                    number = int(line.split(' ')[-2].lstrip())
                    break

            if number is not None:
                if prog not in data:
                    data[prog] = {}
                if conf not in data[prog]:
                    data[prog][conf] = []
                data[prog][conf].append(number)
        for prog in data:
            if conf in data[prog] and isinstance(data[prog][conf], list):
                average = float(sum(data[prog][conf])) / len(data[prog][conf])
                stdev = statistics.stdev(data[prog][conf])
                data[prog][conf] = [average, stdev]

    # Write data to CSV
    write_data(data, relative, output)


#
# The main function.
#
def main():
    # Construct a CLI argument parser
    parser = argparse.ArgumentParser(description='Generate CSV files.')
    parser.add_argument('-b', '--benchmark', choices=benchmarks,
                        default='beebs', metavar='BENCH',
                        help='Name of the benchmark suite')
    parser.add_argument('-t', '--type', choices=['codesize', 'perf'],
                        default='perf', metavar='TYPE',
                        help='Type of the CSV file to generate')
    parser.add_argument('-r', '--relative', action='store_true',
                        help='Generate non-baseline numbers relative to baseline')
    parser.add_argument('-o', '--output', metavar='FILE',
                        help='Path to the output CSV file')

    # Parse CLI arguments
    args = parser.parse_args()
    benchmark = args.benchmark
    typ = args.type
    relative = args.relative
    output = typ + '-' + benchmark + '.csv'
    if args.output is not None:
        output = args.output

    # Generate CSV
    if typ == 'perf':
        gen_csv_perf(benchmark, relative, output)
    else:
        gen_csv_codesize(benchmark, relative, output)


#
# entrance of this script.
#
if __name__ == '__main__':
    main()
