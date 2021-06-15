#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJ=coremark-pro
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"
RUN_CFG="$PROJ_DIR/$PROJ.cfg"

PROGRAMS=(
    "cjpeg-rose7-preset"
    "core"
    "linear_alg-mid-100x100-sp"
    "loops-all-mid-10k-sp"
    "nnet_test"
    "parser-125k"
    "radix2-big-64k"
    "sha-test"
    "zip-test"
)

CONFIGURATIONS=(
    "baseline"
    "ss"
    "sp"
    "cfi"
    "silhouette"
    "invert"
    "sfifull"
)

#
# Load common components.
#
. "$ROOT_DIR/scripts/common.sh"

#
# Entrance of the script.
#
case $1 in
"run" )
    if (( $# == 2 )); then
        for program in ${PROGRAMS[@]}; do
            run $2 $program "Done"
        done
    else
        run $2 $3 "Done"
    fi
    ;;
* )
    if (( $# == 1 )); then
        # Compile each benchmark program
        for program in ${PROGRAMS[@]}; do
            compile $1 $program
        done

        echo Done
    else
        compile $1 $2
    fi
    ;;
esac
