import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(tag = 'Main',):
    with dpg.child_window(tag = 'Filter',parent = 'Main'):
        pass
    with dpg.child_window(tag = 'Sort',parent = 'Main'):
        pass
    with dpg.child_window(tag = 'Table',parent = 'Main'):
        pass


dpg.set_primary_window('Main',True)
dpg.create_viewport(title = 'Filmweb Management', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()

cor_x = 12
cor_y = 12
while dpg.is_dearpygui_running():
    w = dpg.get_item_width('Main')
    h = dpg.get_item_height('Main')
    
    dpg.set_item_width('Filter', int(w*0.3)-cor_x)
    dpg.set_item_width('Sort', int(w*0.3)-cor_x)
    dpg.set_item_width('Table', int(w*0.7)-cor_x-1)
    
    dpg.set_item_height('Filter', int(h*0.7)-cor_y)
    dpg.set_item_height('Sort', int(h*0.3)-cor_y)
    dpg.set_item_height('Table', int(h*1)-21)
    
    dpg.set_item_pos('Table', (int(w*0.3),8))
    dpg.render_dearpygui_frame()
    
dpg.destroy_context()
