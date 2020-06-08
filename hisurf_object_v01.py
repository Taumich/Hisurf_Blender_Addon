bl_info = {
    "name": "Hisurf Objects v0.2",
    "author": "Michael Arenander",
    "version": (0, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new High-Poly Workflow Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy.props import FloatProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y
    scale_z = self.scale.z
    
    x_mirror = -1
    y_mirror = 0
    
    if(self.y_mirror):
        x_mirror = 0
        y_mirror = -1
    else:
        x_mirror = -1
        y_mirror = 0

    verts = [
        Vector((y_mirror * scale_x,  1 * scale_y, 0)),
        Vector(( 1 * scale_x,  1 * scale_y, 0)),
        Vector(( 1 * scale_x, x_mirror * scale_y, 0)),
        Vector((y_mirror * scale_x, x_mirror * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    this_mesh = bpy.data.meshes.new(name="Hisurf_plane")
    this_mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, this_mesh, operator=self)


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new plane with high-poly workflow properties"""
    bl_idname = "mesh.hisurf"
    bl_label = "Add Hisurf Plane"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )
    
    y_mirror: bpy.props.BoolProperty(name="Mirror in y-axis")

    def execute(self, context):

        add_object(self, context)
        
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_clip = True
        
        if(self.y_mirror):
            bpy.context.object.modifiers["Mirror"].use_axis[0] = False
            bpy.context.object.modifiers["Mirror"].use_axis[1] = True
            
        else:
            bpy.context.object.modifiers["Mirror"].use_axis[1] = False
            bpy.context.object.modifiers["Mirror"].use_axis[0] = True
        
        
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.ops.object.shade_smooth()

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Hisurf Plane",
        icon='MOD_SUBSURF')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
