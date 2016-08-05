# coding=utf-8
# from http://blog.biicode.com/bii-internals-compiling-your-python-application-with-cython/
biicode_pkg_path = PATH_TO_BIICODE_MODULE
biicode_python_path = os.path.dirname(biicode_pkg_path)
build_dir = FOLDER_OF_YOUR_CHOICE
src_dir = os.path.abspath(os.path.join(build_dir, 'src'))
if not os.path.exists(src_dir):
       os.makedirs(src_dir)
       ignored_files = ['__init__.py']
       included_dirs = [os.path.join(biicode_pkg_path, dir_) for dir_ in ['client', 'common']]

from Cython.Build import cythonize
def bii_cythonize(force_compile):
    '''
        Creates c files from your source python
        Params:
force_compile: boolean, if true compiles regardeless 
        of whether the file has changed or not
        Returns:
        list of c files relative to biicode_pkg_path
        '''

        c_files = []
        for dir_ in included_dirs:
        for dirname, dirnames, filenames in os.walk(dir_):
            if 'test' in dirnames:
            dirnames.remove('test')

            for filename in filenames:
    file_ = os.path.join(dirname, filename)
    stripped_name = os.path.relpath(file_, biicode_python_path)
file_name, extension = os.path.splitext(stripped_name)

    if extension == '.py':
    target_file = os.path.join(src_dir, file_name + '.c')
    if filename not in ignored_files:
    c_files.append(stripped_name.replace('.py', '.c'))
file_dir = os.path.dirname(target_file)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

        extension = cythonize(stripped_name,
                force=force_compile, 
                build_dir=src_dir)
    return c_files

from distutils import sysconfig

modules = []
for c_file in abs_path_c_files:
relfile = os.path.relpath(c_file, src_dir)
filename = os.path.splitext(relfile)[0]
extName = filename.replace(os.path.sep, ".")
extension = Extension(extName,
        sources=[c_file],
        define_macros=[('PYREX_WITHOUT_ASSERTIONS',
            None)]  # ignore asserts in code
        )
modules.append(extension)

if platform.system() != 'Windows':
cflags = sysconfig.get_config_var('CFLAGS')
opt = sysconfig.get_config_var('OPT')
sysconfig._config_vars['CFLAGS'] = cflags.replace(' -g ', ' ')
sysconfig._config_vars['OPT'] = opt.replace(' -g ', ' ')

if platform.system() == 'Linux':
ldshared = sysconfig.get_config_var('LDSHARED')
sysconfig._config_vars['LDSHARED'] = ldshared.replace(' -g ', ' ')

elif platform.system() == 'Darwin':
#-mno-fused-madd is a deprecated flag that now causes a hard error
# but distuitls still keeps it
# it was used to disable the generation of the fused multiply/add instruction
for flag, flags_line in sysconfig._config_vars.iteritems():
    if ' -g' in str(flags_line):
        sysconfig._config_vars[flag] = flags_line.replace(' -g', '')
        for key in ['CONFIG_ARGS', 'LIBTOOL', 'PY_CFLAGS', 'CFLAGS']:
        value = sysconfig.get_config_var(key)
        if value:
            sysconfig._config_vars[key] = value.replace('-mno-fused-madd', '')
            sysconfig._config_vars[key] = value.replace('-DENABLE_DTRACE',  '')
