from tkinter import *
import tkinter.font as tkfont
from functools import *
import os
import time


class MyNote(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.note_interface()
        self.update_category_buttons()

    def note_interface(self):

        # contains buttons for each new category
        self.categories_list = []

        # keep color: FFBB00
        self.top_color = "#BBD1EA"

    # main frame of task bar on top side
        top_frame = Frame(self.master, heigh="120", bg=self.top_color, bd="10")
        top_frame.pack_propagate(False)
        top_frame.pack(side=TOP, fill=X)

        self.MyNoteTitle = Label(top_frame, bg=self.top_color)
        self.photo0 = PhotoImage(file="title2.gif")
        self.MyNoteTitle.config(image=self.photo0)
        self.MyNoteTitle.pack(side=LEFT, padx=10)

    # icon frame
        icon_frame = Frame(top_frame, heigh="80", bg=self.top_color, bd="10")
        icon_frame.pack(fill=X, side=RIGHT)

        # save
        self.save_button = Button(icon_frame, command=lambda: self.save_note(self.file_name), width=25, height=25,
                                  bg=self.top_color, bd=0, relief=FLAT, activebackground=self.top_color)
        self.photo1 = PhotoImage(file="Save_black-512.gif")
        self.save_button.config(image=self.photo1)
        self.save_button.grid(padx=5, column=1, row=0)

        # delete
        self.delete_button = Button(icon_frame, command=lambda: self.delete_note(self.file_name),
                                    width=25, height=25, bg=self.top_color, bd=0, relief=FLAT,
                                    activebackground=self.top_color)
        self.photo2 = PhotoImage(file="trash.gif")
        self.delete_button.config(image=self.photo2)
        self.delete_button.grid(padx=5, column=2, row=0)

    # main frame of sidebar on left side
        self.sidebar_frame = Frame(self.master, width=250, bg='#e5e5e5')
        self.sidebar_frame.pack(fill=Y, side=LEFT)
        self.sidebar_frame.pack_propagate(True)

    # note title frame
        self.note_title_frame = Frame(self.master, bg="#f6f6f6", height=50)
        self.note_title_frame.pack(expand=False, fill=X)

        self.note_title_label = Label(self.note_title_frame, text="Home", font="Helvetica 15 bold",
                                      bg="#f6f6f6")
        self.note_title_label.pack(side=LEFT, padx=10, pady=10)

    # main frame of note taking area
        self.noteFrame = Frame(self.master, bg="#f6f6f6")
        self.noteFrame.pack(expand=True, fill=BOTH, pady=0, padx=0)

    # Home
        home_title = Frame(self.sidebar_frame, width="250", height="50", bg="#dbdbdb")
        home_title.pack()
        home_title.pack_propagate(False)

        self.home_button = Button(home_title, text="  Home", font="Verdana 11", bg="#dbdbdb",
                                             fg="#444444", command=self.home_menu, width="250", height="50", bd=0,
                                             anchor='w')
        self.home_button.pack(side=LEFT)
        self.color_change_hover(self.home_button)

    # "Categories" section
        # "categopries" label
        categories_title = Frame(self.sidebar_frame, width="250", height="50", bg="#dbdbdb")
        categories_title.pack()
        categories_title.pack_propagate(False)

        self.categories_main_button = Button(categories_title, text="  Notes    ⏶", font="Verdana 11", bg="#dbdbdb",
                                             fg="#444444", command=self.pack_unpack, width="250", height="50", bd=0,
                                             anchor='w')
        self.categories_main_button.pack(side=LEFT)
        self.color_change_hover(self.categories_main_button)

        # "New Category" box
        self.categories_new = Frame(self.sidebar_frame, width="250", height="50", bg="#e5e5e5")
        self.categories_new.pack()
        self.categories_new.pack_propagate(False)
        new_category_button = Button(self.categories_new, text="    ✚    " + "Create New Note", font="Verdana 10",
                                     width="250", height="50", fg="#444444", bg="#e5e5e5", relief="flat", anchor="w",
                                     bd=0, command=self.new_category)
        new_category_button.pack()

        self.pack_settings_button()

    # Home menu
    def home_menu(self):
        self.note_title_label.configure(text="Home")
        self.clear_note_frame()
        print("Home")

    # color change on hover over button
    def color_change_hover(self, widget):
        def on_enter(event):
            widget.configure(bg="#d1d1d1")
        def on_leave(event):
            widget.configure(bg="#dbdbdb")

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)


    def pack_unpack(self):
        if self.categories_new.winfo_manager():
            self.categories_main_button.configure(text="  Notes     ⏷")
            self.destroy_settings_button()

            self.categories_new.forget()
            for button in self.categories_list:
                self.category_frame.destroy()
                button.destroy()
                self.category_frame.destroy()

            self.pack_settings_button()
        else:
            self.categories_main_button.configure(text="  Notes     ⏶")
            self.destroy_settings_button()

            self.categories_new.pack(side=TOP)
            self.update_category_buttons()

    # packs buttons for each saved category in new session
    def update_category_buttons(self):

        for dir in os.listdir(os.getcwd() + "\\note_categories\\"):
            self.destroy_settings_button()
            self.create_category(dir, method="old")

    # "Settings" button
    def pack_settings_button(self):
        self.settingsButton = Frame(self.sidebar_frame, width="250", height="50", bg="#dbdbdb")
        self.settingsButton.pack()
        self.settingsButton.pack_propagate(FALSE)
        self.settings = Button(self.settingsButton, text="  Settings", font="Verdana 11", width="250",
                              height="50", fg="#444444", bg="#dbdbdb", relief="flat", anchor="w", bd=0,
                               command=self.settings_page)
        self.settings.pack()
        self.color_change_hover(self.settings)

    def destroy_settings_button(self):
        self.settingsButton.destroy()
        self.settings.destroy()

    # makes the new category
    def new_category(self):
        self.name_category()

    def create_category_event(self, event):
        name = self.category_name.get()

        # ensures name is >1 long and doesnt already exist
        if len(name) >= 1 and name.title()+".txt" not in os.listdir(os.getcwd() + "\\note_categories\\"):
            self.create_category(name, method="new")

    def create_category(self, name, method=None):

        name = name.title()

        try:
            self.category_name.destroy()
            self.delete_category.destroy()
            self.categoriesCustom.destroy()
            self.destroy_settings_button()

        except AttributeError:
            pass

        # frame that contains all user created categories
        self.category_frame = Frame(self.sidebar_frame, width="250", height="50", bg="pink")
        self.category_frame.pack()
        self.category_frame.pack_propagate(False)

        if name.lower().endswith(".txt"):
            name = name[:-4]

        # ☰ ⌦
        # adds the button and it's name to list to be accessed again
        self.categories_list.append(Button(self.category_frame, text="    ❐    "+name,
                                           command=partial(self.open_category, name), height="50", fg="#444444",
                                           bg="#e5e5e5", relief="flat", anchor="w", font="Verdana 10", width="250",
                                           bd=0))
        self.categories_list[-1].pack()

        if method == "new":
            self.open_category(name)
        elif method == "old":
            pass
        # re-packs settings button so its under all categories of notes.
        self.pack_settings_button()

    # acceses category clicked
    def open_category(self, category_name):

        # saves previously open note
        '''
        cwd = os.getcwd()
        title_get = self.note_title_label.cget("text")

        last_open = cwd + "\\note_categories\\" + title_get + ".txt"
        self.save_note(last_open)
        '''

        try:
            self.text_box_scrollbar.destroy()
            self.textbox.destroy()
        except AttributeError:
            pass

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.noteFrame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        self.textbox = Text(self.noteFrame, bg="#f6f6f6", fg="#444444", relief="flat", spacing3=8, wrap=WORD, bd=0,
                            yscrollcommand=self.text_box_scrollbar.set, width=1, height=1, undo=True)
        self.textbox.pack(fill=BOTH, expand=True, padx=15, pady=10)
        self.text_box_scrollbar.config(command=self.textbox.yview)

        # alters the tab length to only 4 spaces
        font = tkfont.Font(font=['font'])
        tab_width = font.measure(' ' * 5)
        self.textbox.config(tabs=(tab_width,))


        self.textbox.delete(1.0, END)

        cwd = os.getcwd()

        self.file_name = cwd + "\\note_categories\\" + category_name + ".txt"
        self.dir_name = cwd + "\\note_categories\\"

        # makes folder for categories if doesnt already exist
        try:
            os.makedirs(self.dir_name)
        except OSError:
            pass

        # gets contents of category if file exists. If doesnt exist, makes file for category
        try:
            with open(self.file_name, 'r')as file:
                contents = (list(file.readlines()))
                try:
                    del contents[-1]
                except IndexError:
                    pass
                contents = ''.join(contents)
                self.textbox.insert(INSERT, ''.join(contents))
        except FileNotFoundError:
            with open(self.file_name, 'w'):
                pass

        self.MyNoteTitle.configure(text=category_name)
        self.note_title_label.configure(text=category_name)
        print("\nNow editing: " + category_name)
        # print("in " + category_name + ": " + str(contents) + "\n")

    def clear_note_frame(self):
        try:
            self.textbox.forget()
            self.text_box_scrollbar.forget()
        except AttributeError:
            pass

    # save note automatically
    def save_note_auto(self):

        try:
            with open(self.file_name, 'w')as file:
                file.write(self.textbox.get(1.0, END))
        except AttributeError:
            pass
        print("Note saved automatically.")
        root.after(10000)
        self.save_note_auto()

    # save note manually
    def save_note(self, file_name):
        try:
            with open(file_name, 'w')as file:
                file.write(self.textbox.get(1.0, END))
        except AttributeError:
            pass
        print(file_name + " saved.")
        self.last_saved_update()

    # label notifying of last saved date and time
    def last_saved_update(self):
        # "last note saved: 3-15-17" on bottom of textbox for example
        try:
            self.last_saved_label.destroy()
        except AttributeError:
            self.last_saved_label = Label(self.note_title_frame, font="Verdana 7", bg="#f6f6f6", fg="#444444",
                                          text=(str(time.strftime("Last saved: " + '%B %d, %Y' + ' at ' + '%I:%M %p'))))
            self.last_saved_label.pack(side=RIGHT, expand=False, padx=10)

    def delete_note(self, file_name):
        os.remove(file_name)
        for cat in self.categories_list:
            cat.destroy()
            self.category_frame.destroy()

        root.after(1000)
        for dir in os.listdir(os.getcwd() + "\\note_categories\\"):
            self.destroy_settings_button()
            self.create_category(dir, method="old")

    def name_category(self):
        try:
            if self.categoriesCustom:
                self.categoriesCustom.destroy()
        except AttributeError:
            pass

        # provides entry widget for category name
        self.destroy_settings_button()

        self.categoriesCustom = Frame(self.sidebar_frame, width="250", bg="#e5e5e5")
        self.categoriesCustom.pack(fill=X)
        self.categoriesCustom.pack_propagate(False)

        self.category_name = Entry(self.categoriesCustom, font="Verdana 10", fg="#444444", bg="#f4f4f4",
                              relief=FLAT, width=16)
        self.category_name.bind("<Return>", self.create_category_event)
        self.category_name.grid(column=1, row=0, pady=14)

        self.delete_category = Button(self.categoriesCustom, font="Verdana 10", fg="#444444", bg="#e5e5e5",
                                      activebackground="#e5e5e5", relief=FLAT,
                                      text="    ✖    ", command=lambda: self.categoriesCustom.destroy(), bd=0)
        self.delete_category.grid(column=0, row=0, sticky=W)

        self.pack_settings_button()

    def settings_page(self):
        self.note_title_label.configure(text="Settings")
        self.clear_note_frame()
        Settings()


class Settings:
    def __init__(self):
        print("Settings")
        frame = Frame()
        frame.pack(side=TOP)

        label = Label(frame, text="Color Scheme")
        label.pack()



root = Tk()
root.title("My Notes")
root.minsize(600, 400)
root.geometry("820x580")
root.iconbitmap(default='note_icon_converted.ico')

a = MyNote(root)

root.mainloop()
