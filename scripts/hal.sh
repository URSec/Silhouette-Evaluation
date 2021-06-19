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

PROJ=stm32f469i-disco_hal_lib
PROJ_DIR="$ROOT_DIR/workspace/$PROJ"

PROGRAMS=(
    "stm32f469i-disco_hal_lib"
)

CONFIGURATIONS=(
    "baseline"
)

#
# Load common components.
#
. "$ROOT_DIR/scripts/common.sh"

#
# Disable the run() function.
#
unset run

#
# Entrance of the script.
#
if (( $# == 1 )); then
    # Compile each program
    for program in ${PROGRAMS[@]}; do
        compile $1 $program
    done

    echo Done
else
    compile $1 $2
fi
