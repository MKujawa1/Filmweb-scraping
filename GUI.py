import dearpygui.dearpygui as dpg
import pandas as pd 

### Load data
global data
data = pd.read_excel('new_data.xlsx')
### Init edit_data
global edit_data 
edit_data = data
### Get categories
global categories
categories = []
for i in range(len(data)):
    gen = data['genre'][i].split(', ')
    for k in range(len(gen)):
        categories.append(gen[k])
categories = list(set(categories))
categories = sorted(categories)
### Get column names
global keys
keys = list(data.keys())

def add_row():
    '''
    Add data row to table
    '''
    # rows = 0
    global rows
    for j in range(len(edit_data[:500])): # Data limit in table
        with dpg.table_row(parent="maintable"):
            for i in range(len(keys)):
                dpg.add_text(str(edit_data.iloc[rows][i]), tag=f"cell_{rows}{i}{j}")      
        rows += 1

def delete_table():
    '''
    Deleting all elements from table
    
    '''
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
    '''
    Create new table with data

    '''
    global columns
    global rows
    columns = len(keys) 
    rows = 0            
    # create table
    with dpg.table(parent="Table", header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   tag="maintable", row_background=True):
        w = [20,3,3,4,4,18] # Width of column
        for i in range(len(keys)):
            dpg.add_table_column(tag=f"col_{i}", label=f"{keys[i]}",
                                 init_width_or_weight=w[i])
        add_row()

def reset():
    '''
    Reset data to begining.
    
    '''
    global edit_data
    global data
    edit_data = data
    # delete and create table
    delete_table()
    create_table()

def filtering():
    '''
    Filtering data with year, rate, pop rate, want see and genre
    
    '''
    global edit_data    
    global data
    edit_data = data
    ### Get variables
    min_year = int(dpg.get_value('year_start'))
    max_year = int(dpg.get_value('year_stop'))
    min_rate = float(dpg.get_value('rate_start'))
    max_rate = float(dpg.get_value('rate_stop'))
    min_pop = int(dpg.get_value('pop_start'))
    max_pop = int(dpg.get_value('pop_stop'))
    min_want = int(dpg.get_value('want_start'))
    max_want = int(dpg.get_value('want_stop'))
    cat = dpg.get_value('gen')
    ### Filtering
    edit_data = edit_data.drop(edit_data[(edit_data[keys[1]]<=min_year)|(edit_data[keys[1]]>=max_year)].index)
    edit_data = edit_data.drop(edit_data[(edit_data[keys[2]]<=min_rate)|(edit_data[keys[2]]>=max_rate)].index)
    edit_data = edit_data.drop(edit_data[(edit_data[keys[3]]<=min_pop)|(edit_data[keys[3]]>=max_pop)].index)   
    edit_data = edit_data.drop(edit_data[(edit_data[keys[4]]<=min_want)|(edit_data[keys[4]]>=max_want)].index)
    ind = []
    for i in range(len(edit_data)):
        if (cat in edit_data['genre'][edit_data.index[i]])==False:
            ind.append(i)
    edit_data = edit_data.drop(edit_data.index[ind])
    ### delete and create table
    delete_table()
    create_table()
    
def sort_as():
    '''
    Ascending data sorting 
    
    '''
    sort_val = dpg.get_value('radio')
    global edit_data
    if sort_val == 'year':
        edit_data = edit_data.sort_values(by = 'year',ascending = True)
    elif sort_val == 'rate':
        edit_data = edit_data.sort_values(by = 'rate',ascending = True)
    elif sort_val == 'pop rate':
        edit_data = edit_data.sort_values(by = 'pop_rate',ascending = True)
    elif sort_val == 'want see':
        edit_data = edit_data.sort_values(by = 'want_see',ascending = True)
    ### delete and create table
    delete_table()
    create_table()
    
def sort_ds():
    '''
    Descending data sorting
    
    '''
    sort_val = dpg.get_value('radio')
    global edit_data
    if sort_val == 'year':
        edit_data = edit_data.sort_values(by = 'year',ascending = False)
    elif sort_val == 'rate':
        edit_data = edit_data.sort_values(by = 'rate',ascending = False)
    elif sort_val == 'pop rate':
        edit_data = edit_data.sort_values(by = 'pop_rate',ascending = False)
    elif sort_val == 'want see':
        edit_data = edit_data.sort_values(by = 'want_see',ascending = False)
    ### delete and create table
    delete_table()
    create_table()

dpg.create_context()
### Create layout 
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
        dpg.add_text("SORT DATA BY")
        dpg.add_separator()
        dpg.add_radio_button(['year','rate','pop rate','want see'],tag = 'radio',default_value='year')
        dpg.add_button(tag= 'as',label = 'ascending',callback=sort_as)
        dpg.add_same_line()
        dpg.add_button(tag= 'ds',label = 'descending',callback=sort_ds)
    with dpg.child_window(tag = 'Table',parent = 'Main'):
        ### Init table
        create_table()
                    
dpg.set_primary_window('Main',True)
dpg.create_viewport(title = 'Filmweb Management', width=1300, height=600,min_height=600,min_width=1300,x_pos = 10,y_pos = 10)
dpg.setup_dearpygui()
dpg.show_viewport()
### Window resizing
cor_x = 12
cor_y = 12
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    ### Get width and height of Main window
    w = dpg.get_item_width('Main')
    h = dpg.get_item_height('Main')
    ### Set width and height to children windows 
    dpg.set_item_width('Filter', int(w*0.25)-cor_x)
    dpg.set_item_width('Sort', int(w*0.25)-cor_x)
    dpg.set_item_width('Table', int(w*0.75)-cor_x-1)
    dpg.set_item_height('Filter', int(h*0.6)-cor_y)
    dpg.set_item_height('Sort', int(h*0.4)-cor_y)
    dpg.set_item_height('Table', int(h*1)-21)
    ### Set pos to Table
    dpg.set_item_pos('Table', (int(w*0.25),8))
    ### Get width of Filter window    
    w_f = dpg.get_item_width('Filter')
    ### Set pos and width to elements in Filter window
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
    ### Get width and height of Sort window
    w_s = dpg.get_item_width('Sort')
    h_s = dpg.get_item_height('Sort')
    ### Set pos and width to elements in Sort window
    dpg.set_item_pos('ds', pos=(int(w_s*0.5),h_s-27))
    dpg.set_item_width('ds', int(w_s*0.36))
    dpg.set_item_pos('as', pos=(8,h_s-27))
    dpg.set_item_width('as', int(w_s*0.36))
   
dpg.destroy_context()