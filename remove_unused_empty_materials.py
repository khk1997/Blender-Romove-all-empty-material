import bpy


def clean_material_slots(obj):
    mesh = obj.data
    used_indices = {polygon.material_index for polygon in mesh.polygons}
    old_materials = [slot.material for slot in obj.material_slots]
    keep_indices = [
        index
        for index, material in enumerate(old_materials)
        if material is not None and index in used_indices
    ]

    if len(keep_indices) == len(old_materials):
        return

    index_map = {
        old_index: new_index
        for new_index, old_index in enumerate(keep_indices)
    }
    old_polygon_indices = [polygon.material_index for polygon in mesh.polygons]
    kept_materials = [old_materials[index] for index in keep_indices]

    mesh.materials.clear()
    for material in kept_materials:
        mesh.materials.append(material)

    for polygon, old_index in zip(mesh.polygons, old_polygon_indices):
        polygon.material_index = index_map.get(old_index, 0)


# Keep current selection so we can restore it after cleanup.
selected_objects = list(bpy.context.selected_objects)
active_object = bpy.context.view_layer.objects.active
mesh_objects = [
    obj
    for obj in bpy.context.scene.objects
    if obj.type == "MESH"
]

# Make sure we are in Object Mode.
if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode="OBJECT")

for obj in mesh_objects:
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    clean_material_slots(obj)

# Restore original selection.
bpy.ops.object.select_all(action="DESELECT")
for obj in selected_objects:
    if obj.name in bpy.context.scene.objects:
        obj.select_set(True)

if active_object and active_object.name in bpy.context.scene.objects:
    bpy.context.view_layer.objects.active = active_object

# Purge unused orphan data.
# Repeat a few times because removing one data block can orphan another.
for _ in range(5):
    bpy.ops.outliner.orphans_purge(
        do_local_ids=True,
        do_linked_ids=True,
        do_recursive=True
    )

print("Done: removed unused material slots, empty material slots, and purged orphan data.")
