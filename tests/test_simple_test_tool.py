import simple_test_tool
import xml.etree.ElementTree as ET


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
