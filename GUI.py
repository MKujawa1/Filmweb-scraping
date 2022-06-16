import dearpygui.dearpygui as dpg
import pandas as pd 
### Load data
global data
data = pd.read_excel('new_data.xlsx')
global edit_data 
edit_data = data
global categories
categories = []
for i in range(len(data)):
    gen = data['genre'][i].split(', ')
    for k in range(len(gen)):
        categories.append(gen[k])
categories = list(set(categories))
global keys
keys = list(data.keys())

def cell_edit(sender, app_data):

    # remember current cell for later
    global current_cell
    current_cell = app_data[1]
    # show clicked info to user
    
    # store cell contents for later
    cell_content = dpg.get_value(app_data[1])
    print(cell_content)

    # save current parent
    parent = dpg.get_item_parent(current_cell)
    # iterate cells in current row and save the position
    cell_position = None
    cell_before = None
    for child in dpg.get_item_children(parent)[1]:
        # if we saved a cell position, we can save the next one for the before-parameter
        if cell_position:
            cell_before = dpg.get_item_alias(child)
            # escape to not overwrite any saved items
            break
        if dpg.get_item_alias(child) == current_cell:
            cell_position = dpg.get_item_alias(child)
    # delete current cell (meaning the label)
    dpg.delete_item(current_cell)
    # remove the alias if not already happened
    if dpg.does_alias_exist(current_cell):
        dpg.remove_alias(current_cell)
    
    # add an input text widget instead of the label one
    # if we saved a "before"-position, attach it before that position
    if cell_before:
        dpg.add_input_text(tag=current_cell, parent=parent, before=cell_before)
    else:
        dpg.add_input_text(tag=current_cell, parent=parent)
    dpg.set_value(current_cell, cell_content)

def add_row():
    # rows = 0
    global rows
    for j in range(len(edit_data[:200])):
        with dpg.table_row(parent="maintable"):
            for i in range(len(keys)):
                dpg.add_text(str(edit_data.iloc[rows][i]), tag=f"cell_{rows}{i}{j}")
                with dpg.item_handler_registry(tag=f"cell_handler_{rows}{i}{j}") as handler:
                    dpg.add_item_clicked_handler(callback=cell_edit)
                dpg.bind_item_handler_registry(f"cell_{rows}{i}{j}", f"cell_handler_{rows}{i}{j}")
        rows += 1

def delete_table():
    dpg.delete_item("maintable")
    global rows
    global columns
    rows = 0
    columns = 0
    to_delete = []
    for alias in dpg.get_aliases():

        if alias.startswith("row_") or alias.startswith("col_") or alias.startswith("cell_"):
            to_delete.append(alias)

    for alias in to_delete:
        dpg.remove_alias(alias)

def create_table():
    
    global columns
    global rows
    columns = len(keys) 
    rows = 0            
    
    # create table
    with dpg.table(parent="Table", header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   tag="maintable", row_background=True):

        
        w = [20,3,3,4,4,18]
        for i in range(len(keys)):
            dpg.add_table_column(tag=f"col_{i}", label=f"{keys[i]}",
                                 init_width_or_weight=w[i])

        
        
        add_row()

def reset():
    global edit_data
    global data
    edit_data = data
    # delete and create table
    delete_table()
    create_table()

def filtering(sender):
    # test = data.drop(data[(data['genre']=='Komedia')].index)
    global edit_data
    
    global data
    edit_data = data
    min_year = int(dpg.get_value('year_start'))
    max_year = int(dpg.get_value('year_stop'))
    min_rate = float(dpg.get_value('rate_start'))
    max_rate = float(dpg.get_value('rate_stop'))
    min_pop = int(dpg.get_value('pop_start'))
    max_pop = int(dpg.get_value('pop_stop'))
    min_want = int(dpg.get_value('want_start'))
    max_want = int(dpg.get_value('want_stop'))
    cat = dpg.get_value('gen')
    print(min_year)
    
    edit_data = edit_data.drop(edit_data[(edit_data[keys[1]]<=min_year)&(edit_data[keys[1]]>=max_year)].index)
    edit_data = edit_data.drop(edit_data[(edit_data[keys[2]]<=min_rate)&(edit_data[keys[2]]>=max_rate)].index)
    edit_data = edit_data.drop(edit_data[(edit_data[keys[3]]<=min_pop)&(edit_data[keys[3]]>=max_pop)].index)   
    edit_data = edit_data.drop(edit_data[(edit_data[keys[4]]<=min_want)&(edit_data[keys[4]]>=max_want)].index)
    ind = []
    for i in range(len(edit_data)):
        if (cat in edit_data['genre'][i])==False:
            ind.append(i)
    edit_data = edit_data.drop(edit_data.index[ind])
    
    delete_table()
    create_table()
    
dpg.create_context()
with dpg.window(tag = 'Main'):
    with dpg.child_window(tag = 'Filter',parent = 'Main'):
        dpg.add_button(label= 'Reset data',tag = 'rd', callback=reset)
        dpg.add_spacer()
        dpg.add_separator()
        dpg.add_text('FILTER DATA',tag = 'fd_text')
        dpg.add_same_line()
        dpg.add_button(label = 'Filter',tag = 'fd',callback = filtering)
        dpg.add_spacer()
        dpg.add_separator()
        
        dpg.add_text('year range:')
        dpg.add_input_int(label = 'from',tag = 'year_start',default_value=1972)
        dpg.add_same_line()
        dpg.add_input_int(label = 'to',tag = 'year_stop',default_value=2022)
        dpg.add_spacer()
        dpg.add_text('rate:')
        dpg.add_input_float(label = 'from',tag = 'rate_start',default_value=5.0,step = 0.1,format='%.1f')
        dpg.add_same_line()
        dpg.add_input_float(label = 'to',tag = 'rate_stop',default_value=9.8,max_value = float(10),step = 0.1,format='%.1f')
        dpg.add_spacer()
        dpg.add_text('pop rate:')
        dpg.add_input_int(label = 'from',tag = 'pop_start',default_value=3000)
        dpg.add_same_line()
        dpg.add_input_int(label = 'to',tag = 'pop_stop',default_value=1000000)
        dpg.add_spacer()
        dpg.add_text('want see:')
        dpg.add_input_int(label = 'from',tag = 'want_start',default_value=3000)
        dpg.add_same_line()
        dpg.add_input_int(label = 'to',tag = 'want_stop',default_value=1000000)
        dpg.add_spacer()
        dpg.add_text('genre:')
        dpg.add_combo(items=categories,tag = 'gen',default_value='Komedia')
        
        
    with dpg.child_window(tag = 'Sort',parent = 'Main'):
        pass
    with dpg.child_window(tag = 'Table',parent = 'Main'):
        create_table()
        
            
dpg.set_primary_window('Main',True)
dpg.create_viewport(title = 'Filmweb Management', width=1300, height=600,min_height=600,min_width=1300)
dpg.setup_dearpygui()
dpg.show_viewport()

cor_x = 12
cor_y = 12
while dpg.is_dearpygui_running():
    w = dpg.get_item_width('Main')
    h = dpg.get_item_height('Main')
    
    dpg.set_item_width('Filter', int(w*0.25)-cor_x)
    dpg.set_item_width('Sort', int(w*0.25)-cor_x)
    dpg.set_item_width('Table', int(w*0.75)-cor_x-1)
    
    dpg.set_item_height('Filter', int(h*0.6)-cor_y)
    dpg.set_item_height('Sort', int(h*0.4)-cor_y)
    dpg.set_item_height('Table', int(h*1)-21)
    
    dpg.set_item_pos('Table', (int(w*0.25),8))
    dpg.render_dearpygui_frame()
    
    w_f = dpg.get_item_width('Filter')
    
    dpg.set_item_width('year_start', int(w_f*0.35))
    dpg.set_item_width('year_stop', int(w_f*0.35))
    dpg.set_item_width('rate_start', int(w_f*0.35))
    dpg.set_item_width('rate_stop', int(w_f*0.35))
    dpg.set_item_width('pop_start', int(w_f*0.35))
    dpg.set_item_width('pop_stop', int(w_f*0.35))
    dpg.set_item_width('want_start', int(w_f*0.35))
    dpg.set_item_width('want_stop', int(w_f*0.35))
    dpg.set_item_width('gen', int(w_f*0.83))
    dpg.set_item_pos('fd', pos=(int(w_f*0.5),43))
    dpg.set_item_pos('fd_text', pos=(8,43))
    dpg.set_item_width('fd', int(w_f*0.36))
   
    
dpg.destroy_context()
