import os


XLE_USD = r"C:\projects\xle-manipulation\assets\xlerobot\xlerobot\xlerobot.usd"


def load_xle(stage, prim_path="/World/XLeRobot"):
    """
    Add the XLe USD to an existing Isaac Sim stage.

    This function only loads the robot.
    It does not modify the robot pose, joints, or physics.
    """

    if not os.path.exists(XLE_USD):
        raise FileNotFoundError(
            f"XLe USD not found: {XLE_USD}"
        )

    robot_prim = stage.DefinePrim(
        prim_path,
        "Xform"
    )

    robot_prim.GetReferences().AddReference(
        XLE_USD
    )

    return robot_prim