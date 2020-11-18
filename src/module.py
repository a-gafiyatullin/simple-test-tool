import errno
import os
import shutil


class Module:
    """
    Information about a module and its dependencies.


    ...

    Methods
    -------
    topological_sort(modules)
        Topological sort by dependencies and outputs.

    execute_stages()
        Execute all stages for this module.
    """
    MODULE_NAME = 0
    DEST_PATH = 1
    SOURCE_PATH = 2

    def __init__(self, name, dependencies, output_files, stages):
        """
        Parameters
        ----------
        name : str
            module name
        dependencies : list
            list of dependencies of this module (array of dependency name, destination and source path)
        output_files : list
            list of output files and paths for searching them (pair of name and path)
        stages : list
            list of stages
        """
        self._name = name
        self._dependencies = dependencies.copy()
        for dependency in self._dependencies:
            if not os.path.exists(dependency[Module.DEST_PATH]):
                raise FileNotFoundError("Module: Directory " + dependency.path + " doesn't exist!")
        self._output_files = output_files.copy()
        for output_file in self._output_files:
            if not os.path.exists(output_file[Module.DEST_PATH]):
                raise FileNotFoundError("Module: Directory " + output_file.path + " doesn't exist!")
        self._stages = stages.copy()

    @staticmethod
    def __dfs(modules_graph, used_vertices, topological_sorted_vertices, vertex):
        """
        Parameters
        ----------
        modules_graph : list
            2D-array - adjacency lists

        used_vertices : list of bool

        topological_sorted_vertices : list of int

        vertex : int
            vertex number
        """
        used_vertices[vertex] = True
        for vertex_num in modules_graph[vertex]:
            if not used_vertices[vertex_num]:
                Module.__dfs(modules_graph, used_vertices, topological_sorted_vertices, vertex_num)
        topological_sorted_vertices.append(vertex)

    @staticmethod
    def topological_sort(modules):
        """
        Topological sort by dependencies and outputs.

        Parameters
        ----------
        modules : list
            list of Module
        """
        graph = []
        for i in range(len(modules)):
            graph.append([])
        j = 0
        for out_module_iter in modules:
            i = 0
            for in_module_iter in modules:
                for output in out_module_iter._output_files:
                    for dependency in in_module_iter._dependencies:
                        if output[Module.MODULE_NAME] == dependency[Module.MODULE_NAME]:
                            graph[i].append(j)
                            dependency[Module.SOURCE_PATH] = output[Module.DEST_PATH]
                i = i + 1
            j = j + 1

        used_vertices = [False] * len(modules)
        topological_sorted_vertices = []
        for i in range(len(used_vertices)):
            if not used_vertices[i]:
                Module.__dfs(graph, used_vertices, topological_sorted_vertices, i)
        topological_sorted_vertices.reverse()

        ret_modules = []
        for i in topological_sorted_vertices:
            ret_modules.append(modules[i])

        return ret_modules

    def execute_stages(self):
        """
        Execute all stages for this module.
        """
        # copy dependencies
        for dependency in self._dependencies:
            source = dependency[Module.SOURCE_PATH] + os.sep + dependency[Module.MODULE_NAME]
            destination = dependency[Module.DEST_PATH]
            try:
                shutil.copytree(source, destination)
            except OSError as exc:
                if exc.errno == errno.ENOTDIR:
                    shutil.copy(source, destination)
                else:
                    raise
        # execute stages
        for stage in self._stages:
            if not stage.exec():
                return False
