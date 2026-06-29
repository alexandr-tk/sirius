from . import panels, operators, props, materials


bl_info = {
    "name": "Sirius",
    "author": "Alexandr Tkachyov",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > Sirius",
    "description": "Design drone light-shows and export to flight-ready formats.",
    "category": "Object"
}


def register():
    props.register()
    operators.register()
    panels.register()
    


def unregister():
    props.unregister()
    operators.unregister()
    panels.unregister()
    