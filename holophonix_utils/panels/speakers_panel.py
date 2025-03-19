import bpy

class SNA_PT_SPEAKERS_F8536(bpy.types.Panel):
    bl_label = 'Speakers'
    bl_idname = 'SNA_PT_SPEAKERS_F8536'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 2
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_MAIN_PANEL'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MESH_CUBE')

    def draw(self, context):
        layout = self.layout
        
        # Check for speakers
        speakers = [obj for obj in context.scene.objects if "speaker" in obj.name.lower()]
        
        # Speaker management section
        if speakers:
            box = layout.box()
            box.label(text="Speaker Management", icon='OUTLINER_OB_SPEAKER')
            
            # Stats about speakers
            row = box.row()
            row.label(text=f"Speakers: {len(speakers)}", icon='SPEAKER') 
            
            # Speaker actions
            col = box.column(align=True)
            row = col.row(align=True)
            # Temporarily commented until addon is reloaded
            # row.operator('sna.select_all_speakers', text='Select All Speakers', icon='RESTRICT_SELECT_OFF')
            row.label(text="Selection tools will be available after reload")
        else:
            # No speakers message and import option
            box = layout.box()
            col = box.column(align=True)
            col.label(text="No Speakers Found", icon='INFO')
            col.label(text="Import speakers from the 'Project Setup' panel")
            col.label(text="or use the button below:")
            col.separator()
            col.operator('sna.add_speakers_994c8', 
                       text='Import Speakers', 
                       icon='IMPORT')
