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
        topological sort by dependencies and outputs

    execute_stages()
        execute all stages for this module
    """

    MODULE_NAME = 0
    DEST_PATH = 1
    SOURCE_PATH = 2

    VCS_STAGE = 0
    BUILD_STAGE = 1
    TEST_STAGE = 2
    COMMIT_STAGE = 3
    NOTIFICATION_STAGE = 4
    STAGES_NUM = 5

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
        self.dependencies = dependencies.copy()
        for dependency in self.dependencies:
            if not os.path.exists(dependency[Module.DEST_PATH]):
                raise FileNotFoundError("Module: Directory " + dependency.path + " doesn't exist!")
        self.output_files = output_files.copy()
        for output_file in self.output_files:
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
                for output in out_module_iter.output_files:
                    for dependency in in_module_iter.dependencies:
                        if output[Module.MODULE_NAME] == dependency[Module.MODULE_NAME]:
                            graph[i].append(j)
                            dependency[Module.SOURCE_PATH] = output[Module.DEST_PATH]
                i = i + 1
            j = j + 1

        i = 0
        for vert_list in graph:
            graph[i] = list(dict.fromkeys(vert_list))
            i = i + 1

        used_vertices = [False] * len(modules)
        topological_sorted_vertices = []
        for i in range(len(used_vertices)):
            if not used_vertices[i]:
                Module.__dfs(graph, used_vertices, topological_sorted_vertices, i)

        ret_modules = []
        for i in topological_sorted_vertices:
            ret_modules.append(modules[i])

        return ret_modules

    def execute_stages(self):
        """
        Execute all stages for this module.
        """

        # execute stages
        error = False
        if self._stages[Module.VCS_STAGE] is not None:
            if not self._stages[Module.VCS_STAGE].pre_exec():
                error = True
            if not error:
                if not self._stages[Module.VCS_STAGE].exec():
                    error = True
            if not error:
                if not self._stages[Module.VCS_STAGE].post_exec():
                    error = True

        if not error:
            if self._stages[Module.BUILD_STAGE] is not None:
                if not self._stages[Module.BUILD_STAGE].pre_exec():
                    error = True

        # copy dependencies
        for dependency in self.dependencies:
            source = dependency[Module.SOURCE_PATH] + os.sep + dependency[Module.MODULE_NAME]
            destination = dependency[Module.DEST_PATH]
            if self._stages[Module.COMMIT_STAGE] is not None:
                if os.path.exists(source) and os.path.exists(destination + os.sep + dependency[Module.MODULE_NAME]):
                    if self._stages[Module.COMMIT_STAGE].diff(source,
                                                              destination + os.sep + dependency[Module.MODULE_NAME]):
                        result = self._stages[Module.COMMIT_STAGE].get_vcs_obj().add_for_commit(
                            dependency[Module.DEST_PATH], dependency[Module.MODULE_NAME])
                        if not result:
                            return False

            try:
                shutil.copytree(source, destination)
            except OSError as exc:
                if exc.errno == errno.ENOTDIR:
                    shutil.copy(source, destination)
                else:
                    raise

        if not error:
            if self._stages[Module.BUILD_STAGE] is not None:
                if not self._stages[Module.BUILD_STAGE].exec():
                    error = True
                if not error:
                    if not self._stages[Module.BUILD_STAGE].post_exec():
                        error = True

        if not error:
            if self._stages[Module.TEST_STAGE] is not None:
                if not self._stages[Module.TEST_STAGE].pre_exec():
                    error = True
                if not error:
                    if not self._stages[Module.TEST_STAGE].exec():
                        error = True
                if not error:
                    if not self._stages[Module.TEST_STAGE].post_exec():
                        error = True

        if not error:
            if self._stages[Module.COMMIT_STAGE] is not None:
                for output in self.output_files:
                    self._stages[Module.COMMIT_STAGE].get_vcs_obj().add_for_commit(output[Module.DEST_PATH],
                                                                                   output[Module.MODULE_NAME])
                    for dependency in self.dependencies:
                        self._stages[Module.COMMIT_STAGE].get_vcs_obj().add_for_commit(dependency[Module.SOURCE_PATH],
                                                                                       dependency[Module.MODULE_NAME])
            if self._stages[Module.COMMIT_STAGE] is not None:
                if not self._stages[Module.COMMIT_STAGE].exec():
                    error = True

        if self._stages[Module.NOTIFICATION_STAGE] is not None:
            if self._stages[Module.NOTIFICATION_STAGE] is not None:
                if not self._stages[Module.NOTIFICATION_STAGE].pre_exec():
                    error = True
                if not error:
                    if not self._stages[Module.NOTIFICATION_STAGE].exec():
                        error = True
                if not error:
                    if not self._stages[Module.NOTIFICATION_STAGE].post_exec():
                        error = True

        return not error
