from isaacsim.storage.native import get_assets_root_path


SCENES = {
    "simple_room": "/Isaac/Environments/Simple_Room/simple_room.usd",
    "office": "/Isaac/Environments/Office/office.usd",
    "hospital": "/Isaac/Environments/Hospital/hospital.usd",
    "warehouse": "/Isaac/Environments/Simple_Warehouse/warehouse.usd",
    "warehouse_forklifts":
        "/Isaac/Environments/Simple_Warehouse/warehouse_with_forklifts.usd",
    "warehouse_shelves":
        "/Isaac/Environments/Simple_Warehouse/warehouse_multiple_shelves.usd",
    "full_warehouse":
        "/Isaac/Environments/Simple_Warehouse/full_warehouse.usd",
    "grid":
        "/Isaac/Environments/Grid/default_environment.usd",
}


def get_scene_path(scene_name):
    """Return the full Isaac asset path for a named environment."""

    if scene_name not in SCENES:
        available = ", ".join(SCENES.keys())
        raise ValueError(
            f"Unknown scene '{scene_name}'. "
            f"Available: {available}"
        )

    assets_root = get_assets_root_path()

    if assets_root is None:
        raise RuntimeError(
            "Could not resolve Isaac Sim assets root."
        )

    return assets_root + SCENES[scene_name]