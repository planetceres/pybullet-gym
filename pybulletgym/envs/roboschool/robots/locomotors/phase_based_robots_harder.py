from pybulletgym.envs.roboschool.robots.locomotors.walker_base import WalkerBase
from pybulletgym.envs.roboschool.robots.robot_bases import MJCFBasedRobot
import numpy as np
from pybulletgym.envs import gym_utils as ObjectHelper

class AntPhaseHarder(WalkerBase, MJCFBasedRobot):
    foot_list = ['front_left_foot', 'front_right_foot', 'left_back_foot', 'right_back_foot']

    def __init__(self):
        WalkerBase.__init__(self, power=2.5)
        MJCFBasedRobot.__init__(self, "ant.xml", "torso", action_dim=8+1, obs_dim=28+1)
        self.aggressive_cube = None
        self.frame = 0

    def robot_specific_reset(self, bullet_client):
        WalkerBase.robot_specific_reset(self, bullet_client)
        self.frame = 0
        if self.aggressive_cube:
            self._p.resetBasePositionAndOrientation(self.aggressive_cube.bodies[0], [-1.5, 0, 0.05], [0, 0, 0, 1])
        else:
            self.aggressive_cube = ObjectHelper.get_cube(self._p, -1.5,0,0.05)


    def alive_bonus(self, z, pitch):
        if self.frame % 30 == 0 and self.frame > 10:
            target_xyz = np.array(self.body_xyz)
            robot_speed = np.array(self.robot_body.speed())
            angle = self.np_random.uniform(low=-3.14, high=3.14)
            from_dist = 4.0
            attack_speed = self.np_random.uniform(low=20.0,
                                                  high=30.0)  # speed 20..30 (* mass in cube.urdf = impulse)
            time_to_travel = from_dist / attack_speed
            target_xyz += robot_speed * time_to_travel  # predict future position at the moment the cube hits the robot
            position = [target_xyz[0] + from_dist * np.cos(angle),
                        target_xyz[1] + from_dist * np.sin(angle),
                        target_xyz[2] + 1.0]
            attack_speed_vector = target_xyz - np.array(position)
            attack_speed_vector *= attack_speed / np.linalg.norm(attack_speed_vector)
            attack_speed_vector += self.np_random.uniform(low=-1.0, high=+1.0, size=(3,))
            self.aggressive_cube.reset_position(position)
            self.aggressive_cube.reset_velocity(linearVelocity=attack_speed_vector)
        self.frame += 1

        return +1 if z > 0.26 else -1  # 0.25 is central sphere rad, die if it scrapes the ground


class HalfCheetahPhaseHarder(WalkerBase, MJCFBasedRobot):
    foot_list = ["ffoot", "fshin", "fthigh",  "bfoot", "bshin", "bthigh"]  # track these contacts with ground

    def __init__(self):
        WalkerBase.__init__(self, power=0.90)
        MJCFBasedRobot.__init__(self, "half_cheetah.xml", "torso", action_dim=6+1, obs_dim=26+1)
        self.aggressive_cube = None
        self.frame = 0

    def alive_bonus(self, z, pitch):
        if self.frame % 30 == 0 and self.frame > 10:
            target_xyz = np.array(self.body_xyz)
            robot_speed = np.array(self.robot_body.speed())
            angle = self.np_random.uniform(low=-3.14, high=3.14)
            from_dist = 4.0
            attack_speed = self.np_random.uniform(low=20.0,
                                                  high=30.0)  # speed 20..30 (* mass in cube.urdf = impulse)
            time_to_travel = from_dist / attack_speed
            target_xyz += robot_speed * time_to_travel  # predict future position at the moment the cube hits the robot
            position = [target_xyz[0] + from_dist * np.cos(angle),
                        target_xyz[1] + from_dist * np.sin(angle),
                        target_xyz[2] + 1.0]
            attack_speed_vector = target_xyz - np.array(position)
            attack_speed_vector *= attack_speed / np.linalg.norm(attack_speed_vector)
            attack_speed_vector += self.np_random.uniform(low=-1.0, high=+1.0, size=(3,))
            self.aggressive_cube.reset_position(position)
            self.aggressive_cube.reset_velocity(linearVelocity=attack_speed_vector)
        self.frame += 1

        # Use contact other than feet to terminate episode: due to a lot of strange walks using knees
        return +1 if np.abs(pitch) < 1.0 and not self.feet_contact[1] and not self.feet_contact[2] and not self.feet_contact[4] and not self.feet_contact[5] else -1

    def robot_specific_reset(self, bullet_client):
        WalkerBase.robot_specific_reset(self, bullet_client)
        self.jdict["bthigh"].power_coef = 120.0
        self.jdict["bshin"].power_coef  = 90.0
        self.jdict["bfoot"].power_coef  = 60.0
        self.jdict["fthigh"].power_coef = 140.0
        self.jdict["fshin"].power_coef  = 60.0
        self.jdict["ffoot"].power_coef  = 30.0

        self.frame = 0
        if self.aggressive_cube:
            self._p.resetBasePositionAndOrientation(self.aggressive_cube.bodies[0], [-1.5, 0, 0.05], [0, 0, 0, 1])
        else:
            self.aggressive_cube = ObjectHelper.get_cube(self._p, -1.5, 0, 0.05)


class HopperPhaseHarder(WalkerBase, MJCFBasedRobot):
    foot_list = ["foot"]

    def __init__(self):
        WalkerBase.__init__(self, power=0.75)
        MJCFBasedRobot.__init__(self, "hopper.xml", "torso", action_dim=3+1, obs_dim=15+1)
        self.aggressive_cube = None
        self.frame = 0

    def robot_specific_reset(self, bullet_client):
        WalkerBase.robot_specific_reset(self, bullet_client)
        self.frame = 0
        if self.aggressive_cube:
            self._p.resetBasePositionAndOrientation(self.aggressive_cube.bodies[0], [-1.5, 0, 0.05], [0, 0, 0, 1])
        else:
            self.aggressive_cube = ObjectHelper.get_cube(self._p, -1.5,0,0.05)

    def alive_bonus(self, z, pitch):
        if self.frame % 30 == 0 and self.frame > 10:
            target_xyz = np.array(self.body_xyz)
            robot_speed = np.array(self.robot_body.speed())
            angle = self.np_random.uniform(low=-3.14, high=3.14)
            from_dist = 4.0
            attack_speed = self.np_random.uniform(low=20.0,
                                                  high=30.0)  # speed 20..30 (* mass in cube.urdf = impulse)
            time_to_travel = from_dist / attack_speed
            target_xyz += robot_speed * time_to_travel  # predict future position at the moment the cube hits the robot
            position = [target_xyz[0] + from_dist * np.cos(angle),
                        target_xyz[1] + from_dist * np.sin(angle),
                        target_xyz[2] + 1.0]
            attack_speed_vector = target_xyz - np.array(position)
            attack_speed_vector *= attack_speed / np.linalg.norm(attack_speed_vector)
            attack_speed_vector += self.np_random.uniform(low=-1.0, high=+1.0, size=(3,))
            self.aggressive_cube.reset_position(position)
            self.aggressive_cube.reset_velocity(linearVelocity=attack_speed_vector)
        self.frame += 1

        return +1 if z > 0.8 and abs(pitch) < 1.0 else -1


class HumanoidPhaseHarder(WalkerBase, MJCFBasedRobot):
    self_collision = True
    foot_list = ["right_foot", "left_foot"]  # "left_hand", "right_hand"

    def __init__(self, random_yaw = False, random_lean=False):
        WalkerBase.__init__(self, power=0.41)
        MJCFBasedRobot.__init__(self, 'humanoid_symmetric.xml', 'torso', action_dim=17+1, obs_dim=44+1)
        # 17 joints, 4 of them important for walking (hip, knee), others may as well be turned off, 17/4 = 4.25
        self.random_yaw = random_yaw
        self.random_lean = random_lean
        self.aggressive_cube = None
        self.frame = 0

    def robot_specific_reset(self, bullet_client):
        WalkerBase.robot_specific_reset(self, bullet_client)
        self.motor_names  = ["abdomen_z", "abdomen_y", "abdomen_x"]
        self.motor_power  = [100, 100, 100]
        self.motor_names += ["right_hip_x", "right_hip_z", "right_hip_y", "right_knee"]
        self.motor_power += [100, 100, 300, 200]
        self.motor_names += ["left_hip_x", "left_hip_z", "left_hip_y", "left_knee"]
        self.motor_power += [100, 100, 300, 200]
        self.motor_names += ["right_shoulder1", "right_shoulder2", "right_elbow"]
        self.motor_power += [75, 75, 75]
        self.motor_names += ["left_shoulder1", "left_shoulder2", "left_elbow"]
        self.motor_power += [75, 75, 75]
        self.motors = [self.jdict[n] for n in self.motor_names]
        if self.random_yaw:
            position = [0,0,0]
            orientation = [0,0,0]
            yaw = self.np_random.uniform(low=-3.14, high=3.14)
            if self.random_lean and self.np_random.randint(2) == 0:
                if self.np_random.randint(2) == 0:
                    pitch = np.pi/2
                    position = [0, 0, 0.45]
                else:
                    pitch = np.pi*3/2
                    position = [0, 0, 0.25]
                roll = 0
                orientation = [roll, pitch, yaw]
            else:
                position = [0, 0, 1.4]
                orientation = [0, 0, yaw]  # just face random direction, but stay straight otherwise
            self.robot_body.reset_position(position)
            self.robot_body.reset_orientation(p.getQuaternionFromEuler(orientation))
        self.initial_z = 0.8

        self.frame = 0
        if self.aggressive_cube:
            self._p.resetBasePositionAndOrientation(self.aggressive_cube.bodies[0], [-1.5, 0, 0.05], [0, 0, 0, 1])
        else:
            self.aggressive_cube = ObjectHelper.get_cube(self._p, -1.5,0,0.05)


    def apply_action(self, a):
        assert(np.isfinite(a).all())
        force_gain = 1
        for i, m, power in zip(range(17), self.motors, self.motor_power):
            m.set_motor_torque(float(force_gain * power * self.power * np.clip(a[i], -1, +1)))

    def alive_bonus(self, z, pitch):
        if self.frame % 30 == 0 and self.frame > 10:
            target_xyz = np.array(self.body_xyz)
            robot_speed = np.array(self.robot_body.speed())
            angle = self.np_random.uniform(low=-3.14, high=3.14)
            from_dist = 4.0
            attack_speed = self.np_random.uniform(low=20.0,
                                                  high=30.0)  # speed 20..30 (* mass in cube.urdf = impulse)
            time_to_travel = from_dist / attack_speed
            target_xyz += robot_speed * time_to_travel  # predict future position at the moment the cube hits the robot
            position = [target_xyz[0] + from_dist * np.cos(angle),
                        target_xyz[1] + from_dist * np.sin(angle),
                        target_xyz[2] + 1.0]
            attack_speed_vector = target_xyz - np.array(position)
            attack_speed_vector *= attack_speed / np.linalg.norm(attack_speed_vector)
            attack_speed_vector += self.np_random.uniform(low=-1.0, high=+1.0, size=(3,))
            self.aggressive_cube.reset_position(position)
            self.aggressive_cube.reset_velocity(linearVelocity=attack_speed_vector)
        self.frame += 1

        return +2 if z > 0.78 else -1   # 2 here because 17 joints produce a lot of electricity cost just from policy noise, living must be better than dying


class Walker2DPhaseHarder(WalkerBase, MJCFBasedRobot):
    foot_list = ["foot", "foot_left"]

    def __init__(self):
        WalkerBase.__init__(self, power=0.40)
        MJCFBasedRobot.__init__(self, "walker2d.xml", "torso", action_dim=6+1, obs_dim=22+1)
        self.aggressive_cube = None
        self.frame = 0

    def alive_bonus(self, z, pitch):
        if self.frame % 30 == 0 and self.frame > 10:
            target_xyz = np.array(self.body_xyz)
            robot_speed = np.array(self.robot_body.speed())
            angle = self.np_random.uniform(low=-3.14, high=3.14)
            from_dist = 4.0
            attack_speed = self.np_random.uniform(low=20.0,
                                                  high=30.0)  # speed 20..30 (* mass in cube.urdf = impulse)
            time_to_travel = from_dist / attack_speed
            target_xyz += robot_speed * time_to_travel  # predict future position at the moment the cube hits the robot
            position = [target_xyz[0] + from_dist * np.cos(angle),
                        target_xyz[1] + from_dist * np.sin(angle),
                        target_xyz[2] + 1.0]
            attack_speed_vector = target_xyz - np.array(position)
            attack_speed_vector *= attack_speed / np.linalg.norm(attack_speed_vector)
            attack_speed_vector += self.np_random.uniform(low=-1.0, high=+1.0, size=(3,))
            self.aggressive_cube.reset_position(position)
            self.aggressive_cube.reset_velocity(linearVelocity=attack_speed_vector)
        self.frame += 1
        return +1 if z > 0.8 and abs(pitch) < 1.0 else -1

    def robot_specific_reset(self, bullet_client):
        WalkerBase.robot_specific_reset(self, bullet_client)
        for n in ["foot_joint", "foot_left_joint"]:
            self.jdict[n].power_coef = 30.0

        self.frame = 0
        if self.aggressive_cube:
            self._p.resetBasePositionAndOrientation(self.aggressive_cube.bodies[0], [-1.5, 0, 0.05], [0, 0, 0, 1])
        else:
            self.aggressive_cube = ObjectHelper.get_cube(self._p, -1.5, 0, 0.05)