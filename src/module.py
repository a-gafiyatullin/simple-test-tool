import os


class Module:
    """
    Information about a module and its dependencies.
    """
    def __init__(self, name, dependencies, output_files, stages):
        """
        Parameters
        ----------
        name : str
            module name
        dependencies : list
            list of dependencies of this module (pairs of dependency name and destination path)
        output_files : list
            list of output files and paths for searching them (pair of name and path)
        stages : list
            list of stages
        """
        self._name = name
        self._dependencies = dependencies.copy()
        for dependency in self._dependencies:
            if not os.path.exists(dependency.path):
                raise FileNotFoundError("Module: Directory " + dependency.path + " doesn't exist!")
        self._output_files = output_files.copy()
        for output_file in self._output_files:
            if not os.path.exists(output_file.path):
                raise FileNotFoundError("Module: Directory " + output_file.path + " doesn't exist!")
        self._stages = stages.copy()
