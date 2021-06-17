# Silhouette-Evaluation

This repository contains and organizes code that we used to evaluate
Silhouette.  For general information about the Silhouette project, please refer
to the [Silhouette repository](https://github.com/URSec/Silhouette).

## Assumptions and Dependencies

Our evaluation has a few assumptions and dependencies on the environment on
which the experiments are conducted.  Specifically:

- We assume the host operating system is Linux.  Other operating systems may
  work but were not tested.
- We use CMake, Ninja, and Clang to build the LLVM-based Silhouette compiler,
  so `cmake`, `ninja`, and `clang` of appropriate versions must be found in
  `PATH`.
- We use [System Workbench IDE](https://www.openstm32.org/System%2BWorkbench%2Bfor%2BSTM32)
  to build benchmark and application programs and assume the IDE is installed
  at `$HOME/Ac6/SystemWorkbench` (the default installation location).
- We use an STM32F469 Discovery board to run benchmark and application programs
  and assume a readable/writable character device `/dev/ttyACM0` is connected
  to the board's serial port after plugging in the board.
- We use OpenOCD to program binaries onto the board, so `openocd` of an
  appropriate version must be found in `PATH`.
- We use Screen to receive program output from the board's serial port, so
  `screen` of an appropriate version must be found in `PATH`.  If you use
  Screen, please avoid naming your sessions to `ttyACM0`; this is the session
  name we use.

## Directory Hierarchy

```shell
Silhouette-Evaluation
|-- build                 # Directory for building LLVM
|   |-- build.llvm.sh     # Script to build LLVM
|
|-- data                  # Directory containing generated experiment data (to
|                         # be created by our scripts)
|
|-- debug                 # Directory containing compiled binaries and build
|                         # logs (to be created by our scripts)
|
|-- llvm-project          # A submodule of URSec/Silhouette-Compiler containing
|                         # source code of LLVM and Silhouette passes
|
|-- scripts               # Directory containing scripts
|   |-- common.sh         # Common components of scripts (not to be run directly)
|   |-- import.sh         # Script to import projects into IDE
|   |-- hal.sh            # Script to compile HAL library for STM32F469 Discovery
|   |-- beebs.sh          # Script to compile/run BEEBS benchmarks
|   |-- coremark.sh       # Script to compile/run CoreMark benchmark
|   |-- coremark-pro.sh   # Script to compile/run CoreMark-Pro benchmarks
|   |-- pinlock.sh        # Script to compile/run PinLock application
|   |-- pinlock-input.txt # Input to PinLock application
|   |-- stm32apps.sh      # Script to compile/run 4 applications from manufacturer
|   |-- gen_csv.py        # Script to collect experiment results into CSV files
|
|-- workspace             # Directory containing source code
|   |-- beebs             # Source code of BEEBS benchmarks
|   |-- coremark          # Source code of CoreMark benchmark
|   |-- coremark-pro      # Source code of CoreMark-Pro benchmarks
|   |-- pinlock           # Source code of PinLock application
|   |-- stm32apps         # Source code of 4 applications from manufacturer
|   |-- stm32f469i-dis... # Source code of HAL library for STM32F469 Discovery
|
|-- README.md             # This README file
```

## Detailed Steps

### Set up the Evaluation Environment

The following steps will set up the evaluation environment from scratch.  They
only need to be done once.

1. Download [System Workbench IDE](https://www.openstm32.org/System%2BWorkbench%2Bfor%2BSTM32)
   and install it at `$HOME/Ac6/SystemWorkbench`.
   Note that although our scripts build programs using the IDE in headless mode
   (i.e., no GUI required), **the IDE still needs to be run in GUI for the
   first time** in order for the embedded development tools that come with it
   to be unpacked in the file system.
2. Clone this repository.
   ```shell
   git clone --recurse-submodules https://github.com/URSec/Silhouette-Evaluation
   ```
3. Build the Silhouette compiler.  Note that all our scripts in the `build` and
   `scripts` directories are CWD-agnostic; each of them can be run from any
   working directory and would have the same outcome.
   ```shell
   cd Silhouette-Evaluation && ./build/build.llvm.sh
   ```
4. Import all the IDE projects in the `workspace` directory into the IDE.
   ```shell
   ./scripts/import.sh
   ```
5. Build a baseline version of the HAL library.  All our programs will link
   against the baseline HAL library.
   ```shell
   ./scripts/hal.sh baseline
   ```

### Build and Run Programs

We have five scripts `beebs.sh`, `coremark.sh`, `coremark-pro.sh`, `pinlock.sh`,
and `stm32apps.sh` that can compile and run three benchmark suites
([BEEBS](https://beebs.mageec.org), [CoreMark](https://www.eembc.org/coremark),
and [CoreMark-Pro](https://www.eembc.org/coremark-pro)) and five embedded
applications (PinLock, FatFs-RAM, FatFs-uSD, LCD-Animation, and LCD-uSD),
respectively.  These scripts support identical command-line argument formats
```shell
./scripts/<script-name>.sh <conf> [<prog>]
```
or
```shell
./scripts/<script-name>.sh run <conf> [<prog>]
```
where `conf` is the name of a configuration (see below) and `prog` is the name
of a program in the corresponding benchmark/application suite.  If `prog` is
not specified, all the programs in the corresponding benchmark/application
suite will be compiled/run.  For example, running `./scripts/beebs.sh baseline`
will compile all the benchmark programs in BEEBS using the Baseline
configuration, and running `./scripts/coremark-pro.sh run silhouette zip-test`
will run the `zip-test` program in CoreMark-Pro that was compiled using the
Silhouette configuration.

To be more specific, we use seven configurations of experiments for each
benchmark/application suite:
- **Baseline**: Compile the programs without any of our passes, denoted as
  `baseline`;
- **Shadow Stack Only**: Only turn on the shadow stack pass, denoted as `ss`;
- **Store Hardening Only**: Only turn on the store hardening pass, denoted as
  `sp` (for historical reasons);
- **CFI Only**: Only turn on the CFI pass, denoted as `cfi`;
- **Silhouette**: Turn on all the three passes above, denoted as `silhouette`;
- **Silhouette-Invert**: Turn on the Silhouette-Invert passes, denoted as
  `invert`;
- **Silhouette-SFI**: Turn on the shadow stack, SFI, and CFI passes, denoted as
  `sfifull`.

Except for CoreMark and FatFS-RAM, which do not have the Silhouette-SFI
configuration, all other programs can be compiled and run using all seven
configurations.

The following shell code compiles all programs we use, with all possible
configurations:
```shell
for conf in baseline ss sp cfi silhouette invert sfifull; do
    ./beebs.sh $conf
    [ $conf != sfifull ] && ./coremark.sh $conf
    ./coremark-pro.sh $conf
    ./pinlock.sh $conf
    ./stm32apps.sh $conf # fatfs_ram on sfifull will be skipped automatically
done
```

The following shell code runs all programs compiled by the above shell code:
```shell
for conf in baseline ss sp cfi silhouette invert sfifull; do
    ./beebs.sh run $conf
    [ $conf != sfifull ] && ./coremark.sh run $conf
    ./coremark-pro.sh run $conf
    ./pinlock.sh run $conf
    ./stm32apps.sh run $conf # fatfs_ram on sfifull will be skipped automatically
done
```

Note that in order to run programs, an STM32F469 Discovery board must be
connected to the host machine.  Also note that FatFs-uSD, LCD-Animation, and
LCD-uSD require a microSD card inserted into the board's microSD card slot,
and they require different file content to be present in the microSD card's FAT
file system:
- FatFs-uSD does not require preexisting files in the microSD card, but it will
  format the microSD card with a new FAT file system and create a new file.
- LCD-Animation requires the microSD FAT file system to have `/BACK` and
  `/TOP` directories, with the first directory containing a static background
  BMP image and the second directory containing an animated image consisting of
  multiple static BMP frames.
- LCD-uSD requires the microSD FAT file system to have a `/Media` directory
  containing multiple static BMP images.

### Collect Experiment Results

After compiling a benchmark or application program, an ELF binary will be
placed in the `debug` directory, and after running a program, experiment data
with execution time will be generated in the `data` directory.  The names of
all the subdirectories and files under `debug` and `data` are self-explanatory.
For example, `debug/beebs-baseline/baseline-whetstone.elf` is the ELF binary of
the `whetstone` program in BEEBS compiled using the Baseline configuration, and
`data/coremark-pro-cfi/cfi-core.stat` contains the execution time of running
the `core` program in CoreMark-Pro compiled with only the CFI pass turned on.

You can use the `scripts/gen_csv.py` script to collect the raw experiment data,
compute the overhead, and write the summarized results to a CSV file.  This
script takes four optional command-line arguments:

```shell
-b benchmark_name # "beebs", "coremark", "coremark-pro", "pinlock", or
                  # "stm32apps", default "beebs"
-t data_type      # "perf" or "codesize", default "perf"
-r                # Whether to generate relative numbers for non-baseline
                  # configurations, default false
-o output_file    # Path of the output CSV file; if not specified, a default
                  # name "data_type-benchmark_name.csv" will be used
```

For example, if you want to see how Silhouette performs on BEEBS, run
```shell
./scripts/gen_csv.py -b beebs -t perf -r
```
and you will get an output file named `perf-beebs.csv` in the working directory.
