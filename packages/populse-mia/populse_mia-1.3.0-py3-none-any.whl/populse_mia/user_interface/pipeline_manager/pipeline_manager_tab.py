# -*- coding: utf-8 -*- #
"""
Module to define pipeline manager tab appearance, settings and methods.

Contains:
    Class:
        - PipelineManagerTab
        - RunProgress
        - RunWorker

"""

##########################################################################
# Populse_mia - Copyright (C) IRMaGe/CEA, 2018
# Distributed under the terms of the CeCILL license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html
# for details.
##########################################################################

# Populse_MIA imports
from populse_mia.user_interface.pipeline_manager.process_mia import ProcessMIA
from populse_mia.user_interface.pop_ups import (PopUpSelectIteration,
                                                PopUpInheritanceDict)
from populse_mia.user_interface.pipeline_manager.iteration_table import (
                                                                 IterationTable)
from populse_mia.data_manager.project import (COLLECTION_CURRENT,
                                              COLLECTION_INITIAL,
                                              COLLECTION_BRICK, BRICK_NAME,
                                              BRICK_OUTPUTS, BRICK_INPUTS,
                                              TAG_BRICKS, BRICK_INIT,
                                              BRICK_INIT_TIME, TAG_TYPE,
                                              TAG_EXP_TYPE, TAG_FILENAME,
                                              TAG_CHECKSUM, TYPE_NII, TYPE_MAT,
                                              TYPE_TXT, TYPE_UNKNOWN)
from populse_mia.user_interface.pipeline_manager.node_controller import (
                                                                 NodeController)
from populse_mia.user_interface.pipeline_manager.pipeline_editor import (
                                                             PipelineEditorTabs)
from populse_mia.user_interface.pipeline_manager.process_library import (
                                                           ProcessLibraryWidget)
from populse_mia.software_properties import Config

# Capsul imports
from capsul.api import (get_process_instance, NipypeProcess, Pipeline,
                        PipelineNode, StudyConfig, Switch)
from capsul.qt_gui.widgets.pipeline_developper_view import (
                                                         PipelineDevelopperView)

# PyQt5 imports
from PyQt5.QtCore import Signal, Qt, QThread
from PyQt5.QtWidgets import (QMenu, QVBoxLayout, QWidget, QSplitter,
                             QApplication, QToolBar, QAction, QHBoxLayout,
                             QScrollArea, QMessageBox, QProgressDialog,
                             QPushButton)

# Other import
import datetime
import inspect
import os
import re
import sys
import uuid
from collections import OrderedDict
from matplotlib.backends.qt_compat import QtWidgets
from traits.trait_errors import TraitError
from traits.api import TraitListObject, Undefined


if sys.version_info[0] >= 3:
    unicode = str

    def values(d):
        return list(d.values())
else:
    def values(d):
        return d.values()


class PipelineManagerTab(QWidget):
    """
    Widget that handles the Pipeline Manager tab.

    .. Methods:
        - add_plug_value_to_database: add the plug value to the database.
        - add_process_to_preview: add a process to the pipeline
        - controller_value_changed: update history when a pipeline node is
          changed
        - displayNodeParameters: display the node controller when a node is
          clicked
        - init_pipeline: initialize the current pipeline of the pipeline
          editor
        - initialize: clean previous initialization then initialize the current
          pipeline
        - layout_view : initialize layout for the pipeline manager
        - loadParameters: load pipeline parameters to the current pipeline of
          the pipeline editor
        - loadPipeline: load a pipeline to the pipeline editor
        - redo: redo the last undone action on the current pipeline editor
        - runPipeline: run the current pipeline of the pipeline editor
        - saveParameters: save the pipeline parameters of the the current
          pipeline of the pipeline editor
        - savePipeline: save the current pipeline of the pipeline editor
        - savePipelineAs: save the current pipeline of the pipeline editor
          under another name
        - undo: undo the last action made on the current pipeline editor
        - updateProcessLibrary: update the library of processes when a
          pipeline is saved
        - update_clinical_mode: update the visibility of widgets/actions
          depending of the chosen mode
        - update_project: update the project attribute of several objects
        - update_scans_list: update the user-selected list of scans
    """

    item_library_clicked = Signal(str)

    def __init__(self, project, scan_list, main_window):
        """
        Initialization of the Pipeline Manager tab

        :param project: current project in the software
        :param scan_list: list of the selected database files
        :param main_window: main window of the software
        """

        config = Config()

        # Necessary for using MIA bricks
        ProcessMIA.project = project
        self.project = project
        self.inheritance_dict = None
        self.init_clicked = False
        if len(scan_list) < 1:
            self.scan_list = self.project.session.get_documents_names(
                COLLECTION_CURRENT)
        else:
            self.scan_list = scan_list
        self.main_window = main_window
        self.enable_progress_bar = False

        # This list is the list of scans contained in the iteration table
        # If it is empty, the scan list in the Pipeline Manager is the scan
        # list from the data_browser
        self.iteration_table_scans_list = []
        self.brick_list = []

        # Used for the inheritance dictionary
        self.key = {}
        self.ignore = {}
        self.ignore_node = False

        QWidget.__init__(self)

        self.verticalLayout = QVBoxLayout(self)
        self.processLibrary = ProcessLibraryWidget(self.main_window)
        self.processLibrary.process_library.item_library_clicked.connect(
            self.item_library_clicked)
        self.item_library_clicked.connect(self._show_preview)

        # self.diagramScene = DiagramScene(self)
        self.pipelineEditorTabs = PipelineEditorTabs(
            self.project, self.scan_list, self.main_window)
        self.pipelineEditorTabs.node_clicked.connect(
            self.displayNodeParameters)
        self.pipelineEditorTabs.switch_clicked.connect(
            self.displayNodeParameters)
        self.pipelineEditorTabs.pipeline_saved.connect(
            self.updateProcessLibrary)
        self.nodeController = NodeController(
            self.project, self.scan_list, self, self.main_window)
        self.nodeController.visibles_tags = \
            self.project.session.get_shown_tags()

        self.iterationTable = IterationTable(
            self.project, self.scan_list, self.main_window)
        self.iterationTable.iteration_table_updated.connect(
            self.update_scans_list)

        self.previewBlock = PipelineDevelopperView(
            pipeline=None, allow_open_controller=False,
            show_sub_pipelines=True, enable_edition=False)

        self.startedConnection = None

        # Actions
        self.load_pipeline_action = QAction("Load pipeline", self)
        self.load_pipeline_action.triggered.connect(self.loadPipeline)

        self.save_pipeline_action = QAction("Save pipeline", self)
        self.save_pipeline_action.triggered.connect(self.savePipeline)

        self.save_pipeline_as_action = QAction("Save pipeline as", self)
        self.save_pipeline_as_action.triggered.connect(self.savePipelineAs)

        self.load_pipeline_parameters_action = QAction(
            "Load pipeline parameters", self)
        self.load_pipeline_parameters_action.triggered.connect(
            self.loadParameters)

        self.save_pipeline_parameters_action = QAction(
            "Save pipeline parameters", self)
        self.save_pipeline_parameters_action.triggered.connect(
            self.saveParameters)

        self.init_pipeline_action = QAction("Initialize pipeline", self)
        self.init_pipeline_action.triggered.connect(self.initialize)

        self.run_pipeline_action = QAction("Run pipeline", self)
        self.run_pipeline_action.triggered.connect(self.runPipeline)

        # if config.get_clinical_mode() == True:
        #     self.save_pipeline_action.setDisabled(True)
        #     self.save_pipeline_as_action.setDisabled(True)
        #     self.processLibrary.setHidden(True)
        #     self.previewBlock.setHidden(True)

        # Initialize toolbar
        self.menu_toolbar = QToolBar()
        self.tags_menu = QMenu()
        self.tags_tool_button = QtWidgets.QToolButton()
        self.scrollArea = QScrollArea()

        # Initialize Qt layout
        self.hLayout = QHBoxLayout()
        self.splitterRight = QSplitter(Qt.Vertical)
        self.splitter0 = QSplitter(Qt.Vertical)
        self.splitter1 = QSplitter(Qt.Horizontal)

        self.layout_view()

        # To undo/redo
        self.nodeController.value_changed.connect(
            self.controller_value_changed)

    def _show_preview(self, name_item):
        self.previewBlock.centerOn(0, 0)
        self.find_process(name_item)

    def add_plug_value_to_database(self, p_value, brick, node_name,
                                   plug_name, full_name):
        """Add the plug value to the database.

        :param p_value: plug value, a file name or a list of file names
        :param brick: brick id
        :param node_name: name of the node
        :param plug_name: name of the plug
        """
        if type(p_value) in [list, TraitListObject]:
            for elt in p_value:
                self.add_plug_value_to_database(elt, brick, node_name, 
                                                plug_name, full_name)
            return

        # This means that the value is not a filename
        if p_value in ["<undefined>", Undefined] or not os.path.isdir(
                os.path.split(p_value)[0]):
            return
        try:
            open(p_value, 'a').close()
        except IOError:
            raise IOError('Could not open {0} file.'.format(p_value))
        else:
            # Deleting the project's folder in the file name so it can
            # fit to the database's syntax
            old_value = p_value
            p_value = p_value.replace(self.project.folder, "")
            p_value = p_value.replace(os.path.abspath(self.project.folder), "")
            if p_value[0] in ["\\", "/"]:
                p_value = p_value[1:]

            # If the file name is already in the database,
            # no exception is raised
            # but the user is warned
            if self.project.session.get_document(COLLECTION_CURRENT, p_value):
                print("Path {0} already in database.".format(p_value))
            else:
                self.project.session.add_document(COLLECTION_CURRENT, p_value)
                self.project.session.add_document(COLLECTION_INITIAL, p_value)

            # Adding the new brick to the output files
            bricks = self.project.session.get_value(
                COLLECTION_CURRENT, p_value, TAG_BRICKS)
            if bricks is None:
                bricks = []
            bricks.append(self.brick_id)
            self.project.session.set_value(
                COLLECTION_CURRENT, p_value, TAG_BRICKS, bricks)
            self.project.session.set_value(
                COLLECTION_INITIAL, p_value, TAG_BRICKS, bricks)
            # Type tag
            filename, file_extension = os.path.splitext(p_value)
            if file_extension == ".nii":
                self.project.session.set_value(
                    COLLECTION_CURRENT, p_value, TAG_TYPE, TYPE_NII)
                self.project.session.set_value(
                    COLLECTION_INITIAL, p_value, TAG_TYPE, TYPE_NII)
            elif file_extension == ".mat":
                self.project.session.set_value(
                    COLLECTION_CURRENT, p_value, TAG_TYPE, TYPE_MAT)
                self.project.session.set_value(
                    COLLECTION_INITIAL, p_value, TAG_TYPE, TYPE_MAT)
            elif file_extension == ".txt":
                self.project.session.set_value(
                    COLLECTION_CURRENT, p_value, TAG_TYPE, TYPE_TXT)
                self.project.session.set_value(
                    COLLECTION_INITIAL, p_value, TAG_TYPE, TYPE_TXT)
            else:
                self.project.session.set_value(
                    COLLECTION_CURRENT, p_value, TAG_TYPE, TYPE_UNKNOWN)
                self.project.session.set_value(
                    COLLECTION_INITIAL, p_value, TAG_TYPE, TYPE_UNKNOWN)

            inputs = self.inputs
            # iterate = self.iterationTable.check_box_iterate.isChecked()
            # Automatically fill inheritance dictionary if empty
            if self.ignore_node:
                pass
            elif ((self.inheritance_dict is None or old_value not in
                    self.inheritance_dict) and
                  (node_name not in self.ignore) and
                  (node_name + plug_name not in self.ignore)):
                values = {}
                for key in inputs:
                    paths = []
                    if isinstance(inputs[key], list):
                        for val in inputs[key]:
                            if isinstance(val, str):
                                paths.append(val)
                    elif isinstance(inputs[key], str):
                        paths.append(inputs[key])
                    for path in paths:
                        if os.path.exists(path):
                            name, extension = os.path.splitext(path)
                            if extension == ".nii":
                                values[key] = name + extension
                if len(values) >= 1:
                    self.inheritance_dict = {}
                    if len(values) == 1:
                        value = values[list(values.keys(
                        ))[0]]
                        self.inheritance_dict[old_value] = value
                    else:
                        if node_name in self.key:
                            value = values[self.key[node_name]]
                            self.inheritance_dict[old_value] = value
                        elif node_name + plug_name in self.key:
                            value = values[self.key[node_name + plug_name]]
                            self.inheritance_dict[old_value] = value
                        else:
                            pop_up = PopUpInheritanceDict(
                             values, full_name, plug_name,
                             self.iterationTable.check_box_iterate.isChecked())
                            pop_up.exec()
                            self.ignore_node = pop_up.everything
                            if pop_up.ignore:
                                self.inheritance_dict = None
                                if pop_up.all is True:
                                    self.ignore[node_name] = True
                                else:
                                    self.ignore[node_name+plug_name] = True
                            else:
                                value = pop_up.value
                                if pop_up.all is True:
                                    self.key[node_name] = pop_up.key
                                else:
                                    self.key[node_name+plug_name] = pop_up.key
                                self.inheritance_dict[old_value] = value

            # Adding inherited tags
            if self.inheritance_dict:                
                database_parent_file = None
                parent_file = self.inheritance_dict[old_value]
                for scan in self.project.session.get_documents_names(
                        COLLECTION_CURRENT):
                    if scan in str(parent_file):
                        database_parent_file = scan
                banished_tags = [TAG_TYPE, TAG_EXP_TYPE, TAG_BRICKS,
                                 TAG_CHECKSUM, TAG_FILENAME]
                for tag in self.project.session.get_fields_names(
                        COLLECTION_CURRENT):
                    if tag not in banished_tags and database_parent_file is \
                            not None:
                        parent_current_value = self.project.session.get_value(
                            COLLECTION_CURRENT, database_parent_file, tag)
                        self.project.session.set_value(
                            COLLECTION_CURRENT, p_value, tag,
                            parent_current_value)
                        parent_initial_value = self.project.session.get_value(
                            COLLECTION_INITIAL, database_parent_file, tag)
                        self.project.session.set_value(
                            COLLECTION_INITIAL, p_value, tag,
                            parent_initial_value)

            self.project.saveModifications()

    def add_process_to_preview(self, class_process, node_name=None):
        """Add a process to the pipeline.

        :param class_process: process class's name (str)
        :param node_name: name of the corresponding node
           (using when undo/redo) (str)
        """
        # pipeline = self.previewBlock.scene.pipeline
        pipeline = Pipeline()
        if not node_name:
            class_name = class_process.__name__
            i = 1

            node_name = class_name.lower() + str(i)

            while node_name in pipeline.nodes and i < 100:
                i += 1
                node_name = class_name.lower() + str(i)

            process_to_use = class_process()

        else:
            process_to_use = class_process

        try:
            process = get_process_instance(
                process_to_use)
        except Exception as e:
            return

        pipeline.add_process(node_name, process)
        self.previewBlock.set_pipeline(pipeline)

        # Capsul update
        node = pipeline.nodes[node_name]
        # gnode = self.scene.add_node(node_name, node)

        return node, node_name

    def controller_value_changed(self, signal_list):
        """
        Update history when a pipeline node is changed

        :param signal_list: list of the needed parameters to update history
        """
        case = signal_list.pop(0)

        # For history
        history_maker = []

        if case == "node_name":
            history_maker.append("update_node_name")
            for element in signal_list:
                history_maker.append(element)

        elif case == "plug_value":
            history_maker.append("update_plug_value")
            for element in signal_list:
                history_maker.append(element)

        self.pipelineEditorTabs.undos[
            self.pipelineEditorTabs.get_current_editor()].append(history_maker)
        self.pipelineEditorTabs.redos[
            self.pipelineEditorTabs.get_current_editor()].clear()

        if case == "plug_value":
            node_name = signal_list[0]
            if node_name in ['inputs', 'outputs']:
                node_name = ''

        if case == "node_name":
            node_name = signal_list[1]

        self.nodeController.update_parameters(
            self.pipelineEditorTabs.get_current_pipeline().nodes[
                node_name].process)

    def displayNodeParameters(self, node_name, process):
        """
        Display the node controller when a node is clicked

        :param node_name: name of the node to display parameters
        :param process: process instance of the corresponding node
        :return:
        """
        if isinstance(process, Switch):
            pass
        else:
            self.nodeController.display_parameters(
                node_name, process,
                self.pipelineEditorTabs.get_current_pipeline())
            self.scrollArea.setWidget(self.nodeController)

    def find_process(self, path):
        """
        Find the dropped process in the system's paths

        :param path: class's path (e.g. "nipype.interfaces.spm.Smooth") (str)
        """
        package_name, process_name = os.path.splitext(path)
        process_name = process_name[1:]
        __import__(package_name)
        pkg = sys.modules[package_name]
        for name, instance in sorted(list(pkg.__dict__.items())):
            if name == process_name and inspect.isclass(instance):
                try:
                    process = get_process_instance(instance)
                except Exception as e:
                    print(e)
                    return
                else:
                    node, node_name = self.add_process_to_preview(instance)
                    gnode = self.previewBlock.scene.gnodes[node_name]
                    gnode.setPos(0, 0)
                    gnode.updateInfoActived(True)
                    # gnode.active = True
                    # gnode.update_node()
                    rect = gnode.sceneBoundingRect()
                    self.previewBlock.scene.setSceneRect(rect)
                    self.previewBlock.fitInView(
                        rect.x(), rect.y(), rect.width() * 1.2,
                                            rect.height() * 1.2,
                        Qt.KeepAspectRatio)
                    self.previewBlock.setAlignment(Qt.AlignCenter)

    def init_pipeline(self, pipeline=None, pipeline_name=""):
        """
        Initialize the current pipeline of the pipeline editor

        :param pipeline: not None if this method call a sub-pipeline
        :param pipeline_name: name of the parent pipeline
        """
        # Should we add a progress bar for the initialization?
        # self.enable_progress_bar = True
        # if self.enable_progress_bar:
        #     self.progress = InitProgress(
        #         self.project, self.pipelineEditorTabs, pipeline)
        #     self.progress.show()
        #     self.progress.exec()
        #
        # else:
        
        name = os.path.basename(
            self.pipelineEditorTabs.get_current_filename())
        self.main_window.statusBar().showMessage(
            'Pipeline "{0}" is getting initialized. '
            'Please wait.'.format(name))
        QApplication.processEvents()

        config = Config()
        
        # nodes_requir_issue is a dictionary whose keys are the names of the
        # nodes and whose values are the compatibility of the requirements of
        # this node with the current configuration of MIA.
        # - If no requirement defined in the process:
        #   nodes_requir_issue[node_name] == 'MISSING'
        # - If requirement does not match the current MIA configuration:
        #   nodes_requir_issue[node_name] = [NameOfTheThirdPartiesWithProblem]
        # - If requirement matches the current MIA configuration:
        #   nodes_requir_issue have no key corresponding to node_name
        nodes_requir_issue ={}

        # nodes_requir_miss == [] if all processes have a defined requirement
        # object or is a list of node names that do not have a defined
        # requirement 
        nodes_requir_miss = None
        
        # nodes_requir_fail == [] if all processes have requirements
        # corresponding to the current mia configuration or nodes_requir_fail
        # is a list of node names that requirements do not match the current
        # mia's configuration
        nodes_requir_fail = None
        
        # nodes_to_check contains the node names that need to be update
        nodes_to_check = []
        
        # nodes_inputs_ratio is a dictionary whose keys are the node names
        # and whose values are a list of two elements: the first one being
        # the number of activated mandatory input plugs, the second one being
        # the total number of mandatory input plugs of the corresponding node
        # nodes_inputs_ratio = OrderedDict()
        nodes_inputs_ratio = {}

        # nodes_inputs_ratio_list contains the ratio between the number of
        # activated mandatory input plugs and the total number of mandatory
        # input plugs of the corresponding node (the order is the same as
        # nodes_to_check)
        nodes_inputs_ratio_list = []
        
        # If the initialisation is launch for the main pipeline
        if not pipeline:
            pipeline = get_process_instance(
                self.pipelineEditorTabs.get_current_pipeline())
            main_pipeline = True

        else:
            main_pipeline = False

        # Test, if it works, comment.
        #if hasattr(pipeline, 'pipeline_steps'):
        #    pipeline.pipeline_steps.on_trait_change(
        #        self.pipelineEditorTabs.get_current_editor()._reset_pipeline,
        #        remove=True)
        #pipeline.on_trait_change(
        #    self.pipelineEditorTabs.get_current_editor()._reset_pipeline,
        #    'selection_changed', remove=True)
        #pipeline.on_trait_change(
        #    self.pipelineEditorTabs.get_current_editor()._reset_pipeline,
        #    'user_traits_changed', remove=True)

        for node_name, node in pipeline.nodes.items():
            
            # Updating the project attribute of the processes
            if hasattr(node, 'process'):
                process = node.process
                
                if hasattr(process, 'use_project') and process.use_project:
                    process.project = self.project

            nb_plugs_from_in = 0
            nb_plugs = 0

            for plug_name, plug in node.plugs.items():
                
                if ((plug.links_from) and
                    (not plug.output) and
                    (not plug.optional)):
                    nb_plugs += 1
                    
                    # If the link comes from the pipeline "global" inputs, it is
                    # added to compute the ratio
                    if list(plug.links_from)[0][0] == "":
                        nb_plugs_from_in += 1

            if nb_plugs == 0:
                ratio = 0
                
            else:
                ratio = nb_plugs_from_in / nb_plugs

            nodes_to_check.append(node_name)
            nodes_inputs_ratio[node_name] = [nb_plugs_from_in, nb_plugs]
            nodes_inputs_ratio_list.append(ratio)

        # Sorting the nodes_to_check list as the order (the nodes having
        # the highest ratio
        # being at the end of the list)
        nodes_to_check = [x for _, x in sorted(zip(nodes_inputs_ratio_list,
                                                   nodes_to_check))]

        while nodes_to_check:
            # Finding one node that has a ratio of 1,
            # which means that all of its mandatory
            # inputs are "connected"
            key_name = [key for key, value in nodes_inputs_ratio.items() if
                                                           value[0] == value[1]]

            if key_name:
                # This node can be initialized so it is placed at the
                # end of the nodes_to_check list
                nodes_to_check.append(key_name[0])

                # It can also be removed from the dictionary
                del nodes_inputs_ratio[key_name[0]]

            # Reversing the list so that the node to be initialized is
            # at the first place. Using OrderedDict allows to remove the
            # duplicate in the list without losing the order. So if
            # key_name[0] appears twice, it will stay at the first place
            nodes_to_check = list(OrderedDict((x, True) for x in
                                              nodes_to_check[::-1]).keys())
            # print(nodes_to_check)
            node_name = nodes_to_check.pop(0)

            nodes_to_check = nodes_to_check[::-1]

            # Inputs/Outputs nodes will be automatically updated with
            # the method update_nodes_and_plugs_activation of the
            # pipeline object
            if node_name in ['', 'inputs', 'outputs']:
                continue

            # If the node is a pipeline node,
            # each of its nodes has to be initialised
            node = pipeline.nodes[node_name]

            if isinstance(node, PipelineNode):
                sub_pipeline = node.process
                self.init_pipeline(sub_pipeline, node_name)

                for plug_name in node.plugs.keys():

                    # If the plug is an output and is
                    # connected to another one
                    if hasattr(node.plugs[plug_name], 'links_to'):
                        list_info_link = list(
                            node.plugs[plug_name].links_to)

                        for info_link in list_info_link:

                            # The third element of info_link contains the
                            # destination node object
                            if info_link[2] in pipeline.nodes.values():
                                dest_node_name = info_link[0]

                                if dest_node_name:
                                    # Adding the destination node name and
                                    # incrementing the input counter of the
                                    # latter if it is not the pipeline
                                    # "global" outputs ('')
                                    nodes_to_check.append(dest_node_name)
                                    nodes_inputs_ratio[dest_node_name][
                                        0] += 1

                pipeline.update_nodes_and_plugs_activation()
                continue

            # Adding the brick to the bricks history
            self.brick_id = str(uuid.uuid4())
            self.brick_list.append(self.brick_id)
            self.project.session.add_document(COLLECTION_BRICK,
                                              self.brick_id)
            self.project.session.set_value(
                COLLECTION_BRICK, self.brick_id, BRICK_NAME, node_name)
            self.project.session.set_value(
                COLLECTION_BRICK, self.brick_id, BRICK_INIT_TIME,
                datetime.datetime.now())
            self.project.session.set_value(
                COLLECTION_BRICK, self.brick_id, BRICK_INIT, "Not Done")
            self.project.saveModifications()

            process = node.process
            process_name = str(process).split('.')[0].split('_')[0][1:]

            print('\nUpdating the launching parameters for {0} '
                  'process node: {1} ...\n'.format(process_name,
                                                   node_name))

            # TODO 'except' instead of 'if' to test matlab launch ?
            # Test for matlab launch
            if config.get_use_spm_standalone():
                node.process.use_mcr = True
                node.process.paths = config.get_spm_standalone_path().split()
                node.process.matlab_cmd = config.get_matlab_command()

            elif config.get_use_spm():
                node.process.use_mcr = False
                node.process.paths = config.get_spm_path().split()
                node.process.matlab_cmd = config.get_matlab_command()

            # Test for matlab launch
            if not os.path.isdir(
                    os.path.abspath(
                        self.project.folder + os.sep + 'scripts')):
                os.mkdir(os.path.abspath(
                    self.project.folder + os.sep + 'scripts'))

            node.process.output_directory = os.path.abspath(
                                       self.project.folder + os.sep + 'scripts')
            node.process.mfile = True

            # Getting the inheritance_dict, the requirement (dict) and the node
            # outputs list according to its inputs: initResult_dic.
            # - initResult_dic['requirement']:
            # the requirement for the process (list)
            # - initResult_dic['outputs']:
            # a dictionary whose keys are the output plugs name and whose keys
            # are the correponding value
            # - initResult_dic['inheritance_dict']:
            # a dictionary whose keys are the names of the scans in the output
            # plugs and whose values are the names of the scans in the input
            # plugs from that the output scans will inherit the tags
            initResult_dict = {}

            try:
                # The state, linked or not, of the plugs is passed to the
                # list_outputs method, only for nodes not coming from nipype
                # (so those coming from mia_processes and those created
                # by the user): is_plugged object.
                is_plugged = {key: (bool(plug.links_to)
                                    or bool(plug.links_from))
                                            for key, plug in node.plugs.items()}
                initResult_dict = process.list_outputs(is_plugged=is_plugged)

                try:
 
                    if not initResult_dict['outputs']:
                         print("\nInitialisation failed to determine the "
                               "outputs for the process {0}, did you correctly "
                               "define the inputs ...?".format(node_name))
                         
                except KeyError as e:
                    print('\nDue to "{0}" error,\nthe initialisation failed to '
                          'determine the outputs for the node '
                          '{1}...'.format(e, node_name))

                except Exception as e:
                    print('\nThe outputs determination for the node "{0}" '
                          'failed during the initialisation step, due to:\n'
                          '"{1}"...'.format(node_name, e))
                    
            except TraitError as e:
                print('\nTrait error for node "{0}":\n'
                      '"{1}" ...'.format(node_name, e))

            # If the process has no "list_outputs" method,
            # which is the case for Nipype's
            except AttributeError:

                try:
                    # The Nipype Process outputs are always
                    # "private" for Capsul
                    initResult_dict['outputs'] = (process._nipype_interface
                                                  ._list_outputs())
                    tmp_dict = {}
                    
                    for key, value in initResult_dict['outputs'].items():
                        tmp_dict['_' + key] = initResult_dict['outputs'][key]
                        
                    initResult_dict['outputs'] = tmp_dict

                except TypeError:
                    print('\nInitialisation failed to determine the outputs '
                          'for the process "{0}":\nDid you correctly defined '
                          'the inputs ...?'.format(node_name))
      
                except Exception as e:
                    print('Initialisation failed to determine the outputs '
                          'for the process "{0}", due to:\n'
                          '"{1}"...'.format(node_name, e))
                    
            # Management of the requirement object in initResult_dict
            if '_nipype_interface' in dir(process):

                if 'spm' in str(process._nipype_interface):

                    if 'requirement' not in initResult_dict:
                        initResult_dict['requirement'] = ['MATLAB', 'SPM']

                elif 'requirement' not in initResult_dict:
                    initResult_dict['requirement'] = []

            if initResult_dict['requirement'] is not None:
                
                for n, i in enumerate(initResult_dict['requirement']):

                    if re.search('MATLAB', i,  re.IGNORECASE):
                        initResult_dict['requirement'][n] = 'MATLAB'

                    if re.search('SPM', i,  re.IGNORECASE):
                        initResult_dict['requirement'][n] = 'SPM'
                    
            # Management of the outputs and the inheritance_dict objects
            # in the initResult_dict
            if 'outputs' not in initResult_dict:
                    initResult_dict['outputs'] = {}

            if ('inheritance_dict' in initResult_dict and
                initResult_dict['inheritance_dict'] != {}):
                self.inheritance_dict = initResult_dict['inheritance_dict']

            # Here, third-party softwares are managed according to the
            # requirement defined in the bricks.
            # Third-party software currently managed:
            # Matlab - SPM - ...
            if initResult_dict['requirement'] is None:
                nodes_requir_issue[node_name] = 'MISSING'

            elif initResult_dict['requirement']:

                if (('MATLAB' in initResult_dict['requirement']) and
                    (not config.get_use_matlab())):
                    nodes_requir_issue.setdefault(node_name,
                                                  []).append('MATLAB')

                if (('SPM' in initResult_dict['requirement']) and
                    ((not config.get_use_spm()) and
                     (not config.get_use_spm_standalone()))):
                    nodes_requir_issue.setdefault(node_name,
                                                  []).append('SPM')

            # Adding I/O to database history
            inputs = process.get_inputs()
            self.inputs = inputs

            for key in inputs:

                if inputs[key] is Undefined:
                    inputs[key] = "<undefined>"
                        
            # Automatically fills few plugs. Only for the nipype process
            if 'NipypeProcess' in str(process.__class__):
                print('\nUpdating the launching parameters for nipype '
                      'process node: {0} ...'.format(node_name))
                # plugs to be filled automatically
                keys2consider = ['use_mcr', 'paths',
                                 'matlab_cmd', 'output_directory']

                for key in inputs:
                    
                    # use_mcr parameter
                    if (key == keys2consider[0]) and (
                            config.get_use_spm_standalone()):
                        inputs[key] = True
                        
                    elif (key == keys2consider[0]) and (
                            not config.get_use_spm_standalone()):
                        inputs[key] = False
                        
                    # paths parameter
                    if (key == keys2consider[1]) and (
                            config.get_use_spm_standalone()):
                        inputs[key] = config.get_spm_standalone_path().split()
                        
                    elif (key == keys2consider[1]) and (config.get_use_spm()):
                        inputs[key] = config.get_spm_path().split()
                        
                    # matlab_cmd parameter
                    if (key == keys2consider[2]) and (
                            config.get_use_spm_standalone()):
                        inputs[key] = config.get_matlab_command()
                        
                    elif (key == keys2consider[2]) and (
                            not config.get_use_spm_standalone()):
                        inputs[key] = config.get_matlab_path()

                    # output_directory parameter
                    if key == keys2consider[3]:

                        if not os.path.isdir(os.path.abspath(
                                self.project.folder + '/scripts')):
                            os.mkdir(os.path.abspath(self.project.folder
                                                     + '/scripts'))

                        inputs[key] = os.path.abspath(self.project.folder
                                                      + '/scripts')

                    try:
                        node.set_plug_value(key, inputs[key])

                    except TraitError:

                        if isinstance(inputs[key], list) and len(
                                inputs[key]) == 1:

                            try:
                                pipeline.nodes[key].set_plug_value(
                                    key, inputs[key][0])

                            except TraitError as e:
                                print('Trait error for the "{0}" plug ({1}):\n'
                                      '{2} ...'.format(key, inputs[key], e))

            outputs = process.get_outputs() 

            for key in outputs:
                value = outputs[key]
                
                if value is Undefined:
                    outputs[key] = "<undefined>"
                    
            self.project.saveModifications()
            self.project.session.set_value(COLLECTION_BRICK, self.brick_id,
                                           BRICK_INPUTS, inputs)
            self.project.session.set_value(COLLECTION_BRICK, self.brick_id,
                                           BRICK_OUTPUTS, outputs)

            # Update the database with output values obtained
            # from initialisation
            if initResult_dict['outputs']:
                
                for plug_name, plug_value in initResult_dict['outputs'].items():
 
                    if plug_name not in node.plugs.keys():
                        continue
                    
                    if plug_value not in ["<undefined>", Undefined]:
                        
                        if pipeline_name != "":
                            full_name = pipeline_name + "." + node_name
                            
                        else:
                            full_name = node_name
                            
                        self.add_plug_value_to_database(plug_value,
                                                        self.brick_id,
                                                        node_name,
                                                        plug_name, full_name)

                    list_info_link = list(node.plugs[plug_name].links_to)

                    # If the output is connected to another node,
                    # the latter is added to nodes_to_check
                    for info_link in list_info_link:
                        dest_node_name = info_link[0]
                        
                        if dest_node_name:
                            # Adding the destination node name and incrementing
                            # the input counter of the latter
                            nodes_to_check.append(dest_node_name)
                            
                            if dest_node_name in nodes_inputs_ratio:
                                nodes_inputs_ratio[dest_node_name][0] += 1

                    try:
                        node.set_plug_value(plug_name, plug_value)
                        
                    except TraitError:
                        
                        if type(plug_value) is list and len(
                                plug_value) == 1:
                            
                            try:
                                node.set_plug_value(plug_name, plug_value[0])
                                
                            except TraitError as e:
                                print('Trait error for the "{0}" plug of the '
                                      '"{1}" node:\n'
                                      '{2} ...'.format(plug_name, node_name, e))

                    pipeline.update_nodes_and_plugs_activation()

            # Adding I/O to database history again to update outputs
            inputs = process.get_inputs()
            
            for key in inputs:
                value = inputs[key]
                
                if value is Undefined:
                    inputs[key] = "<undefined>"
    
            outputs = process.get_outputs()

            for key in outputs:
                value = outputs[key]

                if value is Undefined:
                    outputs[key] = "<undefined>"

            self.project.session.set_value(COLLECTION_BRICK, self.brick_id,
                                           BRICK_INPUTS, inputs)
            self.project.session.set_value(COLLECTION_BRICK, self.brick_id,
                                           BRICK_OUTPUTS, outputs)
            # Setting brick init state if init finished correctly
            self.project.session.set_value(COLLECTION_BRICK, self.brick_id,
                                           BRICK_INIT, "Done")
     
            self.project.saveModifications()

        # Test, if it works, comment.
        #pipeline.on_trait_change(
        #    self.pipelineEditorTabs.get_current_editor()._reset_pipeline,
        #    'selection_changed', dispatch='ui')
        #pipeline.on_trait_change(
        #    self.pipelineEditorTabs.get_current_editor()._reset_pipeline,
        #    'user_traits_changed', dispatch='ui')
        #if hasattr(pipeline, 'pipeline_steps'):
        #    pipeline.pipeline_steps.on_trait_change(
        #        self.pipelineEditorTabs.get_current_editor()._reset_pipeline,
        #        dispatch='ui')

        # Updating the node controller
        # Display the updated parameters in right part of
        # the Pipeline Manager (controller)
        if main_pipeline:
            node_controller_node_name = self.nodeController.node_name     #### Todo: Fix the problem of the controller that
                                                                          #### keeps the name of the old brick deleted until
                                                                          #### a click on the new one. This can cause a mia
                                                                          #### crash during the initialisation, for example.

            if node_controller_node_name in ['inputs', 'outputs']:
                node_controller_node_name = ''
  
            self.nodeController.display_parameters(
                self.nodeController.node_name,
                pipeline.nodes[node_controller_node_name].process,
                pipeline)
            
        nodes_requir_miss = [nodeName for nodeName in nodes_requir_issue
                                   if nodes_requir_issue[nodeName] == 'MISSING']
        nodes_requir_fail = [nodeName for nodeName in nodes_requir_issue
                              if isinstance(nodes_requir_issue[nodeName], list)]

        if ((nodes_requir_miss or nodes_requir_fail) and
            not (config.get_use_matlab() and
                (config.get_use_spm() or config.get_use_spm_standalone()))):
            
            if ((config.get_use_matlab()) and
                (not config.get_use_matlab_standalone())):

                if config.get_use_spm():
                    message_conf = ("The current MIA configuration uses "
                                    "Matlab and SPM.\n")
                else:
                    message_conf = ("The current MIA configuration uses "
                                    "Matlab but not SPM.\n")
                        
            elif ((config.get_use_matlab()) and
                  (config.get_use_matlab_standalone())):

                if config.get_use_spm_standalone():
                    message_conf = ("The current MIA configuration uses Matlab "
                                    "Compiler Runtime and SPM standalone.\n")
                else:
                    message_conf = ("The current MIA configuration uses Matlab "
                                    "Compiler Runtime but not SPM standalone."
                                    "\n")

            elif not config.get_use_matlab():
                message_conf = ("The current MIA configuration does not use "
                                "Matlab (including the Compiler Runtime "
                                "version) or SPM (including the standalone "
                                "version).\n")
            
            message_base1 = ''
        
            if nodes_requir_miss: # So, initResult_dict['requirement'] is None

                if len(nodes_requir_miss) == 1:
                    message_base1 = ('-'*90 + '\nThe required third-party '
                                     'products are not properly defined in the '
                                     'following process:\n- {0}\n'
                                     .format(nodes_requir_miss[0]))

                else:
                    message_base1 = ('-'*90 + '\nThe required third-party '
                                     'products are not properly defined in the '
                                     'following processes:\n')

                    for nodeName in nodes_requir_miss:
                        message_base1 = message_base1 + ("- {0}\n"
                                                         .format(nodeName))

                message_end = ('\nPlease, update your configuration in the MIA '
                               'preferences, if necessary ...')
            
            mess_base2 = ''
        
            if nodes_requir_fail: 
                message_end = ('\nPlease, update your configuration in the MIA '
                               'preferences to meet the requirements of '
                               'the pipeline ...')

                if not nodes_requir_miss:
                    mess_base2 =  mess_base2 + '-'*90 + '\nThe '
                
                else:
                    mess_base2 =  mess_base2 + '\nIn addition, the '

                mess_base2 =  mess_base2 + ('following bricks have '
                                            'requirements that do not '
                                            'correspond to the current MIA '
                                            'configuration (problematic third-'
                                            'party software(s) is(are) '
                                            'specified):\n')
                
                for nodeName in nodes_requir_fail:
                    mess_base2 = mess_base2 + ('- {0}: {1}\n'
                                               .format(nodeName,
                                                       ', '.join(
                                                           nodes_requir_issue[
                                                               nodeName])))

            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setWindowTitle("MIA configuration warning!")
            self.msg.setText(message_conf + message_base1 +
                             mess_base2 + message_end)
            
            yes_button = self.msg.addButton("Open MIA preferences",
                                            QMessageBox.YesRole)

            if (nodes_requir_miss) and (not nodes_requir_fail):
                ok_button = self.msg.addButton(QMessageBox.Ok)

            self.msg.exec()
            
            if self.msg.clickedButton() == yes_button:
                self.main_window.software_preferences_pop_up()
                self.msg.close()
                
            else:
                self.msg.close()

            if nodes_requir_fail:
                self.main_window.statusBar().showMessage(
                'Pipeline "{0}" was not initialised successfully.'.format(name))

            else:
                self.main_window.statusBar().showMessage(
                    'The pipeline "{0}" has been initialised, but the '
                    'requirements of some bricks must be verified.'
                    .format(name))

        else:
            self.main_window.statusBar().showMessage(
                'Pipeline "{0}" has been initialised.'.format(name))

    def initialize(self):
        """Clean previous initialization then initialize the current
        pipeline."""

        if self.init_clicked:
            for brick in self.brick_list:
                self.main_window.data_browser.table_data.delete_from_brick(
                    brick)
        self.ignore_node = False
        self.key = {}
        self.ignore = {}
        self.init_pipeline() # When clicking on the Pipeline > Initialize
                             # pipeline in the Pipeline Manager tab,
                             # this is the first method launched.

        # ** pathway from the self.init_pipeline() command (ex. for the
        #    User_processes Smooth brick):
        #      info1: self is a populse_mia.user_interface.pipeline_manager
        #             .pipeline_manager_tab.PipelineManagerTab object
        #
        # ** populse_mia/user_interface/pipeline_manager/pipeline_manager_tab.py
        #    class PipelineManagerTab(QWidget):
        #    method init_pipeline(self, pipeline=None, pipeline_name=""):
        #      use: initResult_dict = process.list_outputs(
        #                                                 is_plugged=is_plugged)
        #      info1: process is the brick (node, process, etc.)
        #             <User_processes.preprocess.spm.spatial_preprocessing
        #             .Smooth object at ...> object
        
        # ** User_processes/preprocess/spm/spatial_preprocessing.py
        #    class Smooth(Process_Mia)
        #    list_outputs method:
        #      use: super(Smooth, self).list_outputs(). Using the inheritance
        #           to ProcessMIA class, list_outputs method.
        #      info1: here we are in the place where we deal with plugs.
        #
        #** Some characteristics for the pipeline object
        #   (for User_processes Smooth brick):
        #       pipeline is a capsul.pipeline.pipeline.Pipeline object
        #       pipeline.nodes is a dictionary
        #       pipeline.nodes["smooth1"] is a capsul.pipeline.pipeline_nodes
        #         .ProcessNode object
        #       pipeline.nodes["smooth1"].plugs is a dictionary. Each key is a
        #         plug displayed in the Pipeline manager tab
        #       pipeline.nodes["smooth1"].plugs["fwhm"] is a capsul.pipeline
        #         .pipeline_nodes.Plug object
        #       If the plus is not connected,  pipeline.nodes["smooth1"]
        #         .plugs["fwhm"].links_to (in case of output link) : set()
        #       If the plus is connected,  pipeline.nodes["smooth1"]
        #         .plugs["fwhm"].links_to (in case of output link):
        #         {('', 'fwhm', <capsul.pipeline.pipeline_nodes.PipelineNode
        #         object at 0x7f4688109c50>, <capsul.pipeline.pipeline_nodes
        #         .Plug object at 0x7f46691e4888>, False)}
        #       So, it is possble to check if the plug is connected with:
        #         if pipeline.nodes["smooth1"].plugs["fwhm"].links_to: etc ...
        #         or a  if pipeline.nodes["smooth1"].plugs["fwhm"].links_from:
        #         etc ...

        self.init_clicked = True

    def layout_view(self):
        """Initialize layout for the pipeline manager tab"""
        self.setWindowTitle("Diagram editor")

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.nodeController)

        # Toolbar
        self.tags_menu.addAction(self.load_pipeline_action)
        self.tags_menu.addAction(self.save_pipeline_action)
        if Config().get_clinical_mode():
            self.save_pipeline_action.setDisabled(True)
            self.pipelineEditorTabs.get_current_editor(
            ).disable_overwrite = True
        else:
            self.save_pipeline_action.setEnabled(True)
            self.pipelineEditorTabs.get_current_editor(
            ).disable_overwrite = False
        self.tags_menu.addAction(self.save_pipeline_as_action)
        self.tags_menu.addSeparator()
        self.tags_menu.addAction(self.load_pipeline_parameters_action)
        self.tags_menu.addAction(self.save_pipeline_parameters_action)
        self.tags_menu.addSeparator()
        self.tags_menu.addAction(self.init_pipeline_action)
        self.tags_menu.addAction(self.run_pipeline_action)

        self.tags_tool_button.setText('Pipeline')
        self.tags_tool_button.setPopupMode(
            QtWidgets.QToolButton.MenuButtonPopup)
        self.tags_tool_button.setMenu(self.tags_menu)

        # Layouts

        self.hLayout.addWidget(self.tags_tool_button)
        self.hLayout.addStretch(1)

        self.splitterRight.addWidget(self.iterationTable)
        self.splitterRight.addWidget(self.scrollArea)
        self.splitterRight.setSizes([400, 400])

        # previewScene = QGraphicsScene()
        # previewScene.setSceneRect(QtCore.QRectF())
        # self.previewDiagram = QGraphicsView()
        # self.previewDiagram.setEnabled(False)

        self.splitter0.addWidget(self.processLibrary)
        self.splitter0.addWidget(self.previewBlock)

        self.splitter1.addWidget(self.splitter0)
        self.splitter1.addWidget(self.pipelineEditorTabs)
        self.splitter1.addWidget(self.splitterRight)
        self.splitter1.setSizes([200, 800, 200])

        # self.splitter2 = QSplitter(Qt.Vertical)
        # self.splitter2.addWidget(self.splitter1)
        # self.splitter2.setSizes([800, 100])

        self.verticalLayout.addLayout(self.hLayout)
        self.verticalLayout.addWidget(self.splitter1)

    def loadPipeline(self):
        """
        Load a pipeline to the pipeline editor

        """
        self.pipelineEditorTabs.load_pipeline()

    def loadParameters(self):
        """
        Load pipeline parameters to the current pipeline of the pipeline editor

        """
        self.pipelineEditorTabs.load_pipeline_parameters()

        self.nodeController.update_parameters()

    def redo(self):
        """
        Redo the last undone action on the current pipeline editor

        Actions that can be redone:
            - add_process
            - delete_process
            - export_plug
            - export_plugs
            - remove_plug
            - update_node_name
            - update_plug_value
            - add_link
            - delete_link

        """
        c_e = self.pipelineEditorTabs.get_current_editor()

        # We can redo if we have an action to make again
        if len(self.pipelineEditorTabs.redos[c_e]) > 0:
            to_redo = self.pipelineEditorTabs.redos[c_e].pop()
            # The first element of the list is the type of action made
            # by the user
            action = to_redo[0]

            if action == "delete_process":
                node_name = to_redo[1]
                class_process = to_redo[2]
                links = to_redo[3]
                c_e.add_process(
                    class_process, node_name, from_redo=True, links=links)

            elif action == "add_process":
                node_name = to_redo[1]
                c_e.del_node(node_name, from_redo=True)

            elif action == "export_plug":
                temp_plug_name = to_redo[1]
                c_e._remove_plug(
                    _temp_plug_name=temp_plug_name, from_redo=True)

            elif action == "export_plugs":
                # No redo possible
                pass

            elif action == "remove_plug":
                temp_plug_name = to_redo[1]
                new_temp_plugs = to_redo[2]
                optional = to_redo[3]
                c_e._export_plug(temp_plug_name=new_temp_plugs[0],
                                 weak_link=False,
                                 optional=optional,
                                 from_redo=True,
                                 pipeline_parameter=temp_plug_name[1])

                # Connecting all the plugs that were connected
                # to the original plugs
                for plug_tuple in new_temp_plugs:
                    # Checking if the original plug is a pipeline
                    # input or output to adapt
                    # the links to add.
                    if temp_plug_name[0] == 'inputs':
                        source = ('', temp_plug_name[1])
                        dest = plug_tuple
                    else:
                        source = plug_tuple
                        dest = ('', temp_plug_name[1])

                    c_e.scene.add_link(source, dest, active=True, weak=False)

                    # Writing a string to represent the link
                    source_parameters = ".".join(source)
                    dest_parameters = ".".join(dest)
                    link = "->".join((source_parameters, dest_parameters))

                    c_e.scene.pipeline.add_link(link)
                    c_e.scene.update_pipeline()

            elif action == "update_node_name":
                node = to_redo[1]
                new_node_name = to_redo[2]
                old_node_name = to_redo[3]
                c_e.update_node_name(
                    node, new_node_name, old_node_name, from_redo=True)

            elif action == "update_plug_value":
                node_name = to_redo[1]
                new_value = to_redo[2]
                plug_name = to_redo[3]
                value_type = to_redo[4]
                c_e.update_plug_value(
                    node_name, new_value, plug_name,
                    value_type, from_redo=True)

            elif action == "add_link":
                link = to_redo[1]
                c_e._del_link(link, from_redo=True)

            elif action == "delete_link":
                source = to_redo[1]
                dest = to_redo[2]
                active = to_redo[3]
                weak = to_redo[4]
                c_e.add_link(source, dest, active, weak, from_redo=True)
                # link = source[0] + "." + source[1]
                # + "->" + dest[0] + "." + dest[1]

            c_e.scene.pipeline.update_nodes_and_plugs_activation()
            self.nodeController.update_parameters()

    def runPipeline(self):
        """Run the current pipeline of the pipeline editor."""

        name = os.path.basename(self.pipelineEditorTabs.get_current_filename())
        self.brick_list = []
        self.main_window.statusBar().showMessage(
            'Pipeline "{0}" is getting run. Please wait.'.format(name))
        QApplication.processEvents()
        self.key = {}
        self.ignore = {}
        self.ignore_node = False

        if self.iterationTable.check_box_iterate.isChecked():
            iterated_tag = self.iterationTable.iterated_tag
            tag_values = self.iterationTable.tag_values_list
            ui_iteration = PopUpSelectIteration(iterated_tag, tag_values)
            if ui_iteration.exec():
                tag_values = ui_iteration.final_values
                pipeline_progress = dict()
                pipeline_progress['size'] = len(tag_values)
                pipeline_progress['counter'] = 1
                pipeline_progress['tag'] = iterated_tag
                for tag_value in tag_values:
                    self.brick_list = []
                    # Status bar update
                    pipeline_progress['tag_value'] = tag_value

                    idx_combo_box = self.iterationTable.combo_box.findText(
                        tag_value)
                    self.iterationTable.combo_box.setCurrentIndex(
                        idx_combo_box)
                    self.iterationTable.update_table()

                    self.init_pipeline()
                    self.main_window.statusBar().showMessage(
                        'Pipeline "{0}" is getting run for {1} {2}. '
                        'Please wait.'.format(name, iterated_tag, tag_value))
                    QApplication.processEvents()
                    self.progress = RunProgress(self.pipelineEditorTabs,
                                                pipeline_progress)
                    self.progress.show()
                    self.progress.exec()
                    pipeline_progress['counter'] += 1
                    self.init_clicked = False
                    # # self.init_pipeline(self.pipeline)
                    # idx = self.progress.value()
                    # idx += 1
                    # self.progress.setValue(idx)
                    # QApplication.processEvents()

            self.main_window.statusBar().showMessage(
                'Pipeline "{0}" has been run for {1} {2}. Please wait.'.format(
                    name, iterated_tag, tag_values))

        else:
            
            try:
                self.progress = RunProgress(self.pipelineEditorTabs)
                self.progress.show()
                self.progress.exec()
                
            except Exception as e:
                print('\n When the pipeline was launched, the following '
                      'exception was raised: {0} ...'.format(e, ))
                self.main_window.statusBar().showMessage(
                    'Pipeline "{0}" has not been correctly run.'.format(name))
                
            else:
                self.main_window.statusBar().showMessage(
                    'Pipeline "{0}" has been correctly run.'.format(name))

            self.init_clicked = False

    def saveParameters(self):
        """
        Save the pipeline parameters of the the current pipeline of the
        pipeline editor

        """
        self.pipelineEditorTabs.save_pipeline_parameters()

    def savePipeline(self):
        """
        Save the current pipeline of the pipeline editor

        """
        self.main_window.statusBar().showMessage(
            'The pipeline is getting saved. Please wait.')
        # QApplication.processEvents()

        filename = self.pipelineEditorTabs.get_current_filename()

        if filename:
            self.pipelineEditorTabs.save_pipeline(new_file_name=filename)

        else:
            self.pipelineEditorTabs.save_pipeline()

        self.main_window.statusBar().showMessage(
            'The pipeline has been saved.')

    def savePipelineAs(self):
        """
        Save the current pipeline of the pipeline editor under another name

        """

        self.main_window.statusBar().showMessage(
            'The pipeline is getting saved. Please wait.')

        self.pipelineEditorTabs.save_pipeline()

        self.main_window.statusBar().showMessage(
            'The pipeline has been saved.')

    def undo(self):
        """
        Undo the last action made on the current pipeline editor

        Actions that can be undone:
            - add_process
            - delete_process
            - export_plug
            - export_plugs
            - remove_plug
            - update_node_name
            - update_plug_value
            - add_link
            - delete_link

        """
        c_e = self.pipelineEditorTabs.get_current_editor()

        # We can undo if we have an action to revert
        if len(self.pipelineEditorTabs.undos[c_e]) > 0:
            to_undo = self.pipelineEditorTabs.undos[c_e].pop()
            # The first element of the list is the type of action made
            # by the user
            action = to_undo[0]

            if action == "add_process":
                node_name = to_undo[1]
                c_e.del_node(node_name, from_undo=True)

            elif action == "delete_process":
                node_name = to_undo[1]
                class_name = to_undo[2]
                links = to_undo[3]
                c_e.add_process(
                    class_name, node_name, from_undo=True, links=links)

            elif action == "export_plug":
                temp_plug_name = to_undo[1]
                c_e._remove_plug(
                    _temp_plug_name=temp_plug_name, from_undo=True)

            elif action == "export_plugs":
                parameter_list = to_undo[1]
                node_name = to_undo[2]
                for parameter in parameter_list:
                    temp_plug_name = ('inputs', parameter)
                    c_e._remove_plug(
                        _temp_plug_name=temp_plug_name,
                        from_undo=True,
                        from_export_plugs=True)
                self.main_window.statusBar().showMessage(
                    "Plugs {0} have been removed.".format(str(parameter_list)))

            elif action == "remove_plug":
                temp_plug_name = to_undo[1]
                new_temp_plugs = to_undo[2]
                optional = to_undo[3]
                c_e._export_plug(temp_plug_name=new_temp_plugs[0],
                                 weak_link=False,
                                 optional=optional, from_undo=True,
                                 pipeline_parameter=temp_plug_name[1])

                # Connecting all the plugs that were connected
                # to the original plugs
                for plug_tuple in new_temp_plugs:
                    # Checking if the original plug is a pipeline
                    # input or output to adapt
                    # the links to add.
                    if temp_plug_name[0] == 'inputs':
                        source = ('', temp_plug_name[1])
                        dest = plug_tuple
                    else:
                        source = plug_tuple
                        dest = ('', temp_plug_name[1])

                    c_e.scene.add_link(source, dest, active=True, weak=False)

                    # Writing a string to represent the link
                    source_parameters = ".".join(source)
                    dest_parameters = ".".join(dest)
                    link = "->".join((source_parameters, dest_parameters))

                    c_e.scene.pipeline.add_link(link)
                    c_e.scene.update_pipeline()

            elif action == "update_node_name":
                node = to_undo[1]
                new_node_name = to_undo[2]
                old_node_name = to_undo[3]
                c_e.update_node_name(node, new_node_name, old_node_name,
                                     from_undo=True)

            elif action == "update_plug_value":
                node_name = to_undo[1]
                old_value = to_undo[2]
                plug_name = to_undo[3]
                value_type = to_undo[4]
                c_e.update_plug_value(node_name, old_value, plug_name,
                                      value_type, from_undo=True)

            elif action == "add_link":
                link = to_undo[1]
                c_e._del_link(link, from_undo=True)

            elif action == "delete_link":
                source = to_undo[1]
                dest = to_undo[2]
                active = to_undo[3]
                weak = to_undo[4]
                c_e.add_link(source, dest, active, weak, from_undo=True)
                # link = source[0] + "." + source[1] +
                # "->" + dest[0] + "." + dest[1]

            c_e.scene.pipeline.update_nodes_and_plugs_activation()
            self.nodeController.update_parameters()

    def update_clinical_mode(self):
        """
        Update the visibility of widgets/actions depending of the chosen mode

        """
        config = Config()

        # If the clinical mode is chosen, the process library is not available
        # and the user cannot save a pipeline
        if config.get_clinical_mode():
            self.save_pipeline_action.setDisabled(True)
            self.pipelineEditorTabs.get_current_editor(
            ).disable_overwrite = True
        else:
            self.save_pipeline_action.setDisabled(False)
            self.pipelineEditorTabs.get_current_editor(
            ).disable_overwrite = False

        # If the clinical mode is chosen, the process library is not available
        # and the user cannot save a pipeline
        # if config.get_clinical_mode() == True:
        #     self.processLibrary.setHidden(True)
        #     self.previewBlock.setHidden(True)
        #     self.save_pipeline_action.setDisabled(True)
        #     self.save_pipeline_as_action.setDisabled(True)
        # else:
        # self.processLibrary.setHidden(False)
        # self.previewBlock.setHidden(False)
        # self.save_pipeline_action.setDisabled(False)
        # self.save_pipeline_as_action.setDisabled(False)

    def update_project(self, project):
        """
        Update the project attribute of several objects

        :param project: current project in the software
        """
        self.project = project
        self.nodeController.project = project
        self.pipelineEditorTabs.project = project
        self.nodeController.visibles_tags = \
            self.project.session.get_shown_tags()
        self.iterationTable.project = project

        # Necessary for using MIA bricks
        ProcessMIA.project = project

    def update_scans_list(self, iteration_list):
        """
        Update the user-selected list of scans

        :param iteration_list: current list of scans in the iteration table
        """
        if self.iterationTable.check_box_iterate.isChecked():
            self.iteration_table_scans_list = iteration_list
            self.pipelineEditorTabs.scan_list = iteration_list
        else:
            self.iteration_table_scans_list = []
            self.pipelineEditorTabs.scan_list = self.scan_list
        if not self.pipelineEditorTabs.scan_list:
            self.pipelineEditorTabs.scan_list = \
                self.project.session.get_documents_names(COLLECTION_CURRENT)
        self.pipelineEditorTabs.update_scans_list()

    def updateProcessLibrary(self, filename):
        """
        Update the library of processes when a pipeline is saved

        :param filename: file name of the pipeline that has been saved
        """
        filename_folder, file_name = os.path.split(filename)
        module_name = os.path.splitext(file_name)[0]
        class_name = module_name.capitalize()

        tmp_file = os.path.join(filename_folder, module_name + '_tmp')

        # Changing the "Pipeline" class name to the name of file
        with open(filename, 'r') as f:
            with open(tmp_file, 'w') as tmp:
                for line in f:
                    line = line.strip('\r\n')
                    if 'class ' in line:
                        line = 'class {0}(Pipeline):'.format(class_name)
                    tmp.write(line + '\n')

        with open(tmp_file, 'r') as tmp:
            with open(filename, 'w') as f:
                for line in tmp:
                    f.write(line)

        os.remove(tmp_file)
        config = Config()

        if os.path.relpath(filename_folder) != \
                os.path.relpath(os.path.join(
                    config.get_mia_path(), 'processes', 'User_processes')):
            return

        # Updating __init__.py
        init_file = os.path.join(
            config.get_mia_path(), 'processes',
            'User_processes', '__init__.py')

        # Checking that import line is not already in the file
        pattern = 'from .{0} import {1}\n'.format(module_name, class_name)
        file = open(init_file, 'r')
        flines = file.readlines()
        file.close()
        if pattern not in flines:
            with open(init_file, 'a') as f:
                print('from .{0} import {1}'.format(
                    module_name, class_name), file=f)

        package = 'User_processes'
        path = os.path.relpath(os.path.join(filename_folder, '..'))

        # If the pipeline has already been saved
        if 'User_processes.' + module_name in sys.modules.keys():
            # removing the previous version of the module
            del sys.modules['User_processes.' + module_name]
            # this adds the new module version to the sys.modules dictionary
            __import__('User_processes')

        # Adding the module path to the system path
        if path not in sys.path:
            sys.path.insert(0, path)

        self.processLibrary.pkg_library.add_package(package, class_name,
                                                    init_package_tree=True)

        if os.path.relpath(path) not in self.processLibrary.pkg_library.paths:
            self.processLibrary.pkg_library.paths.append(os.path.relpath(path))

        self.processLibrary.pkg_library.save()


class RunProgress(QProgressDialog):
    """Create the pipeline progress bar and launch the thread.

    The progress bar is closed when the thread finishes.

    :param diagram_view: A pipelineEditorTabs
    :param settings: dictionary of settings when the pipeline is iterated
    """

    def __init__(self, diagram_view, settings=None):

        super(RunProgress, self).__init__("Please wait while the pipeline is "
                                          "running...", None, 0, 0)
        
        if settings:
            self.setWindowTitle(
                "Pipeline is running ({0}/{1})".format(
                    settings["counter"], settings["size"]))
            self.setLabelText('Pipeline is running for {0} in {1}. '
                              'Please wait.'.format(settings['tag_value'],
                                                    settings['tag']))
        else:
            self.setWindowTitle("Pipeline running")
            
        self.setWindowFlags(
            Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setModal(True)

        self.diagramView = diagram_view

        self.setMinimumDuration(0)
        self.setValue(0)
        self.setMinimumWidth(350) # For mac OS
        
        self.worker = RunWorker(self.diagramView)
        self.worker.finished.connect(self.close)
        self.worker.start()
        
class RunWorker(QThread):
    """Run the pipeline"""

    def __init__(self, diagram_view):
        super().__init__()
        self.diagramView = diagram_view

    def run(self):

        def _check_nipype_processes(pplne):
            for node_name, node in pplne.nodes.items():
                if isinstance(node.process, Pipeline):
                    if node_name != "":
                        _check_nipype_processes(node.process)
                elif isinstance(node.process, NipypeProcess):
                    node.process.activate_copy = False

        _check_nipype_processes(self.diagramView.get_current_pipeline())

        pipeline = get_process_instance(  
             self.diagramView.get_current_pipeline())

        # Reading config
        config = Config()
        spm_standalone_path = config.get_spm_standalone_path()
        spm_path = config.get_spm_path()
        matlab_path = config.get_matlab_path()
        matlab_standalone_path = config.get_matlab_standalone_path()
        use_spm = config.get_use_spm()
        use_spm_standalone = config.get_use_spm_standalone()
        use_matlab = config.get_use_matlab()

        if use_spm_standalone == True and os.path.exists(
                spm_standalone_path) and os.path.exists(
            matlab_standalone_path):

            if os.path.exists(matlab_path):
                study_config = StudyConfig(
                    use_spm=True, spm_directory=spm_standalone_path,
                    spm_exec=matlab_standalone_path,
                    matlab_exec=matlab_path,
                    output_directory=spm_standalone_path, spm_standalone=True)
            else:
                study_config = StudyConfig(
                    use_spm=True, spm_directory=spm_standalone_path,
                    spm_exec=matlab_standalone_path,
                    output_directory=spm_standalone_path, spm_standalone=True)

        # Using without SPM standalone
        elif use_spm == True and use_matlab == True:
            study_config = StudyConfig(
                use_spm=True, matlab_exec=matlab_path,
                spm_directory=spm_path, spm_standalone=False,
                use_matlab=True, output_directory=spm_path)
        else:
            study_config = StudyConfig(use_spm=False)

        study_config.reset_process_counter()

        try:
            study_config.run(pipeline, verbose=1)

            #** pathway from the study_config.run(pipeline, verbose=1) command:
            #   (ex. for the User_processes Smooth brick):
            #     info1: study_config = StudyConfig(...) defined before
            #     info2: from capsul.api import (..., StudyConfig, ...) defined
            #            before
            
            #** capsul/study_config/study_config.py
            #   class StudyConfig(Controller)
            #    run method:
            #     use: result = self._run(process_node.process,
            #                             output_directory,
            #                             verbose) ou
            #          result = self._run(process_node,
            #                             output_directory,
            #                             verbose)
            #     info1: _run() is a private method of the
            #            StudyConfig(Controller) class in the
            #            capsul/study_config/study_config.py module
            #
            #** capsul/study_config/study_config.py
            #   class StudyConfig(Controller)
            #   run method:
            #     use: returncode, log_file = run_process(output_directory,
            #                                             process_instance,
            #                                             cachedir=cachedir,
            #                            generate_logging=self.generate_logging,
            #                            verbose=verbose, **kwargs)
            #     info1: from capsul.study_config.run import run_process defined
            #            in the capsul/study_config/study_config.py module
            
            #** capsul/study_config/run.py; run_process function:
            #     use: returncode = process_instance._run_process()
            #     info1: process_instance is the brick (node, process, etc.)
            #            object (ex.  <User_processes.preprocess.spm
            #            .spatial_preprocessing.Smooth object at ...>)
            #     info2: homemade bricks do not have a mandatory _run_process
            #            method but they inherit the Process_Mia class (module
            #            mia_processes/process_mia.py) that has the
            #            _run_process method
            
            #** mia_processes/process_mia.py
            #   class Process_Mia(ProcessMIA)
            #   _run_process method
            #     use: self.run_process_mia()
            #     info1: self is the brick (node, process, etc.) object
            #            <User_processes.preprocess.spm.spatial_preprocessing
            #            .Smooth object at ...>
            
            #** User_processes/preprocess/spm/spatial_preprocessing.py
            #   class Smooth(Process_Mia)
            #   run_process_mia method:
            #     info1: this is the method where we do what we want when
            #            launching a brick (node, process, etc.).
            #     use1: super(Smooth, self).run_process_mia()
            #     info2: it calls the run_process_mia method of the Process_Mia
            #            class inherited by the Smooth class. run_process_mia
            #            method of the Process_Mia class manages the hidden
            #            matlab parameters (use_mcr, matlab_cmd, etc)
            #     use2: self.process.run()
            #     info3: self.process is a <nipype.interfaces.spm.preprocess
            #            .Smooth> object. This object inherits from the nipype
            #            SPMCommand class, which itself inherits from the nipype
            #            BaseInterface class. The BaseInterface class
            #            (nipype/interfaces/base.core.py module) have the run()
            #            method)
            #     info4: from this method run(), we are outside of mia ...
            #
            #** pipeline object introspection: see initialize method in the
            #                                  PipelineManagerTab class, this
            #                                  module
           
        except (OSError, ValueError, Exception) as e:
            print('\n{0} has not been launched:\n{1}\n'.format(pipeline.name,
                                                               e))
        # haven't yet found how to raise the exception in the try block in
        # PipelineManagerTab.runPipeline() above. So the
        # self.main_window.statusBar().showMessage() gives the
        # "has been correctly run" message even if a problem has occurred here!

            #self.diagramView.main_window.statusBar().showMessage(
            #        'Pipeline "{0}" has not been correctly run.'.format(pipeline.name))
            
            #self.msg = QMessageBox()
            #self.msg.setIcon(QMessageBox.Critical)
            #self.msg.setText("SPM standalone is not set")
            #self.msg.setInformativeText(
            #    "SPM processes cannot be run with SPM standalone not set.\n"
            #    "You can activate it and set the paths in MIA preferences.")
            #self.msg.setWindowTitle("Error")
            #self.msg.setStandardButtons(QMessageBox.Ok)
            #self.msg.buttonClicked.connect(self.msg.close)
            #self.msg.show()

            #except ValueError as e:
            #    print("\n{0} has not been launched:\n{1}\n".format(pipeline.name,
            #                                                       e))
