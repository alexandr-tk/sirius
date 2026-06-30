import bpy

# Import classes
from ..operators.create_takeoff_grid import CreateTakeoffGrid
from ..operators.change_led_color import ChangeLEDColor

from ..panels.takeoff_grid import TakeoffGridPanel
from ..panels.led_control import LEDControlPanel

from ..props import DroneShowSettings


CLASSES = [DroneShowSettings, CreateTakeoffGrid, ChangeLEDColor, TakeoffGridPanel, LEDControlPanel]

def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_props = bpy.props.PointerProperty(type=DroneShowSettings)

def unregister():
    del bpy.types.Scene.my_props

    for cls in reversed (CLASSES):
        bpy.utils.unregister_class(cls)

