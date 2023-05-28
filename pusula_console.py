import PySimpleGUI as sg
import os, signal
import time
import threading
import sys
import json
from os import path
from dotenv import load_dotenv

load_dotenv()

status_files_dir = os.getenv('ROOT_DIRECTORY') + "/status_files"
pistorasiat_root = os.getenv('PISTORASIAT_ROOT_DIRECTORY')
pistorasiat_user = os.getenv('PISTORASIAT_USERNAME')

sockets = {
    "A": {
        "text" : "Lämmitin",
        "status" : False
    },
    "B": {
        "text" : "Sänky",
        "status" : False
    },
    "C": {
        "text" : "Hylly",
        "status" : False
    },
    "D": {
        "text" : "Kone",
        "status" : False
    },
    "E": {
        "text" : "Raketti",
        "status" : False
    },
    "F": {
        "text" : "Joost",
        "status" : False
    },
    "G": {
        "text" : "Puu",
        "status" : False
    },
    "H": {
        "text" : "Kasvit",
        "status" : False
    },
}

group_a_status = False
group_a_text = "Kaikki sisävalot"
group_b_status = False
group_b_text = "Kaikki ulkovalot"
i_status = 'off'
all_processes = []
kastelu_seconds = 15
button_pressed = False
pistorasiat_address=os.getenv('PISTORASIAT_ADDRESS')

tab1_layout =  [
    [
        sg.Button(group_a_text, button_color='black on white', key='GROUP_A', font=('Helvetica', 20), size=(20,2))
    ],
 #   [
 #       sg.Button(group_b_text, button_color='black on white', key='GROUP_B', font=('Helvetica', 20), size=(20,2))
 #   ],
    [
        sg.Button('Kastelu ' + str(kastelu_seconds) + 's', button_color='black on white', key='I', font=('Helvetica', 20), size=(20,2))
    ],
    [
        sg.ProgressBar(kastelu_seconds, orientation='h', size=(35,10), key='progressbar', bar_color='green on white')
    ]
]

tab2_layout = [
    [
        sg.Button(sockets['B']['text'], button_color='black on white', key='B', font=('Helvetica', 15), size=(9,1)),
        sg.Button(sockets['C']['text'], button_color='black on white', key='C', font=('Helvetica', 15), size=(9,1))
    ],
    [
        sg.Button(sockets['D']['text'], button_color='black on white', key='D', font=('Helvetica', 15), size=(9,1)),
        sg.Button(sockets['E']['text'], button_color='black on white', key='E', font=('Helvetica', 15), size=(9,1))
    ],
    [
        sg.Button(sockets['A']['text'], button_color='black on white', key='A', font=('Helvetica', 15), size=(9,1)),
        sg.Button(sockets['F']['text'], button_color='black on white', key='F', font=('Helvetica', 15), size=(9,1))
    ],
    [
        sg.Button(sockets['G']['text'], button_color='black on white', key='G', font=('Helvetica', 15), size=(9,1)),
        sg.Button(sockets['H']['text'], button_color='black on white', key='H', font=('Helvetica', 15), size=(9,1))
    ]
]

layout = [
    [
        sg.TabGroup([
            [
                sg.Tab('Ryhmät', tab1_layout),
                sg.Tab('Yksittäiset', tab2_layout)
            ]
        ],
        border_width=(0))
    ],
    [
        sg.Exit(font=('Helvetica', 20), size=(20,2))
    ]
]

window = sg.Window('Pusula console', layout, size=(320,480), element_justification="center", finalize=True)
window.Maximize()
progress_bar = window['progressbar']

def button_status():
    global sockets
    global group_a_status
    global group_b_status
    pistorasiat_status = ''

    if path.exists(status_files_dir + "/all_status.json"):
        with open(status_files_dir + "/all_status.json") as f:
            pistorasiat_status = json.load(f)

    for pistorasia_item in pistorasiat_status:
        if pistorasia_item in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            if pistorasiat_status[pistorasia_item]["status"] == "is_read_on":
                sockets[pistorasia_item]["status"] = False
                window[pistorasia_item].update(button_color='white on green')
            else:
                sockets[pistorasia_item]["status"] = True
                window[pistorasia_item].update(button_color='black on white')

    # sisävalot status
    if pistorasiat_status["GROUP_A"]["status"] == "is_read_on":
      group_a_status = False
      window['GROUP_A'].update(button_color='white on green')
    elif pistorasiat_status["GROUP_A"]["status"] == "is_read_off":
      group_a_status = True
      window['GROUP_A'].update(button_color='black on white')
    else:
      group_a_status = True
      window['GROUP_A'].update(button_color='black on yellow')

    # ulkovalot status
    if pistorasiat_status["GROUP_B"]["status"] == "is_read_on":
      group_b_status = False
#      window['GROUP_B'].update(button_color='white on green')
    elif pistorasiat_status["GROUP_B"]["status"] == "is_read_off":
      group_b_status = True
#      window['GROUP_B'].update(button_color='black on white')
    else:
      group_b_status = True
#      window['GROUP_B'].update(button_color='black on yellow')

def kastelu_hold():
    global kastelu_seconds_left
    global i_status
    print('A thread on')
    window['I'].update('Käynnistetään ...', button_color='black on yellow')
    os.system("ssh " + pistorasiat_user + "@" + str(pistorasiat_address) + " 'python3 " + pistorasiat_root + "/remote_control.py H on'")
    while True:
        if kastelu_seconds_left > 0:
            kastelu_seconds_left = kastelu_seconds_left - 1
            x = str(kastelu_seconds_left)
            window['I'].update('Kastellaan .. ' + x + 's', button_color='white on red')
            progress_bar.UpdateBar(abs(kastelu_seconds - kastelu_seconds_left))
            time.sleep(1)
        else:
            window['I'].update('Sammutetaan ...', button_color='black on yellow')
            os.system("ssh " + pistorasiat_user + "@" + str(pistorasiat_address) + " 'python3 " + pistorasiat_root + "/remote_control.py H off'")
            os.system("ssh " + pistorasiat_user + "@" + str(pistorasiat_address) + " 'python3 " + pistorasiat_root + "/remote_control.py H off'")
            os.system("ssh " + pistorasiat_user + "@" + str(pistorasiat_address) + " 'python3 " + pistorasiat_root + "/remote_control.py H off'")
            i_status = 'off'
            break

    # if kastelu.is_alive():
    window['I'].update('Kastelu ' + str(kastelu_seconds) + 's', button_color='black on white')
    progress_bar.UpdateBar(0)
    print('A thread off')

def switch(target, status, button_cta_text):
    global button_pressed
    button_pressed = True
    if status == 'on': button_loading_text = 'Syttyy ...'
    if status == 'off': button_loading_text = 'Sammuu ...'
    window[target].update(button_loading_text, button_color='black on yellow')
    os.system("ssh " + pistorasiat_user + "@" + str(pistorasiat_address) + " 'python3 " + pistorasiat_root + "/remote_control.py " + target + " " + status + "'")
    window[target].update(button_cta_text, button_color='black on white')
    button_pressed = False

button_status()

while True:
    event, values = window.read(timeout=500)

    # exit
    if event in (sg.WIN_CLOSED, 'Exit'):
        filename = status_files_dir + "/pidof_pusula_console"

        with open(filename) as f:
            content = f.readline()

        os.kill(int(content), signal.SIGKILL)
        break

    # sisävalot
    elif event == 'GROUP_A':
        if group_a_status:
            group_a_on = threading.Thread(target=switch, args=("GROUP_A", "on", group_a_text), daemon=True)
            group_a_on.start()
        else:
            group_a_off = threading.Thread(target=switch, args=("GROUP_A", "off", group_a_text), daemon=True)
            group_a_off.start()

    # ulkovalot
    elif event == 'GROUP_B':
        if group_b_status:
            group_b_on = threading.Thread(target=switch, args=("GROUP_B", "on", group_b_text), daemon=True)
            group_b_on.start()
        else:
            group_b_on = threading.Thread(target=switch, args=("GROUP_B", "off", group_b_text), daemon=True)
            group_b_on.start()

    # kastelu
    elif event == 'I':
        print(i_status)
        if i_status == 'off':
            kastelu = threading.Thread(target=kastelu_hold, daemon=True)
            kastelu_seconds_left = kastelu_seconds
            kastelu.start()
            i_status = 'on'
        elif h_status == 'on':
            if kastelu.is_alive():
                print('A off')
                kastelu_seconds_left = 0
            i_status = 'off'

    # yksittäinen
    elif event in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        if sockets[event]["status"]:
            socket_on = threading.Thread(target=switch, args=(event, "on", sockets[event]["text"]), daemon=True)
            socket_on.start()
        else:
            socket_on = threading.Thread(target=switch, args=(event, "off", sockets[event]["text"]), daemon=True)
            socket_on.start()

    if not button_pressed:
        button_status()

window.close()

