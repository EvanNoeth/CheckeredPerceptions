import sys, time, os
import qi
from tkinter import OFF
import PySimpleGUI as sg

session = None
tts = None
posture = None
led = None
motion = None

if len(sys.argv) > 1 and len(sys.argv) < 3: #ensures proper number of arguments
    ROBOT_IP = sys.argv[1]
    ROBOT_PORT = 9559
else:
    print("please provide proper number of arguments")
    print("Proper program usage: python3 name.py IP_ADDRESS_HERE")
    sys.exit(1)

def nao_init():
    # initialize nao stuff

    global session
    session = qi.Session()
    try:
        print(f"Connecting to NAO at {ROBOT_IP}:{ROBOT_PORT}...")
        session.connect(f"tcp://{ROBOT_IP}:{ROBOT_PORT}")
        print("Successfully connected to NAO!")
    except RuntimeError as e:
        print(f"Failed to connect to the robot at {ROBOT_IP}: {e}")
        print("Please try again")
        sys.exit(1)

    try:
        global tts
        global posture
        global mostion
        global led
        tts = session.service("ALTextToSpeech") #initialized text-to-speech service
        tts.setVolume(1)
        posture = session.service("ALRobotPosture")
        led = session.service("ALLeds")
        motion = session.service("ALMotion")
        pass
    except Exception as e:
        print(f"Failed to load services: {e}")
        sys.exit(1)

    
def window_main():
    sg.set_options(font=("Arial", 8))

    move_prompt_1 = "Move piece at: "
    move_prompt_2 = "to: "
    taking_piece_prompt = "taking your piece at: "

    comments = ["You basically rolled out the red carpet for that sweep.",
                "Two triple jumps in one game. Well played.",
                "I'm actually impressed at how bad you are at this.",
                "That was the easiest king of my life.",
                "Handing me a king right there is basically conceding, just F Y I.",
                "Enjoy watching this king tear through your pieces.",
                "Running that king back and forth isn't changing the scoreboard",
                "Are you playing checkers or just making up your own game?",
                "You know there's rules right by you right?",
                "Congrats on the tie. It's the closest you'll ever get to beating me",
                "Well that's game. I think a ten year old could have given me more trouble.",
                "What a choke, totally saw that coming.",
                "Take your time. It's not going to change the outcome.",
                "That's really your move?",
                "Not what I would have done.",
                "You know if you're going to lose a piece, you should at least try to trade?",
                "Candy land seems more your tempo.",
                "I'm just making observations.",
                "I doubt that.",
                ]

    comment_buttons = [[sg.Button(x, key=x)] for x in comments]

    layout = [
                [sg.Text('MOVE COMMAND')],
                [sg.Checkbox("and then", key="and_then_box")],
                [sg.Text(move_prompt_1), sg.Input(key="from_tile", size=(5, 5), do_not_clear=False), sg.Text(move_prompt_2), sg.Input(key="to_tile", size=(5, 5), do_not_clear=False)],
                [sg.Checkbox(taking_piece_prompt, key="taking_piece_box"), sg.Input(key="taken_tile", size=(5, 5), do_not_clear=False)],
                [sg.Button("submit move command", key="submit_move_command")],
                [sg.Text('')],
                [sg.Text('Comments')],
                comment_buttons,
                [sg.Text('')],
                [sg.Text('TTS Input:')],
                [sg.Input(key="tts_input", do_not_clear=False), sg.Button("Submit")],
                [sg.Text('')],
                [sg.Text("Physical Controls")],
                [sg.Button("Stand"), sg.Button("Sit"), sg.Button("Sitting Rest")],
                [sg.Text('')],
                ]

    window = sg.Window('Title', layout)

    while True:         # The Event Looop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # comments
        if event in comments:
            tts.say(event)
            continue

        if event == "Submit":
            tts_input = values["tts_input"]
            window["tts_input"].update()
            tts.say(tts_input)
            continue

        if event == "submit_move_command":
            out = ""
            if (values["and_then_box"]):
                out += "And then "
            
            out += "I'll move my piece at "
            out += coord_from_input(values["from_tile"])
            out += " to "
            out += coord_from_input(values["to_tile"])

            if (values["taking_piece_box"]):
                out += " taking your piece at "
                out += coord_from_input(values["taken_tile"])

            tts.say(out)

            # clear input boxes
            window["from_tile"].update()
            window["to_tile"].update()
            window["taken_tile"].update()
            continue

        if event == "Sit":
            posture.goToPosture("Sit", 1)

    window.close()

def coord_from_input(input):
    if (str(int(input)) != input):
        # input is not a number, return original
        return input
    # map input number to location on board
    input = int(input)

    # do not put in a number that isn't [1.. 32]
    locations = ["B8",
                 "D8",
                 "F8",
                 "H8",
                 "A7",
                 "C7",
                 "E7",
                 "G7",
                 "B6",
                 "D6",
                 "F6",
                 "H6",
                 "A5",
                 "C5",
                 "E5",
                 "G5",
                 "B4",
                 "D4",
                 "F4",
                 "H4",
                 "A3",
                 "C3",
                 "E3",
                 "G3",
                 "B2",
                 "D2",
                 "F2",
                 "H2",
                 "A1",
                 "C1",
                 "E1",
                 "G1",
                ]

    return locations[input - 1]

def main():
    nao_init()
    window_main()

if __name__ == "__main__":
    main()
