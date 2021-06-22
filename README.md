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
|   |-- project-template  # Source code of a project template for new projects
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

Note that compilation using our scripts must be done one at a time (i.e., **no
parallel compiling of multiple programs**).  This is because the System
Workbench IDE runs a singleton mode.

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

## Extend the Evaluation

In some cases you might want to extend Silhouette's evaluation to support other
programs and/or to use other boards.  Here we provide some general guidance to
do that.

### Compile and Run Other Programs

To compile and run a new program on the same STM32F469 Discovery board, the
easiest way is to use the IDE in GUI.  The System Workbench IDE has full
debugging support for the board and can be used to kick off a new project
quickly.  However, in order to use Silhouette, the new project's settings must
be tweaked a bit.  Specifically:
- The C/C++ compiler for the project needs to be changed from
  `arm-none-eabi-gcc` to the LLVM-based Silhouette compiler (i.e.,
  `build/llvm/bin/clang`).
- Add `--target=arm-none-eabi` to the project's compiler flags to tell the
  compiler that we are doing cross compilation for bare-metal ARM targets.
- The following options must be added to the project's compiler flags to enable
  the Silhouette passes:
  - `-mllvm -enable-arm-silhouette-str2strt`: This option enables the store
    hardening pass.
  - `-mllvm -enable-arm-silhouette-shadowstack`: This option enables the shadow
    stack pass.
  - `-mllvm -enable-arm-silhouette-cfi`: This option enables the CFI pass.
- If using link time optimization (LTO), the following changes must be made:
  - Similar to changing the C/C++ compiler, the linker for the project also
    needs to be changed from `arm-none-eabi-gcc` to the Silhouette compiler.
  - Similarly, add `--target=arm-none-eabi` to the project's linker flags.
  - Instead of adding the three Silhouette options to the compiler flags, add
    them to the linker flags in the form of
    `-Wl,-mllvm,-enable-arm-silhouette-passname` where `passname` is replaced
    with `str2strt`, `shadowstack`, or `cfi`.
- Unlike the default `arm-none-eabi-gcc`, the Silhouette compiler cannot
  automatically find where C and compiler runtime libraries are.  So the
  include path and the library search path for both libraries must be
  specified explicitly.  In our evaluation, we did not transform these
  libraries by Silhouette; instead, we used pre-compiled versions provided by
  the IDE, by adding the following include path:
  - `${openstm32_compiler_path}/../arm-none-eabi/include`

  and adding the following library search paths:
  - `${openstm32_compiler_path}/../arm-none-eabi/lib/thumb/v7e-m/fpv4-sp/hard`
  - `${openstm32_compiler_path}/../arm-none-eabi/lib`
  - `${openstm32_compiler_path}/../lib/gcc/arm-none-eabi/7.3.1/thumb/v7e-m/fpv4-sp/hard`
  - `${openstm32_compiler_path}/../lib/gcc/arm-none-eabi/7.3.1`
  - `${openstm32_compiler_path}/../lib/gcc`

  The IDE is able to figure out the location of `${openstm32_compiler_path}`,
  resolve all these paths, and find the correct headers to include and
  libraries to link against.

In addition to the changes to the project's settings, developers need to note
the following facts:
- Silhouette requires the memory protection unit (MPU) to be configured
  correctly to enforce W^X and provide a protected shadow stack, so MPU
  configuration code must exist and be run during system initialization.
- Silhouette adopts the parallel shadow stack design and uses a constant shadow
  stack offset.  Developers can use the
  `-mllvm -arm-silhouette-shadowstack-offset=` option (or the linker flag form
  when using LTO) to specify a different shadow stack offset than the default
  14-MB offset; this is important for the shadow stack to work correctly if the
  shadow stack placement is different from what we used in the evaluation.
- Since unprivileged stores cannot write to the System region regardless of the
  MPU configuration, developers would want to vet all code that needs to access
  the System region and place vetted functions in the trusted computing base
  (TCB) so that they do not undergo the store hardening transformation.  In our
  evaluation, vetted functions (including MPU configuration code) are marked
  with `__attribute__((section("privileged_functions")))`; Silhouette passes
  will recognize this section attribute and skip transformations on such
  functions.  The TCB in our evaluation also includes the HAL library, which is
  compiled separately without enabling any of the Silhouette passes (see Step 5
  in the [setup phase](#set-up-the-evaluation-environment)).

To ease the burden of correctly setting up a new project from scratch, we have
configured a project template in the `workspace` directory for developers to
extend.  The directory hierarchy of the template is as follows:

```shell
project-template
|-- inc                       # Directory containing headers
|   |-- stm32f4xx_it.h        # (From IDE) header of core exception handler declarations
|
|-- src                       # Directory containing source code
|   |-- main.c                # Source of main function
|   |-- init_f469.c           # Source of clock, UART, and MPU initialization code
|   |-- stm32f4xx_it.c        # (From IDE) source of core exception handler definitions
|   |-- syscalls.c            # (From IDE) source of minimal system calls
|   |-- system_stm32f4xx.c    # (From IDE) source of system initialization code
|
|-- startup                   # Directory containing startup code
|   |-- startup_stm32f469xx.S # (From IDE) source of startup code
|
|-- gen_cproject.py           # Script to generate IDE project configuration files
|
|-- LinkerScript.ld           # Linker script to use
|
|-- .project                  # IDE's project description file
|
|-- .cproject                 # IDE's project configuration file (to be generated)
|
|-- .settings                 # Directory containing some other IDE project
                              # configuration files (to be generated)
```

The core of the template is the `gen_cproject.py` script, which we wrote to
generate a `.cproject` file that describes all combinations of configuration-,
project-, program-, and library-specific settings.  Developers can modify this
script to generate a `.cproject` file that tailors the IDE's build process for
their programs.  For example, developers can define specific macros and add
specific compiler flags in each element of the `libraries`, `programs`,
`middlewares`, and `configurations` variables.  Developers can look at existing
projects' `gen_cproject.py` script to see how we configured existing
benchmark/application projects.

After generating a `.cproject` file by the script, developers can import the
new project into the IDE and start normal development.

### Port to Another Board

Porting existing Silhouette-enabled programs to another board can be
straightforward, hard, or even impossible.  This is because different boards
can have different memory size and location, different types of peripherals,
different kind of processors, etc.  The best advice we can give is to follow
the standard development procedure of the target board (e.g., use the
vendor-provided IDE) to first get a program running correctly and then try to
apply Silhouette's transformations.
