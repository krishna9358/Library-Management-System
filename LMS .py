# LMS 
'''
Patch Notes of v0.3.0
1. Data files reduced to 2.
2. Password secured with md5 encryption.
3. Redesigned interfaces.
4. Added new feature:- Delete Mutiple books.
5. Add Multiple books option is made more precise.
6. Contact me option filled with hyperlinks.
7. Changes in Loading screen.
8. More organized windows.
9. Added more graphics.
10. Bugs fixed.
'''

from tkinter import *
import tkinter.messagebox
# import win32com.client
import pickle
import sys
from tkinter.ttk import Progressbar
from time import sleep
from datetime import datetime
import hashlib
import webbrowser


# def speak(str):
#     if str == "":
#         pass

#     # else:
#     #     speaker = win32com.client.Dispatch("SAPI.SpVoice")

#         # speaker.Speak(str)

Data_file = "LibraryData.dat"

Pass_file = "Librarypass.dat"

GENRES = ["Poetry", "Drama", "Prose", "Nonfiction", "Media", "Misc."]

SC_Code = "282006"

try:
    with open(Pass_file, "rb") as f:
        password = pickle.load(f)

except Exception as e:
    print(e)
    tkinter.messagebox.showwarning("LIBRARY MANAGEMENT SYSTEM", "Some data files are missing.")
    sys.exit()

class Library():
    def __init__(self, List_of_books, Author_Names, Date_of_book_add, Genres, Lender_Sno, Lend_Date, Lender_name):

        self.List_of_books = List_of_books
        self.Author_Names = Author_Names
        self.Genres = Genres
        self.Lender_Sno = Lender_Sno
        self.Lender_name = Lender_name
        self.Date_of_book_add = Date_of_book_add
        self.Lend_Date = Lend_Date

    def display_books(self, bool):

        win1 = Toplevel()
        win1.geometry("400x400")
        win1.config(bg = "white")
        # win1.iconphoto(False, icon)

        def highlight_searched(*args):

            search = search_inp.get()

            lbx.selection_clear(0,END)

            for i, items in enumerate(all_books):
                if search.lower() in items.lower():
                    lbx.selection_set(i)

                elif search.lower() not in items.lower():
                    lbx.selection_clear(i)

            if search == "":
                lbx.selection_clear(0,END)


        search_inp = StringVar(win1)
        search_inp.set("")
        search_inp.trace('w', highlight_searched)
        search_bar = Entry(win1, textvar = search_inp, bg = "white", width = 35)
        search_bar.place(x = 5, y = 5)


        def gensearch(*args):
            lbx.selection_clear(0, END)
            gen_input = genvar.get()
            for index, key in enumerate(self.Genres):
                if gen_input == self.Genres[key]:
                    lbx.selection_set(index)
                else:
                    lbx.selection_clear(index)


        Button(win1, text = "Search", font = ("calibri", 8), command = highlight_searched, bg = "white").place(x = 230, y = 1)

        genvar = StringVar(win1)
        genvar.set("Select Genre")
        genvar.trace('w', gensearch)

        genre_filter = OptionMenu(win1, genvar, *GENRES)
        genre_filter.place(x = 280, y = 1)
        genre_filter.config(bg = "white")

        def bookdetails(event):
            selected = lbx.curselection()[0]
            bname = self.List_of_books[selected]

            win2 = Toplevel()
            win2.geometry("400x400")
            win2.config(bg="white")
            # win2.iconphoto(False, icon)

            Label(win2, text = bname, font = ("calibri", 24, "bold"), bg = "white").pack()

            Label(win2, text = f"Author: {self.Author_Names[bname]}", font = ("calibri", 18), bg = "white").pack(side = TOP, anchor = "nw", pady = 20)

            Label(win2, text = f"Genre: {self.Genres[bname]}", font = ("calibri", 18), bg = "white").pack(side = TOP, anchor = "nw")

            Label(win2, text = f"Added on: {self.Date_of_book_add[bname]}", font = ("calibri", 18), bg = "white").pack(side = TOP, anchor = "nw", pady = 20)

            if self.Lender_name[bname] == None:

                Label(win2, text = f"Lent By: {self.Lender_name[bname]}", font = ("calibri", 18), bg = "white").pack(side = TOP, anchor = "nw")

            else:

                Label(win2, text=f"Lent By: {self.Lender_name[bname]}({self.Lender_Sno[bname]})", font=("calibri", 18), bg="white").pack(side=TOP, anchor="nw")

                Label(win2, text=f"Lent On: {self.Lend_Date[bname]}", font=("calibri", 18), bg="white").pack(side=TOP, anchor="nw", pady=20)



        lbx = Listbox(win1, font = ("calibri", 18), bg = "white")
        lbx.bind("<Double Button-1>", bookdetails)
        lbx.pack(pady = 40, fill = BOTH, expand = True)

        sy = Scrollbar(lbx, orient = VERTICAL)
        sy.pack(side = RIGHT, fill = Y)

        sx = Scrollbar(lbx, orient = HORIZONTAL)
        sx.pack(side = BOTTOM, fill = X)


        lbx['yscrollcommand'] = sy.set
        lbx['xscrollcommand'] = sx.set


        sy.config(command = lbx.yview)
        sx.config(command = lbx.xview)

        all_books = []

        for index, books in enumerate(self.List_of_books):
            lbx.insert(END, f"{index+1}. {books}")
            all_books.append(f"{index+1}. {books}")

        if bool:
            speak("Successfully Displayed the books")

        elif bool == False:
            lbx.config(selectmode = MULTIPLE)

            def Deleteselbook():
                selected = lbx.curselection()

                all_ripe_books = []
                for items in selected:
                    all_ripe_books.append(self.List_of_books[items])

                if tkinter.messagebox.askyesno("Delete Multiple Books", f"Do you really want to delete {len(all_ripe_books)} books."):
                    for books in all_ripe_books:
                        self.delete_book(books, False)

                    win1.destroy()

                    tkinter.messagebox.showinfo("Delete Multiple books", f"successfully deleted {len(all_ripe_books)} books")

                else:
                    pass

            Button(win1, text = "Delete selected book(s)", bg = "white", command = Deleteselbook).pack()

    def add_book_wizard(self):
        global win3

        win3 = Toplevel()
        win3.geometry("500x400")
        win3.resizable(0,0)
        win3.config(bg="white")
        # win3.iconphoto(False, icon)

        Label(win3, text = "Donation of a book", font = ("calibri", 24, "bold"), bg = "white").pack()

        Label(win3, text = "Name of Book", font = ("calibri", 18), bg = "white").pack(side = LEFT, anchor = N, pady = 20, padx = 10)

        book_name = StringVar()
        book_name.set("")

        book_inp = Entry(win3, textvar = book_name)
        book_inp.place(x = 200, y = 70)

        Label(win3, text = "Name of Author", font = ("calibri", 18), bg = "white").place(x = 10, y = 100)

        auth_name = StringVar()
        auth_name.set("")

        auth_inp = Entry(win3, textvar = auth_name)
        auth_inp.place(x = 200, y = 105)

        Label(win3, text="Select Genre", font=("calibri", 18), bg="white").place(x=10, y=140)

        genvar = StringVar(win3)
        genvar.set("Select Genre")

        genre_input = OptionMenu(win3, genvar, *GENRES)
        genre_input.place(x=200, y=145)
        genre_input.config(bg="white")

        Button(win3, text = "Add Book", bg = "white", font = ("calibri", 18, "bold"), command  = lambda: self.add_book(book_name.get(), auth_name.get(), genvar.get(), True)).place(x = 350, y = 330)

    def add_book(self, Name_of_Book, Name_of_Author, Genre, bool):
        global win3

        if Name_of_Book == "":
            tkinter.messagebox.showerror("Donation of a book", "Some fields are missing therefore we cannot add the book")

        elif Name_of_Author == "":
            tkinter.messagebox.showerror("Donation of a book", "Some fields are missing therefore we cannot add the book")

        elif Genre == "Select Genre":
            tkinter.messagebox.showerror("Donation of a book", "Some fields are missing therefore we cannot add the book")

        else:
            if bool:
                if tkinter.messagebox.askyesno("Donation of a book", f"Name of book is {Name_of_Book}, Author is {Name_of_Author}, Genre is {Genre}. Do you really want to add this book?"):

                    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                    self.List_of_books.append(Name_of_Book)
                    self.Author_Names[Name_of_Book] = Name_of_Author
                    self.Genres[Name_of_Book] = Genre
                    self.Lender_Sno[Name_of_Book] = None
                    self.Lender_name[Name_of_Book] = None
                    self.Lend_Date[Name_of_Book] = None
                    self.Date_of_book_add[Name_of_Book] = date

                    with open(Data_file, "wb") as f:
                        pickle.dump(Shukla_Library, f)

                else:
                    pass

            else:

                date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.List_of_books.append(Name_of_Book)
                self.Author_Names[Name_of_Book] = Name_of_Author
                self.Genres[Name_of_Book] = Genre
                self.Lender_Sno[Name_of_Book] = None
                self.Lender_name[Name_of_Book] = None
                self.Lend_Date[Name_of_Book] = None
                self.Date_of_book_add[Name_of_Book] = date

                with open(Data_file, "wb") as f:
                    pickle.dump(Shukla_Library, f)

        try:
            win3.destroy()
        except:
            pass

    def lend_book_wizard(self):
        win4 = Toplevel()
        win4.geometry("500x400")
        win4.resizable(0, 0)
        win4.config(bg="white")
        # win4.iconphoto(False, icon)

        Label(win4, text="Lend a book", font=("calibri", 24, "bold"), bg="white").pack()

        Label(win4, text="Name of Book", font=("calibri", 18), bg="white").pack(side=LEFT, anchor=N, pady=20,
                                                                                        padx=10)

        book_name = StringVar()
        book_name.set("")

        book_inp = Entry(win4, textvar=book_name)
        book_inp.place(x=200, y=70)

        Label(win4, text="Name of Lender", font=("calibri", 18), bg="white").place(x=10, y=100)

        lender_name = StringVar()
        lender_name.set("")

        lender_inp = Entry(win4, textvar=lender_name)
        lender_inp.place(x=200, y=105)

        Label(win4, text="SRNo. of Lender", font=("calibri", 18), bg="white").place(x=10, y=140)

        snovar = StringVar(win4)
        snovar.set("")

        sno_input = Entry(win4, textvar = snovar)
        sno_input.place(x=200, y=145)

        def lend_book():
            sno = snovar.get()
            name = lender_name.get()
            book = book_name.get()
            if sno == "":
                tkinter.messagebox.showerror("Lend of a book",
                                             "Some fields are missing therefore we cannot lend this book")

            elif name == "":
                tkinter.messagebox.showerror("Lend a book",
                                             "Some fields are missing therefore we cannot lend this book")

            elif book == "":
                tkinter.messagebox.showerror("Lend a book",
                                             "Some fields are missing therefore we cannot lend this book")

            else:
                if book in self.List_of_books:
                    if self.Lender_name[book] == None and self.Lend_Date[book] == None and self.Lender_Sno[book] == None:
                        if tkinter.messagebox.askyesno("Lend a book", f"Name of book is {book}, Lender's name is {name}({sno}). Do you really want to lend this book?"):
                            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                            self.Lender_Sno[book] = sno

                            self.Lender_name[book] = name

                            self.Lend_Date[book] = date

                            with open(Data_file, "wb") as f:
                                pickle.dump(Shukla_Library, f)

                            tkinter.messagebox.showinfo("Lend a book", f"Successfully provided the book named {book} to {name}({sno})")
                            speak(f"Successfully provided the book named {book} to {name}")


                        else:
                            pass
                    else:

                        tkinter.messagebox.showinfo("Lend a book", f"This book is not available and it is taken by {self.Lender_name[book]}({self.Lender_Sno[book]}) on {self.Lend_Date[book]}")

                        speak(f"This book is not available and it is taken by {self.Lender_name[book]}")



                else:
                    tkinter.messagebox.showwarning("Lend a book", f"The book you entered named {book} does not belongs to this library")

            win4.destroy()

        Button(win4, text="Lend Book", bg="white", font=("calibri", 18, "bold"),
               command=lend_book).place(x=350, y=330)

    def return_book_wizard(self):

        win5 = Toplevel()
        win5.geometry("500x400")
        win5.resizable(0, 0)
        win5.config(bg="white")
        # win5.iconphoto(False, icon)

        Label(win5, text="Return a book", font=("calibri", 24, "bold"), bg="white").pack()

        Label(win5, text="Name of Book", font=("calibri", 18), bg="white").pack(side=LEFT, anchor=N, pady=20,
                                                                                        padx=10)

        book_name = StringVar()
        book_name.set("")

        book_inp = Entry(win5, textvar=book_name)
        book_inp.place(x=250, y=70)

        Label(win5, text="Name/SRNo. of Lender", font=("calibri", 18), bg="white").place(x=10, y=100)

        lender_name = StringVar()
        lender_name.set("")

        lender_inp = Entry(win5, textvar=lender_name)
        lender_inp.place(x=250, y=105)

        def return_book():
            book = book_name.get()
            name = lender_name.get()

            if book == "":

                tkinter.messagebox.showerror("Return a book", f"Some fields are missing therefore we cannot return this book")

            elif name == "":

                tkinter.messagebox.showerror("Return a book", f"Some fields are missing therefore we cannot return this book")

            else:

                if book in self.List_of_books:

                    if self.Lender_name[book] == name or self.Lender_Sno[book] == name:

                        if tkinter.messagebox.askyesno("Return a book", "Do you really want to return this book?"):
                            self.Lender_Sno[book] = None

                            self.Lender_name[book] = None

                            self.Lend_Date[book] = None

                            with open(Data_file, "wb") as f:
                                pickle.dump(Shukla_Library, f)

                            tkinter.messagebox.showinfo("Return a book", "Book returned successully")

                            speak("Book returned successully")

                        else:

                            tkinter.messagebox.showerror("Return a book", "This book is not lent by anyone")
                            speak("This book is not lent by anyone")


                    else:

                        tkinter.messagebox.showerror("Return a book", "This Book is not taken by you.")
                        speak("This Book is not taken by you.")

                else:

                    tkinter.messagebox.showerror("Return a book", "This book named {} does not belongs to our library".format(book))
                    speak("This book does not belongs to our library")

            win5.destroy()

        Button(win5, text = "Return Book", bg = "white", font = ("calibri", 18, "bold"),
               command = return_book).place(x=320, y=330)

    def delete_book(self, book, bool):
        global win7

        if bool:

            if tkinter.messagebox.askyesno("Delete a book", f"Do you really want to delete the book named {book}"):
                self.List_of_books.remove(book)
                self.Author_Names.pop(book)
                self.Genres.pop(book)
                self.Lender_Sno.pop(book)
                self.Lender_name.pop(book)
                self.Lend_Date.pop(book)
                self.Date_of_book_add.pop(book)

                with open(Data_file, "wb") as f:
                    pickle.dump(Shukla_Library, f)

                win7.destroy()

                tkinter.messagebox.showinfo("Delete a book", "Successfully deleted the book")
                speak("Successfully deleted the book")

            else:
                win7.destroy()

        else:
            self.List_of_books.remove(book)
            self.Author_Names.pop(book)
            self.Genres.pop(book)
            self.Lender_Sno.pop(book)
            self.Lender_name.pop(book)
            self.Lend_Date.pop(book)
            self.Date_of_book_add.pop(book)

            with open(Data_file, "wb") as f:
                pickle.dump(Shukla_Library, f)

    def delete_book_wizard(self):

        global win7

        win6 = Toplevel()
        win6.geometry("400x300")
        win6.resizable(0, 0)
        win6.config(bg = "white")
        # win6.iconphoto(False, icon)

        Label(win6, text = "Password Verification", font = ("calibri", 24, "bold"), bg="white").pack()

        Label(win6, text = "Enter Password", font = ("calibri", 18), bg = "white").pack(side = LEFT, anchor = N, pady = 20, padx = 10)

        passentry = StringVar()
        passentry.set("")

        passinp = Entry(win6, textvar = passentry, show = "*")
        passinp.pack(side = LEFT, anchor = N, pady = 25)


        def passcheck():
            global win7

            pass_user = passentry.get()

            if hashlib.md5(pass_user.encode()).hexdigest() == password:

                win6.destroy()

                win7 = Toplevel()
                win7.geometry("400x300")
                win7.resizable(0, 0)
                win7.config(bg="white")
                # win7.iconphoto(False, icon)

                Label(win7, text = "Delete a book", font = ("calibri", 24, "bold"), bg="white").pack()

                Label(win7, text = "Name of book", font = ("calibri", 18), bg = "white").pack(side=LEFT, anchor=N, pady=20, padx=10)

                bookentry = StringVar()
                bookentry.set("")

                bookinp = Entry(win7, textvar =bookentry)
                bookinp.pack(side = LEFT, anchor = N, pady = 25)


                Button(win7, text="Delete Book", font=("calibri", 18, "bold"), bg="white", command = lambda: self.delete_book(bookentry.get(), True)).place(x=230, y=230)

            else:

                tkinter.messagebox.showinfo("Password Verification", "Wrong Password. Please try again later")
                win6.destroy()
        Button(win6, text = "Submit", font = ("calibri", 18, "bold"), bg = "white", command = passcheck).place(x = 270, y = 230)


Loadscreen = Tk()
Loadscreen.config(bg = "white")
Loadscreen.overrideredirect(True)
Loadscreen.geometry("600x330")

Loadscreen_width = 600
Loadscreen_height = 330

Loadscreen_positionRight = int(Loadscreen.winfo_screenwidth()/2 - Loadscreen_width/2)
Loadscreen_positionDown = int(Loadscreen.winfo_screenheight()/2 - Loadscreen_height/2)

Loadscreen.geometry("+{}+{}".format(Loadscreen_positionRight, Loadscreen_positionDown))

Label(Loadscreen, text = "Welcome to Library Management System", bg = "white", fg = "#160149", font = ("calibri", 24, "bold")).pack(pady = 30)

# img0 = ImageTk.PhotoImage(Image.open("icon.ico"))
# Label(Loadscreen, image=img0).pack()

Label(Loadscreen, text="Loading...", bg = "white", fg = "green", font = ("calibri", 24, "bold")).pack(pady = 20)

progress = Progressbar(Loadscreen,orient = HORIZONTAL, length = 500, mode = 'determinate')

def window_progress():
    progress['value'] = 20
    Loadscreen.update()
    sleep(1)

    progress['value'] = 40
    Loadscreen.update()
    sleep(1)

    progress['value'] = 50
    Loadscreen.update()
    sleep(1)

    progress['value'] = 60
    Loadscreen.update()
    sleep(1)

    progress['value'] = 80
    Loadscreen.update()
    sleep(1)

    progress['value'] = 100
    Loadscreen.destroy()


progress.pack(pady = 10)

window_progress()


mainwin = Tk()
mainwin.resizable(0,0)
mainwin.config(bg = "white")


mainwin.title("Library Management System")
# icon = ImageTk.PhotoImage(file = "icon.ico")
# mainwin.iconphoto(False, icon)

try:
    with open(Data_file, "rb") as f:
        data = pickle.load(f)
except:
    tkinter.messagebox.showerror("Library Management System", "Some Files are missing therefore we cannot load the software")
    sys.exit()

List_of_Books = data.List_of_books
Authors = data.Author_Names
Add_Date = data.Date_of_book_add
bookgen = data.Genres
lendSno = data.Lender_Sno
lendDate = data.Lend_Date
lendName = data.Lender_name


Shukla_Library = Library(List_of_Books, Authors, Add_Date, bookgen, lendSno, lendDate, lendName)


def addmbook():

    win12 = Toplevel()
    win12.resizable(0, 0)
    win12.geometry("600x500")
    win12.config(bg="white")
    # win12.iconphoto(False, icon)

    Label(win12, text = "Add Multiple books", font = ("calibri", 24, "bold"), bg = "white").pack()

    l = Label(win12, text = "Click Here", font = ("calibri", 18, "underline"), bg = "white", fg = "blue", cursor = "hand2")

    def openhelp(event):

        win13 = Toplevel()

        # win13.iconphoto(False, icon)
        frame = Frame(win13, width=300, height=300)
        frame.pack(expand=True, fill=BOTH)
        can = Canvas(frame, bg = "white")
        can.pack(fill = BOTH, expand = True)


        Label(can, text = "How to add multiple books?", font = ("calibri", 24, "bold"), bg = "white").pack()

        Label(can, text = "To add multiple books through wizard follow the following steps:-", font = ("calibri", 20, "bold"), bg = "white").pack(anchor = NW, pady = 20)

        Label(can, text = "1. Open the wizard an interface similar to one below will open.", font = ("calibri", 14), bg = "white").pack(anchor = NW)

        img3 = Image.open("emptybook.png")
        img3 = img3.resize((200,200), Image.ANTIALIAS)
        img4 = ImageTk.PhotoImage(img3)

        label = Label(can, image=img4)
        label.image = img4
        label.pack(pady = 20)

        Label(can, text = "2. Enter each book in the following format:-\nName, Author, Genre.", font = ("calibri", 14), bg = "white").place(x = 1, y = 360)
        Label(can, text = "While entering genre, you have to enter a no. i.e.", font = ("calibri", 14), bg = "white").pack(anchor = NW, pady = 10)

        for index, items in enumerate(GENRES):
            Label(can, text = f"{index+1} for {items}", font = ("calibri", 14), bg = "white").pack(anchor = NW, padx = 10)

        Label(can,text="3. An example of entry of one book is given below. Press enter key after you fill all details the textbox will be cleared and then you have to enter next book in same format. After adding all the books press \n Add Book(s) button.", font=("calibri", 14), bg="white").pack(anchor=NW)


        img4 = Image.open("add book.png")
        img4 = img4.resize((200,200), Image.ANTIALIAS)
        img5 = ImageTk.PhotoImage(img4)

        label2 = Label(can, image = img5)
        label2.image = img5
        label2.pack()

        Label(can, text="Note:- If Genre is Misc. You can enter anything except 1,2,3,4,5 to use this genre.", font=("calibri", 10), bg="white").pack(anchor=NW)

    l.bind("<Button-1>", openhelp)
    l.place(x = 80, y = 60)

    Label(win12, text = "to see how to add multiple books.", font = ("calibri", 18), bg = "white").place(x = 190, y = 60)

    t = Text(win12, font = ("calibri", 16), width = 50, height = 10, borderwidth = 2, relief = GROOVE)
    t.pack(pady = 80)

    def addtolist(event):

        text = t.get(1.0, END)
        t.delete(1.0, END)

        raw_item = text.split(",")
        raw_item = map(lambda s: s.strip(), raw_item)
        raw_item = [i for i in raw_item]

        if len(raw_item) == 3:
            list_of_raw_items.append(raw_item)

        elif len(raw_item) > 0 and len(raw_item) < 3:

            tkinter.messagebox.showerror("Add Multiple Books", f"The book you recently entred named {raw_item[0]} is missing some details. This book won't be added please enter this book again.")

        elif len(raw_item) > 3:
            tkinter.messagebox.showerror("Add Multiple Books", f"The book you recently entred named {raw_item[0]} is missing some details. This book won't be added please enter this book again.")

        else:
            pass

    t.bind("<Return>", addtolist)

    list_of_raw_items = []

    def show_books():

        win14 = Toplevel()
        win14.geometry("870x500")
        win14.config(bg="white")
        # win14.iconphoto(False, icon)

        def selbook(event):
            Author_list.selection_clear(0, END)
            Genre_list.selection_clear(0, END)

            selection = Book_list.curselection()[0]

            Author_list.selection_set(selection)
            Genre_list.selection_set(selection)

        def selauthor(event):
            Book_list.selection_clear(0, END)
            Genre_list.selection_clear(0, END)

            selection = Author_list.curselection()[0]

            Book_list.selection_set(selection)
            Genre_list.selection_set(selection)

        def selgenre(event):
            Author_list.selection_clear(0, END)
            Book_list.selection_clear(0, END)

            selection = Genre_list.curselection()[0]

            Author_list.selection_set(selection)
            Book_list.selection_set(selection)

        Label(win14, text = "Books", font = ("calibri", 24, "bold"), bg = "white").pack(side = TOP, anchor = W)

        Label(win14, text = "Author", font = ("calibri", 24, "bold"), bg = "white").place(x = 255, y = 1)

        Label(win14, text = "Genre", font = ("calibri", 24, "bold"), bg = "white").place(x = 500, y = 1)

        Book_list = Listbox(win14, font = ("calibri", 18))

        Book_list.pack(side = LEFT, anchor = N, fill = Y)

        sy1 = Scrollbar(win14)
        sy1.pack(side = LEFT, anchor = N, fill = Y)

        Book_list['yscrollcommand'] = sy1.set

        sy1.config(command=Book_list.yview)

        sx1 = Scrollbar(Book_list, orient = HORIZONTAL)
        sx1.pack(side = BOTTOM, ipadx = 90, fill = X)

        Book_list['xscrollcommand'] = sx1.set

        sx1.config(command = Book_list.xview)


        Author_list = Listbox(win14, font = ("calibri", 18), exportselection = False)
        Author_list.pack(side = LEFT, anchor = N, fill = Y)
        sy2 = Scrollbar(win14)
        sy2.pack(side=LEFT, anchor=N, fill = Y)

        Author_list['yscrollcommand'] = sy2.set

        sy2.config(command=Author_list.yview)

        sx2 = Scrollbar(Author_list, orient=HORIZONTAL)
        sx2.pack(side=BOTTOM, ipadx=90, fill=X)

        Author_list['xscrollcommand'] = sx2.set

        sx2.config(command=Author_list.xview)

        Genre_list = Listbox(win14, font = ("calibri", 18), exportselection = False)
        Genre_list.pack(side = LEFT, anchor = N, fill = Y)

        sy3 = Scrollbar(win14)
        sy3.pack(side=LEFT, anchor=N, fill = Y)

        Genre_list['yscrollcommand'] = sy3.set

        sy3.config(command = Genre_list.yview)

        sx3 = Scrollbar(Genre_list, orient=HORIZONTAL)
        sx3.pack(side=BOTTOM, ipadx=90, fill=X)

        Genre_list['xscrollcommand'] = sx3.set

        sx3.config(command=Genre_list.xview)

        all_books = []

        all_authors = []

        all_genres = []

        Book_list.bind("<ButtonRelease-1>", selbook)
        Author_list.bind("<ButtonRelease-1>", selauthor)
        Genre_list.bind("<ButtonRelease-1>", selgenre)

        def deleteabook():
            selected = Book_list.curselection()[0]

            Book_list.delete(selected)
            all_books.pop(selected)

            Author_list.delete(selected)
            all_authors.pop(selected)

            Genre_list.delete(selected)
            all_genres.pop(selected)


        def addallbook():
            for index, items in enumerate(all_books):
                Shukla_Library.add_book(items, all_authors[index], all_genres[index], False)

            win12.destroy()
            win14.destroy()

            tkinter.messagebox.showinfo("Add multiple books", f"Successfully added {len(all_books)} books.")

        Button(win14, text = "Delete", font = ("calibri", 18), bg = "white", command = deleteabook).place(x = 760, y = 50)
        Button(win14, text = "Add", font = ("calibri", 18), bg = "white", command = addallbook).place(x = 760, y = 400)

        for items in list_of_raw_items:

            Book_list.insert(END, items[0])
            all_books.append(items[0])

            Author_list.insert(END, items[1])
            all_authors.append(items[1])

            if items[2] == "1":

                Genre_list.insert(END, GENRES[0])
                all_genres.append(GENRES[0])

            elif items[2] == "2":

                Genre_list.insert(END, GENRES[1])
                all_genres.append(GENRES[1])

            elif items[2] == "3":

                Genre_list.insert(END, GENRES[2])
                all_genres.append(GENRES[2])

            elif items[2] == "4":

                Genre_list.insert(END, GENRES[3])
                all_genres.append(GENRES[3])

            elif items[2] == "5":

                Genre_list.insert(END, GENRES[4])
                all_genres.append(GENRES[4])

            else:

                Genre_list.insert(END, GENRES[5])
                all_genres.append(GENRES[5])


    def viewbooks():

        if len(list_of_raw_items) == 0:

            tkinter.messagebox.showwarning("Add Multiple Books", "Please enter book(s) first.")

        else:

            show_books()

    Button(win12, text = "Add book(s)", font = ("calibri", 18, "bold"), bg = "white", command = viewbooks).place(x = 400, y = 400)

def delmbook():
    win16 = Toplevel()
    win16.geometry("400x300")
    win16.resizable(0, 0)
    win16.config(bg="white")
    # win16.iconphoto(False, icon)

    Label(win16, text="Password Verification", font=("calibri", 24, "bold"), bg="white").pack()

    Label(win16, text="Enter Password", font=("calibri", 18), bg="white").pack(side=LEFT, anchor=N, pady=20, padx=10)

    passentry = StringVar(win16)
    passentry.set("")

    passinp = Entry(win16, textvar=passentry, show="*")
    passinp.pack(side=LEFT, anchor=N, pady=25)

    def passcheck():
        pass_user = passentry.get()

        if hashlib.md5(pass_user.encode()).hexdigest() == password:

            win16.destroy()
            Shukla_Library.display_books(False)

        else:

            win16.destroy()
            tkinter.messagebox.showerror("Delete all books", "Wrong Password! Please try again later.")

    Button(win16, text="Submit", font=("calibri", 18, "bold"), bg="white", command=passcheck).place(x=270, y=230)

def passchange():

    win9 = Toplevel()
    win9.geometry("400x300")
    win9.resizable(0, 0)
    win9.config(bg="white")
    # win9.iconphoto(False, icon)

    Label(win9, text="Change Password", font = ("calibri", 24, "bold"), bg="white").pack()

    Label(win9, text="Enter School Code", font = ("calibri", 18), bg="white").pack(side=LEFT, anchor=N, pady=20, padx=10)

    scentry = StringVar()
    scentry.set("")

    scinp = Entry(win9, textvar=scentry, show="*")
    scinp.pack(side=LEFT, anchor=N, pady=25)

    def sccheck():

        scinput = scentry.get()

        if scinput == SC_Code:

            win9.destroy()

            win10 = Toplevel()
            win10.geometry("500x400")
            win10.resizable(0, 0)
            win10.config(bg="white")
            # win10.iconphoto(False, icon)

            Label(win10, text="Change Password", font=("calibri", 24, "bold"), bg="white").pack()

            Label(win10, text="Enter New Password", font=("calibri", 18), bg="white").pack(side=LEFT, anchor=N, pady=20, padx=10)

            pass_name = StringVar()
            pass_name.set("")

            pass_inp = Entry(win10, textvar=pass_name, show = "*")
            pass_inp.place(x=250, y=70)

            Label(win10, text="Confirm Password", font=("calibri", 18), bg="white").place(x=10, y=100)

            conpass_name = StringVar()
            conpass_name.set("")

            conpass_inp = Entry(win10, textvar=conpass_name, show = "*")
            conpass_inp.place(x=250, y=105)

            def passfchange():

                global password

                passval = pass_name.get()
                conpassval = conpass_name.get()

                if passval == conpassval:

                    newpass = hashlib.md5(passval.encode()).hexdigest()

                    password = newpass

                    with open(Pass_file, "wb") as f:
                        pickle.dump(newpass, f)

                    tkinter.messagebox.showinfo("Change Password", "Password reset successfull.")

                    win10.destroy()

                else:

                    tkinter.messagebox.showwarning("Change Password", "New Password does not match in both the fields please try again.")

                    pass_name.set("")

                    conpass_name.set("")


            Button(win10, text="Submit", font=("calibri", 18, "bold"), bg="white", command = passfchange).place(x=380, y=330)


        else:

            win9.destroy()

            tkinter.messagebox.showwarning("Change Password", "Wrong School Code! Please try again later.")

    Button(win9, text="Submit", font=("calibri", 18, "bold"), bg="white", command=sccheck).place(x=270, y=230)

def delallbook():

    win8 = Toplevel()
    win8.geometry("400x300")
    win8.resizable(0, 0)
    win8.config(bg="white")
    # win8.iconphoto(False, icon)

    Label(win8, text="Password Verification", font=("calibri", 24, "bold"), bg="white").pack()

    Label(win8, text="Enter Password", font=("calibri", 18), bg="white").pack(side=LEFT, anchor=N, pady=20, padx=10)

    passentry = StringVar()
    passentry.set("")

    passinp = Entry(win8, textvar=passentry, show="*")
    passinp.pack(side=LEFT, anchor=N, pady=25)

    def passcheck():
        pass_user = passentry.get()

        if hashlib.md5(pass_user.encode()).hexdigest() == password:

            win8.destroy()

            if tkinter.messagebox.askyesno("Delete all books", "Do you really want to delete all books and their data? You won't be able to recover that."):
                all_books = [i for i in Shukla_Library.List_of_books]
                for books in all_books:
                    Shukla_Library.delete_book(books, False)

            else:

                pass

        else:

            win8.destroy()
            tkinter.messagebox.showerror("Delete all books", "Wrong Password! Please try again later.")


    Button(win8, text="Submit", font=("calibri", 18, "bold"), bg="white", command=passcheck).place(x=270, y=230)

def about():
    tkinter.messagebox.showinfo("About me", "This function is a work in progress. It will be available to be accessed very soon in future updates.")

def ex():
    on_closing()


menubar = Menu(mainwin)
m1 = Menu(menubar, tearoff = 0)
m1.add_command(label = "Add multiple books", command = addmbook)
m1.add_command(label = "Delete Multiple books", command = delmbook)
m1.add_command(label = "Change Password", command = passchange)
m1.add_command(label = "Delete all books", command = delallbook)

m2 = Menu(menubar, tearoff = 0)
m2.add_command(label = "About me", command = about)
# m2.add_command(label = "Contact me", command = contact)

menubar.add_cascade(label = "Options", menu = m1)
menubar.add_cascade(label = "About", menu = m2)
menubar.add_command(label = "Exit", command = ex)

mainwin.config(menu = menubar)


Label(mainwin, text = "Welcome to Library Management System", bg = "white", fg = "red", font = ("calibri", 40, "bold")).pack(padx = 20)


# img1 = Image.open("100.png")
# img1 = img1.resize((400,500), Image.ANTIALIAS)
# img2 = ImageTk.PhotoImage(img1)
# Label(mainwin, image = img2).pack(side = LEFT, pady = 50, padx = 50)

Label(mainwin, text = "Select What you want to do", bg = "white", fg = "green", font = ("calibri", 20, "bold")).pack(side = TOP, anchor = "w", pady = 50, padx = 50)

list_of_commands = ["Display Books Available", "Donate a book", "Lend a book", "Return a book", "Delete a book"]


user_inp = StringVar()
user_inp.set("radio")

for commands in list_of_commands:

    Radiobutton(mainwin, text = commands, bg = "white", fg = "#160149", font = ("calibri", 20, "bold"), variable = user_inp, value = commands).pack(side = TOP, anchor = "w", padx = 50)

def but0click():

    input = user_inp.get()

    if input == list_of_commands[0]:

        Shukla_Library.display_books(True)

    elif input == list_of_commands[1]:

        Shukla_Library.add_book_wizard()

    elif input == list_of_commands[2]:

        Shukla_Library.lend_book_wizard()

    elif input == list_of_commands[3]:

        Shukla_Library.return_book_wizard()

    else:

        Shukla_Library.delete_book_wizard()


but0 = Button(mainwin, text = "Next", font = ("calibri", 20, "bold"),bg = "white", fg = "green",  command = but0click).pack(ipadx = 5, side = TOP, anchor = "w", padx = 70, pady = 50)

def on_closing():
    if tkinter.messagebox.askokcancel("LIBRARY MANAGEMENT SYSTEM", "Do you really want to quit?"):
        with open(Data_file, 'wb') as f:
            pickle.dump(Shukla_Library, f)
        mainwin.destroy()


mainwin.protocol("WM_DELETE_WINDOW", on_closing)


mainwin.mainloop()
