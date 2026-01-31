import bpy

def create_drone_emission_material(drone_name):
    mat = bpy.data.materials.new(name=f'LED color of {drone_name}')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    emission = nodes.new(type="ShaderNodeEmission")
    emission.name = "Drone Glow"
    emission.inputs["Color"].default_value = (1,1,1,1)
    emission.inputs["Strength"].default_value = 5.0

    output = nodes.new(type="ShaderNodeOutputMaterial")
    links.new(emission.outputs["Emission"], output.inputs["Surface"])


def configure_lighting_compositing():
    bpy.context.scene.view_settings.view_transform = 'Filmic' 

    bpy.context.scene.use_nodes=True

    nodes = bpy.context.scene.node_tree.nodes
    links = bpy.context.scene.node_tree.links

    nodes.clear()

    glare = nodes.new(type="CompositorNodeGlare")
    glare.glare_type = "FOG_GLOW"
    glare.quality = "HIGH"
    glare.threshold = 0.1

    render_layers = nodes.new(type = "CompositorNodeRLayers")
    render_layers.name = "Render Layers"

    composite = nodes.new(type= "CompositorNodeComposite")
    composite.name = "Composite"

    links.new(render_layers.outputs["Image"], glare.inputs["Image"])
    links.new(glare.outputs["Image"], composite.inputs["Image"])
    

