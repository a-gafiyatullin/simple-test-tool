from build.cmake import Cmake
from build.make import Make
from module import Module
from notification.mail import Email
from test import Test
from vcs.git import Git
from vcs.svn import SVN
import xml.etree.ElementTree as ET
import sys


def create_vcs_stage(stage_root, module_name):
    stage_type = stage_root.get('Type')
    paths = []
    for path in stage_root.findall('Path'):
        paths.append(path.get('Path'))
    log_enable = True if stage_root.get('LogEnable') == 'True' else False
    log_name = ''
    log_path = ''

    if log_enable:
        log_name = stage_root.get('LogName')
        log_path = stage_root.get('LogPath')

    interrupt_on_fail = True if stage_root.get('InterruptOnFail') == 'True' else False

    if stage_type == 'Git':
        return Git(paths, module_name, interrupt_on_fail, log_enable, log_path, log_name)
    elif stage_type == 'SVN':
        return SVN(paths, module_name, interrupt_on_fail, log_enable, log_path, log_name)


def create_build_stage(stage_root, module_name):
    stage_type = stage_root.get('Type')
    stage_path = stage_root.get('Path')
    log_enable = True if stage_root.get('LogEnable') == 'True' else False
    log_name = ''
    log_path = ''

    if log_enable:
        log_name = stage_root.get('LogName')
        log_path = stage_root.get('LogPath')

    interrupt_on_fail = True if stage_root.get('InterruptOnFail') == 'True' else False

    if stage_type == 'CMake':
        return Cmake(stage_path, module_name, interrupt_on_fail, log_enable, log_path, log_name)
    elif stage_type == 'Make':
        return Make(stage_path, module_name, interrupt_on_fail, log_enable, log_path, log_name)


def create_notification_stage(stage_root, module_name, loggers):
    stage_type = stage_root.get('Type')

    if stage_type == 'Email':
        email_to = stage_root.get('EmailTo')
        email_from = stage_root.get('EmailFrom')
        smtp_ip = stage_root.get('SmtpServerAddress')
        smtp_port = stage_root.get('SmtpServerPort')
        password = stage_root.get('Password')

        return Email(loggers, smtp_ip, int(smtp_port), email_from, password, email_to)


def create_test_stage(stage_root, module_name):
    paths = []
    for path in stage_root.findall('Path'):
        paths.append(path.get('Path'))
    log_enable = True if stage_root.get('LogEnable') == 'True' else False
    log_name = ''
    log_path = ''

    if log_enable:
        log_name = stage_root.get('LogName')
        log_path = stage_root.get('LogPath')

    interrupt_on_fail = True if stage_root.get('InterruptOnFail') == 'True' else False

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


def create_module(module_root):
    module_name = module_root.get('Name')

    stages = []  # array of stages
    log_files = []  # array of the log files paths
    stages_root = module_root.find('Stages')
    for stage in stages_root:
        if stage.tag == 'Build':
            stages.append(create_build_stage(stage, module_name))
            print('Created Build stage for ' + module_name + '\n')
        elif stage.tag == 'VCS':
            stages.append(create_vcs_stage(stage, module_name))
            print('Created VCS stage for ' + module_name + '\n')
        elif stage.tag == 'Test':
            stages.append(create_test_stage(stage, module_name))
            print('Created Test stage for ' + module_name + '\n')
        elif stage.tag == 'Notification':
            continue
        else:
            print("Unrecognized " + stage.tag + ' stage!\n')
            continue

        log_file = stages[-1].get_log_file_path()
        if log_file is not None:
            log_files.append(log_file)

    notification_stage = stages_root.find('Notification')
    if notification_stage is not None:
        stages.append(create_notification_stage(notification_stage, module_name, log_files))
        print('Created Notification stage for ' + module_name + '\n')

    return Module(module_name, read_dependencies(module_root), read_outputs(module_root), stages)


def main():
    if len(sys.argv) < 2:
        print('usage: python3 simple-test-tool.py [path_to_config]')
        exit(-1)

    modules = []  # array of Modules

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    for module in root.iter('Module'):
        modules.append(create_module(module))


if __name__ == '__main__':
    main()
