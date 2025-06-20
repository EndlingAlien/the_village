# in charge of the gui interface
import tkinter as tk
import game_db as db


def get_users_from_db():
    # result = db.MockDatabase().retrieve_all_users()
    # names = [name[0].capitalize() for name in result]
    names = [
        "michelle", "lester", "tommy", "joey", "val", "denise", "ricky", "wanda",
        "duke", "nancy", "carl", "edith", "marvin", "june", "hector", "gloria",
        "stan", "betty", "marge", "clint", "roger", "elaine", "barry", "brenda",
        "doug", "rhonda", "earl", "frank", "judy", "leo", "irene", "vinnie"
    ]
    return names


def show_all_users(event=None):
    user_list_window = Fake_Window(root, display_close=True, display_content=True, can_drag=True)
    user_list_window.user_list()


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

        # region Title Bar
        self.title_bar = tk.Frame(self.window, bg='#010881', relief='raised')
        self.title_label = tk.Label(self.title_bar, text='title text', fg="white", bg="#010881", font=('Modern DOS 9x16', 16))
        self.close_btn = tk.Frame(self.title_bar, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        self.close_label = tk.Label(self.close_btn, fg='black', bg='#C0C0C0', font=('Modern DOS 9x16', 15), text='X')
        self.title_bar.pack(fill="x")
        self.title_label.pack(side="left", padx=5)
        # endregion

        #region Drag Functions
        # Only allow dragging by the title bar
        def start_drag(event):
            self.window._drag_start_x = event.x
            self.window._drag_start_y = event.y

        def do_drag(event):
            x = self.window.winfo_x() + (event.x - self.window._drag_start_x)
            y = self.window.winfo_y() + (event.y - self.window._drag_start_y)
            self.window.place(x=x, y=y)
        #endregion

        #region Window Checks
        if self.display_content:
            self.content_area = tk.Label(self.window, bg="#C0C0C0")
            self.content_area.pack(fill="both", expand=True)

        if self.can_drag:
            self.title_bar.bind("<Button-1>", start_drag)
            self.title_bar.bind("<B1-Motion>", do_drag)

        if self.display_close:
            self.close_btn.pack(side='right', pady=2)
            self.close_label.pack()
            self.close_label.bind("<Button-1>", lambda e: self.close_window())
        #endregion

        self.window.place(x=450, y=220, width=250, height=250)
        # TODO: ______________TESTING AREA_______________
        #  Create logic for login btn/func,
        #  get input from user entry, password can be rando but required for vibes
        #  After 'Login page' done, create transition then home screen

    # Window Base [Error Pop Up] (currently styled as user not found)
    def create_error(self):
        # alert pop up window
        self.title_label.configure(text='ERROR: Text Here', font=('Modern DOS 9x16', 16), bg='#b8272c')
        self.window['highlightthickness'] = .5
        self.title_bar.configure(bg='#b8272c', height=50, highlightthickness=2, highlightbackground='black')
        canvas = tk.Canvas(self.window, bg='#C0C0C0', highlightthickness=0)

        # Place your error Frame on top
        error_frame = tk.Frame(canvas, bg='#C0C0C0', bd=2, highlightbackground='black', highlightthickness=2)
        error_window = canvas.create_window(20, 20, window=error_frame, anchor='nw', width=200, height=60)

        self.error_label = tk.Label(error_frame, text="ERROR: CRITICAL FAILURE", bg='#C0C0C0', fg='black', font=('Modern DOS 9x16', 13))
        self.error_label.pack(padx=10, pady=10)

        yes_frame = tk.Frame(canvas, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        yes_window = canvas.create_window(35, 100, window=yes_frame, anchor='nw', width=70, height=30)

        yes_btn_label = tk.Label(yes_frame, fg='black', bg='#C0C0C0', font=('Modern DOS 9x16', 11), text='Yes')
        yes_btn_label.pack()

        no_frame = tk.Frame(canvas, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        no_window = canvas.create_window(150, 100, window=no_frame, anchor='nw', width=60, height=30)

        no_btn_label = tk.Label(no_frame, fg='black', bg='#C0C0C0', font=('Modern DOS 9x16', 11), text='No')
        no_btn_label.pack()

        # Draw red angled bars
        for i in range(0, 400, 20):
            canvas.create_line(i, -5, i - 100, 230, fill='#b8272c', width=6)

            canvas.pack(fill='both', expand=True)

        self.window.place(x=450, y=220, width=250, height=180)

    #region Custom Windows
    def create_login_window(self):
        #login window for game
        self.title_label.configure(text='Welcome to BLiSS95', font=('Modern DOS 9x16', 16))
        instruct_label = tk.Label(self.content_area, fg='black', bg="#C0C0C0", text='Type a user name and password to log on to BLiSS95.',
                                  font=('Modern DOS 9x16', 13))
        instruct_label.pack()

        user_label = tk.Label(self.content_area, fg='black', bg="#C0C0C0", text='User name:', font=('Modern DOS 9x16', 13))
        user_label.place(x=40, y=45)

        password_label = tk.Label(self.content_area, fg='black', bg="#C0C0C0", text='Password:', font=('Modern DOS 9x16', 13))
        password_label.place(x=40, y=80)

        user_entry = tk.Entry(self.content_area, bd=1, relief='sunken', highlightthickness=.5)
        user_entry.place(x=130, y=45)

        password_entry = tk.Entry(self.content_area, bd=1, relief='sunken', highlightthickness=.5)
        password_entry.place(x=130, y=80)

        login_btn = tk.Frame(self.content_area, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        login_btn_label = tk.Label(login_btn, fg='black', bg='#C0C0C0', font=('Modern DOS 9x16', 13), text='Login')
        login_btn.place(x=385, y=75, width=65)
        login_btn_label.pack()

        user_list_btn = tk.Frame(self.content_area, bg='#C0C0C0', relief='raised', bd=2, highlightthickness=2, highlightbackground='black')
        user_list_label = tk.Label(user_list_btn, fg='black', bg='#C0C0C0', font=('Modern DOS 9x16', 13), text='Possible Users')
        user_list_btn.place(x=360, y=40)
        user_list_label.pack()
        user_list_label.bind("<Button-1>", show_all_users)

        self.window.place(x=750, y=420, width=520, height=160)

    def user_list(self):
        #returns a list of users
        self.title_label.configure(text="[DIR] USERS - C:\\BLiSS\\SYS")
        self.window.place(width=400, height=240)

        scrollbar = tk.Scrollbar(self.content_area, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        label = tk.Label(self.content_area, text='The list of users currently present.\nAre you?', font=('Modern DOS 9x16', 17), bg='#C0C0C0')
        label.pack(pady=15, padx=2)
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
        for item in users:
            listbox.insert(users.index(item), item)
        listbox.pack(pady=10)

    #endregion

    def close_window(self):
        #destroys the current window (the one clicked)
        self.window.destroy()


def login():
    # TODO: this will .get() the entry for users, passwords is for shits and giggles
    #  when player clicks the login_btn,
    #  if user in db, pop up window double checks they wanna log in
    #  if user not in db, pop up window asks, user not found, do you wanna make a new user
    #  login will close and the screen will 'transition' to home screen
    #  but should still require info to make it feel real
    pass


root = tk.Tk()
root.title("Welcome to BLiSS95")
root.configure(bg='#008080')  # classic teal Win95 background
root.minsize(width=500, height=310)

login_window = Fake_Window(root, display_content=True).create_login_window()




root.mainloop()
