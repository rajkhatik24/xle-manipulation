from pxr import UsdGeom, Gf


def add_box(stage, prim_path, position, size):
    cube = UsdGeom.Cube.Define(stage, prim_path)
    cube.CreateSizeAttr(1.0)

    xform = UsdGeom.Xformable(cube)

    xform.AddTranslateOp().Set(
        Gf.Vec3d(*position)
    )

    xform.AddScaleOp().Set(
        Gf.Vec3f(*size)
    )

    return cube


def add_table(stage):
    # Tabletop
    add_box(
        stage,
        "/World/ManipulationTable/Top",
        position=(0.8, 0.0, 0.75),
        size=(1.0, 0.7, 0.05),
    )

    # Legs
    positions = [
        (0.35,  0.30, 0.375),
        (0.35, -0.30, 0.375),
        (1.25,  0.30, 0.375),
        (1.25, -0.30, 0.375),
    ]

    for i, position in enumerate(positions):
        add_box(
            stage,
            f"/World/ManipulationTable/Leg_{i}",
            position=position,
            size=(0.05, 0.05, 0.75),
        )