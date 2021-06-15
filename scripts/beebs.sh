#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJ=beebs
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"
RUN_CFG="$PROJ_DIR/$PROJ.cfg"

PROGRAMS=(
    "aha-compress"
    "aha-mont64"
    "bs"
    "bubblesort"
    "cnt"
    "compress"
    "cover"
    "crc"
    "crc32"
    "ctl-stack"
    "ctl-string"
    "ctl-vector"
    "cubic"
    "dijkstra"
    "dtoa"
    "duff"
    "edn"
    "expint"
    "fac"
    "fasta"
    "fdct"
    "fibcall"
    "fir"
    "frac"
    "huffbench"
    "insertsort"
    "janne_complex"
    "jfdctint"
    "lcdnum"
    "levenshtein"
    "ludcmp"
    "matmult-float"
    "matmult-int"
    "mergesort"
    "miniz"
    "minver"
    "nbody"
    "ndes"
    "nettle-aes"
    "nettle-arcfour"
    "nettle-cast128"
    "nettle-des"
    "nettle-md5"
    "nettle-sha256"
    "newlib-exp"
    "newlib-log"
    "newlib-mod"
    "newlib-sqrt"
    "ns"
    "nsichneu"
    "picojpeg"
    "prime"
    "qrduino"
    "qsort"
    "qurt"
    "recursion"
    "rijndael"
    "select"
    "sglib-arraybinsearch"
    "sglib-arrayheapsort"
    "sglib-arrayquicksort"
    "sglib-dllist"
    "sglib-hashtable"
    "sglib-listinsertsort"
    "sglib-listsort"
    "sglib-queue"
    "sglib-rbtree"
    "slre"
    "sqrt"
    "st"
    "statemate"
    "stb_perlin"
    "stringsearch1"
    "strstr"
    "tarai"
    "trio-snprintf"
    "trio-sscanf"
    "ud"
    "whetstone"
    "wikisort"
)

PROGRAMS_EXCLUDED=(
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
        for prog in ${PROGRAMS[@]}; do
            if [[ " ${PROGRAMS_EXCLUDED[@]} " =~ " $prog " ]]; then
                continue
            fi
            run $2 $prog "Finished"
        done
    else
        run $2 $3 "Finished"
    fi
    ;;
* )
    if (( $# == 1 )); then
        # Compile each benchmark program
        for prog in ${PROGRAMS[@]}; do
            if [[ " ${PROGRAMS_EXCLUDED[@]} " =~ " $prog " ]]; then
                continue
            fi
            compile $1 $prog
        done

        echo Done
    else
        compile $1 $2
    fi
    ;;
esac
