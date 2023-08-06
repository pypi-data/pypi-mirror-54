import os
import sys
import json
import time
import git
import zipfile
import re
import codecs
from shutil import copyfile

try:
    from tools import *
except:
    from yoctools.tools import *

class Component:
    def __init__(self, path=''):
        self.name = ''
        self.path = path
        self.type = 'common'
        self.version = 'master'
        self.depends = []
        self.description = ''
        self.version = ''
        self.license = ''
        self.historyVersion = {}
        self.updated = ''
        self.repo_url = ''
        self.repo = None
        self.yoc_version = ''
        self.includes = []
        self.sources = []
        self.defconfig = []
        self.AFLAGS = ''
        self.CFLAGS = ''
        self.CXXFLAGS = ''
        self.LDFLAGS = ''
        self.ld_script = ''
        self.depends_on = []  # 该组件被哪个组件依赖
        self.installs = []

        if self.path:
            # self.update_aone()
            self.load_package()


    def loader_json(self, js):
        self.js = js
        self.name = js['name']
        self.depends = js['depends']
        self.description = js['description']
        self.version = js['versions']
        self.license = js['license']
        self.repo_url = js['aboutURL']

        self.updated = js['updated']

        for ver in js['historyVersion']:
            self.historyVersion[ver['version']] = ver['url']

        if self.name == 'yoc_base':
            self.depends = [
                {"name": "minilibc", "version": "master"},
                {"name": "aos", "version": "master"},
                {"name": "csi", "version": "master"},
                {"name": "rhino", "version": "master"},
                {"name": "lwip", "version": "master"},
            ]
            # print(json.dumps(js, indent=4))

        if self.type == "common":
            self.path = 'components/' + self.name
        elif self.type == 'chip':
            self.path = 'chip/' + self.name
        elif self.type == 'board':
            self.path = 'boards/' + self.name
        elif self.type == 'solution':
            self.path = 'solutions/' + self.name
        else:
            self.path = 'components/' + self.name


    def download(self, yoc_path=''):
        if self.repo_url:
            if (not os.path.exists(self.path)) or (not os.path.isdir(os.path.join(self.path, '.git'))):
                print('git clone %s (%s)...' % (self.name, self.version))
                self.repo = git.Repo.init(self.path)
                origin = self.repo.create_remote(name='origin', url=http2git(self.repo_url))
                origin.fetch()

                self.repo.create_head(self.version, origin.refs.master)  # create local branch "master" from remote "master"
                self.repo.heads.master.set_tracking_branch(origin.refs.master)  # set local "master" to track remote "master
                self.repo.heads.master.checkout()  # checkout local "master" to working tree
        elif self.version in self.historyVersion.keys():
            zip_url = self.historyVersion[self.version]
            filename = http_get(zip_url, os.path.join(yoc_path, '.cache'))
            zipf = zipfile.ZipFile(filename)
            if self.path != '.':
                zipf.extractall('components/')
            else:
                zipf.extractall('.')


    def update_aone(self):
        if self.repo == None:
            self.repo = git.Repo.init(self.path)

        try:
            aone = self.repo.remotes['aone']
        except:
            aone_url = 'git@gitlab.alibaba-inc.com:yoc7/' + self.name + '.git'
            aone = self.repo.create_remote(name='aone', url=aone_url)


    def zip(self, path):
        zipName = os.path.join(path, '.cache', self.name + '-' + self.version + '.zip')
        if os.path.exists(zipName):
            os.remove(zipName)
        zip_path(self.path, zipName)

        return zipName


    def show(self):
        if os.path.isdir(self.path):
            status = '*'
        else:
            status = ' '

        s1 = self.name + ' (' + self.version + ')'
        size = len(s1)

        text1, text2 = string_strip(self.description, 80)
        print("%s %s %s - %s" % (status, s1, ' ' * (40 - size), text1))
        while text2:
            text1, text2 = string_strip(text2, 80)
            print(' ' * 46 + text1)


    def get_parameters(self):
        return self.package

    def get_sources(self, build):
        sources = []
        for s in self.sources:
            v = s.split('?')
            if len(v) > 1:
                x = re.search('<(.+?)>', v[1], re.M|re.I)
                if build and build.get_variable(x.group(1)) not in ['y', 'Y', 'T', '1', 'yes']:
                    continue

            fn = build.convert(v[0])
            f = build.env.Glob(fn)
            if not f:
                print("not found file:", fn)
                exit(0)

            sources.append(f)
        return sources


    def load_package(self):
        filename = os.path.join(self.path, 'package.yaml')
        self.package = load_package(filename)
        if self.package == None:
            return

        def package_get(name, value):
            if name in self.package.keys():
                return self.package[name]
            return value

        self.name = package_get('name', self.name)
        self.type = package_get('type', self.type)
        self.description = package_get('description', self.description)
        self.yoc_version = package_get('yoc_version', '')
        if self.repo:
            self.version    = self.repo.active_branch.name
        self.sources     = package_get('SOURCES', [])
        self.defconfig   = package_get('DEFCONFIG', [])
        self.board_name  = package_get('board_name', '')
        self.installs    = package_get('EXPORT_INCS', [])
        self.board       = package_get('BOARD', None)
        if self.board:
            self.ld_script = os.path.join(self.path, self.board.ld_script)

        self.AFLAGS   = package_get('AFLAGS', '').split()
        self.CFLAGS   = package_get('CFLAGS', '').split()
        self.CCFLAGS  = package_get('CCFLAGS', '').split()
        self.CXXFLAGS = package_get('CXXFLAGS', '').split()
        self.LDFLAGS  = package_get('LDFLAGS', '').split()

        self.includes = []
        if 'LOCAL_INCS' in self.package:
            for inc in self.package['LOCAL_INCS']:
                path = os.path.join(self.path, inc)
                if os.path.isdir(path):
                    self.includes.append(path)
        self.package['CPPPATH'] = self.includes


        if 'depends' in self.package:
            self.depends = []
            for d in self.package['depends']:
                if type(d) == dict:
                    for k, v in d.items():
                        self.depends.append(k)
                else:
                    self.depends.append(d)

        del self.package['name']
        if 'SOURCES' in self.package:
            del self.package['SOURCES']


    def getDependList(self, components):
        deps = []
        def ccc(comp):
            if comp.path not in deps:
                deps.append(comp)
            for dep in comp.depends:
                c = components.get(dep)
                if c:
                    ccc(c)

        ccc(self)
        return deps


class ComponentGroup:
    def __init__(self):
        self.components = {}

    def add(self, component):
        self.components[component.name] = component

    def size(self):
        return len(self.components)


    def get(self, name):
        if name in self.components:
            return self.components[name]

    def remove(self, name):
        if name in self.components:
            del self.components[name]

    def show(self):
        for _, component in self.components.items():
            component.show()

    def items(self):
        return self.components.items()

    def download(self, name):
        if name in self.components:
            component = self.components[name]
            if component:
                component.download()


    def calc_depend(self):
        for _, component in self.components.items():
            component.depends_on = []
        for _, component in self.components.items():
            for dep in component.depends:
                p = self.get(dep)
                if p:
                    p.depends_on.append(component)


def string_strip(text, size):
    L = 0
    R = ''
    i = 0
    for c in text:
        if c >= '\u4E00' and c <= '\u9FA5':
            # print(c)
            L += 2
        else:
            # print('  ', c)
            L += 1
        R += c
        i += 1
        if L >= size:
            break
    return R, text[i:]


def version_compr(a, b):
    if b[:2] == '>=':
        return a >= b[2:]
    if b[:1] == '>':
        return a > b[1:]
    return a == b


if __name__ == "__main__":
    compr = version_compr('v7.2.2', '>=v7.2.1')
    print(compr)

    compr = version_compr('v7.2.2', '>v7.2.1')
    print(compr)

    compr = version_compr('v7.2.1', 'v7.2.1')
    print(compr)