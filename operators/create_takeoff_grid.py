import bpy
from ..materials import create_drone_emission_material, configure_lighting_compositing

class CreateTakeoffGrid(bpy.types.Operator):
    bl_idname = "object.create_takeoff_grid"
    bl_label = "Create Takeoff Grid"
    bl_description = "Create a grid of drones placed using your defined parameters"
    
    def execute(self,context):
        props = context.scene.my_props
        
        rows = props.rows_count
        cols = props.cols_count
        drones_total = props.drone_count
        
        if(rows*cols<drones_total):
            self.report({'WARNING'}, 
            "The total number of drones is greater than your grid can accomodate"
            )
        
        else:
            hor_spc = props.horizontal_spacing
            vert_spc = props.vertical_spacing
            
            start_pos_x = (rows-1)/2 * hor_spc
            start_pos_y = (cols-1)/2 * vert_spc
            
            drones_collection = bpy.data.collections.new("Drones")
            bpy.context.scene.collection.children.link(drones_collection)
            configure_lighting_compositing()

            drone_cnt = 0
            for i in range(cols):
                for j in range(rows):
                    drone_cnt+=1
                    bpy.ops.mesh.primitive_uv_sphere_add(
                        radius=0.5,
                        location = (start_pos_x - hor_spc*j, start_pos_y - vert_spc*i, 0)
                    )
                    drone = bpy.context.active_object
                    drone.name ="Drone "+str(drone_cnt)
                    create_drone_emission_material(drone.name)
                    emission_mat = bpy.data.materials.get(f'LED color of {drone.name}')
                    if drone.data.materials:
                        drone.data.materials[0] = emission_mat
                    else:
                        drone.data.materials.append(emission_mat)

                    for coll in drone.users_collection:
                        coll.objects.unlink(drone)
                    drones_collection.objects.link(drone)
                    if(drone_cnt==drones_total):
                        return {'FINISHED'}
            
        return {'FINISHED'}