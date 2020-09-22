from stage import Stage


class Module:
    """
    Information about a module and its dependencies.


    ...

    Methods
    -------
    add_stage(stage)
        add new stage for this module
    """
    def __init__(self, name, dependencies, output_files):
        """
        Parameters
        ----------
        name : str
            module name
        dependencies : list
            list of dependencies of this module (pairs of dependency name and destination path)
        output_files : list
            list of output files and paths for searching them (pair of name and path)
        """
        self._name = name
        self._dependencies = dependencies.copy()
        self._output_files = output_files.copy()
        self._stages = []

    def add_stage(self, stage):
        """
        Add new stage for this module.

        Parameters
        ----------
        stage : Stage
            new stage
        """
        self._stages.append(stage)
