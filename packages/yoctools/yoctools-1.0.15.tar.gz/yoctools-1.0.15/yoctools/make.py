#! /bin/env python

import os
import sys

try:
    from yoc import YoC
    from tools import load_package
except:
    from yoctools.yoc import YoC
    from yoctools.tools import load_package

import SCons.Script as scons

scons.AddOption('--verbose', dest='verbose', default=True,
    action='store_false',
    help='verbose command line output')

scons.AddOption('--component',
        dest='component',
        type='string',
        nargs=1,
        action='store',
        help='compile component list.')


class Make(object):
    def __init__(self):
        self.yoc = YoC()
        self.build_env = self.yoc.genBuildEnv()


    def library(self, name, src, **parameters):
        self.build_env.library(name, src, **parameters)


    def library_yaml(self):
        pack = load_package('package.yaml')
        if pack:
            name = pack['name']
            component = self.yoc.components.get(name)

            sources = component.get_sources(self.build_env)
            pack = component.get_parameters()

            self.build_env.library(name, sources, **pack)


    def program(self, **parameters):
        pack = load_package('package.yaml')

        if pack:
            name = pack['name']
            component = self.yoc.components.get(name)
            sources = component.get_sources(self.build_env)
            pack = component.get_parameters()
            pack['LD_SCRIPT'] = self.yoc.current_board.ld_script

            self.build_env.program(name + '.elf', sources, **pack)


    def build_package(self, packages):
        for d in packages:
            file_name = os.path.join(d, 'SConscript')
            if os.path.isfile(file_name):
                scons.SConscript(file_name, exports={"env" : self.build_env.env.Clone()})
