import inspect
import operator
import os
import pybullet
from typing import List

import numpy as np

from scene_object_bases import SceneObject, SlicingSceneObject, SlicableSceneObject
from .scene_bases import Scene

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0, parentdir)


class PickAndPlaceScene(Scene):
    """
    The goal of this scene is to set up a scene for picking up and moving
    an object to another location.

    """

    def __init__(self, bullet_client, gravity, timestep, frame_skip):
        super().__init__(bullet_client, gravity, timestep, frame_skip)

        self.multiplayer = False
        self.sceneLoaded = 0
        self.objects_of_interest = []  # type: List[str]

    def episode_restart(self, bullet_client: pybullet):
        self._p = bullet_client
        Scene.episode_restart(self, bullet_client)
        if self.sceneLoaded == 0:
            self.sceneLoaded = 1

            # Load the table
            filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "table",
                                    "table.urdf")
            self._p.loadURDF(filename, [1, 0, 0], [0, 0, 90, 90])
            # Load the plane
            filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "plane",
                                    "plane.urdf")
            self._p.loadURDF(filename)

            # Load the cube
            filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "cubes",
                                    "cube_target_no_collision.urdf")
            self._p.loadURDF(filename, [1, -0.3, 0.75])

            # Load the cube
            filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "cubes",
                                    "cube_small.urdf")
            self._p.loadURDF(filename, [1, 0.3, 0.65])


class PickKnifeAndCutScene(Scene):
    """
    The goal of this scene is to set up a scene for picking up a knife, and cutting a sphere or a square

    """

    def __init__(self, bullet_client, gravity, timestep, frame_skip):
        super().__init__(bullet_client, gravity, timestep, frame_skip)

        self.multiplayer = False
        self.sceneLoaded = 0
        self.scene_objects = []  # type: List[SceneObject]

    def episode_restart(self, bullet_client: pybullet):
        self._p = bullet_client
        Scene.episode_restart(self, bullet_client)

        """ If the scene isn't loaded, then load the models """
        if self.sceneLoaded <= 0:
            self.sceneLoaded = 1

            filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "table",
                                    "table.urdf")
            self._p.loadURDF(filename, [1, 0, 0], [0, 0, 90, 90])
            # Load the plane
            filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "plane",
                                    "plane.urdf")
            self._p.loadURDF(filename)

            filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "knives",
                                    "knife.urdf")
            self.scene_objects.append(SlicingSceneObject(bullet_client, filename, [0.70, 0.28, 0.9],
                                      self._p.getQuaternionFromEuler([np.deg2rad(90), 0, np.deg2rad(-90)]),
                                      flags=pybullet.URDF_USE_MATERIAL_COLORS_FROM_MTL |
                                      pybullet.URDF_USE_MATERIAL_TRANSPARANCY_FROM_MTL, slicing_parts=['blade']))

            self.scene_objects.append(
                SlicingSceneObject(bullet_client, filename, [0.85, -0.29, 0.8],
                                   self._p.getQuaternionFromEuler([np.deg2rad(90), 0, 0]),
                            flags=pybullet.URDF_USE_MATERIAL_COLORS_FROM_MTL |
                                  pybullet.URDF_USE_MATERIAL_TRANSPARANCY_FROM_MTL, slicing_parts=['blade']))

            self.scene_objects.append(
                SlicingSceneObject(bullet_client, filename, [0.90, -0.24, 0.9],
                                   self._p.getQuaternionFromEuler([np.deg2rad(90), 0, np.deg2rad(90)]),
                            flags=pybullet.URDF_USE_MATERIAL_COLORS_FROM_MTL |
                                  pybullet.URDF_USE_MATERIAL_TRANSPARANCY_FROM_MTL, slicing_parts=['blade']))

    def dynamic_object_load(self, bullet_client: pybullet):
        """

            As a note, the remove order does not matter, the reload does matter.
            Also, you cannot currently have non-removable objects loaded after removable objects.

        :param bullet_client:
        :return:
        """
        self._dynamic_object_clear()

        if self.sceneLoaded == 1:
            self.sceneLoaded = 2

            # # Load the cube
            # filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "cubes",
            #                         "cube_target_no_collision.urdf")
            # self.scene_objects.append(SceneObject(bullet_client, filename, [0.8, -0.4, 0.70]))
            # # #
            filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "cubes",
                                    "cube_concave.urdf")
            self.scene_objects.append(SlicableSceneObject(bullet_client, filename, [0.8, 0.3, 0.70], removable=True))

            filename = os.path.join(os.path.dirname(__file__), "..", "assets", "things", "cubes",
                                    "cube_concave.urdf")
            self.scene_objects.append(SlicableSceneObject(bullet_client, filename, [0.82, -0.22, 0.70], removable=True))

        # Checks if any non-removable object are being loaded after removable objects.
        if any(map(operator.not_, [__.removable for __ in self.scene_objects[
                                                          [_.removable for _ in self.scene_objects].index(True):]])):
            raise Exception('You have an object that is not removable being loaded after removable objects.'
                            ' For now, you need to load non-removable objects before removable ones. This is due to'
                            ' bullet3 currently overriding removable objects the later loaded non-removable objects.'
                            ' Basically... put non-removable objects first.')

        # Load scene objects that require interaction
        for scene_object in self.scene_objects:
            scene_object.reload()

    def calc_state(self):
        """
        We want to update the states of the objects of interest during manipulation.
        The main interest is the position of each of the objects of interest so we can
        easily build a reward system around them.

        We also want to be able to add advanced object behaviors such as breaking into smaller
        pieces.

        :return:
        """

        """ Handle the knife blade collision """
        for scene_object in list(reversed([_ for _ in self.scene_objects if not _.removed])):
            scene_object.calc_state(self)

        return 0

    def _dynamic_object_clear(self):
        """
        Some objects might be split into smaller objects or duplicated.
        The original state will most likely not have this, so calling this method is
        important for state restoration.

        As a note, the remove order does not matter, the reload does matter.
        Also, you cannot currently have non-removable objects loaded after removable objects.

        :return:
        """
        for scene_object in reversed(sorted(self.scene_objects, key=lambda x: x.bodyIndex)):
            if scene_object.removable and not scene_object.removed:
                # So I think it doesnt like orphans
                self._p.removeBody(scene_object.bodyIndex)
                scene_object.removed = True
                if not scene_object.reloadable:
                    self.scene_objects.remove(scene_object)
