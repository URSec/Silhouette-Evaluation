#!/usr/bin/env bash

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
        usage
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
# Print out the usage of the script.
#
usage() {
    echo
    echo "Usage: $0 [<proj>]"
    echo
    echo "Import a project <proj> into the IDE.  If <proj> is not given, all "
    echo "projects will be imported."
    echo
}

#
# Disable the compile() and run() functions.
#
unset compile
unset run

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
