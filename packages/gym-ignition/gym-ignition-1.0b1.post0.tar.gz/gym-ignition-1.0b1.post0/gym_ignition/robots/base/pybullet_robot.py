# Copyright (C) 2019 Istituto Italiano di Tecnologia (IIT). All rights reserved.
# This software may be modified and distributed under the terms of the
# GNU Lesser General Public License v2.1 or any later version.

import os
import pybullet
import numpy as np
from gym_ignition.base import robot
from gym_ignition.utils import logger, resource_finder
from typing import List, Tuple, Dict, Union, NamedTuple
from gym_ignition.base.robot.robot_joints import JointControlMode


class JointControlInfo(NamedTuple):
    mode: JointControlMode
    PID: robot.PID = None


JointControlMode2PyBullet = {
    JointControlMode.POSITION: pybullet.PD_CONTROL,
    JointControlMode.POSITION_INTERPOLATED: None,
    JointControlMode.VELOCITY: pybullet.PD_CONTROL,
    JointControlMode.TORQUE: pybullet.TORQUE_CONTROL,
}


class ContactPyBullet(NamedTuple):
    contactFlag: int
    bodyUniqueIdA: int
    bodyUniqueIdB: int
    linkIndexA: int
    linkIndexB: int
    positionOnA: List[float]
    positionOnB: List[float]
    contactNormalOnB: List[float]
    contactDistance: float
    normalForce: float
    lateralFriction1: float
    lateralFrictionDir1: List[float]
    lateralFriction2: float
    lateralFrictionDir2: List[float]


class JointInfoPyBullet(NamedTuple):
    jointIndex: int
    jointName: bytes
    jointType: int
    qIndex: int
    uIndex: int
    flags: int
    jointDamping: float
    jointFriction: float
    jointLowerLimit: float
    jointUpperLimit: float
    jointMaxForce: float
    jointMaxVelocity: float
    linkName: bytes
    jointAxis: List
    parentFramePos: List
    parentFrameOrn: List
    parentIndex: int


class PyBulletRobot(robot.robot_abc.RobotABC,
                    robot.robot_joints.RobotJoints,
                    robot.robot_contacts.RobotContacts,
                    robot.robot_baseframe.RobotBaseFrame):
    """
    A "class"`Robot` implementation for the PyBullet simulator.

    Args:
        p: An instance of the pybullet simulator.
        model_file: The file (URDF, SDF) containing the robot model.
        plane_id: the pybullet ID associated with the plane model. It is used to
            compute contacts between the robot and the plane.
    """

    def __init__(self,
                 p: pybullet,
                 model_file: str,
                 plane_id: int = None,
                 keep_fixed_joints: bool = False) -> None:

        self._pybullet = p
        self._plane_id = plane_id
        self._keep_fixed_joints = keep_fixed_joints

        # Find the model file
        model_abs_path = resource_finder.find_resource(model_file)

        # Initialize the parent classes
        super().__init__()
        self.model_file = model_abs_path

        # Load the model
        self._robot_id = self._load_model(self.model_file)
        assert self._robot_id is not None, "Failed to load the robot model"

        # Other private attributes
        self._links_name2index_dict = None
        self._joints_name2index_dict = None

        # TODO
        self._base_frame = None
        self._base_constraint = None
        self._initial_joint_positions = None

        # Create a map from the joint name to its control info
        self._jointname2jointcontrolinfo = dict()

        # Initialize all the joints in POSITION mode
        for name in self.joint_names():
            self._jointname2jointcontrolinfo[name] = JointControlInfo(
                mode=JointControlMode.POSITION)
            ok_mode = self.set_joint_control_mode(name, JointControlMode.POSITION)
            assert ok_mode, \
                "Failed to initialize the control mode of joint '{}'".format(name)

    # ==============================
    # PRIVATE METHODS AND PROPERTIES
    # ==============================

    def delete_simulated_robot(self):
        # Remove the robot from the simulation
        self._pybullet.removeBody(self._robot_id)

    @property
    def _joints_name2index(self) -> Dict[str, int]:
        if self._joints_name2index_dict is not None:
            return self._joints_name2index_dict

        self._joints_name2index_dict = dict()
        joints_info = self._get_joints_info()

        for _, info in joints_info.items():
            joint_idx = info.jointIndex
            joint_name = info.jointName.decode()
            self._joints_name2index_dict[joint_name] = joint_idx

        return self._joints_name2index_dict

    @property
    def _links_name2index(self) -> Dict[str, int]:
        if self._links_name2index_dict is not None:
            return self._links_name2index_dict

        self._links_name2index_dict = dict()

        for _, info in self._get_joints_info().items():
            self._links_name2index_dict[info.linkName.decode()] = info.jointIndex

        return self._links_name2index_dict

    def _load_model(self, filename: str, **kwargs) -> int:
        # Get the file extension
        extension = os.path.splitext(filename)[1][1:]

        if extension == "sdf":
            model_id = self._pybullet.loadSDF(filename, **kwargs)[0]
        else:
            model_id = self._pybullet.loadURDF(
                filename,
                flags=pybullet.URDF_USE_INERTIA_FROM_FILE,
                **kwargs)

        return model_id

    def _get_joints_info(self) -> Dict[str, JointInfoPyBullet]:
        joints_info = {}

        for j in range(self._pybullet.getNumJoints(self._robot_id)):
            # Get the joint info from pybullet
            joint_info_pybullet = self._pybullet.getJointInfo(self._robot_id, j)

            # Store it in a namedtuple
            joint_info = JointInfoPyBullet._make(joint_info_pybullet)

            # Add the dict entry
            joints_info[joint_info.jointName.decode()] = joint_info

        return joints_info

    def _get_contact_info(self) -> List[ContactPyBullet]:
        # Get the all contact points in the simulation
        pybullet_contacts = self._pybullet.getContactPoints()

        # List containing only the contacts that involve the robot model
        contacts = []

        # Extract only the robot contacts
        for pybullet_contact in pybullet_contacts:
            contact = ContactPyBullet._make(pybullet_contact)
            contacts.append(contact)

        return contacts

    # =====================
    # robot.Robot INTERFACE
    # =====================

    def name(self) -> str:
        # TODO
        pass

    def valid(self) -> bool:
        try:
            # TODO: improve the check
            self._pybullet.getBasePositionAndOrientation(self._robot_id)
            return True
        except:
            return False

    # ==================================
    # robot_joints.RobotJoints INTERFACE
    # ==================================

    def dofs(self) -> int:
        dofs = len(self.joint_names())

        if self._keep_fixed_joints:
            assert dofs == self._pybullet.getNumJoints(self._robot_id), \
                "Number of DoFs does not match with the simulated model"

        return dofs

    def joint_names(self) -> List[str]:
        joints_names = []

        # Get Joint names
        for _, info in self._get_joints_info().items():
            if not self._keep_fixed_joints and info.jointType == pybullet.JOINT_FIXED:
                continue

            # Strings are byte-encoded. They have to be decoded with UTF-8 (default).
            joints_names.append(info.jointName.decode())

        return joints_names

    def joint_type(self, joint_name: str) -> robot.robot_joints.JointType:
        joint_info = self._get_joints_info()[joint_name]
        joint_type_pybullet = joint_info.jointType

        if joint_type_pybullet == pybullet.JOINT_FIXED:
            return robot.robot_joints.JointType.FIXED
        elif joint_type_pybullet == pybullet.JOINT_REVOLUTE:
            return robot.robot_joints.JointType.REVOLUTE
        else:
            raise Exception(
                "Joint type '{}' not yet supported".format(joint_type_pybullet))

    def joint_control_mode(self, joint_name: str) -> JointControlMode:
        return self._jointname2jointcontrolinfo[joint_name].mode

    def set_joint_control_mode(self, joint_name: str, mode: JointControlMode) -> bool:
        # Store the control mode and initialize the PID
        if mode in {JointControlMode.TORQUE}:
            pid = None
            self._jointname2jointcontrolinfo[joint_name] = JointControlInfo(mode=mode)
        elif mode in {JointControlMode.POSITION, JointControlMode.VELOCITY}:
            # Initialize a default PID
            pid = robot.PID(p=1, i=0, d=0)
            self._jointname2jointcontrolinfo[joint_name] = JointControlInfo(
                mode=mode, PID=pid)
        elif mode == JointControlMode.POSITION_INTERPOLATED:
            raise Exception("Control mode POSITION_INTERPOLATED is not supported")
        else:
            raise Exception("Control mode '{}' not recognized".format(mode))

        mode_pybullet = JointControlMode2PyBullet[mode]
        joint_idx_pybullet = self._joints_name2index[joint_name]

        # Disable the default joint motorization setting a 0 maximum force
        if mode == JointControlMode.TORQUE:
            # Disable the PID if was configured
            self._pybullet.setJointMotorControl2(
                bodyIndex=self._robot_id,
                jointIndex=joint_idx_pybullet,
                controlMode=pybullet.PD_CONTROL,
                positionGain=0,
                velocityGain=0)
            # Put the motor in IDLE for torque control
            self._pybullet.setJointMotorControl2(
                bodyIndex=self._robot_id,
                jointIndex=joint_idx_pybullet,
                controlMode=pybullet.VELOCITY_CONTROL,
                force=0)

        # Change the control mode of the joint
        if mode == JointControlMode.POSITION:
            self._pybullet.setJointMotorControl2(
                bodyIndex=self._robot_id,
                jointIndex=joint_idx_pybullet,
                controlMode=mode_pybullet,
                positionGain=pid.p,
                velocityGain=pid.d)
        elif mode == JointControlMode.VELOCITY:
            # TODO: verify that setting the gains in this way processes the reference
            #  correctly.
            self._pybullet.setJointMotorControl2(
                bodyIndex=self._robot_id,
                jointIndex=joint_idx_pybullet,
                controlMode=mode_pybullet,
                positionGain=pid.i,
                velocityGain=pid.p)

        return True

    def initial_positions(self) -> np.ndarray:
        return np.zeros(self.dofs())

    def set_initial_positions(self, positions: np.ndarray) -> bool:
        if positions.size != self.dofs():
            return False

        self._initial_joint_positions = positions
        return True

    def joint_position(self, joint_name: str) -> float:
        joint_idx = self._joints_name2index[joint_name]
        return self._pybullet.getJointState(self._robot_id, joint_idx)[0]

    def joint_velocity(self, joint_name: str) -> float:
        joint_idx = self._joints_name2index[joint_name]
        return self._pybullet.getJointState(self._robot_id, joint_idx)[1]

    def joint_positions(self) -> List[float]:
        joint_states = self._pybullet.getJointStates(self._robot_id, range(self.dofs()))
        joint_positions = [state[0] for state in joint_states]
        return joint_positions

    def joint_velocities(self) -> List[float]:
        joint_states = self._pybullet.getJointStates(self._robot_id, range(self.dofs()))
        joint_velocities = [state[1] for state in joint_states]
        return joint_velocities

    def joint_pid(self, joint_name: str) -> Union[robot.PID, None]:
        return self._jointname2jointcontrolinfo[joint_name].PID

    def dt(self) -> float:
        raise NotImplementedError

    def set_dt(self, step_size: float) -> bool:
        raise NotImplementedError

    def set_joint_force(self, joint_name: str, force: float, clip: bool = False) -> bool:

        if self._jointname2jointcontrolinfo[joint_name].mode != JointControlMode.TORQUE:
            raise Exception("Joint '{}' is not controlled in TORQUE".format(joint_name))

        joint_idx_pybullet = self._joints_name2index[joint_name]
        mode_pybullet = JointControlMode2PyBullet[JointControlMode.TORQUE]

        # Clip the force if specified
        if clip:
            fmin, fmax = self.joint_force_limit(joint_name)
            force = fmin if force < fmin else fmax if force > fmax else force

        # Set the joint force
        self._pybullet.setJointMotorControl2(bodyUniqueId=self._robot_id,
                                             jointIndex=joint_idx_pybullet,
                                             controlMode=mode_pybullet,
                                             force=force)

        return True

    def set_joint_position(self, joint_name: str, position: float) -> bool:

        if self._jointname2jointcontrolinfo[joint_name].mode != JointControlMode.POSITION:
            raise Exception("Joint '{}' is not controlled in POSITION".format(joint_name))

        pid = self._jointname2jointcontrolinfo[joint_name].PID

        joint_idx_pybullet = self._joints_name2index[joint_name]
        mode_pybullet = JointControlMode2PyBullet[JointControlMode.POSITION]

        # Change the control mode of the joint
        self._pybullet.setJointMotorControl2(
            bodyUniqueId=self._robot_id,
            jointIndex=joint_idx_pybullet,
            controlMode=mode_pybullet,
            targetVelocity=position,
            positionGain=pid.p,
            velocityGain=pid.d)

        return True

    def set_joint_velocity(self, joint_name: str, velocity: float) -> bool:

        if self._jointname2jointcontrolinfo[joint_name].mode not in \
                {JointControlMode.POSITION, JointControlMode.VELOCITY}:
            raise Exception("Joint '{}' is not controlled in VELOCITY".format(joint_name))

        pid = self._jointname2jointcontrolinfo[joint_name].PID

        joint_idx_pybullet = self._joints_name2index[joint_name]
        mode_pybullet = JointControlMode2PyBullet[JointControlMode.POSITION]

        # Change the control mode of the joint
        self._pybullet.setJointMotorControl2(
            bodyUniqueId=self._robot_id,
            jointIndex=joint_idx_pybullet,
            controlMode=mode_pybullet,
            targetVelocity=velocity,
            positionGain=pid.p,
            velocityGain=pid.d)

        return True

    def set_joint_interpolated_position(self, joint_name: str, position: float):
        return NotImplementedError

    def set_joint_pid(self, joint_name: str, pid: robot.PID) -> bool:

        mode = self._jointname2jointcontrolinfo[joint_name].mode
        assert mode != JointControlMode.POSITION_INTERPOLATED

        if mode == JointControlMode.TORQUE:
            logger.warn(
                f"Joint '{joint_name}' is torque controlled. "
                f"Setting the PID has no effect")
            return False

        if mode == JointControlMode.POSITION and pid.i != 0.0:
            raise Exception("Integral term not supported for POSITION mode")
        elif mode == JointControlMode.VELOCITY and pid.d != 0.0:
            raise Exception("Derivative term not supported for VELOCITY mode")

        # Store the new PID
        self._jointname2jointcontrolinfo[joint_name]._replace(PID=pid)

        # Update the PIDs setting again the control mode
        ok_mode = self.set_joint_control_mode(joint_name, mode)
        assert ok_mode, "Failed to set the control mode"

        return True

    def reset_joint(self,
                    joint_name: str,
                    position: float = None,
                    velocity: float = None) -> bool:

        joint_idx_pybullet = self._joints_name2index[joint_name]
        self._pybullet.resetJointState(bodyUniqueId=self._robot_id,
                                       jointIndex=joint_idx_pybullet,
                                       targetValue=position,
                                       targetVelocity=velocity)

        return True

    def update(self, current_time: float) -> bool:
        raise NotImplementedError

    def joint_position_limits(self, joint_name: str) -> Tuple[float, float]:
        # Get Joint info
        joint_info = self._get_joints_info()[joint_name]

        return joint_info.jointLowerLimit, joint_info.jointUpperLimit

    def joint_force_limit(self, joint_name: str) -> float:
        # Get Joint info
        joint_info = self._get_joints_info()[joint_name]

        return joint_info.jointMaxForce

    # =====================================
    # robot_joints.RobotBaseFrame INTERFACE
    # =====================================

    def set_base_frame(self, frame_name: str) -> bool:
        # TODO: check that it exists
        self._base_frame = frame_name
        return True

    def base_frame(self) -> str:
        return self._base_frame

    def base_pose(self) -> Tuple[np.ndarray, np.ndarray]:
        # Get the values
        pos, quat = self._pybullet.getBasePositionAndOrientation(self._robot_id)

        # Convert tuples into lists
        pos = np.array(pos)
        quat = np.array(quat)

        # PyBullet returns xyzw, the interface instead returns wxyz
        quat = np.roll(quat, 1)

        return pos, quat

    def base_velocity(self) -> Tuple[np.ndarray, np.ndarray]:
        # TODO: double check
        # Get the values
        lin, ang = self._pybullet.getBaseVelocity(self._robot_id)

        # Convert tuples into lists
        lin = np.array(lin)
        ang = np.array(ang)

        return lin, ang

    def reset_base_pose(self,
                        position: np.ndarray,
                        orientation: np.ndarray,
                        floating: bool = False) -> bool:

        assert position.size == 3, "Position should be a list with 3 elements"
        assert orientation.size == 4, "Orientation should be a list with 4 elements"

        # PyBullet wants xyzw, but the function argument quaternion is wxyz
        orientation = np.roll(orientation, -1)

        if not floating:
            # Set a constraint between base_link and world
            self._base_constraint = self._pybullet.createConstraint(
                self._robot_id, -1, -1, -1, self._pybullet.JOINT_FIXED,
                [0, 0, 0], [0, 0, 0], position, orientation)
        else:
            self._pybullet.resetBasePositionAndOrientation(
                self._robot_id, position, orientation)

        return True

    def reset_base_velocity(self,
                            linear_velocity: np.ndarray,
                            angular_velocity: np.ndarray) -> bool:
        raise NotImplementedError

    def base_wrench(self) -> np.ndarray:
        assert self._base_constraint is not None, "The robot is not fixed base"
        constraint_wrench = self._pybullet.getConstraintState(self._base_constraint)
        # print("Constraint State =", constraint_wrench)
        return np.array(constraint_wrench)

    # =============
    # RobotContacts
    # =============

    def links_in_contact(self) -> List[str]:
        # Get the all contact points in the simulation
        all_contacts = self._get_contact_info()

        # List containing only the contacts that involve the robot model
        contacts_robot = []

        # Extract only the robot contacts
        for contact in all_contacts:
            if contact.bodyUniqueIdA == self._robot_id or \
                    contact.bodyUniqueIdB == self._robot_id:
                contacts_robot.append(contact)

        # List containing the names of the link with active contacts
        links_in_contact = []

        for contact in contacts_robot:
            # Link of the link in contact
            link_idx_in_contact = None

            # Get the index of the link in contact.
            # The robot body could be either body A or body B.
            if contact.bodyUniqueIdA == self._robot_id:
                link_idx_in_contact = contact.linkIndexA
            elif contact.bodyUniqueIdB == self._robot_id:
                link_idx_in_contact = contact.linkIndexB

            # Get the link name from the index and add it to the returned list
            for link_name, link_idx in self._links_name2index.items():
                if link_idx == link_idx_in_contact:
                    if link_name not in links_in_contact:

                        # Do not consider the contact if the wrench is (almost) zero
                        wrench = self.total_contact_wrench_on_link(link_name)

                        if np.linalg.norm(wrench) < 1e-6:
                            continue

                        # Append the link name to the list of link in contact
                        links_in_contact.append(link_name)

        return links_in_contact

    def contact_data(self, contact_link_name: str):  # TODO
        raise NotImplementedError

    def total_contact_wrench_on_link(self, contact_link_name: str) -> np.ndarray:
        # TODO: finish the implementation of this method

        # Get the all contact points in the simulation
        all_contacts = self._get_contact_info()

        # List containing only the contacts that involve the robot model
        contacts_robot = []

        # Extract only the robot contacts
        for contact in all_contacts:
            if contact.bodyUniqueIdA == self._robot_id or contact.bodyUniqueIdB == \
                    self._robot_id:
                contacts_robot.append(contact)

        contact_link_idx = self._links_name2index[contact_link_name]

        # List containing only the contacts that involve the link
        contacts_link = []

        for contact in contacts_robot:
            if contact.bodyUniqueIdA == self._robot_id and \
                    contact.linkIndexA == contact_link_idx or \
               contact.bodyUniqueIdB == self._robot_id and \
                    contact.linkIndexB == contact_link_idx:
                contacts_link.append(contact)

        total_force = np.zeros(3)

        for contact in contacts_link:
            # TODO: handle that id could be either body a or b
            force_1 = contact.normalForce * np.array(contact.contactNormalOnB)
            force_2 = contact.lateralFriction1 * np.array(contact.lateralFrictionDir1)
            force_3 = contact.lateralFriction2 * np.array(contact.lateralFrictionDir2)

            # TODO: compose the force transforming it in wrench applied to the link frame
            total_force += force_1 + force_2 + force_3

        return total_force
