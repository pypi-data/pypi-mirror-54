/*
 * Copyright (C) 2019 Istituto Italiano di Tecnologia (IIT)
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms of the
 * GNU Lesser General Public License v2.1 or any later version.
 */

#ifndef GYMPP_GAZEBO_IGNITIONROBOT_H
#define GYMPP_GAZEBO_IGNITIONROBOT_H

#include "gympp/Robot.h"

#include <ignition/gazebo/Entity.hh>
#include <ignition/gazebo/EntityComponentManager.hh>
#include <sdf/Element.hh>

#include <functional>
#include <memory>

namespace gympp {
    namespace gazebo {
        class IgnitionRobot;
    } // namespace gazebo
} // namespace gympp

class gympp::gazebo::IgnitionRobot : public gympp::Robot
{
private:
    class Impl;
    std::unique_ptr<Impl, std::function<void(Impl*)>> pImpl;

public:
    IgnitionRobot();
    ~IgnitionRobot() override;

    bool configureECM(const ignition::gazebo::Entity& entity,
                      const std::shared_ptr<const sdf::Element>& sdf,
                      ignition::gazebo::EntityComponentManager& ecm);
    bool valid() const override;

    // ===========
    // GET METHODS
    // ===========

    RobotName name() const override;
    JointNames jointNames() const override;

    double jointPosition(const JointName& jointName) const override;
    double jointVelocity(const JointName& jointName) const override;

    JointPositions jointPositions() const override;
    JointVelocities jointVelocities() const override;

    StepSize dt() const override;
    PID jointPID(const JointName& jointName) const override;

    // ===========
    // SET METHODS
    // ===========

    bool setdt(const StepSize& stepSize) override;

    bool setJointForce(const JointName& jointName, const double jointForce) override;
    bool setJointPositionTarget(const JointName& jointName,
                                const double jointPositionReference) override;
    bool setJointVelocityTarget(const JointName& jointName,
                                const double jointVelocityReference) override;

    bool setJointPosition(const JointName& jointName, const double jointPosition) override;
    bool setJointVelocity(const JointName& jointName, const double jointVelocity) override;

    bool setJointPID(const JointName& jointName, const PID& pid) override;

    bool resetJoint(const JointName& jointName,
                    const double jointPosition = 0,
                    const double jointVelocity = 0) override;

    bool update(const std::chrono::duration<double> time) override;
};

#endif // GYMPP_GAZEBO_IGNITIONROBOT_H
