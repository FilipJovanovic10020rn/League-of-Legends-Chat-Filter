import keyboard
from pynput import mouse

file_path = 'ban_words.txt' 

with open(file_path, 'r') as file:
    content = file.read()
    flaggedWords = content.split()

flagged_words_lower = [word.lower() for word in flaggedWords]

string = ''
startTyping = False

def on_key_press(event):
    global flaggedWords
    global string
    global startTyping
    
    if event.name == 'space':
        if startTyping:

            words_to_check = string.lower().split()

            flagged = False
            for word in words_to_check:
                if word in flagged_words_lower:
                    print(f"Rec {word} je flegovana")

                    words_to_check.remove(word)
                    string = ' '.join(words_to_check)
                    string += ' '

                    for i in range(len(word)+1):
                        keyboard.send('backspace')

                    flagged = True
            if flagged == False:
                string += ' '
    elif event.name == 'enter':
        if startTyping:
            print(f"Key Pressed: {string} with the length of {len(string)}")
            startTyping = False
            string = ''
        else:
            startTyping = True
            string = ''
    elif event.name == 'esc':
        startTyping = False
        string = ''
    else:
        if startTyping:
            if len(event.name) == 1:
                string += event.name

                words_to_check = string.lower().split()

                for word in words_to_check:
                    if word in flagged_words_lower:

                        words_to_check.remove(word)

                        string = ' '.join(words_to_check)
                        string += ' '

                        for i in range(len(word)):
                            keyboard.send('backspace')

                        if len(string) == 1:
                            string = string[:-1]


            elif event.name == 'backspace':
                if len(string) > 0:
                    string = string[:-1]

def on_mouse_click(x, y, button, pressed):
    global startTyping
    global string


    if button == button.left and not pressed and startTyping == True:
        print(f"X pos is {x}, Y pos is {y}")
        #Positions of the chatBox
        if (x < 1042 or x > 1478) or (y < 929 or y > 968):
            keyboard.send('esc')
            startTyping = False
            string = ''
            print(f"Kliknuo si van polja za cet pa ga gasim")



import threading
import time
import psutil
import win32gui

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def is_app_selected(window_title):
    hwnd = win32gui.GetForegroundWindow()
    selected_window_title = win32gui.GetWindowText(hwnd)
    return selected_window_title == window_title



# Dovde je logika iza chat filtera i za proveru da li radi funkcije

###################################################################

# Odavde krece pokretanje programa i threading

def task(exit_flag):
    global startTyping
    global string


    stop_thread2 = threading.Event() # Event used to signal thread2 to stop

    def another_task():
        global startTyping
        global string

        while not stop_thread2.is_set():


            startTyping = False
            string = ''

            keyboard.on_press(on_key_press)


            mouse_listener = mouse.Listener(on_click=on_mouse_click)

            mouse_listener.start()

            while not stop_thread2.is_set():
                time.sleep(0.1)  # Adjust the sleep duration as needed

            keyboard.unhook_all()

            mouse_listener.stop()



    thread2 = None


    while not exit_flag.is_set(): # TODO button za menjanje promenljive
    # Checks if you're in a game
        process_name = "League of Legends.exe"
        if is_process_running(process_name):
            app_title = "League of Legends (TM) Client"  
            if is_app_selected(app_title):
                if thread2 is None or not thread2.is_alive():
                    thread2 = threading.Thread(target=another_task)
                    stop_thread2.clear()
                    thread2.start()
            else:
                if thread2 is not None and thread2.is_alive():
                    stop_thread2.set()  # Signal thread2 to stop
                    thread2.join()
                    thread2 = None

        time.sleep(2.5)  

        # Check for an exit condition
        if stop_thread2.is_set():
            if thread2 is not None and thread2.is_alive():
                stop_thread2.set()  # Signal thread2 to stop
                thread2.join()



###################################################################

# Create the exit flag as a shared variable
exit_flag = threading.Event()

# Create and start the first thread
thread = threading.Thread(target=task, args=(exit_flag,))
thread.start()


# ovde cemo staviti na klik dugmeta
# Wait for the termination signal (e.g., Ctrl+C)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("KeyboardInterrupt: Stopping the program.")
    exit_flag.set()
    # stop_thread2.set()

thread.join()

print("Program ended.")

