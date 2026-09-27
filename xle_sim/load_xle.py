from isaacsim import SimulationApp

simulation_app = SimulationApp({
    "headless": False
})

import os
import omni.usd
from pxr import UsdGeom


# Windows path because this script executes inside Windows Isaac Python
XLE_USD = r"C:\projects\xle-manipulation\assets\xlerobot\xlerobot\xlerobot.usd"


def main():
    print("\n==============================")
    print("XLE USD LOAD TEST")
    print("==============================")
    print(f"Loading: {XLE_USD}")

    if not os.path.exists(XLE_USD):
        raise FileNotFoundError(f"XLe USD not found: {XLE_USD}")

    # Create a clean stage
    omni.usd.get_context().new_stage()

    stage = omni.usd.get_context().get_stage()

    # Create a prim that will reference the XLe USD
    robot_prim = stage.DefinePrim("/World/XLeRobot", "Xform")
    robot_prim.GetReferences().AddReference(XLE_USD)

    print("XLe reference added successfully.")

    # Give Isaac a moment to resolve/load USD references
    for _ in range(100):
        simulation_app.update()

    # Print top-level children for debugging
    print("\nStage children:")

    world = stage.GetPrimAtPath("/World")

    for child in world.GetChildren():
        print(f"  {child.GetPath()}")

    print("\nXLe should now be visible in Isaac Sim.")
    print("Close the Isaac window when you're finished inspecting it.\n")

    # Keep application running
    while simulation_app.is_running():
        simulation_app.update()


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
