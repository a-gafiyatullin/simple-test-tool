import simple_test_tool
import xml.etree.ElementTree as ET
import pytest
import os
import subprocess


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
    path = ET.SubElement(tests, 'Path')
    path.set('Path', 'TEST/')

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
    tests.set('LogName', 'TEST_test.log')
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
    build.set('Path', os.getcwd() + os.sep + 'tests' + os.sep + 'Cmake-build-test')
    build.set('LogEnable', 'Off')
    build.set('InterruptOnFail', 'On')

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

    test_path = ET.SubElement(test, 'Path')
    test_path.set('Path', root_dir + 'test.sh')

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

    build_obj.exec()
    assert os.path.exists(
        os.getcwd() + os.sep + 'tests' + os.sep + 'Cmake-build-test/build/CMake-build-test-exec') is True


def test_make_build_stage():
    root = create_xml_input_file_make()
    module = root.find('Module')

    name = module.get('Name')
    assert name == 'TEST'

    stages = module.find('Stages')
    build = stages.find('Build')

    build_obj = simple_test_tool.create_build_stage(build, name)
    assert build_obj is not None

    build_obj.exec()
    assert os.path.exists(os.getcwd() + os.sep + 'tests' + os.sep + 'Cmake-build-test/make-build-test-exec') is True


def test_git_vcs_and_test_stage():
    root = create_xml_input_file_git_and_test()
    module = root.find('Module')

    name = module.get('Name')
    assert name == 'TEST'

    stages = module.find('Stages')
    vcs = stages.find('VCS')

    vcs_obj = simple_test_tool.create_vcs_stage(vcs, name)
    assert vcs_obj is not None

    vcs_obj.exec()
    assert os.path.exists(os.getcwd() + os.sep + 'tests' + os.sep + 'VCS-test/simple-test-tool') is True

    test = stages.find('Test')

    test_obj = simple_test_tool.create_test_stage(test, name)
    assert test_obj is not None

    test_obj.exec()
