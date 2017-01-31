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

        self.categories_list = []

        self.top_color = "#FFBB00"
        # tiny bit darker: "#9BA0A1"

    # main frame of task bar on top side
        top_frame = Frame(self.master, heigh="110", bg=self.top_color, bd="10")
        top_frame.pack_propagate(False)
        top_frame.pack(side=TOP, fill=X)

        self.MyNoteTitle = Label(top_frame, bg=self.top_color, fg="#000000")
        self.photo0 = PhotoImage(file="title2.gif")
        self.MyNoteTitle.config(image=self.photo0)
        self.MyNoteTitle.pack(side=LEFT)

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
        self.sidebar_frame.pack(side=LEFT, fill=Y)
        self.sidebar_frame.pack_propagate(FALSE)

    # note title frame
        self.note_title_frame = Frame(self.master, bg="#f6f6f6")
        self.note_title_frame.pack(expand=False, fill=X)

        self.note_title_label = Label(self.note_title_frame, text="Test Title", font="Helvetica 24",
                                      bg="#f6f6f6")
        self.note_title_label.pack(side=LEFT, padx=10, pady=10)

    # main frame of note taking area
        self.noteFrame = Frame(self.master, bg="#f6f6f6")
        self.noteFrame.pack(expand=True, fill=BOTH, pady=0, padx=0)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.noteFrame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        self.textbox = Text(self.noteFrame, bg="#f6f6f6", fg="#444444", relief="flat", spacing3=8, wrap=WORD, bd=0,
                            yscrollcommand=self.text_box_scrollbar.set, width=1, height=1)
        self.textbox.pack(fill=BOTH, expand=True, padx=15, pady=10)
        self.text_box_scrollbar.config(command=self.textbox.yview)

        # alters the tab length to only 4 spaces
        font = tkfont.Font(font=['font'])
        tab_width = font.measure(' ' * 5)
        self.textbox.config(tabs=(tab_width,))

    # "Categories" section
        # "categopries" label
        categories_title = Frame(self.sidebar_frame, width="250", height="50", bg="#d6d6d6")
        categories_title.pack()
        categories_title.pack_propagate(FALSE)
        categories = Label(categories_title, text="  Notes", font="Verdana 11", bg="#d6d6d6", fg="#444444")
        categories.pack(side=LEFT)

        # "New Category" box
        categories_new = Frame(self.sidebar_frame, width="250", height="50", bg="#e5e5e5")
        categories_new.pack()
        categories_new.pack_propagate(False)
        new_category_button = Button(categories_new, text="    ➕    " + "Create New Note", font="Verdana 10",
                                     width="250", height="50", fg="#444444", bg="#e5e5e5", relief="flat", anchor="w",
                                     bd=0, command=self.new_category)
        new_category_button.pack()

        self.pack_settings_button()

    # packs buttons for each saved category in new session
    def update_category_buttons(self):
        for dir in os.listdir(os.getcwd() + "\\note_categories\\"):
            self.settingsButton.destroy()
            self.settings.destroy()
            self.create_category(dir, method="old")

    # "Settings" button
    def pack_settings_button(self):
        self.settingsButton = Frame(self.sidebar_frame, width="250", height="50", bg="#d6d6d6")
        self.settingsButton.pack()
        self.settingsButton.pack_propagate(FALSE)
        self.settings = Button(self.settingsButton, text="  Settings", font="Verdana 11", width="250",
                              height="50", fg="#444444", bg="#d6d6d6", relief="flat", anchor="w", bd=0)
        self.settings.pack(side=LEFT)

    # makes the new category
    def new_category(self):
        self.name_category()

    def create_category_event(self, event):
        name = self.category_name.get()
        if len(name) >= 1:
            self.create_category(name, method="new")

    def create_category(self, name, method=None):

        name = name.title()

        try:
            self.category_name.destroy()
            self.delete_category.destroy()
            self.categoriesCustom.destroy()
            self.settingsButton.destroy()
            self.settings.destroy()

        except AttributeError:
            pass

        # frame that contains all user created categories
        self.category_frame = Frame(self.sidebar_frame, width="250", height="50", bg="#e5e5e5")
        self.category_frame.pack()
        self.category_frame.pack_propagate(False)

        if name.lower().endswith(".txt"):
            name = name[:-4]

        # adds the button and it's name to list to be accessed again
        self.categories_list.append(Button(self.category_frame, text="    ✒    "+name,
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
                contents = file.readlines()
                self.textbox.insert(INSERT, ''.join(contents))
                print("in " + category_name + ": " + str(contents))
        except FileNotFoundError:
            with open(self.file_name, 'w'):
                pass

        self.MyNoteTitle.configure(text=category_name)
        self.note_title_label.configure(text=category_name)
        print("\nNow editing: " + category_name)

    # save note manually
    def save_note(self, file_name):
        try:
            with open(file_name, 'w')as file:
                file.write(self.textbox.get(1.0, END))
        except AttributeError:
            pass
        print("Note saved.")

        # "last note saved: 3-15-17" on bottom of textbox for example
        try:
            self.last_saved_label.destroy()
        except AttributeError:
            self.last_saved_label = Label(self.noteFrame, font="Verdana 7", bg="#f6f6f6", fg="#444444",
                                          text=(str(time.strftime("Last saved: " + '%B %d, %Y' + ' at ' + '%I:%M %p'))))
            self.last_saved_label.pack(side=LEFT, fill=X, expand=False)

    def delete_note(self, file_name):
        os.remove(file_name)

    def name_category(self):
        try:
            if self.categoriesCustom:
                self.categoriesCustom.destroy()
        except AttributeError:
            pass

        # provides entry widget for category name
        self.settingsButton.destroy()
        self.settings.destroy()

        self.categoriesCustom = Frame(self.sidebar_frame, width="250", bg="#e5e5e5")
        self.categoriesCustom.pack(fill=X)
        self.categoriesCustom.pack_propagate(False)

        self.category_name = Entry(self.categoriesCustom, font="Verdana 10", fg="#444444", bg="#f4f4f4",
                              relief=FLAT, width=16)
        self.category_name.bind("<Return>", self.create_category_event)
        self.category_name.grid(column=1, row=0, pady=14)

        self.delete_category = Button(self.categoriesCustom, font="Verdana 10", fg="#444444", bg="#e5e5e5",
                                      activebackground="#e5e5e5", relief=FLAT,
                                      text="    ❌    ", command=lambda: self.categoriesCustom.destroy(), bd=0)
        self.delete_category.grid(column=0, row=0, sticky=W)

        self.pack_settings_button()

root = Tk()
root.title("My Notes")
root.minsize(600, 400)
root.geometry("1280x720")
root.iconbitmap(default='note_icon (1).ico')

a = MyNote(root)

root.mainloop()