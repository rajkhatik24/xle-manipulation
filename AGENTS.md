# XLE Manipulation — Agent Guide

## Project Goal

Build a sim-to-real manipulation pipeline for the XLe robot.

Current scope is manipulation only.

Pipeline:

1. Simulate XLe in NVIDIA Isaac Sim.
2. Teleoperate XLe in simulation.
3. Record manipulation demonstrations.
4. Train an imitation-learning policy.
5. Run policy inference in Isaac Sim.
6. Add domain randomization / synthetic data.
7. Transfer the pipeline to the physical XLe robot.

Future scope includes mobile-base navigation and SLAM, but those are NOT
current priorities.

---

## System Architecture

The development machine runs Windows 11 with WSL2.

### Windows

NVIDIA Isaac Sim 6.0.1 is installed natively at:

C:\isaac-sim

Isaac simulation scripts MUST execute using the Windows Isaac Python
environment.

From WSL, use:

./scripts/isaac.sh <script>

Example:

./scripts/isaac.sh xle_sim/load_xle.py

Do not attempt to run Isaac Sim using the normal WSL Python environment.

### WSL

The project is accessed from WSL at:

/mnt/c/projects/xle-manipulation

The WSL Python environment is:

~/.venvs/xle-manipulation

Activate with:

source ~/.venvs/xle-manipulation/bin/activate

WSL is intended for:

- development
- Git
- data processing
- ML training
- dataset inspection
- utilities
- future ROS tooling

---

## Current Robot Asset

The XLe Isaac asset is located at:

assets/xlerobot/xlerobot/xlerobot.usd

It originated from the XLeRobot repository Isaac Sim assets.

The complete asset hierarchy was copied because the main USD references
supporting USD payloads, meshes, physics configuration, and materials.

Do not move individual USD files without checking their references.

---

## Code Organization

Current responsibilities:

### `xle_sim/`

XLe-specific simulation functionality.

- `robot.py` — reusable XLe loading functionality
- `load_xle.py` — standalone XLe loading smoke test
- `controllers/` — future XLe control and IK logic

### `environments/`

Environment/world definitions independent of the robot.

- `scenes.py` — registry and resolution of Isaac environment assets

Environment code should not contain XLe-specific control or loading logic.

### `scripts/`

Executable entry points and launch utilities.

- `isaac.sh` — launch scripts using native Windows Isaac Python from WSL
- `run_scenes.py` — compose an environment with the XLe robot

### `teleop/`

Human input interfaces. Future keyboard and Quest VR implementations belong
here.

### `recording/`

Demonstration recording and replay infrastructure.

### `tasks/`

Task-specific definitions such as pick-and-place.

### `training/`

Model training, configuration, and dataset processing.

### `inference/`

Learned-policy execution.

Avoid duplicating functionality between these modules. Entry-point scripts
should primarily compose reusable modules rather than implement robot,
environment, or controller logic themselves.

---

## Current Status

Working:

- Git repository
- WSL development environment
- WSL -> Windows Isaac launcher
- Isaac SimulationApp launch
- XLe USD loading in Isaac Sim
- Reusable XLe loader in `xle_sim/robot.py`
- Isaac environment registry in `environments/scenes.py`
- Scene runner in `scripts/run_scenes.py`
- XLe successfully composed into the Isaac `simple_room` environment

Standalone XLe test:

    ./scripts/isaac.sh xle_sim/load_xle.py

Scene test:

    ./scripts/isaac.sh scripts/run_scenes.py --scene simple_room

Current known limitation:

- XLe spawn placement inside environments has not been configured yet.
- In `simple_room`, XLe currently appears on/near the table.
- Spawn placement is intentionally deferred and should be implemented as a
  separate change.

---

## Planned Architecture

teleop input
    |
    v
end-effector command
    |
    v
XLE controller / IK
    |
    v
joint targets
    |
    v
Isaac articulation

Teleoperation sources should eventually be interchangeable:

Keyboard ----\
Quest VR ----- > common EE action interface -> XLE controller
Policy -------/

The controller should NOT depend directly on keyboard input.

---

## Observation Interface

Target observation structure:

- external RGB camera
- wrist RGB camera
- joint positions
- joint velocities
- end-effector pose
- gripper state

Additional observations may be added later.

---

## Action Interface

Prefer task-space commands rather than direct keyboard-to-joint mappings.

Target action representation:

[dx, dy, dz, droll, dpitch, dyaw, gripper]

The same action interface should eventually work for:

- keyboard teleoperation
- VR teleoperation
- learned policy inference

---

## Data Collection

Demonstrations should record synchronized:

- RGB observations
- robot state
- end-effector state
- commanded actions
- gripper commands
- timestamps
- episode metadata

Prefer established formats compatible with Isaac Lab / LeRobot / robomimic
where practical instead of creating unnecessary custom dataset formats.

---

## Sim-to-Real Principle

Keep high-level interfaces independent of whether the robot is simulated or
physical.

Desired abstraction:

robot.get_observation()
robot.apply_action(action)

Simulation implementation:

Isaac articulation

Real implementation:

XLe hardware SDK / ROS interface

Training and policy code should depend on the abstraction rather than directly
on Isaac APIs whenever practical.

---

## Development Rules

1. Keep milestones small and testable.
2. Do not introduce ROS unless it solves an actual integration requirement.
3. Do not introduce the mobile base or SLAM during the manipulation milestone.
4. Do not add domain randomization until baseline manipulation works.
5. Do not train a policy until demonstration replay works reliably.
6. Keep teleoperation input separate from robot control.
7. Prefer reusable modules over large standalone scripts.
8. Preserve the Windows Isaac / WSL training separation.
9. Never assume an Isaac API version; this project currently uses Isaac Sim 6.0.1.
10. Test changes in simulation before modifying training infrastructure.

---

## Near-Term Milestones

M1 - Load XLe USD                     DONE
M2 - Inspect articulation/joints
M3 - Command individual joints
M4 - End-effector IK controller
M5 - Keyboard teleoperation
M6 - Basic manipulation scene
M7 - Cameras and observations
M8 - Demonstration recording
M9 - Demonstration replay
M10 - Behavioral cloning baseline
M11 - Policy inference in simulation
M12 - Domain randomization
M13 - Quest VR teleoperation
M14 - Physical XLe integration
M15 - Sim-to-real experiments

Do not skip milestones without a specific reason.
