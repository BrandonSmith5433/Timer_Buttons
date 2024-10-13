import pygsheets
from google.oauth2.credentials import Credentials

SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
my_credentials = Credentials.from_authorized_user_file("/home/brandonsmith5433/Desktop/TimerButtons/TimerButtonsProject/token.json", SCOPES)
gc = pygsheets.authorize(custom_credentials=my_credentials)
cell_list = []
spreadsheet_key= '13boRyfm3qdod6Xvst1DqpUU4sgStL9cO_mrVLL26C4A'

sh = gc.open_by_key(spreadsheet_key)

wks = sh[0]
global offset
offset = 2

wks.update_values(
    'A1:D1',[['Name', 'Color', 'Turn Start', 'Turn End']])

def updateCell(records, index):
    global offset
    turn_start = records.get("Start time")
    turn_end = records.get("End time")
    name = records.get("Name")
    color = records.get("Color")
    
    wks.update_values(
    'A'+ str(offset)+":"+'D'+str(offset),[[name, color, turn_start, turn_end]])
   
   
    #wks.update_value('A' + str(offset), name)
    #wks.update_value('B' + str(offset), color)
    #wks.update_value('C' + str(offset), round(turn_time, 2))
    #wks.update_value('D' + str(offset), pause_count)
    #wks.update_value('E' + str(offset), round(pause_time, 2))
    
    offset += 1
