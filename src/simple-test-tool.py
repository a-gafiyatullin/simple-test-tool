from build.cmake import Cmake
from build.make import Make
from test import Test
from vcs.git import Git
from vcs.svn import SVN


def create_build_stage(stage_root, module_name):
    stage = stage_root.find('Build')

    stage_type = stage.get('Type')
    paths = []
    for path in stage.findall('Path'):
        paths.append(path.get('Path'))
    log_enable = True if stage.get('LogEnable') == 'True' else False
    log_name = ''
    log_path = ''

    if log_enable:
        log_name = stage.get('LogName')
        log_path = stage.get('LogPath')

    interrupt_on_fail = True if stage.get('InterruptOnFail') == 'True' else False

    if stage_type == 'Git':
        return Git(paths, module_name, interrupt_on_fail, log_enable, log_path, log_name)
    elif stage_type == 'SVN':
        return SVN(paths, module_name, interrupt_on_fail, log_enable, log_path, log_name)


def create_vcs_stage(stage_root, module_name):
    stage = stage_root.find('VCS')

    stage_type = stage.get('Type')
    stage_path = stage.get('Path')
    log_enable = True if stage.get('LogEnable') == 'True' else False
    log_name = ''
    log_path = ''

    if log_enable:
        log_name = stage.get('LogName')
        log_path = stage.get('LogPath')

    interrupt_on_fail = True if stage.get('InterruptOnFail') == 'True' else False

    if stage_type == 'Cmake':
        return Cmake(stage_path, module_name, interrupt_on_fail, log_enable, log_path, log_name)
    elif stage_type == 'Make':
        return Make(stage_path, module_name, interrupt_on_fail, log_enable, log_path, log_name)


def create_test_stage(stage_root, module_name):
    stage = stage_root.find('Test')

    paths = []
    for path in stage.findall('Path'):
        paths.append(path.get('Path'))
    log_enable = True if stage.get('LogEnable') == 'True' else False
    log_name = ''
    log_path = ''

    if log_enable:
        log_name = stage.get('LogName')
        log_path = stage.get('LogPath')

    interrupt_on_fail = True if stage.get('InterruptOnFail') == 'True' else False

    return Test(paths, module_name, interrupt_on_fail, log_enable, log_path, log_name)


def read_outputs(module_root):
    outputs = module_root.find('Outputs')

    outputs_list = []
    for output in outputs.findall('Output'):
        outputs_list.append((output.get('Name'), output.get('Path')))

    return outputs_list


def read_dependencies(module_root):
    dependencies = module_root.find('Dependencies')

    dependencies_list = []
    for dependency in dependencies.findall('Dependency'):
        dependencies_list.append((dependency.get('Name'), dependency.get('Path')))

    return dependencies_list
