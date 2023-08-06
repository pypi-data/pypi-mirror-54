import os
import re
import SCons.Script as scons


# toolchains options
CROSS_TOOL_PATH   = '/opt/gcc-csky-abiv2/bin'

class Builder(object):
    def __init__(self):
        self.PREFIX  = 'csky-elfabiv2-'
        self.SIZE    = self.PREFIX + 'size'
        self.OBJDUMP = self.PREFIX + 'objdump'
        self.OBJCPY  = self.PREFIX + 'objcopy'
        self.STRIP   = self.PREFIX + 'strip'

        self.DEBUG   = 'release'
        self.lib_path = ''
        self.variable = {}
        self.export_includes = []

        self.env = scons.Environment(tools = ['default'],
            AS   = self.PREFIX + 'gcc',
            CC   = self.PREFIX + 'gcc',
            CXX  = self.PREFIX + 'g++',
            AR   = self.PREFIX + 'ar', ARFLAGS = '-rc',
            LINK = self.PREFIX + 'g++',
        )
        # self.env.Decider('timestamp-newer')
        self.env.Decider('make')
        # self.env.Decider('MD5')

        self.env.PrependENVPath('TERM', "xterm-256color")
        self.env.PrependENVPath('PATH', os.getenv('PATH'))

        if scons.GetOption('verbose'):
            self.env.Replace(
                ARCOMSTR = 'AR $TARGET',
                ASCOMSTR = 'AS $TARGET',
                ASPPCOMSTR = 'AS $TARGET',
                CCCOMSTR = 'CC $TARGET',
                CXXCOMSTR = 'CXX $TARGET',
                # LINKCOMSTR = 'LINK $TARGET',
                INSTALLSTR = 'INSTALL $TARGET'
            )

        self.yoc_compile_flags = \
            ' -ffunction-sections -fdata-sections' + \
            ' -g -Wpointer-arith -Wundef -Wall -Wl,-EL' + \
            ' -fno-inline-functions -nostdlib -fno-builtin -mistack' + \
            ' -fno-strict-aliasing -fno-strength-reduce'


    def SetInstallPath(self, path):
        self.lib_path = os.path.join(path, "lib")

    def set_cpu(self, cpu):
        flags = ['-MP', '-MMD']
        self.CPU = cpu.lower()
        if self.CPU in ['ck801', 'ck802', 'ck803', 'ck805', 'ck803f', 'ck803ef', 'ck803efr1', 'ck803efr2', 'ck803efr3', 'ck804ef', 'ck805f']:
            DEVICE = '-mcpu=' + self.CPU
            flags.append('-mcpu=' + self.CPU)
            if 'f' in self.CPU:
                flags.append('-mhard-float')

            if self.CPU == 'ck803ef':
                flags.append('-mhigh-registers -mdsp')
        else:
            print ('Please make sure your cpu mode')
            exit(0)

        if self.DEBUG == 'debug':
            flags.append(['-O0', '-g'])
        else:
            flags.append('-Os')

        # CCFLAGS  += self.yoc_compile_flags

        self.env.AppendUnique(
            ASFLAGS = flags,
            CCFLAGS = flags,
            CXXFLAGS = flags,
            LINKFLAGS = flags
        )


    def library(self, name, src, **parameters):
        if name and src:
            env = self.env.Clone()
            group = parameters
            if 'CCFLAGS' in group:
                env.AppendUnique(CCFLAGS = group['CCFLAGS'].split())
            if 'CPPPATH' in group:
                if type(group['CPPPATH']) == type('str'):
                    env.AppendUnique(CPPPATH=group['CPPPATH'].split())
                else:
                    env.AppendUnique(CPPPATH=group['CPPPATH'])

            if 'CPPFLAGS' in group:
                env.AppendUnique(CPPFLAGS=group['CPPFLAGS'].split())
            env.AppendUnique(CPPPATH=self.export_includes)
            objs = env.StaticLibrary(os.path.join(self.lib_path, name), src)
            env.Default(objs)


    def program(self, name, source, **parameters):
        env = self.env.Clone()
        if 'CPPPATH' in parameters:
            for path in parameters['CPPPATH']:
                env.AppendUnique(CPPPATH=path)
            del parameters['CPPPATH']

        parameters['LIBPATH'] = self.lib_path + ':' + self.lib_path

        linkflags =  ' -Wl,--whole-archive -l' + ' -l'.join(parameters['LIBS'])
        linkflags += ' -Wl,--no-whole-archive -nostartfiles -Wl,--gc-sections -lm '

        if 'LD_SCRIPT' in parameters:
            linkflags += ' -T ' + parameters['LD_SCRIPT']
            del parameters['LD_SCRIPT']

        linkflags += ' -Wl,-ckmap="yoc.map" -Wl,-zmax-page-size=1024'

        env.AppendUnique(LINKFLAGS=linkflags.split())
        env.AppendUnique(CPPPATH=self.export_includes)

        del parameters['LIBS']

        v = env.Program(target=name, source=source, **parameters)

        env.Default(v)


    def get_variable(self, var):
        if var in self.variable:
            return self.variable[var]


    def convert(self, var):
        x = re.findall('<(.+?)>', var)
        for key in x:
            value = self.get_variable(key)
            if value:
                var = var.replace('<'+key+'>', self.variable[key])
            else:
                print('not found variable:', var)

        return var
