#!/usr/bin/env bash

ROOT_DIR=`dirname $0 | sed 's/$/\/../' | xargs realpath`

PROJECTS=(
    "stm32f469i-disco_hal_lib"
    "beebs"
    "coremark"
    "coremark-pro"
    "stm32apps"
    "pinlock"
)

#
# Import a project into the IDE workspace.
#
# $1: the project name.
#
import() {
    # Check if the project name is valid
    if [[ ! " ${PROJECTS[@]} " =~ " $1 " ]]; then
        echo "Project must be one of the following:"
        echo "${PROJECTS[@]}"
        exit 1
    fi

    # Check if the project file is there
    if [[ ! -f "$ROOT_DIR/workspace/$1/.project" ]]; then
        echo "No .project file exists for $1!"
        exit 1
    fi

    # Do import
    local eclipse_args=(
        "-nosplash"
        "--launcher.suppressErrors"
        "-application org.eclipse.cdt.managedbuilder.core.headlessbuild"
        "-data $ROOT_DIR/workspace"
        "-import"
    )
    local import_log=`mktemp -q`
    echo "Importing $1 ......"
    "$ECLIPSE" ${eclipse_args[@]} "$ROOT_DIR/workspace/$1" >& "$import_log"
    if (( $? != 0 )); then
        echo "Importing failed!"
        echo "Check $import_log for details"
        exit 1
    fi
}

#
# Load common components.
#
. "$ROOT_DIR/scripts/common.sh"

#
# Entrance of the script.
#
if (( $# == 0 )); then
    for project in ${PROJECTS[@]}; do
        import $project
    done
else
    import $1
fi
