from reportData import *
import PySimpleGUI as sg
from datetime import datetime

sg.theme('Black')

layout = [
          [sg.Input(key='-DEPARTURE-', size=(20,1)), sg.CalendarButton("DATE TO START SEARCH", close_when_date_chosen=True,  target='-DEPARTURE-', location=(0,0), no_titlebar=False )],
          [sg.Input(key='-ARRIVAL-', size=(20,1)), sg.CalendarButton("DATE TO END SEARCH", close_when_date_chosen=True,  target='-ARRIVAL-', location=(0,0), no_titlebar=False )],
          [sg.Text('Reports:')],
          [sg.Text(size=(40, 2), font=('Helvetica', 10), justification='center', key='-TIME_DIFFERENCE-')],
          [sg.Button('Create Report'), sg.Exit()]
]

window = sg.Window('Calendar', layout)


# This is to make sure that the arrival date is not before the departure date
def is_arrival_before_departure(departure_string, arrival_string):
    # 2021-08-01 13:09:43
    departure_object = datetime.strptime(departure_string, '%Y-%m-%d %H:%M:%S')
    arrival_object = datetime.strptime(arrival_string, '%Y-%m-%d %H:%M:%S')
    return arrival_object < departure_object

# This is to make sure that the arrival date is not before the departure date
def arrival_departure_difference(departure_string, arrival_string):
    # 2021-08-01 13:09:43
    departure_object = datetime.strptime(departure_string, '%Y-%m-%d %H:%M:%S')
    arrival_object = datetime.strptime(arrival_string, '%Y-%m-%d %H:%M:%S')
    return arrival_object - departure_object

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Create Report':
        outtro = searchAndReport(str(values['-DEPARTURE-']),str(values['-ARRIVAL-']))
        window['-TIME_DIFFERENCE-'].update(outtro)
window.close()






