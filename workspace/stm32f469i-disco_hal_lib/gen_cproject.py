#!/usr/bin/env python3

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
project_name = 'stm32f469i-disco_hal_lib'


#
# Dict of dependent libraries.
#
libraries = {
    'c': {
        'includes': [
            '${openstm32_compiler_path}/../arm-none-eabi/include',
        ],
    },
}


#
# Dict of programs to compile.
#
programs = {
    'stm32f469i-disco_hal_lib': {
        'defines': [
            'STM32F469xx',
            'USE_HAL_DRIVER',
        ],
        'includes': [
            '${ProjDirPath}/Utilities/Components/ili9325',
            '${ProjDirPath}/Utilities/Components/s25fl512s',
            '${ProjDirPath}/Utilities/Components/cs43l22',
            '${ProjDirPath}/Utilities/Components/ili9341',
            '${ProjDirPath}/Utilities/Components/ampire480272',
            '${ProjDirPath}/Utilities/Components/n25q512a',
            '${ProjDirPath}/Utilities/Components/s5k5cag',
            '${ProjDirPath}/Utilities/Components/mfxstm32l152',
            '${ProjDirPath}/CMSIS/device',
            '${ProjDirPath}/Utilities/Components/n25q128a',
            '${ProjDirPath}/Utilities/Components/ts3510',
            '${ProjDirPath}/Utilities/Components/st7735',
            '${ProjDirPath}/HAL_Driver/Inc/Legacy',
            '${ProjDirPath}/Utilities/Components/lis302dl',
            '${ProjDirPath}/Utilities/Components/otm8009a',
            '${ProjDirPath}/Utilities/STM32469I-Discovery',
            '${ProjDirPath}/Utilities/Components/stmpe1600',
            '${ProjDirPath}/Utilities/Components/Common',
            '${ProjDirPath}/Utilities/Components/ov2640',
            '${ProjDirPath}/Utilities/Components/l3gd20',
            '${ProjDirPath}/HAL_Driver/Inc',
            '${ProjDirPath}/Utilities',
            '${ProjDirPath}/Utilities/Components/stmpe811',
            '${ProjDirPath}/Utilities/Components/lis3dsh',
            '${ProjDirPath}/Utilities/Components/wm8994',
            '${ProjDirPath}/Utilities/Fonts',
            '${ProjDirPath}/Utilities/Components/n25q256a',
            '${ProjDirPath}/Utilities/Components/ls016b8uy',
            '${ProjDirPath}/Utilities/Components/ft6x06',
            '${ProjDirPath}/Utilities/Components/exc7200',
            '${ProjDirPath}/Utilities/Components/st7789h2',
            '${ProjDirPath}/Utilities/Log',
            '${ProjDirPath}/Utilities/Components/ampire640480',
            '${ProjDirPath}/Utilities/Components/lsm303dlhc',
            '${ProjDirPath}/CMSIS/core',
        ],
        'directories': {
            'HAL_Driver': 'Src/stm32f4xx_hal_timebase_tim_template.c|Src/stm32f4xx_hal_timebase_rtc_wakeup_template.c|Src/stm32f4xx_hal_timebase_rtc_alarm_template.c',
            'Utilities': 'Fonts|Log',
        },
    },
}


#
# Dict of configurations.
#
configurations = {
    'baseline': {},
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
    xml += '    <project id="' + project_name + '.null" name="' + project_name + '"/>\n'
    xml += '  </storageModule>\n'
    xml += '  <storageModule moduleId="org.eclipse.cdt.core.LanguageSettingsProviders"/>\n'
    xml += '</cproject>\n'
    return xml


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
    xml =  '    <scannerConfigBuildInfo instanceId="fr.ac6.managedbuild.config.gnu.cross.lib.release.' + program_id + ';fr.ac6.managedbuild.config.gnu.cross.lib.release.' + program_id + '.;fr.ac6.managedbuild.tool.gnu.cross.c.compiler.' + program_id + ';fr.ac6.managedbuild.tool.gnu.cross.c.compiler.input.c.' + program_id + '">\n'
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
# @board: the name of the board to use.
# @conf: the name of the configuration to use.
# @program: the name of the program.
#
def gen_core_settings_config(conf, program):
    program_id = conf + '-' + program

    xml =  '    <!-- Configuration of ' + program_id + ' -->\n'
    xml += '    <cconfiguration id="fr.ac6.managedbuild.config.gnu.cross.lib.release.' + program_id + '">\n'
    xml += '      <storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="fr.ac6.managedbuild.config.gnu.cross.lib.release.' + program_id + '" moduleId="org.eclipse.cdt.core.settings" name="' + program_id + '">\n'
    xml += '        <externalSettings>\n'
    xml += '          <externalSetting>\n'
    xml += '            <entry flags="VALUE_WORKSPACE_PATH" kind="includePath" name="/' + project_name + '"/>\n'
    xml += '            <entry flags="VALUE_WORKSPACE_PATH" kind="libraryPath" name="/' + project_name + '/' + program_id + '"/>\n';
    xml += '            <entry flags="RESOLVED" kind="libraryFile" name="' + program + '" srcPrefixMapping="" srcRootPath=""/>\n'
    xml += '          </externalSetting>\n'
    xml += '        </externalSettings>\n'
    xml += '        <extensions>\n'
    xml += '          <extension id="org.eclipse.cdt.core.ELF" point="org.eclipse.cdt.core.BinaryParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GmakeErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.CWDLocator" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '        </extensions>\n'
    xml += '      </storageModule>\n'
    xml += '      <storageModule moduleId="cdtBuildSystem" version="4.0.0">\n'
    xml += '        <configuration artifactExtension="a" artifactName="' + program + '" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.staticLib" buildProperties="org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.staticLib,org.eclipse.cdt.build.core.buildType=org.eclipse.cdt.build.core.buildType.release" cleanCommand="rm -rf" description="" id="fr.ac6.managedbuild.config.gnu.cross.lib.release.' + program_id + '" name="' + program_id + '" optionalBuildProperties="org.eclipse.cdt.docker.launcher.containerbuild.property.selectedvolumes=,org.eclipse.cdt.docker.launcher.containerbuild.property.volumes=" parent="fr.ac6.managedbuild.config.gnu.cross.lib.release">\n'
    xml += '          <folderInfo id="fr.ac6.managedbuild.config.gnu.cross.lib.release.' + program_id + '." name="/" resourcePath="">\n'
    xml += '            <toolChain id="fr.ac6.managedbuild.toolchain.gnu.cross.lib.release.' + program_id + '" name="Ac6 STM32 MCU GCC" superClass="fr.ac6.managedbuild.toolchain.gnu.cross.lib.release">\n'
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
    xml += '                <option id="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.fdata.' + program_id + '" name="Place the data in their own section (-fdata-sections)" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.fdata" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    xml += '                <option id="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.ffunction.' + program_id + '" name="Place the function in their own section (-ffunction-sections)" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.compiler.ffunction" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    xml += '                <option id="fr.ac6.managedbuild.gnu.c.compiler.option.optimization.level.' + program_id + '" name="Optimization Level" superClass="fr.ac6.managedbuild.gnu.c.compiler.option.optimization.level" useByScannerDiscovery="false" value="fr.ac6.managedbuild.gnu.c.optimization.level.most" valueType="enumerated"/>\n'
    xml += '                <option defaultValue="gnu.c.debugging.level.none" id="gnu.c.compiler.option.debugging.level.' + program_id + '" name="Debug Level" superClass="gnu.c.compiler.option.debugging.level" useByScannerDiscovery="false" value="gnu.c.debugging.level.default" valueType="enumerated"/>\n'
    # Add macro definitions
    xml += '                <option id="gnu.c.compiler.option.preprocessor.def.symbols.' + program_id + '" name="Defined symbols (-D)" superClass="gnu.c.compiler.option.preprocessor.def.symbols" useByScannerDiscovery="false" valueType="definedSymbols">\n'
    for library in libraries:
        if 'defines' in libraries[library]:
            for define in libraries[library]['defines']:
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
    xml += '                </option>\n'
    # Add include paths
    xml += '                <option id="gnu.c.compiler.option.include.paths.' + program_id + '" name="Include paths (-I)" superClass="gnu.c.compiler.option.include.paths" useByScannerDiscovery="false" valueType="includePath">\n'
    for library in libraries:
        if 'includes' in libraries[library]:
            for include in libraries[library]['includes']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in configurations[conf]:
        for include in configurations[conf]["includes"]:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in programs[program]:
        for include in programs[program]['includes']:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    xml += '                </option>\n'
    # Add other C flags
    xml += '                <option id="fr.ac6.managedbuild.gnu.c.compiler.option.misc.other.' + program_id + '" name="Other flags" superClass="fr.ac6.managedbuild.gnu.c.compiler.option.misc.other" useByScannerDiscovery="false" value="--target=arm-none-eabi'
    for library in libraries:
        if 'cflags' in libraries[library]:
            for cflag in libraries[library]['cflags']:
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
    xml += '              <tool id="fr.ac6.managedbuild.tool.gnu.cross.c.linker.' + program_id + '" name="MCU GCC Linker" superClass="fr.ac6.managedbuild.tool.gnu.cross.c.linker"/>\n'
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
    xml += '              <tool command="' + clang_path + '" id="fr.ac6.managedbuild.tool.gnu.cross.assembler.lib.release.' + program_id + '" name="MCU GCC Assembler" superClass="fr.ac6.managedbuild.tool.gnu.cross.assembler.lib.release">\n'
    # Add include paths
    xml += '                <option id="gnu.both.asm.option.include.paths.' + program_id + '" name="Include paths (-I)" superClass="gnu.both.asm.option.include.paths" useByScannerDiscovery="false" valueType="includePath">\n'
    for library in libraries:
        if 'includes' in libraries[library]:
            for include in libraries[library]['includes']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in configurations[conf]:
        for include in configurations[conf]["includes"]:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in programs[program]:
        for include in programs[program]['includes']:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
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
    if 'directories' in programs[program]:
        for directory in programs[program]['directories']:
            xml += '            <entry excluding="' + programs[program]['directories'][directory] + '" flags="VALUE_WORKSPACE_PATH|RESOLVED" kind="sourcePath" name="' + directory + '"/>\n'
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
            xml += '  <configuration id="fr.ac6.managedbuild.config.gnu.cross.lib.release.' + program_id + '" name="' + program_id + '">\n'
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
