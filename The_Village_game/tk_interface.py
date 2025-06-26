# in charge of the gui interface
import tkinter as tk
import game_db as db
import re
from PIL import Image, ImageTk
import random
import time
import sys
from tkinter import messagebox
import time
import sys

# TODO: REMINDER SO WE DONT MAKE THE SAME BUG!!!!!!!!!!!
# When creating classmethods, win=self (from fake window), add to self variables in FakeWindow -> win.new_variable : func will have access
# example: win.error_label in create_error -> user_error can use error_label as self.error_label


def display_home_screen():
    clear_screen(root)
    
    bliss_img = Image.open('images/bg_with_icons.jpg')
    bliss_img = bliss_img.resize((1280, 720))
    photo = ImageTk.PhotoImage(bliss_img)


    bg_canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
    bg_canvas.pack(fill="both", expand=True)

    bg_canvas.create_image(0, 0, image=photo, anchor="nw")
    bg_canvas.image = photo  # Keep a reference!

    bottom_bar = tk.Frame(bg_canvas, width=4000, height=88, bg='#C0C0C0', highlightthickness=3, relief='raised')
    bg_canvas.create_window(0, 725, window=bottom_bar)

    time_label = tk.Label(bg_canvas, text=' 3:33 AM ', font=('Modern DOS 9x16', 20), fg='black', bg='#B3B3B3', highlightthickness=2, relief='sunken')
    bg_canvas.create_window(1212, 701, window=time_label)

    escape_label = tk.Label(bg_canvas,
                            text=' ESCAPE ',
                            font=('Modern DOS 9x16', 20),
                            fg='black',
                            bg='#B3B3B3',
                            highlightthickness=2,
                            relief='raised',
                            highlightbackground='black')
    bg_canvas.create_window(60, 701, window=escape_label, width=110, height=35)

    # region Interactive Icons
    log_icon = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    bg_canvas.move(log_icon, 260, 20)

    archive_icon = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='')
    bg_canvas.move(archive_icon, 485, 52)

    game_icon = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='')
    bg_canvas.move(game_icon, 350, 160)
    # endregion
    # region Non-interactive icons
    # Add invisible rectangles on this canvas [where they will click, remove outline for it to work]
    # region Icon
    dos_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    tree_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    people_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    phone_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    comp_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    occult_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    prog_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    lan_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    folder_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    earth_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    cam_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    aol_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    trash_rect = bg_canvas.create_rectangle(50, 50, 120, 120, fill='', outline='yellow')
    # endregion
    # region Icon Placement
    bg_canvas.move(dos_rect, -23, -40)
    bg_canvas.move(tree_rect, -23, 78)
    bg_canvas.move(people_rect, -23, 180)
    bg_canvas.move(phone_rect, -23, 290)
    bg_canvas.move(comp_rect, -23, 415)
    bg_canvas.move(occult_rect, -23, 530)
    bg_canvas.move(prog_rect, 80, -40)
    bg_canvas.move(lan_rect, 80, 78)
    bg_canvas.move(folder_rect, 80, 180)
    bg_canvas.move(earth_rect, 80, 290)
    bg_canvas.move(cam_rect, 80, 415)
    bg_canvas.move(aol_rect, 80, 530)
    bg_canvas.move(trash_rect, 1122, 530)

    # endregion

    # endregion

    def clicked_game(event):
        game_window = Fake_Window(root, display_close=True, display_content=False).create_game_window()

    def clicked_archive(event):
        archive_window = Fake_Window(root, display_content=True, display_close=True).create_archive_window()

    bg_canvas.tag_bind(game_icon, '<Button-1>', clicked_game)
    bg_canvas.tag_bind(archive_icon, '<Button-1>', clicked_archive)



# region Functions
def get_users_from_db():
    result = db.MockDatabase().retrieve_all_users()
    names = [name[0].capitalize() for name in result]
    return names


def show_all_users(event=None):
    user_list_window = Fake_Window(root, display_close=True, display_content=True, can_drag=True)
    user_list_window.user_list()


def clear_screen(parent):
    for widget in root.winfo_children():
        widget.destroy()


# endregion

# region Transition to Home Screen

# region Typewriter + bsod_message
def typewriter_tk_advanced(text_widget, text, char_delay=30, line_delay=500):
    lines = text.split('\n')
    current_line = 0

    def insert_text(content):
        text_widget.configure(state='normal')
        text_widget.insert('end', content)
        text_widget.see('end')  # Auto-scroll to bottom
        text_widget.configure(state='disabled')

    def print_line_slow(line, char_idx=0):
        if char_idx < len(line):
            insert_text(line[char_idx])
            text_widget.after(char_delay, print_line_slow, line, char_idx + 1)
        else:
            insert_text('\n')
            text_widget.after(line_delay, print_next_line)

    def print_line_fast(line):
        insert_text(line + '\n')
        text_widget.after(line_delay, print_next_line)

    def print_next_line():
        nonlocal current_line
        if current_line >= len(lines):
            return
        line = lines[current_line]
        current_line += 1

        if line.startswith('>>'):
            print_line_slow(line)
        else:
            print_line_fast(line)

    print_next_line()


POST_ramble = (
    "BOOT COMPLETE. STANDBY FOR SYSTEM CHECK...\n[OK] Memory Stable\n"
    "[OK] Neural Echoes Contained\n[OK] Retinal Burn Offset Calibrated\n[OK] Subconscious Firewall Deployed\n[OK] Brainwave Interference Suppressed\n"
    "[OK] Sensory Dampeners Calibrated\n\n"
    "[WARNING] Unauthorized Presence Detected\n\n>> You shouldn't be here.\n>> They’ll see you now.\n\n"
    ">> You think this is a village?\n>> NO.\n\n> AUTHENTICATION BYPASSED :: OVERRIDE [COVEN-LEVEL]\n"
    "\n>> It’s a mouth.\n>> It’s hungry.\n>> It's not worship-it was never worship\n\n"
    "\n> BIOS LOCKED BY [HIGH PRIEST PERMISSION]\n\n>> They're trying to kick me out\n"
    ">> You need to read carefully\n\n\n> SYSTEM ROOT FOUND IN FLESH_DRIVE:\\village_core.sys"
    "\n\n>> They think the lights are gods.\n>> They're just teeth with rules.\n\n"
    ">> I saw what’s under the chapel.\n\n>> YOU ARE THE VARIABLE\n>> They've been waiting for a change in "
    "the pattern\n>> You think you’re playing a game\n\n>> THIS ISNT A GAME\n>> THIS ISNT A GAME"
    "\n>> THIS ISNT A GAME\n>> THIS ISNT A GAME\n>> THIS ISNT A GAME\n\n> CLOCK SYNC FAILED — SYSTEM NOW ON VILLAGE TIME"
    "\n\n>> You need to leave. YOU NEED TO—\n\nCONNECTION TERMINATED.SYSTEM RESTORING DEFAULT MESSAGE...\n\n"
    "> NETWORK CONNECTION TO: ritual.node — [SECURE]\n> FORCED RESTART INITIATED\n> FIRMWARE LOCKED :: ESCAPE IMPOSSIBLE"
    "\n\n> GLORY TO THE VILLAGE\n> GLORY TO THE BEAMS\n> GLORY TO THE MEAT\n\n> END OF LINE _\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
)

bsod_message = ("*** STOP: 0x0000DEAD (0xC0DEFEED, 0xBAADF00D, 0xDEADC0DE, 0xFEEDFACE)\n\nA critical error has occurred in the BLiSS95 Kernel.\n"
                "The system has encountered an unrecoverable fault in the Cultic Process Handler.\n\nMemory corruption detected in sector 13:\n"
                "Unable to verify ritual integrity.\nThe Village Protocol has been breached.\n\n>>> DO NOT ATTEMPT TO RESTART <<<\n\n"
                "If you see this screen, your presence is already logged.\nContact your Administrator of the Beams for assistance.\n"
                "Press any key to initiate the Rite of Renewal...\n\n*** SYSTEM HALTED ***")


# endregion


def transition_to_home(event=None):
    clear_screen(root)
    root.configure(bg='black')

    post_label = tk.Label(root,
                          text="BLiSS95 Boot v2.3\nPerforming Memory Check... OK\nLoading Archetype Protocol... █▒▒▒▒▒▒▒▒▒",
                          font=('Modern DOS 9x16', 20),
                          bg='black',
                          fg='white',
                          justify='left')
    post_label.pack(side='top', anchor='w')

    output_frame = tk.Frame(root, bg='black')
    output_frame.pack(side='top', anchor='w')

    output_text = tk.Text(root,
                          font=('Modern DOS 9x16', 18),
                          bg='black',
                          fg='red',
                          insertbackground='white',
                          wrap='word',
                          borderwidth=0,
                          highlightthickness=0,
                          padx=0,
                          pady=0)

    output_text.pack(fill='both', expand=True, anchor='n', pady=0)
    output_text.configure(state='disabled')

    root.after(1500, lambda: post_label.configure(text="BLiSS95 Boot v2.3\nPerforming Memory Check... OK\nLoading Archetype Protocol... ██▒▒▒▒▒▒▒▒"))
    root.after(3000, lambda: post_label.configure(text="BLiSS95 Boot v2.3\nPerforming Memory Check... OK\nLoading Archetype Protocol... █████▒▒▒▒▒"))
    root.after(6000, lambda: post_label.configure(text="BLiSS95 Boot v2.3\nPerforming Memory Check... OK\nLoading Archetype Protocol... █████████▒"))
    root.after(6300, lambda: post_label.destroy())

    root.after(7300, lambda: typewriter_tk_advanced(output_text, POST_ramble, char_delay=25, line_delay=380))
    root.after(46000, lambda: bsod_transition())
    root.after(49200, lambda: load_home())


def bsod_transition():
    clear_screen(root)
    root.configure(bg='#1e71d4')
    post_label = tk.Label(root,
                          text=bsod_message,
                          font=('Modern DOS 9x16', 30),
                          bg='#1e71d4',
                          fg='white')
    post_label.pack(fill='both', expand=True)


def load_home():
    clear_screen(root)
    root.configure(bg='black')
    welcome = tk.Label(root, text="Welcome Home", font=('Modern DOS 9x16', 20),
                       bg='#008080', fg='white', justify='center')

    # fade from black to win95 teal
    colors = ['#20181f', '#302c3f', '#2f4661', '#1a6379', '#008080']
    delay = 1000  # 1 second

    for i, color in enumerate(colors):
        root.after(delay * (i + 1), lambda c=color: root.configure(bg=c))

    root.after(6300, lambda: welcome.pack(fill='both', expand=True))
    root.after(7000, lambda: display_home_screen())


# endregion

class Fake_Window(tk.Frame):
    def __init__(self, parent, display_close=False, display_content=False, can_drag=False, *args, **kwargs):
        """
        Makes an empty window for configuring [looks like Windows-95]
        :param parent: The tk window
        :param title: Title of the window
        :param args: Args for tk
        :param kwargs: Kwargs for tk
        """
        super().__init__(parent, *args, **kwargs)
        self.window = tk.Frame(parent, bg="#C0C0C0", bd=2, relief="raised", highlightthickness=2, highlightbackground='black')

        self.display_close = display_close
        self.display_content = display_content
        self.can_drag = can_drag

        # Window Base [Error Pop Up]
        # region Title Bar
        self.title_bar = tk.Frame(self.window, bg='#010881', relief='raised')
        self.title_label = tk.Label(self.title_bar, text='title text', fg="white", bg="#010881", font=('Modern DOS 9x16', 16))
        self.close_btn = tk.Frame(self.title_bar, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        self.close_label = tk.Label(self.close_btn, fg='black', bg='#C0C0C0', font=('Modern DOS 9x16', 15), text='X')
        self.title_bar.pack(fill="x")
        self.title_label.pack(side="left", padx=5)

        # endregion

        self.content_area = tk.Label(self.window, bg="#C0C0C0")

        # region Drag Functions
        # Only allow dragging by the title bar
        def start_drag(event):
            self.window._drag_start_x = event.x
            self.window._drag_start_y = event.y

        def do_drag(event):
            x = self.window.winfo_x() + (event.x - self.window._drag_start_x)
            y = self.window.winfo_y() + (event.y - self.window._drag_start_y)
            self.window.place(x=x, y=y)

        # endregion

        # region Window Checks
        if self.display_content:
            self.content_area.pack(fill="both", expand=True)

        if self.can_drag:
            self.title_bar.bind("<Button-1>", start_drag)
            self.title_bar.bind("<B1-Motion>", do_drag)

        if self.display_close:
            self.close_btn.pack(side='right', pady=2)
            self.close_label.pack()
            self.close_label.bind("<Button-1>", lambda e: self.close_window())
        # endregion
        # self.window.place(x=450, y=220, width=250, height=250)

    # Window Base [Error Pop-Up]
    @classmethod
    def create_error(cls, parent):
        # Create the base Fake_Window instance
        win = cls(parent, display_close=False, display_content=False, can_drag=False)

        # Title bar and label styling
        win.title_label.configure(text='ERROR: Error Code', font=('Modern DOS 9x16', 16), bg='#b8272c')
        win.title_bar.configure(bg='#b8272c', height=50, highlightthickness=2, highlightbackground='black')
        win.window['highlightthickness'] = .5

        # Create the canvas
        win.error_canvas = tk.Canvas(win.window, bg='#C0C0C0', highlightthickness=0)
        win.error_canvas.pack(fill='both', expand=True)

        # Red angled bars
        for i in range(0, 400, 20):
            win.error_canvas.create_line(i, -5, i - 100, 230, fill='#b8272c', width=6)

        # Error message area
        win.error_frame = tk.Frame(win.error_canvas, bg='#C0C0C0', bd=2, highlightbackground='black', highlightthickness=2)
        win.error_canvas.create_window(20, 20, window=win.error_frame, anchor='nw', width=200, height=60)

        win.error_label = tk.Label(
            win.error_frame,
            text='error message',
            bg='#C0C0C0',
            fg='black',
            font=('Modern DOS 9x16', 13)
        )
        win.error_label.pack(padx=10, pady=10)

        # "Yes" button
        yes_frame = tk.Frame(win.error_canvas, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        win.error_canvas.create_window(35, 100, window=yes_frame, anchor='nw', width=70, height=30)

        win.yes_btn_label = tk.Label(yes_frame, text='Yes', font=('Modern DOS 9x16', 13), bg='#C0C0C0', fg='black')
        win.yes_btn_label.pack()

        # "No" button
        no_frame = tk.Frame(win.error_canvas, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        win.error_canvas.create_window(165, 100, window=no_frame, anchor='nw', width=60, height=30)

        win.no_btn_label = tk.Label(no_frame, text='No', font=('Modern DOS 9x16', 13), bg='#C0C0C0', fg='black')
        win.no_btn_label.pack()

        # Final window placement (optional override here)
        win.window.place(x=450, y=220, width=250, height=180)

        return win

    # Window Base [Pop-Up]
    @classmethod
    def create_pop_up(cls, parent):
        # Create the base Fake_Window instance
        win = cls(parent, display_close=False, display_content=False)
        win.window.place(x=870, y=410, width=220, height=145)

        win.title_label.configure(text='Title text', bg='#F2B914', fg='black')
        win.title_bar.configure(bg='#F2B914')
        win.warning_label = tk.Label(win.window,
                                     text='You can fit 15 words\nin the space of this\npop up box word word',
                                     font=('Modern DOS 9x16', 15),
                                     bg='#C0C0C0')
        win.warning_label.pack(pady=5)

        btn_frame = tk.Frame(win.window, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        btn_frame.place(x=85, y=93)
        win.btn_label = tk.Label(btn_frame, text='OK', font=('Modern DOS 9x16', 17), bg='#C0C0C0')
        win.btn_label.pack()
        win.btn_label.bind("<Button-1>", lambda e: win.close_window())

        return win

    # region Custom Windows
    def create_game_window(self):
        self.window.place(x=200, y=100, width=900, height=520)
        self.title_label.configure(text="The_Village")

        #region Inventory Section
        inventory_label_frame = tk.Frame(self.window, bg='black', highlightthickness=2, highlightbackground='white')
        inventory_label_frame.place(x=0, y=33, width=300, height=40)

        inventory_label = tk.Label(inventory_label_frame, text='Inventory:', font=('Modern DOS 9x16', 17), bg='black', fg='white')
        inventory_label.pack(pady=5)

        inventory_item_frame = tk.Frame(self.window, bg='black', highlightthickness=2, highlightbackground='white')
        inventory_item_frame.place(x=0, y=73, width=300, height=200)

        inventory_tools_label = tk.Label(inventory_item_frame,
                                   text='Tools:',
                                   font=('Modern DOS 9x16', 20, 'underline'),
                                   bg='black',
                                   fg='Red',
                                   justify='left')
        inventory_tools_label.place(x=0, y=0)
        #TODO Tool inventory items in list here, add as they collect
        inventory_tools = tk.Label(inventory_item_frame, text='Key\nScrewdriver\nHammer\nKnife', font=('Modern DOS 9x16', 17), bg='black', fg='white', justify='left')
        inventory_tools.place(x=0, y=22)

        inventory_docs_label = tk.Label(inventory_item_frame, text='Documents:', font=('Modern DOS 9x16', 20, 'underline'), bg='black', fg='red'
                                  , justify='left')
        inventory_docs_label.place(x=0, y=100)
        #TODO Documents inventory items in list here, add as they collect
        inventory_docs = tk.Label(inventory_item_frame, text='Decoder\nBible\nLetter', font=('Modern DOS 9x16', 17), bg='black', fg='white'
                                  , justify='left')
        inventory_docs.place(x=0, y=123)

        inventory_other_label = tk.Label(inventory_item_frame, text='Other:', font=('Modern DOS 9x16', 20, 'underline'), bg='black', fg='red', justify='left')
        inventory_other_label.place(x=180, y=0)
        #TODO Other inventory items in list here, add as they collect
        inventory_other = tk.Label(inventory_item_frame, text='Mask', font=('Modern DOS 9x16', 17), bg='black', fg='white', justify='left')
        inventory_other.place(x=180, y=23)

        inventory_vials_label = tk.Label(inventory_item_frame, text='Vials:', font=('Modern DOS 9x16', 20, 'underline'), bg='black', fg='red'
                                   , justify='left')
        inventory_vials_label.place(x=180, y=100)
        #TODO vials inventory items in list here, add as they collect
        inventory_vials = tk.Label(inventory_item_frame, text='Red\nBlue\nGreen', font=('Modern DOS 9x16', 17), bg='black', fg='white'
                                  , justify='left')
        inventory_vials.place(x=180, y=123)
        #endregion

        #region Choices Section
        choice_label_frame = tk.Frame(self.window, bg='black', highlightthickness=2, highlightbackground='white')
        choice_label_frame.place(x=0, y=273, width=300, height=40)

        choice_label = tk.Label(choice_label_frame, text='What are you going to do?:', font=('Modern DOS 9x16', 17), bg='black', fg='white')
        choice_label.pack(pady=5)

        choices_frame = tk.Frame(self.window, bg='black', highlightthickness=2, highlightbackground='white')
        choices_frame.place(x=0, y=313, width=300, height=200)

        choice_listbox = tk.Listbox(choices_frame,
                                    activestyle='none',
                                    height=6,
                                    width=30,
                                    font=('Modern DOS 9x16', 19),
                                    justify='center',
                                    bg='black',
                                    fg='white',
                                    selectbackground='red',
                                    selectforeground='black')

        #TODO: Where you plugin options, from main.py
        choices = ['Go Forward', 'Go Left', 'Go Right', 'Use the Vials', 'Use the Mask']  # For testing purposes

        def select_choice():
            cs = choice_listbox.curselection()
            # TODO: This is the users int choice for db *0 = 1, 1 = 2, 2 = 3, etc*
            # cant force listbox to start at index 1
            user_choice = cs[0]
            for i in cs:
                choice_name = choice_listbox.get(i)
                print(f"Choice: {user_choice}:{choice_name}")  # For Testing purposes
                user_choice_label.configure(text=choice_name)

        for item in choices:
            choice_listbox.insert(choices.index(item), item)

        choice_listbox.pack(pady=10)
        choice_listbox.bind("<<ListboxSelect>>", lambda e: select_choice())

        check_choice_label = tk.Label(choices_frame, text="You've selected:", font=('Modern DOS 9x16', 15), bg='black', fg='white')
        check_choice_label.pack(side='left', anchor='n')

        user_choice_label = tk.Label(choices_frame, text='', font=('Modern DOS 9x16', 15), bg='black', fg='white')
        user_choice_label.pack(side='left', anchor='n')
        
        #region Funcs
        def on_enter(event):
            event.widget.configure(bg='red')
            event.widget.configure(fg='black')

        def on_leave(event):
            event.widget.configure(bg='black')
            event.widget.configure(fg='white')

        # TODO This will 'confirm' choice, progressing the game to next scene
        def clicked_choice(event):
            event.widget.configure(bg='black')
            event.widget.configure(fg='green')
        #endregion
        
        confirm_choice_frame = tk.Frame(choices_frame, bg='black')
        confirm_choice_frame.place(x=100, y=170, width=100, height=24)

        confirm_choice = tk.Label(confirm_choice_frame, text="Continue?", font=('Modern DOS 9x16', 15), bg='black', fg='white', width=20, height=10)
        confirm_choice.pack()
        confirm_choice.bind("<Enter>", on_enter)
        confirm_choice.bind("<Leave>", on_leave)
        confirm_choice.bind("<Button-1>", clicked_choice)
        #endregion

        #region Dialogue Section
        ascii_frame = tk.Frame(self.window, bg='black', highlightthickness=2, highlightbackground='white')
        ascii_frame.place(x=300, y=33, width=593, height=327)
        # TODO Will need to configure Ascii in separate .py file to assure 'game scenes' look right
        ascii_box = tk.Text(ascii_frame,
                            bg="black",
                            fg="white",
                            font=('Modern DOS 9x16', 10),
                            wrap="none",
                            highlightthickness=0,
                            height=25,  # Enough to fit the full image
                            width=50)  # Adjust for art's max width
        # TODO plugin Ascii art here
        ascii_box.insert("1.0", r'''  
              ////\\\\\
              |      |
             @  O  O  @
              |  ~   |         \__
               \ -- /          |\ |
             ___|  |___        | \|
            /          \      /|__|
           /            \    / /
          /  /| .  . |\  \  / /
         /  / |      | \  \/ /
        <  <  |      |  \   /
         \  \ |  .   |   \_/
          \  \|______|
            \_|______|
              |      |
              |  |   |
              |  |   |
              |__|___|
              |  |  |
              (  (  |
              |  |  |
              |  |  |
             _|  |  |
         cccC_Cccc___)
        ''')

        ascii_box.config(state="disabled")
        ascii_box.pack(expand=True)

        dialogue_frame = tk.Frame(self.window, bg='black', highlightthickness=2, highlightbackground='white')
        dialogue_frame.place(x=300, y=360, width=593, height=153)
        # TODO plugin dialogue/follow_up/locked_text as text here
        dialogue_box = tk.Label(dialogue_frame,
                            text="You decide to accept the rancher's offer and follow him inside. He leads you to a small dining table and hands you a drink, before promptly entering the kitchen to prep some food.",
                            bg="black", fg="white",
                            font=('Modern DOS 9x16', 17),
                            wraplength=550,
                            justify="left")
        dialogue_box.pack()
        #endregion

    def create_archive_window(self):
        self.window.place(x=350, y=100, width=530, height=400)
        self.title_label.configure(text="The_Archive")
        self.content_area.configure(bg='black')

        title_frame = tk.Frame(self.window, bg='black', highlightthickness=2, highlightbackground='white')
        title_frame.place(x=3, y=35, width=517,)
        title_label = tk.Label(title_frame, text='What truth do you wish to seek?', font=('Modern DOS 9x16', 26), bg='black', fg='white', height=2)
        title_label.pack()
        # TODO Lead to endings Section (ending catalogue)
        endings_frame = tk.Frame(self.window, bg='red')
        endings_frame.place(x=30, y=150, width=120, height=185)
        endings_frame_label = tk.Label(self.window, text='Endings', font=('Modern DOS 9x16', 20), bg='black', fg='white')
        endings_frame_label.place(x=45, y=350)
        endings_art = tk.Text(endings_frame,
                            bg="darkred",
                            fg="black",
                            font=('Modern DOS 9x16', 6, 'bold'),
                            wrap="none",
                            highlightthickness=0,
                            height=30,  # Enough to fit the full image
                            width=80)  # Adjust for art's max width

        endings_art.insert("1.0", r'''
        
                                            .""--.._
                                           []      `'--.._
                                           ||__           `'-,
                                         `)||_ ```'--..       \
                     _                    /|//}        ``--._  |
                  .'` `'.                /////}              `\/
                 /  .""".\              //{///    
                /  /_  _`\\            // `||
                | |(_)(_)||          _//   ||
                | |  /\  )|        _///\   ||
                | |L====J |       / |/ |   ||
               /  /'-..-' /    .'`  \  |   ||
              /   |  :: | |_.-`      |  \  ||
             /|   `\-::.| |          \   | ||
           /` `|   /    | |          |   / ||
         |`    \   |    / /          \  |  ||
        |       `\_|    |/      ,.__. \ |  ||
        /                     /`    `\ ||  ||
                   .         /        \||  ||
                             |         |/  ||
                 /           |         (   ||
                 .           /          )  ||
                  \          |             ||
                  |          /             ||
                 /          |              ||
                |           /              ||
          \    /`           |              ||
           \  |             \              ||
 
''')
        endings_art.config(state="disabled")
        endings_art.place(x=-40, y=0)
        # TODO Lead to items section (key items dict in main.py)
        items_frame = tk.Frame(self.window, bg='#6aa84e')
        items_frame.place(x=200, y=150, width=120, height=185)
        items_frame_label = tk.Label(self.window, text='Items', font=('Modern DOS 9x16', 20), bg='black', fg='white')
        items_frame_label.place(x=225, y=350)
        items_art = tk.Text(items_frame,
                              bg="#6aa84e",
                              fg="black",
                              font=('Modern DOS 9x16', 8, 'bold'),
                              wrap="none",
                              highlightthickness=0,
                              height=30,  # Enough to fit the full image
                              width=30)  # Adjust for art's max width
        items_art.insert("1.0", r'''
        
        
        
    ,'/        \`.
    : (         ) :       
    |  `._____,'  |        
    |             |       
    |   _     _   |           
    | <)_(> <)_(> |      
    |      |      |   
    |      |      | 
    :  |.`.|,'/|  : 
    :  | \,`./ |  ; 
    \  :       ; /    
     \  \/\_/\/ /   
      \  `---' /    
       `.    ,'
         ` .'
                ''')
        items_art.config(state="disabled")
        items_art.pack()
        # TODO Create 'verses' dict for lore
        lore_frame = tk.Frame(self.window, bg='#3b78d8')
        lore_frame.place(x=370, y=150, width=120, height=185)
        lore_frame_label = tk.Label(self.window, text='Verses', font=('Modern DOS 9x16', 20), bg='black', fg='white')
        lore_frame_label.place(x=390, y=350)
        lore_art = tk.Text(lore_frame,
                            bg="#3b78d8",
                            fg="black",
                            font=('Modern DOS 9x16', 6, 'bold'),
                            wrap="none",
                            highlightthickness=0,
                            height=30,  # Enough to fit the full image
                            width=50)  # Adjust for art's max width
        lore_art.insert("1.0", r'''
  __________________________
  /\                         \
 /  \            ____         \
/ \/ \          /\   \         \
\ /\  \         \ \   \         \
 \  \  \     ____\_\   \______   \
  \   /\\   /\                \   \
   \ /\/ \  \ \_______    _____\   \
    \\/ / \  \/______/\   \____/    \
     \ / /\\         \ \   \         \
      \ /\/ \         \ \   \         \
       \\/ / \         \ \   \         \
        \ /   \         \ \   \         \
         \\  /\\         \ \   \         \
          \ /\  \         \ \___\         \
           \\    \         \/___/          \
            \  \/ \                         \
             \ /\  \_________________________\
              \  \ / ______________________  /
               \  / ______________________  /
                \/_________________________/

                        ''')
        lore_art.config(state="disabled")
        lore_art.pack()


    def create_login_window(self):
        # login window for game
        self.title_label.configure(text='Welcome to BLiSS95', font=('Modern DOS 9x16', 16))
        instruct_label = tk.Label(self.content_area, fg='black', bg="#C0C0C0", text='Type a user name and password to log on to BLiSS95.',
                                  font=('Modern DOS 9x16', 13))
        instruct_label.pack()

        user_label = tk.Label(self.content_area, fg='black', bg="#C0C0C0", text='User name:', font=('Modern DOS 9x16', 13))
        user_label.place(x=40, y=45)

        password_label = tk.Label(self.content_area, fg='black', bg="#C0C0C0", text='Password:', font=('Modern DOS 9x16', 13))
        password_label.place(x=40, y=80)

        self.user_entry = tk.Entry(self.content_area, bd=1, relief='sunken', highlightthickness=.5, font=('Modern DOS 9x16', 15))
        self.user_entry.place(x=130, y=45)

        password_entry = tk.Entry(self.content_area, bd=1, relief='sunken', highlightthickness=.5, font=('Modern DOS 9x16', 15), show="*")
        password_entry.place(x=130, y=80)

        def user_check(event=None):
            user_name = self.user_entry.get()
            password = password_entry.get()

            # Check for empty, whitespace, or invalid username (only letters allowed)
            if not user_name.strip() or not re.fullmatch(r"[A-Za-z]+", user_name):
                Fake_Window.create_pop_up(root).invalid_name_pop()
                return

            # Check if password is empty or too short
            if not password.strip() or len(password) < 4:
                Fake_Window.create_pop_up(root).invalid_pass_pop()
                return

            # Proceed with user existence check
            if db.MockDatabase().check_if_user_exists(user_name.lower()):
                Fake_Window.create_pop_up(root).user_login_pop(user_name)
            else:
                Fake_Window.create_error(root).user_error(user_name)

        login_btn = tk.Frame(self.content_area, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        login_btn_label = tk.Label(login_btn, fg='black', bg='#C0C0C0', font=('Modern DOS 9x16', 13), text='Login')
        login_btn.place(x=385, y=75, width=65)
        login_btn_label.pack()
        login_btn_label.bind("<Button-1>", user_check)

        user_list_btn = tk.Frame(self.content_area, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        user_list_label = tk.Label(user_list_btn, fg='black', bg='#C0C0C0', font=('Modern DOS 9x16', 13), text='Possible Users')
        user_list_btn.place(x=360, y=40)
        user_list_label.pack()
        user_list_label.bind("<Button-1>", show_all_users)

        self.window.place(x=400, y=300, width=520, height=160)

    def user_error(self, entry_value):
        self.title_label.configure(text="We haven't met before?", font=('Modern DOS 9x16', 14))
        self.error_label.configure(text="A name is missing.\nIs it yours?")

        def pressed_yes(event=None):
            self.title_label.configure(text=f"Hello, {entry_value.capitalize()}.")
            self.error_label.configure(text="Shall we proceed?")
            self.yes_btn_label.configure(text="Ready")
            self.no_btn_label.configure(text="Wait")
            root.configure(bg='#008080')
            self.yes_btn_label.bind("<Button-1>", lambda e: transition_to_home())
            self.no_btn_label.bind("<Button-1>", no_again)

        def pressed_no(event=None):
            self.no_btn_label.bind("<Button-1>", lambda e: self.close_window())

        def no_again(event=None):
            self.title_label.configure(text="ӺɆȺⱤ ⱲłⱠⱠ ɃɆ ȾⱧł₦Ɇ Ɇ₦ɆᛗɎ", font=('Modern DOS 9x16', 13))
            self.error_label.configure(text="₳rE̴̛̻͓̘̹͖̯̫̊̓̋ͫͭ̑ͭ͠  yO͎Ʉ sɄR̷̨̟͎͓̥̳͇̯̼͋̂̐͂̊͟e", font=('Modern DOS 9x16', 16))
            root.configure(bg='black')
            self.yes_btn_label.configure(text="aǤȺł₦")
            self.no_btn_label.configure(text="ⱤɄ₦")
            self.no_btn_label.bind("<Button-1>", lambda e: self.close_window())
            self.yes_btn_label.bind("<Button-1>", pressed_yes)

        self.yes_btn_label.bind("<Button-1>", pressed_yes)
        self.no_btn_label.bind("<Button-1>", pressed_no)
        x, y = self.random_x_y()
        self.window.place(x=x, y=y, width=270, height=180)

    def user_list(self):
        # returns a list of users
        self.title_label.configure(text="[DIR] USERS - C:\\BLiSS\\SYS")
        self.window.place(x=450, y=260, width=400, height=240)

        scrollbar = tk.Scrollbar(self.content_area, orient="vertical")

        list_label = tk.Label(self.content_area, text='The list of users currently present.\nAre you?', font=('Modern DOS 9x16', 17), bg='#C0C0C0')
        list_label.pack(pady=15, padx=2)
        listbox = tk.Listbox(self.content_area,
                             activestyle='none',
                             height=6,
                             width=20,
                             font=('Modern DOS 9x16', 16),
                             justify='center',
                             bg='#C0C0C0',
                             yscrollcommand=scrollbar.set)

        users = get_users_from_db()
        scrollbar.config(command=listbox.yview)
        print(len(users))

        for item in users:
            listbox.insert(users.index(item), item)
        listbox.pack(pady=10)

        if len(users) > 6:
            scrollbar.pack(side="right", fill="y")

    # region Pop-Ups
    def invalid_name_pop(self):
        self.title_label.configure(text="Watchers Do Not Approve", font=('Modern DOS 9x16', 13))
        self.warning_label.configure(text='You have entered either:\nnothing, or unique symbols.\nTell us your name.')
        x, y = self.random_x_y()
        self.window.place(x=x, y=y, width=230, height=145)

    def invalid_pass_pop(self):
        self.title_label.configure(text="You Withhold the Key", font=('Modern DOS 9x16', 13))
        self.warning_label.configure(text='Enter the password.\nFour keys.\nWe wait for you.')
        x, y = self.random_x_y()
        self.window.place(x=x, y=y, width=230, height=145)

    def user_login_pop(self, entry_value):
        self.title_label.configure(text=f"Welcome back, {entry_value.capitalize()}.", font=('Modern DOS 9x16', 13))
        self.warning_label.configure(text="The village watches.\nThe gates open.\nYour journey begins.")
        self.btn_label.bind("<Button-1>", lambda e: transition_to_home())
        self.window.place(x=500, y=350, width=230, height=145)

    # endregion
    # endregion

    def close_window(self):
        root.configure(bg='#008080')
        # destroys the current window (the one clicked)
        self.window.destroy()

    def random_x_y(self):
        x = random.randint(360, 800)  # Horizontal range
        y = random.randint(200, 400)  # Vertical range
        return x, y


root = tk.Tk()
root.title("Welcome to BLiSS95")
root.configure(bg='#008080')  # classic teal Win95 background
WIDTH = 1280
HEIGHT = 720
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

#login_window = Fake_Window(root, display_content=True).create_login_window()

display_home_screen()
#test_win = Fake_Window(root, display_content=True, display_close=True).create_archive_window()
root.mainloop()
