from datetime import date
import simple_test_tool
import xml.etree.ElementTree as ET
import pytest
import os
import subprocess
from module import Module


def create_xml_input_file_outputs():
    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create outputs
    test_outputs = ET.SubElement(test_module, 'Outputs')
    test_output = ET.SubElement(test_outputs, 'Output')
    test_output.set('Name', 'Output1')
    test_output.set('Path', 'OutputDir1')
    test_output = ET.SubElement(test_outputs, 'Output')
    test_output.set('Name', 'Output2')
    test_output.set('Path', 'OutputDir2')

    return root


def create_xml_input_file_dependencies():
    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create dependencies
    test_dependencies = ET.SubElement(test_module, 'Dependencies')
    test_dependency = ET.SubElement(test_dependencies, 'Dependency')
    test_dependency.set('Name', 'Dependency1')
    test_dependency.set('Path', 'DependencyDir1')
    test_dependency = ET.SubElement(test_dependencies, 'Dependency')
    test_dependency.set('Name', 'Dependency2')
    test_dependency.set('Path', 'DependencyDir2')

    return root


def create_xml_input_file_tests():
    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create Stages
    stages = ET.SubElement(test_module, 'Stages')
    # create Test stage
    tests = ET.SubElement(stages, 'Test')
    tests.set('LogEnable', 'Off')
    tests.set('InterruptOnFail', 'On')

    return root


def create_xml_input_file_telegram():
    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create Stages
    stages = ET.SubElement(test_module, 'Stages')
    # create Test stage
    notification = ET.SubElement(stages, 'Notification')
    notification.set('Type', 'Telegram')
    notification.set('Token', '12345678')
    notification.set('ChatID', '12345678')

    return root


def create_xml_input_file_tests_fail():
    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create Stages
    stages = ET.SubElement(test_module, 'Stages')
    # create Test stage
    tests = ET.SubElement(stages, 'Test')
    tests.set('LogEnable', 'Off')
    tests.set('InterruptOnFail', 'On')
    # create Path
    path = ET.SubElement(tests, 'MainScript')
    path.set('Path', 'TEST' + os.sep)

    return root


def create_xml_input_file_log_fail():
    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create Stages
    stages = ET.SubElement(test_module, 'Stages')
    # create Test stage
    tests = ET.SubElement(stages, 'Test')
    tests.set('LogEnable', 'On')
    tests.set('LogPath', 'TEST_path')
    tests.set('InterruptOnFail', 'On')

    return root


def create_xml_input_file_cmake():
    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create Stages
    stages = ET.SubElement(test_module, 'Stages')
    # create Build stage
    build = ET.SubElement(stages, 'Build')
    build.set('Type', 'CMake')
    build.set('Path', os.getcwd() + os.sep + 'tests' + os.sep + 'Cmake-build-test')
    build.set('LogEnable', 'Off')
    build.set('InterruptOnFail', 'On')

    target = ET.SubElement(build, 'Target')
    target.set('Name', 'all')

    return root


def create_xml_input_file_make():
    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create Stages
    stages = ET.SubElement(test_module, 'Stages')
    # create Build stage
    build = ET.SubElement(stages, 'Build')
    build.set('Type', 'Make')
    build.set('Path', os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test')
    build.set('LogEnable', 'Off')
    build.set('InterruptOnFail', 'On')

    target = ET.SubElement(build, 'Target')
    target.set('Name', 'all')

    return root


def create_xml_input_file_custom_build():
    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create Stages
    stages = ET.SubElement(test_module, 'Stages')
    # create Build stage
    build = ET.SubElement(stages, 'Build')
    build.set('Type', 'Custom')
    build.set('Path', os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test')
    build.set('LogEnable', 'Off')
    build.set('InterruptOnFail', 'On')

    main_script = ET.SubElement(build, 'MainScript')
    main_script.set('Path', 'tests' + os.sep + 'Make-build-test' + os.sep + 'main_build_script.sh')
    pre_script = ET.SubElement(build, 'PreScript')
    pre_script.set('Path', 'tests' + os.sep + 'Make-build-test' + os.sep + 'pre_build_script.sh')
    post_script = ET.SubElement(build, 'PostScript')
    post_script.set('Path', 'tests' + os.sep + 'Make-build-test' + os.sep + 'post_build_script.sh')

    return root


def create_xml_input_file_git_and_test():
    # clone repository
    root_dir = os.getcwd() + os.sep + 'tests' + os.sep + 'VCS-test' + os.sep
    curr_dir = os.getcwd()
    os.chdir(root_dir)
    subprocess.run(root_dir + 'prepare.sh', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir(curr_dir)

    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create Stages
    stages = ET.SubElement(test_module, 'Stages')
    # create VCS stage
    vcs = ET.SubElement(stages, 'VCS')
    vcs.set('Type', 'Git')
    vcs.set('LogEnable', 'Off')
    vcs.set('InterruptOnFail', 'On')

    vcs_path = ET.SubElement(vcs, 'Path')
    vcs_path.set('Path', root_dir + 'simple-test-tool')

    # create Test stage
    test = ET.SubElement(stages, 'Test')
    test.set('LogEnable', 'Off')
    test.set('InterruptOnFail', 'On')

    test_path = ET.SubElement(test, 'MainScript')
    test_path.set('Path', root_dir + 'test.sh')

    return root


def create_xml_input_file_modules():
    # create root
    root = ET.Element('STT')

    # create Cmake Module
    cmake_module = ET.SubElement(root, 'Module')
    cmake_module.set('Name', 'Cmake-build-test')

    # create Stages
    cmake_stages = ET.SubElement(cmake_module, 'Stages')
    # create Build stage
    cmake_build = ET.SubElement(cmake_stages, 'Build')
    cmake_build.set('Type', 'CMake')
    cmake_build.set('Path', os.getcwd() + os.sep + 'tests' + os.sep + 'Cmake-build-test')
    cmake_build.set('LogEnable', 'Off')
    cmake_build.set('InterruptOnFail', 'On')

    cmake_target = ET.SubElement(cmake_build, 'Target')
    cmake_target.set('Name', 'all')

    # create Outputs
    cmake_outputs = ET.SubElement(cmake_module, 'Outputs')
    cmake_output = ET.SubElement(cmake_outputs, 'Output')
    cmake_output.set('Name', 'CMake-build-test-exec')
    cmake_output.set('Path', os.getcwd() + os.sep + 'tests' + os.sep + 'Cmake-build-test' + os.sep + 'build')

    # create Make Module
    make_module = ET.SubElement(root, 'Module')
    make_module.set('Name', 'Make-build-test')

    # create Stages
    make_stages = ET.SubElement(make_module, 'Stages')
    # create Build stage
    make_build = ET.SubElement(make_stages, 'Build')
    make_build.set('Type', 'Make')
    make_build.set('Path', os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test')
    make_build.set('LogEnable', 'Off')
    make_build.set('InterruptOnFail', 'On')

    make_target = ET.SubElement(make_build, 'Target')
    make_target.set('Name', 'all')

    # create Dependencies
    make_dependencies = ET.SubElement(make_module, 'Dependencies')
    make_dependency = ET.SubElement(make_dependencies, 'Dependency')
    make_dependency.set('Name', 'CMake-build-test-exec')
    make_dependency.set('Path', os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test')

    return root


def create_xml_input_file_log_exception():
    make_dir = os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test'

    # create root
    root = ET.Element('STT')

    # create Module
    test_module = ET.SubElement(root, 'Module')
    test_module.set('Name', 'TEST')

    # create Stages
    stages = ET.SubElement(test_module, 'Stages')
    # create Build stage
    build = ET.SubElement(stages, 'Build')
    build.set('Type', 'Make')
    build.set('Path', make_dir)
    build.set('LogEnable', 'On')
    build.set('LogPath', make_dir)
    build.set('InterruptOnFail', 'On')

    target = ET.SubElement(build, 'Target')
    target.set('Name', 'all')

    return root


def test_parse_outputs():
    root = create_xml_input_file_outputs()
    module = root.find('Module')

    assert module.get('Name') == 'TEST'

    outputs = module.find('Outputs')
    outputs_list = simple_test_tool.read_outputs(outputs)

    expected = [('Output1', 'OutputDir1'), ('Output2', 'OutputDir2')]
    assert len(outputs_list) == len(expected)
    assert all([a == b] for a, b in zip(outputs_list, expected))


def test_parse_dependencies():
    root = create_xml_input_file_dependencies()
    module = root.find('Module')

    assert module.get('Name') == 'TEST'

    dependencies = module.find('Dependencies')
    dependencies_list = simple_test_tool.read_dependencies(dependencies)

    expected = [('Dependency1', 'DependencyDir1'), ('Dependency2', 'DependencyDir2')]
    assert len(dependencies_list) == len(expected)
    assert all([a == b] for a, b in zip(dependencies_list, expected))


def test_create_tests_stage():
    root = create_xml_input_file_tests()
    module = root.find('Module')

    name = module.get('Name')
    assert name == 'TEST'

    stages = module.find('Stages')
    tests = stages.find('Test')

    test_obj = simple_test_tool.create_test_stage(tests, name)
    assert test_obj is not None


def test_create_tests_stage_fail():
    with pytest.raises(FileNotFoundError):
        root = create_xml_input_file_tests_fail()
        module = root.find('Module')

        name = module.get('Name')
        assert name == 'TEST'

        stages = module.find('Stages')
        tests = stages.find('Test')

        simple_test_tool.create_test_stage(tests, name)


def test_create_tests_log_fail():
    with pytest.raises(FileNotFoundError):
        root = create_xml_input_file_log_fail()
        module = root.find('Module')

        name = module.get('Name')
        assert name == 'TEST'

        stages = module.find('Stages')
        tests = stages.find('Test')

        simple_test_tool.create_test_stage(tests, name)


def test_cmake_build_stage():
    root = create_xml_input_file_cmake()
    module = root.find('Module')

    name = module.get('Name')
    assert name == 'TEST'

    stages = module.find('Stages')
    build = stages.find('Build')

    build_obj = simple_test_tool.create_build_stage(build, name)
    assert build_obj is not None

    build_obj.pre_exec()
    build_obj.exec()
    build_obj.post_exec()
    
    assert os.path.exists(
        os.getcwd() + os.sep + 'tests' + os.sep + 'Cmake-build-test' + os.sep + 'build' + os.sep
        + 'CMake-build-test-exec') is True


def test_make_build_stage():
    root = create_xml_input_file_make()
    module = root.find('Module')

    name = module.get('Name')
    assert name == 'TEST'

    stages = module.find('Stages')
    build = stages.find('Build')

    build_obj = simple_test_tool.create_build_stage(build, name)
    assert build_obj is not None

    build_obj.pre_exec()
    build_obj.exec()
    build_obj.post_exec()
    
    assert os.path.exists(os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test' + os.sep
                          + 'make-build-test-exec') is True


def test_custom_build_stage():
    root = create_xml_input_file_custom_build()
    module = root.find('Module')

    name = module.get('Name')
    assert name == 'TEST'

    stages = module.find('Stages')
    build = stages.find('Build')

    build_obj = simple_test_tool.create_build_stage(build, name)
    assert build_obj is not None

    build_obj.pre_exec()
    build_obj.exec()
    build_obj.post_exec()

    assert os.path.exists(os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test' + os.sep
                          + 'make-build-test-exec') is True


def test_git_vcs_and_test_stage():
    root = create_xml_input_file_git_and_test()
    module = root.find('Module')

    name = module.get('Name')
    assert name == 'TEST'

    stages = module.find('Stages')
    vcs = stages.find('VCS')

    vcs_obj = simple_test_tool.create_vcs_stage(vcs, name)
    assert vcs_obj is not None

    vcs_obj.pre_exec()
    vcs_obj.exec()
    vcs_obj.post_exec()
    
    assert os.path.exists(os.getcwd() + os.sep + 'tests' + os.sep + 'VCS-test' + os.sep + 'simple-test-tool') is True

    test = stages.find('Test')

    test_obj = simple_test_tool.create_test_stage(test, name)
    assert test_obj is not None

    test_obj.pre_exec()
    test_obj.exec()
    test_obj.post_exec()


def test_create_module():
    root = create_xml_input_file_modules()

    modules = []  # array of Module

    for module in root.iter('Module'):
        modules.append(simple_test_tool.create_module(module))
        assert modules[-1] is not None

    topological_sorted_modules = Module.topological_sort(modules)
    assert topological_sorted_modules is not None

    topological_sorted_modules[0].execute_stages()
    topological_sorted_modules[1].execute_stages()
    assert os.path.exists(
        os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test' + os.sep + 'CMake-build-test-exec') is True

    topological_sorted_modules[1].execute_stages()
    assert os.path.exists(os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test' + os.sep +
                          'make-build-test-exec') is True


def test_input_test_xml():
    base_dir = os.getcwd() + os.sep + 'tests' + os.sep + 'Make-build-test' + os.sep
    simple_test_tool.main('tests' + os.sep + 'input_test.xml')

    assert os.path.exists(base_dir + 'make-build-test-exec') is True
    assert os.path.exists(base_dir + str(date.today()) + '-Make-build-test.Make.txt') is True


def test_commit():
    # clone repository
    root_dir = os.getcwd() + os.sep + 'tests' + os.sep + 'VCS-test' + os.sep
    curr_dir = os.getcwd()
    os.chdir(root_dir)
    subprocess.run(root_dir + 'prepare.sh', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    open(root_dir + 'simple-test-tool' + os.sep + 'test_file_for_commit.txt', 'w').close()

    simple_test_tool.main('input_commit_test.xml')

    os.chdir(curr_dir)

    assert os.path.exists(root_dir + 'simple-test-tool' + os.sep + str(date.today())
                          + '-simple-test-tool.Commit.txt') is True
    assert os.path.exists(root_dir + 'simple-test-tool' + os.sep + str(date.today())
                          + '-simple-test-tool.Git-Commit.txt') is True


def test_telegram_stage():
    root = create_xml_input_file_telegram()
    module = root.find('Module')

    name = module.get('Name')
    assert name == 'TEST'

    stages = module.find('Stages')
    build = stages.find('Notification')

    notification_obj = simple_test_tool.create_notification_stage(build, name)
    assert notification_obj is not None
