from .blender import registry

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
    registry.register()

def unregister():
    registry.unregister()
    