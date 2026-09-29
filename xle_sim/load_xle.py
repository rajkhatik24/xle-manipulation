from isaacsim import SimulationApp
from xle_sim.robot import load_xle
simulation_app = SimulationApp({
    "headless": False
})

import os
import omni.usd
from pxr import UsdGeom, UsdLux, Gf



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



        # ---------------------------------------------------------
    # Lighting
    # ---------------------------------------------------------

    # Ambient/environment lighting
    dome_light = UsdLux.DomeLight.Define(stage, "/World/DomeLight")
    dome_light.CreateIntensityAttr(1000.0)

    # Directional light for stronger shadows / shape definition
    distant_light = UsdLux.DistantLight.Define(stage, "/World/DistantLight")
    distant_light.CreateIntensityAttr(3000.0)
    distant_light.CreateAngleAttr(0.5)

    # Rotate the directional light
    light_xform = UsdGeom.Xformable(distant_light)
    light_xform.AddRotateXYZOp().Set(Gf.Vec3f(-45.0, 30.0, 0.0))
    # Create a prim that will reference the XLe USD
    robot_prim = load_xle(stage)

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