#!/usr/bin/env python3

# Copyright (C) 2019-2021 University of Rochester
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

import argparse
import os
import sys


#
# Path to the root directory of whole project.
#
root = '${workspace_loc}/..'

#
# Path to our Clang.
#
clang_path = root + '/build/llvm/bin/clang'

#
# Path to the directory of this project.
#
project_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

#
# Project name.
#
project_name = 'beebs'


#
# Dict of libraries that need to be linked.
#
libraries = {
    'c': {
        'includes': [
            '${openstm32_compiler_path}/../arm-none-eabi/include',
        ],
        'library_paths': [
            '${openstm32_compiler_path}/../arm-none-eabi/lib/thumb/v7e-m/fpv4-sp/hard',
            '${openstm32_compiler_path}/../arm-none-eabi/lib',
        ],
        'objects': [
            '${openstm32_compiler_path}/../arm-none-eabi/lib/thumb/v7e-m/fpv4-sp/hard/crt0.o',
        ],
    },
    'gcc': {
        'library_paths': [
            '${openstm32_compiler_path}/../lib/gcc/arm-none-eabi/7.3.1/thumb/v7e-m/fpv4-sp/hard',
            '${openstm32_compiler_path}/../lib/gcc/arm-none-eabi/7.3.1',
            '${openstm32_compiler_path}/../lib/gcc',
        ],
        'objects': [
            '${openstm32_compiler_path}/../lib/gcc/arm-none-eabi/7.3.1/thumb/v7e-m/fpv4-sp/hard/crti.o',
            '${openstm32_compiler_path}/../lib/gcc/arm-none-eabi/7.3.1/thumb/v7e-m/fpv4-sp/hard/crtbegin.o',
            '${openstm32_compiler_path}/../lib/gcc/arm-none-eabi/7.3.1/thumb/v7e-m/fpv4-sp/hard/crtend.o',
            '${openstm32_compiler_path}/../lib/gcc/arm-none-eabi/7.3.1/thumb/v7e-m/fpv4-sp/hard/crtn.o',
        ],
    },
    'stm32f469i-disco_hal_lib': {
        'defines': [
            'STM32',
            'STM32F4',
            'STM32F469NIHx',
            'STM32F469I_DISCO',
            'STM32F469xx',
            'USE_HAL_DRIVER',
        ],
        'includes': [
            '${workspace_loc:/stm32f469i-disco_hal_lib/CMSIS/core}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/CMSIS/device}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/HAL_Driver/Inc/Legacy}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/HAL_Driver/Inc}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/STM32469I-Discovery}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/ampire480272}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/ampire640480}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/Common}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/cs43l22}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/exc7200}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/ft6x06}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/ili9325}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/ili9341}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/l3gd20}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/lis302dl}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/lis3dsh}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/ls016b8uy}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/lsm303dlhc}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/mfxstm32l152}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/n25q128a}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/n25q256a}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/n25q512a}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/otm8009a}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/ov2640}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/s25fl512s}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/s5k5cag}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/st7735}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/st7789h2}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/stmpe1600}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/stmpe811}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/ts3510}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Components/wm8994}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Fonts}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities/Log}',
            '${workspace_loc:/stm32f469i-disco_hal_lib/Utilities}',
        ],
        'library_paths': [
            '${workspace_loc:/stm32f469i-disco_hal_lib/baseline-stm32f469i-disco_hal_lib}',
        ],
    },
}


#
# Dict of middlewares that are used.
#
middlewares = {
}


#
# Dict of programs to compile and link.
#
programs = {
    'aha-compress': {},
    'aha-mont64': {},
    'bs': {},
    'bubblesort': {},
    'cnt': {},
    'compress': {},
    'cover': {},
    'crc': {},
    'crc32': {},
    'ctl-stack': { 'defines': [ 'CTL_STACK', ], },
    'ctl-string': {},
    'ctl-vector': { 'defines': [ 'CTL_VECTOR', ], },
    'cubic': {},
    'dijkstra': {},
    'dtoa': {},
    'duff': {},
    'edn': {},
    'expint': {},
    'fac': {},
    'fasta': {},
    'fdct': {},
    'fibcall': {},
    'fir': {},
    'frac': {},
    'huffbench': {},
    'insertsort': {},
    'janne_complex': {},
    'jfdctint': {},
    'lcdnum': {},
    'levenshtein': {},
    'ludcmp': {},
    'matmult-float': { 'defines': [ 'MATMULT_FLOAT', ], },
    'matmult-int': { 'defines': [ 'MATMULT_INT', ], },
    'mergesort': {},
    'miniz': {},
    'minver': {},
    'nbody': {},
    'ndes': {},
    'nettle-aes': {},
    'nettle-arcfour': {},
    'nettle-cast128': {},
    'nettle-des': {},
    'nettle-md5': {},
    'nettle-sha256': {},
    'newlib-exp': {},
    'newlib-log': {},
    'newlib-mod': {},
    'newlib-sqrt': {},
    'ns': {},
    'nsichneu': {},
    'picojpeg': {},
    'prime': {},
    'qrduino': {},
    'qsort': {},
    'qurt': {},
    'recursion': {},
    'rijndael': {},
    'select': {},
    'sglib-arraybinsearch': {},
    'sglib-arrayheapsort': { 'defines': [ 'HEAP_SORT', ], },
    'sglib-arrayquicksort': { 'defines': [ 'QUICK_SORT', ], },
    'sglib-dllist': {},
    'sglib-hashtable': {},
    'sglib-listinsertsort': {},
    'sglib-listsort': {},
    'sglib-queue': {},
    'sglib-rbtree': {},
    'slre': {},
    'sqrt': {},
    'st': {},
    'statemate': {},
    'stb_perlin': {},
    'stringsearch1': {},
    'strstr': {},
    'tarai': {},
    'trio-snprintf': {
        'defines': [
            'TRIO_DEPRECATED=0',
            'TRIO_ERRORS=0',
            'TRIO_EXTENSION=0',
            'TRIO_FEATURE_FLOAT=0',
            'TRIO_MICROSOFT=0',
            'TRIO_SNPRINTF',
            'TRIO_SNPRINTF_ONLY',
        ],
    },
    'trio-sscanf': {
        'defines': [
            'TRIO_DEPRECATED=0',
            'TRIO_ERRORS=0',
            'TRIO_EMBED_NAN=1',
            'TRIO_EMBED_STRING=1',
            'TRIO_EXTENSION=0',
            'TRIO_FEATURE_CLOSURE=0',
            'TRIO_FEATURE_DYNAMICSTRING=0',
            'TRIO_FEATURE_FD=0',
            'TRIO_FEATURE_FILE=0',
            'TRIO_FEATURE_FLOAT=0',
            'TRIO_FEATURE_LOCALE=0',
            'TRIO_FEATURE_STDIO=0',
            'TRIO_FEATURE_STRERR=0',
            'TRIO_MICROSOFT=0',
            'TRIO_SSCANF',
        ],
    },
    'ud': {},
    'whetstone': {},
    'wikisort': {},
}


#
# Dict of configurations.
#
configurations = {
    'baseline': {
        'cflags': [
            '-flto',
        ],
        'ldflags': [
            '-flto',
        ],
    },
    'ss': {
        'cflags': [
            '-flto',
        ],
        'ldflags': [
            '-flto',
            '-Wl,-mllvm,-enable-arm-silhouette-shadowstack',
        ],
    },
    'sp': {
        'cflags': [
            '-flto',
        ],
        'ldflags': [
            '-flto',
            '-Wl,-mllvm,-enable-arm-silhouette-str2strt',
        ],
    },
    'cfi': {
        'cflags': [
            '-flto',
        ],
        'ldflags': [
            '-flto',
            '-Wl,-mllvm,-enable-arm-silhouette-cfi',
        ],
    },
    'silhouette': {
        'defines': [
            'SS_STACK2HEAP',
        ],
        'cflags': [
            '-flto',
        ],
        'ldflags': [
            '-flto',
            '-Wl,-mllvm,-enable-arm-silhouette-shadowstack',
            '-Wl,-mllvm,-enable-arm-silhouette-str2strt',
            '-Wl,-mllvm,-enable-arm-silhouette-cfi',
        ],
    },
    'invert': {
        'defines': [
            'SS_FLIP_USER_KERNEL_PERM',
            'SS_STACK2HEAP',
        ],
        'cflags': [
            '-flto',
        ],
        'ldflags': [
            '-flto',
            '-Wl,-mllvm,-enable-arm-silhouette-shadowstack',
            '-Wl,-mllvm,-enable-arm-silhouette-cfi',
            '-Wl,-mllvm,-enable-arm-silhouette-invert',
        ],
    },
    'sfifull': {
        'defines': [
            'SS_STACK2HEAP',
        ],
        'cflags': [
            '-flto',
        ],
        'ldflags': [
            '-flto',
            '-Wl,-mllvm,-enable-arm-silhouette-shadowstack',
            '-Wl,-mllvm,-enable-arm-silhouette-cfi',
            '-Wl,-mllvm,-enable-arm-silhouette-sfi=full',
        ],
    },
}

###############################################################################

#
# Generate and return the cproject header.
#
def gen_header():
    xml =  '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    xml += '<?fileVersion 4.0.0?>\n'
    xml += '<cproject storage_type_id="org.eclipse.cdt.core.XmlProjectDescriptionStorage">\n'
    return xml


#
# Generate and return the cproject footer.
#
def gen_footer():
    xml =  '  <storageModule moduleId="cdtBuildSystem" version="4.0.0">\n'
    xml += '    <project id="' + project_name + '.fr.ac6.managedbuild.target.gnu.cross.exe" name="Executable" projectType="fr.ac6.managedbuild.target.gnu.cross.exe"/>\n'
    xml += '  </storageModule>\n'
    xml += '  <storageModule moduleId="org.eclipse.cdt.core.LanguageSettingsProviders"/>\n'
    xml += '  <storageModule moduleId="org.eclipse.cdt.make.core.buildtargets"/>\n'
    xml += '  <storageModule moduleId="org.eclipse.cdt.internal.ui.text.commentOwnerProjectMappings"/>\n'
    xml += '</cproject>\n'
    return xml

#
# Generate and return the header of refresh scopes.
#
def gen_refresh_scope_header():
    return '  <storageModule moduleId="refreshScope" versionNumber="2">\n'


#
# Generate and return the refresh scope for a given configuration and program.
#
# @conf: the name of the configuration.
# @program: the name of the program.
#
def gen_refresh_scope_config(conf, program):
    program_id = conf + '-' + program
    xml =  '    <configuration configurationName="' + program_id + '">\n'
    xml += '      <resource resourceType="PROJECT" workspacePath="/' + project_name + '"/>\n'
    xml += '    </configuration>\n'
    return xml


#
# Generate and return the footer of refresh scopes.
#
def gen_refresh_scope_footer():
    return '  </storageModule>\n'


#
# Generate and return the header of scanner configurations.
#
def gen_scanner_header():
    xml =  '  <storageModule moduleId="scannerConfiguration">\n'
    xml += '    <autodiscovery enabled="false" problemReportingEnabled="false" selectedProfileId=""/>\n'
    return xml


#
# Generate and return the scanner configuration for a given configuration and
# program.
#
# @conf: the name of the configuration.
# @program: the name of the program.
#
def gen_scanner_config(conf, program):
    program_id = conf + '-' + program
    xml =  '    <scannerConfigBuildInfo instanceId="fr.ac6.managedbuild.config.gnu.cross.exe.release.' + program_id + ';fr.ac6.managedbuild.config.gnu.cross.exe.release.' + program_id + '.;fr.ac6.managedbuild.tool.gnu.cross.c.compiler.' + program_id + ';fr.ac6.managedbuild.tool.gnu.cross.c.compiler.input.c.' + program_id + '">\n'
    xml += '      <autodiscovery enabled="false" problemReportingEnabled="false" selectedProfileId=""/>\n'
    xml += '    </scannerConfigBuildInfo>\n'
    return xml


#
# Generate and return the footer of scanner configurations.
#
def gen_scanner_footer():
    return '  </storageModule>\n'


#
# Generate and return the header of core settings.
#
def gen_core_settings_header():
    return '  <storageModule moduleId="org.eclipse.cdt.core.settings">\n'


#
# Generate and return the core setting for a given program.
#
# @conf: the name of the configuration to use.
# @program: the name of the program.
#
def gen_core_settings_config(conf, program):
    program_id = conf + '-' + program

    xml =  '    <!-- Configuration of ' + program_id + ' -->\n'
    xml += '    <cconfiguration id="fr.ac6.managedbuild.config.gnu.cross.exe.release.' + program_id + '">\n'
    xml += '      <storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="fr.ac6.managedbuild.config.gnu.cross.exe.release.' + program_id + '" moduleId="org.eclipse.cdt.core.settings" name="' + program_id + '">\n'
    xml += '        <externalSettings/>\n'
    xml += '        <extensions>\n'
    xml += '          <extension id="org.eclipse.cdt.core.ELF" point="org.eclipse.cdt.core.BinaryParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GmakeErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GLDErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.CWDLocator" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '        </extensions>\n'
    xml += '      </storageModule>\n'
    xml += '      <storageModule moduleId="cdtBuildSystem" version="4.0.0">\n'
    xml += '        <configuration artifactExtension="elf" artifactName="${ConfigName}" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.exe" buildProperties="org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.exe,org.eclipse.cdt.build.core.buildType=org.eclipse.cdt.build.core.buildType.release" cleanCommand="rm -rf" description="" id="fr.ac6.managedbuild.config.gnu.cross.exe.release.' + program_id + '" name="' + program_id + '" optionalBuildProperties="org.eclipse.cdt.docker.launcher.containerbuild.property.selectedvolumes=,org.eclipse.cdt.docker.launcher.containerbuild.property.volumes=" parent="fr.ac6.managedbuild.config.gnu.cross.exe.release" postannouncebuildStep="Printing size information:" postbuildStep="arm-none-eabi-size -B &quot;${BuildArtifactFileName}&quot;">\n'
    xml += '          <folderInfo id="fr.ac6.managedbuild.config.gnu.cross.exe.release.' + program_id + '." name="/" resourcePath="">\n'
    xml += '            <toolChain id="fr.ac6.managedbuild.toolchain.gnu.cross.exe.release.' + program_id + '" name="Ac6 STM32 MCU GCC" superClass="fr.ac6.managedbuild.toolchain.gnu.cross.exe.release">\n'
    xml += '              <option id="fr.ac6.managedbuild.option.gnu.cross.mcu.' + program_id + '" name="Mcu" superClass="fr.ac6.managedbuild.option.gnu.cross.mcu" value="STM32F469NIHx" valueType="string"/>\n'
    xml += '              <option id="fr.ac6.managedbuild.option.gnu.cross.fpu.' + program_id + '" name="Floating point hardware" superClass="fr.ac6.managedbuild.option.gnu.cross.fpu" value="fr.ac6.managedbuild.option.gnu.cross.fpu.fpv4-sp-d16" valueType="enumerated"/>\n'
    xml += '              <option id="fr.ac6.managedbuild.option.gnu.cross.floatabi.' + program_id + '" name="Floating-point ABI" superClass="fr.ac6.managedbuild.option.gnu.cross.floatabi" value="fr.ac6.managedbuild.option.gnu.cross.floatabi.hard" valueType="enumerated"/>\n'
    xml += '              <option id="fr.ac6.managedbuild.option.gnu.cross.board.' + program_id + '" name="Board" superClass="fr.ac6.managedbuild.option.gnu.cross.board" value="STM32F469I-DISCO" valueType="string"/>\n'
    xml += '              <option id="fr.ac6.managedbuild.option.gnu.cross.prefix.' + program_id + '" name="Prefix" superClass="fr.ac6.managedbuild.option.gnu.cross.prefix" value="" valueType="string"/>\n'
    xml += '              <targetPlatform archList="all" binaryParser="org.eclipse.cdt.core.ELF" id="fr.ac6.managedbuild.targetPlatform.gnu.cross.' + program_id + '" isAbstract="false" osList="all" superClass="fr.ac6.managedbuild.targetPlatform.gnu.cross"/>\n'
    xml += '              <builder buildPath="${workspace_loc:/' + project_name + '}/Release" id="fr.ac6.managedbuild.builder.gnu.cross.' + program_id + '" keepEnvironmentInBuildfile="false" managedBuildOn="true" name="Gnu Make Builder" parallelBuildOn="true" parallelizationNumber="optimal" superClass="fr.ac6.managedbuild.builder.gnu.cross"/>\n'
    ###########################################################################
    # Set up C compiler
    ###########################################################################
    xml += '              <tool command="' + clang_path + '" id="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.' + program_id + '" name="MCU GCC Compiler" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.compiler">\n'
    xml += '                <option id="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.fdata.' + program_id + '" name="Place the data in their own section (-fdata-sections)" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.fdata" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    xml += '                <option id="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.ffunction.' + program_id + '" name="Place the function in their own section (-ffunction-sections)" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.ffunction" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    xml += '                <option id="fr.ac6.managedbuild.gnu.c.compiler.option.optimization.level.' + program_id + '" name="Optimization Level" superClass="fr.ac6.managedbuild.gnu.c.compiler.option.optimization.level" useByScannerDiscovery="false" value="fr.ac6.managedbuild.gnu.c.optimization.level.most" valueType="enumerated"/>\n'
    xml += '                <option defaultValue="gnu.c.debugging.level.none" id="gnu.c.compiler.option.debugging.level.' + program_id + '" name="Debug Level" superClass="gnu.c.compiler.option.debugging.level" useByScannerDiscovery="false" value="gnu.c.debugging.level.default" valueType="enumerated"/>\n'
    # Add macro definitions
    xml += '                <option id="gnu.c.compiler.option.preprocessor.def.symbols.' + program_id + '" name="Defined symbols (-D)" superClass="gnu.c.compiler.option.preprocessor.def.symbols" useByScannerDiscovery="false" valueType="definedSymbols">\n'
    for library in libraries:
        if 'defines' in libraries[library]:
            for define in libraries[library]['defines']:
                define = define.replace('"', '\&quot;')
                xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    for middleware in middlewares:
        if 'defines' in middlewares[middleware]:
            for define in middlewares[middleware]['defines']:
                define = define.replace('"', '\&quot;')
                xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    if 'defines' in configurations[conf]:
        for define in configurations[conf]['defines']:
            define = define.replace('"', '\&quot;')
            xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    if 'defines' in programs[program]:
        for define in programs[program]['defines']:
            define = define.replace('"', '\&quot;')
            xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    xml += '                  <listOptionValue builtIn="false" value="BENCHMARK_NAME=&quot;' + program + '&quot;"/>\n'
    xml += '                </option>\n'
    # Add include paths
    xml += '                <option id="gnu.c.compiler.option.include.paths.' + program_id + '" name="Include paths (-I)" superClass="gnu.c.compiler.option.include.paths" useByScannerDiscovery="false" valueType="includePath">\n'
    for library in libraries:
        if 'includes' in libraries[library]:
            for include in libraries[library]['includes']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    for middleware in middlewares:
        if 'includes' in middlewares[middleware]:
            for include in middlewares[middleware]['includes']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in configurations[conf]:
        for include in configurations[conf]["includes"]:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in programs[program]:
        for include in programs[program]['includes']:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    xml += '                  <listOptionValue builtIn="false" value="&quot;' + '${ProjDirPath}/inc' + '&quot;"/>\n'
    xml += '                </option>\n'
    # Add other C flags
    xml += '                <option id="fr.ac6.managedbuild.gnu.c.compiler.option.misc.other.' + program_id + '" name="Other flags" superClass="fr.ac6.managedbuild.gnu.c.compiler.option.misc.other" useByScannerDiscovery="false" value="--target=arm-none-eabi'
    for library in libraries:
        if 'cflags' in libraries[library]:
            for cflag in libraries[library]['cflags']:
                xml += ' ' + cflag
    for middleware in middlewares:
        if 'cflags' in middlewares[middleware]:
            for cflag in middlewares[middleware]['cflags']:
                xml += ' ' + cflag
    if 'cflags' in configurations[conf]:
        for cflag in configurations[conf]['cflags']:
            xml += ' ' + cflag
    if 'cflags' in programs[program]:
        for cflag in programs[program]['cflags']:
            xml += ' ' + cflag
    xml += '" valueType="string"/>\n'
    xml += '                <option id="gnu.c.compiler.option.optimization.flags.' + program_id + '" name="Other optimization flags" superClass="gnu.c.compiler.option.optimization.flags" useByScannerDiscovery="false" value="" valueType="string"/>\n'
    xml += '                <option id="gnu.c.compiler.option.dialect.std.' + program_id + '" name="Language standard" superClass="gnu.c.compiler.option.dialect.std" useByScannerDiscovery="false" value="gnu.c.compiler.dialect.default" valueType="enumerated"/>\n'
    xml += '                <option id="gnu.c.compiler.option.misc.verbose.' + program_id + '" name="Verbose (-v)" superClass="gnu.c.compiler.option.misc.verbose" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    xml += '                <option id="gnu.c.compiler.option.include.files.' + program_id + '" name="Include files (-include)" superClass="gnu.c.compiler.option.include.files" useByScannerDiscovery="false"/>\n'
    xml += '                <inputType id="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.input.c.' + program_id + '" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.input.c"/>\n'
    xml += '                <inputType id="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.input.s.' + program_id + '" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.input.s"/>\n'
    xml += '              </tool>\n'
    ###########################################################################
    # Set up C++ compiler
    ###########################################################################
    xml += '              <tool id="fr.ac6.managedbuild.tool.gnu.cross.cpp.compiler.' + program_id + '" name="MCU G++ Compiler" superClass="fr.ac6.managedbuild.tool.gnu.cross.cpp.compiler">\n'
    xml += '                <option id="fr.ac6.managedbuild.gnu.cpp.compiler.option.optimization.level.' + program_id + '" name="Optimization Level" superClass="fr.ac6.managedbuild.gnu.cpp.compiler.option.optimization.level" useByScannerDiscovery="false" value="fr.ac6.managedbuild.gnu.cpp.optimization.level.most" valueType="enumerated"/>\n'
    xml += '                <option defaultValue="gnu.cpp.compiler.debugging.level.none" id="gnu.cpp.compiler.option.debugging.level.' + program_id + '" name="Debug Level" superClass="gnu.cpp.compiler.option.debugging.level" useByScannerDiscovery="false" valueType="enumerated"/>\n'
    xml += '              </tool>\n'
    ###########################################################################
    # Set up C linker
    ###########################################################################
    xml += '              <tool command="' + clang_path + '" id="fr.ac6.managedbuild.tool.gnu.cross.c.linker.' + program_id + '" name="MCU GCC Linker" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.linker">\n'
    xml += '                <option id="fr.ac6.managedbuild.tool.gnu.cross.c.linker.gcsections.' + program_id + '" name="Discard unused sections (-Wl,--gc-sections)" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.linker.gcsections" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add linker script
    xml += '                <option id="fr.ac6.managedbuild.tool.gnu.cross.c.linker.script.' + program_id + '" name="Linker Script (-T)" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.linker.script" useByScannerDiscovery="false" value="${ProjDirPath}/LinkerScript.ld" valueType="string"/>\n'
    # Add linked libraries
    xml += '                <option id="gnu.c.link.option.libs.' + program_id + '" name="Libraries (-l)" superClass="gnu.c.link.option.libs" useByScannerDiscovery="false" valueType="libs">\n'
    for library in libraries:
        xml += '                  <listOptionValue builtIn="false" value="' + library + '"/>\n'
    xml += '                </option>\n'
    # Add other linker flags
    xml += '                <option id="gnu.c.link.option.ldflags.' + program_id + '" name="Linker flags" superClass="gnu.c.link.option.ldflags" useByScannerDiscovery="false" value="--target=arm-none-eabi -fuse-ld=lld'
    for library in libraries:
        if 'ldflags' in libraries[library]:
            for ldflag in libraries[library]['ldflags']:
                xml += ' ' + ldflag
    for middleware in middlewares:
        if 'ldflags' in middlewares[middleware]:
            for ldflag in middlewares[middleware]['ldflags']:
                xml += ' ' + ldflag
    if 'ldflags' in configurations[conf]:
        for ldflag in configurations[conf]['ldflags']:
            xml += ' ' + ldflag
    if 'ldflags' in programs[program]:
        for ldflag in programs[program]['ldflags']:
            xml += ' ' + ldflag
    xml += '" valueType="string"/>\n'
    # Add library search paths
    xml += '                <option id="gnu.c.link.option.paths.' + program_id + '" name="Library search path (-L)" superClass="gnu.c.link.option.paths" useByScannerDiscovery="false" valueType="libPaths">\n'
    for library in libraries:
        if 'library_paths' in libraries[library]:
            for library_path in libraries[library]['library_paths']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + library_path + '&quot;"/>\n'
    xml += '                </option>\n'
    # Add other objects
    xml += '                <option id="gnu.c.link.option.userobjs.' + program_id + '" name="Other objects" superClass="gnu.c.link.option.userobjs" useByScannerDiscovery="false" valueType="userObjs">\n'
    for library in libraries:
        if 'objects' in libraries[library]:
            for obj in libraries[library]['objects']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + obj + '&quot;"/>\n'
    xml += '                </option>\n'
    xml += '                <inputType id="cdt.managedbuild.tool.gnu.c.linker.input.' + program_id + '" superClass="cdt.managedbuild.tool.gnu.c.linker.input">\n'
    xml += '                  <additionalInput kind="additionalinputdependency" paths="$(USER_OBJS)"/>\n'
    xml += '                  <additionalInput kind="additionalinput" paths="$(LIBS)"/>\n'
    xml += '                </inputType>\n'
    xml += '              </tool>\n'
    ###########################################################################
    # Set up C++ linker
    ###########################################################################
    xml += '              <tool id="fr.ac6.managedbuild.tool.gnu.cross.cpp.linker.' + program_id + '" name="MCU G++ Linker" superClass="fr.ac6.managedbuild.tool.gnu.cross.cpp.linker"/>\n'
    ###########################################################################
    # Set up archiver
    ###########################################################################
    xml += '              <tool id="fr.ac6.managedbuild.tool.gnu.archiver.' + program_id + '" name="MCU GCC Archiver" superClass="fr.ac6.managedbuild.tool.gnu.archiver"/>\n'
    ###########################################################################
    # Set up assembler
    ###########################################################################
    xml += '              <tool command="' + clang_path + '" id="fr.ac6.managedbuild.tool.gnu.cross.assembler.exe.release.' + program_id + '" name="MCU GCC Assembler" superClass="fr.ac6.managedbuild.tool.gnu.cross.assembler.exe.release">\n'
    # Add include paths
    xml += '                <option id="gnu.both.asm.option.include.paths.' + program_id + '" name="Include paths (-I)" superClass="gnu.both.asm.option.include.paths" useByScannerDiscovery="false" valueType="includePath">\n'
    for library in libraries:
        if 'includes' in libraries[library]:
            for include in libraries[library]['includes']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    for middleware in middlewares:
        if 'includes' in middlewares[middleware]:
            for include in middlewares[middleware]['includes']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in configurations[conf]:
        for include in configurations[conf]["includes"]:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in programs[program]:
        for include in programs[program]['includes']:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    xml += '                  <listOptionValue builtIn="false" value="&quot;' + '${ProjDirPath}/inc' + '&quot;"/>\n'
    xml += '                </option>\n'
    xml += '                <option id="gnu.both.asm.option.flags.' + program_id + '" name="Assembler flags" superClass="gnu.both.asm.option.flags" useByScannerDiscovery="false" value="--target=arm-none-eabi -c" valueType="string"/>\n'
    xml += '                <inputType id="cdt.managedbuild.tool.gnu.assembler.input.' + program_id + '" superClass="cdt.managedbuild.tool.gnu.assembler.input"/>\n'
    xml += '                <inputType id="fr.ac6.managedbuild.tool.gnu.cross.assembler.input.' + program_id + '" superClass="fr.ac6.managedbuild.tool.gnu.cross.assembler.input"/>\n'
    xml += '              </tool>\n'
    xml += '            </toolChain>\n'
    xml += '          </folderInfo>\n'
    ###########################################################################
    # Set up source entries
    ###########################################################################
    xml += '          <sourceEntries>\n'
    for middleware in middlewares:
        if 'directories' in middlewares[middleware]:
            for directory in middlewares[middleware]['directories']:
                xml += '            <entry excluding="' + middlewares[middleware]['directories'][directory] + '" flags="VALUE_WORKSPACE_PATH|RESOLVED" kind="sourcePath" name="' + directory + '"/>\n'
    beebs_exclude = ''
    for p in programs:
        if p != program:
            beebs_exclude += p + '|'
    beebs_exclude = beebs_exclude[:-1]
    xml += '            <entry excluding="' + beebs_exclude + '" flags="VALUE_WORKSPACE_PATH|RESOLVED" kind="sourcePath" name="src"/>\n'
    xml += '            <entry flags="VALUE_WORKSPACE_PATH|RESOLVED" kind="sourcePath" name="startup"/>\n'
    xml += '          </sourceEntries>\n'
    xml += '        </configuration>\n'
    xml += '      </storageModule>\n'
    xml += '      <storageModule moduleId="org.eclipse.cdt.core.externalSettings"/>\n'
    xml += '    </cconfiguration>\n'

    return xml


#
# Generate and return the footer of core settings.
#
def gen_core_settings_footer():
    return '  </storageModule>\n'


#
# Generate and return the whole cproject file content for all configurations.
#
def gen_cproject():
    xml =  gen_header()

    # Generate core settings for each pair of configuration and program
    xml += gen_core_settings_header()
    for conf in configurations:
        for program in sorted(programs.keys()):
            xml += gen_core_settings_config(conf, program)
    xml += gen_core_settings_footer()

    # Generate refresh scope for each pair of configuration and program
    xml += gen_refresh_scope_header()
    for conf in configurations:
        for program in sorted(programs.keys()):
            xml += gen_refresh_scope_config(conf, program)
    xml += gen_refresh_scope_footer()

    # Generate scanner configuration for each pair of configuration and program
    xml += gen_scanner_header()
    for conf in configurations:
        for program in sorted(programs.keys()):
            xml += gen_scanner_config(conf, program)
    xml += gen_scanner_footer()

    xml += gen_footer()

    return xml


#
# Generate and return the file content of language.settings.xml which disables
# discovering compiler's built-in language settings.
#
def gen_language_settings():
    xml  = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    xml += '<project>\n'
    for conf in configurations:
        for program in sorted(programs.keys()):
            program_id = conf + '-' + program
            xml += '  <configuration id="fr.ac6.managedbuild.config.gnu.cross.exe.release.' + program_id + '" name="' + program_id + '">\n'
            xml += '    <extension point="org.eclipse.cdt.core.LanguageSettingsProvider">\n'
            xml += '      <provider copy-of="extension" id="org.eclipse.cdt.ui.UserLanguageSettingsProvider"/>\n'
            xml += '      <provider-reference id="org.eclipse.cdt.core.ReferencedProjectsLanguageSettingsProvider" ref="shared-provider"/>\n'
            xml += '      <provider-reference id="org.eclipse.cdt.managedbuilder.core.MBSLanguageSettingsProvider" ref="shared-provider"/>\n'
            xml += '    </extension>\n'
            xml += '  </configuration>\n'
    xml += '</project>\n'

    return xml


#
# The main function.
#
def main():
    # Generate a .cproject file for all configurations
    conf_filename = project_dir + '/.cproject'
    xml = gen_cproject()
    with open(conf_filename, 'w') as f:
        f.write(xml)

    # In addition, also generate language.settings.xml that disable discovering
    # compiler's built-in language settings
    settings_dir = project_dir + '/.settings'
    if not os.path.isdir(settings_dir):
        os.mkdir(settings_dir)
    with open(settings_dir + '/language.settings.xml', 'w') as f:
        f.write(gen_language_settings())


if __name__ == '__main__':
    main()
