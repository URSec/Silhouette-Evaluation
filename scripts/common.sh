#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`
DATA_DIR="$ROOT_DIR/data"

if [[ ! -x "$HOME/Ac6/SystemWorkbench/eclipse" ]]; then
    echo "IDE not found!"
    exit 1
fi
export ECLIPSE="$HOME/Ac6/SystemWorkbench/eclipse"

#
# Print out the usage of the script.
#
usage() {
    echo
    echo "Usage: $0 <conf> [<prog>]"
    echo
    echo "Compile a program <prog> under the configuration <conf>.  If <prog> "
    echo "is not given, all programs will be compiled."
    echo
    if type -t run > /dev/null; then
        echo "Or: $0 run <conf> [<prog>]"
        echo
        echo "Run a program <prog> under the configuration <conf>.  If <prog> "
        echo "is not given, all programs will be run."
        echo
    fi
}

#
# Compile a program.
#
# $1: the configuration.
# $2: the program to compile.
#
compile() {
    # Check if necessary variables are defined
    if [[ -z "$CONFIGURATIONS" ]] || [[ -z "$PROGRAMS" ]] ||
       [[ -z "$PROJ" ]] || [[ -z "$PROJ_DIR" ]]; then
        echo "One or more necessary variables undefined!"
        exit 1
    fi

    # Check if the configuration name is valid
    if [[ ! " ${CONFIGURATIONS[@]} " =~ " $1 " ]]; then
        echo "Configuration must be one of the following:"
        echo "${CONFIGURATIONS[@]}"
        usage
        exit 1
    fi

    # Check if the program name is valid
    if [[ ! " ${PROGRAMS[@]} " =~ " $2 " ]]; then
        echo "Program must be one of the following:"
        echo "${PROGRAMS[@]}"
        usage
        exit 1
    fi

    # Make a debug directory
    local debug_dir="$ROOT_DIR/debug/$PROJ-$1"
    if [[ ! -d "$debug_dir" ]]; then
        mkdir -p "$debug_dir"
    fi

    local elf="$PROJ_DIR/$1-$2/$1-$2.elf"
    local lib="$PROJ_DIR/$1-$2/lib$2.a"
    rm -rf "$elf" "$lib"

    # Do compile
    local eclipse_args=(
        "-nosplash"
        "--launcher.suppressErrors"
        "-application org.eclipse.cdt.managedbuilder.core.headlessbuild"
        "-data $ROOT_DIR/workspace"
        "-cleanBuild"
    )
    echo "Compiling $2 for $1 ......"
    local build_log="$debug_dir/build-$2.log"
    "$ECLIPSE" ${eclipse_args[@]} $PROJ/$1-$2 >& "$build_log"
    if [[ ! -x "$elf" ]] && [[ ! -f "$lib" ]]; then
        # Try again; the IDE sometimes may fail for no reason, but it's
        # unlikely to happen twice in a row
        "$ECLIPSE" ${eclipse_args[@]} $PROJ/$1-$2 >& "$build_log"
        if [[ ! -x "$elf" ]] && [[ ! -f "$lib" ]]; then
            echo "Compiling $2 failed!"
            echo "Check $build_log for details"
            exit 1
        fi
    fi

    # Copy the generated binary/library to the debug directory
    if [[ -x "$elf" ]]; then
        echo "Copying $1-$2.elf to debug/$PROJ-$1 ......"
        cp "$elf" "$debug_dir"
    else
        echo "Copying lib$2.a to debug/$PROJ-$1 ......"
        cp "$lib" "$debug_dir"
    fi

    echo "Done compiling $2 for $1"
    echo
}

#
# Run an already compiled benchmark program.
#
# $1: the configuration to use.
# $2: the program to run.
# $3: a string to grep for checking if the program has finished executing.
# $4: a file containing input to the program (default none).
# $5: number of iterations to run (default 1).
#
run() {
    # Check if necessary variables are defined
    if [[ -z "$CONFIGURATIONS" ]] || [[ -z "$PROGRAMS" ]] ||
       [[ -z "$PROJ" ]] || [[ -z "$PROJ_DIR" ]] || [[ -z "$RUN_CFG" ]]; then
        echo "One or more necessary variables undefined!"
        exit 1
    fi
    # Check if the configuration name is valid
    if [[ ! " ${CONFIGURATIONS[@]} " =~ " $1 " ]]; then
        echo "Configuration must be one of the following:"
        echo "${CONFIGURATIONS[@]}"
        usage
        exit 1
    fi

    # Check if the program name is valid
    if [[ ! " ${PROGRAMS[@]} " =~ " $2 " ]]; then
        echo "Program must be one of the following:"
        echo "${PROGRAMS[@]}"
        usage
        exit 1
    fi

    # Check if the number of iterations is actually a number
    local iters=1
    if [[ -n "$5" ]]; then
        if [[ "$5" =~ ^[0-9]+$ ]]; then
            iters="$5"
        else
            echo "Number of iterations must be an integer!"
            exit 1
        fi
    fi

    # Check if the ELF binary is there
    local debug_dir="$ROOT_DIR/debug/$PROJ-$1"
    local elf="$debug_dir/$1-$2.elf"
    if [[ ! -x "$elf" ]]; then
        echo "No $elf found!"
        echo "Try to compile first!"
        exit 1
    fi

    for iter in `seq 0 $(( iters - 1 ))`; do
        # Kill all screens first
        screen -X kill >& /dev/null

        local perf_dir="$DATA_DIR/$PROJ-$1"
        if [[ ! -d "$perf_dir" ]]; then
            mkdir -p "$perf_dir"
        fi

        local perf_data="$perf_dir/$1-$2.stat"
        if (( $iters != 1 )); then
            perf_data="$perf_dir/$1-$2.$iter-stat"
        fi
        rm -rf "$perf_data"

        # Open screen to receive the output
        screen -dm -L -fn -Logfile "$perf_data" /dev/ttyACM0 115200
        screen -X logfile flush 0

        # Program the binary onto the board
        echo "Programming $1-$2.elf onto the board ......"
        local openocd_log=`mktemp -q`
        openocd -f "$RUN_CFG" -c "program $elf reset exit" 2> "$openocd_log"
        if (( $? != 0 )); then
            echo "OpenOCD failed!"
            echo "Check $openocd_log for details"
            exit 1
        fi

        # Feed input to the serial port
        if [[ -n "$4" ]] && [[ -f "$4" ]]; then
            sleep 0.01
            screen -X readreg p "$4"
            screen -X paste p
        fi

        echo "Running $PROJ-$1/$2 ......"
        grep "$3" "$perf_data" >& /dev/null
        while (( $? != 0 )); do
            sleep 1
            grep "$3" "$perf_data" >& /dev/null
        done
        sleep 1
        screen -X kill

        # Print out the result
        echo "Result:"
        echo "============================================================="
        cat "$perf_data"
        echo
    done
}
