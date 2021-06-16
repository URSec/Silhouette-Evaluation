#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJ=stm32apps
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"
RUN_CFG="$PROJ_DIR/$PROJ.cfg"

PROGRAMS=(
    "fatfs_ram"
    "fatfs_usd"
    "lcd_animation"
    "lcd_usd"
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
            run $2 $program "Elapsed time"
        done
    else
        run $2 $3 "Elapsed time"
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
