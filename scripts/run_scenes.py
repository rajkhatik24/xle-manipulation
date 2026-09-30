from isaacsim import SimulationApp
from xle_sim.robot import load_xle
simulation_app = SimulationApp({
    "headless": False
})

import argparse
import omni.usd

from environments.scenes import SCENES, get_scene_path
from environments.props import add_table

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--scene",
        choices=SCENES.keys(),
        default="simple_room",
    )

    args = parser.parse_args()

    scene_path = get_scene_path(args.scene)

    print("\n==============================")
    print("SCENE TEST")
    print("==============================")
    print(f"Scene: {args.scene}")
    print(f"USD:   {scene_path}")

    omni.usd.get_context().open_stage(scene_path)

    # Give the USD time to load.
    for _ in range(100):
        simulation_app.update()
    stage = omni.usd.get_context().get_stage()

    if stage is None:
        raise RuntimeError("Failed to load scene.")

    robot = load_xle(stage)

    print(f"XLe added at: {robot.GetPath()}")

    if args.scene == "grid":
        add_table(stage)
        print("Manipulation table added.")

    # Allow the XLe references to resolve
    for _ in range(100):
        simulation_app.update()
    print("Scene loaded.")

    while simulation_app.is_running():
        simulation_app.update()


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()