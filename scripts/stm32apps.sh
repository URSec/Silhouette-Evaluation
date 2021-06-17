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
            if [[ "$2" = "sfifull" ]] && [[ "$program" = "fatfs_ram" ]]; then
                continue
            fi
            run $2 $program "Elapsed time"
        done
    else
        if [[ "$2" = "sfifull" ]] && [[ "$3" = "fatfs_ram" ]]; then
            echo "Combination not allowed"
            exit 1
        fi
        run $2 $3 "Elapsed time"
    fi
    ;;
* )
    if (( $# == 1 )); then
        # Compile each benchmark program
        for program in ${PROGRAMS[@]}; do
            if [[ "$1" = "sfifull" ]] && [[ "$program" = "fatfs_ram" ]]; then
                continue
            fi
            compile $1 $program
        done

        echo Done
    else
        if [[ "$1" = "sfifull" ]] && [[ "$2" = "fatfs_ram" ]]; then
            echo "Combination not allowed"
            exit 1
        fi
        compile $1 $2
    fi
    ;;
esac
