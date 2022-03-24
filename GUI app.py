from importlib.resources import contents
import tkinter as tk
import os
import json

#Create the window 600 by 400 px which is not resizeable
window = tk.Tk()
window.resizable(width = False, height = False)

#Class budget
class Budget:
    whole_budget = tk.StringVar()
    copy_whole_budget = whole_budget

    def __init__(self, category, category_budget):
        self.category = category
        self.category_budget = category_budget

    def deposit(self, d_input):         #deposit amount into a category
        Budget.whole_budget -= d_input
        self.category_budget += d_input

    def show_deposit(self):             #show the amount deposited into a category
        return self.category_budget

    def withdraw(self, w_input):        #withdraw amount from a category
        Budget.whole_budget += w_input
        self.category_budget -= w_input

    def compute(self):                  #calculates amount of a category from the whole budget in %
        return (self.category_budget / Budget.copy_whole_budget) * 100

#Clear function
def clear():
    os.system("cls")

#Create a frame 600x400 px inside the window
frame1 = tk.LabelFrame(window, width = 600, height = 400)
frame1.pack()

#Create another frame for another page with all the interactions
frame2 = tk.LabelFrame(window, width = 600, height = 400)

#Create third frame for changeing the amount
frame3 = tk.LabelFrame(window, width = 600, height = 400)

#Create label and entry box where the budget amount is introduced inside frame 1
label1 = tk.Label(frame1, text = "Enter your amount below", font = (25))
label1.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)
entry1 = tk.Entry(frame1, font = (25))
entry1.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

#-----functions-----
#Function for changeing frame 1 to frame 2

def next_page():
    Budget.whole_budget.set("Your budget is: " + entry1.get())
    frame2.pack(padx = 10, pady = 10)
    frame1.pack_forget()

#Function for changing frame 2 to frame 1
def change_budget_page():
    frame3.pack()
    frame2.pack_forget()

#Create a button that changes the sets the amount introduced
button1 = tk.Button(frame1, text = "Lol buton", command = next_page)
button1.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)

#Create a label for showing the total amount
label2 = tk.Label(frame2, textvariable = Budget.whole_budget, font = (45))
label2.grid(column = 1, row = 1, padx = 10, pady = 10)

#Create button for changing amount
button2 = tk.Button(frame2, text = "Add amount", command = change_budget_page)
button2.grid(column = 2, row = 1, padx = 10, pady = 10)

#Label with all the categories inside
label_cat = tk.Label(frame2, text = "Your categories are:", font = (25))
label_cat.grid(column = 1, row = 2, padx = 10, pady = 10)

def get_json():
    with open("data.json", "r") as f:
        return json.load(f)
json_file = get_json()

cat_list_title = [key for key, value in json_file.items()]



#List of categories
lb = tk.Listbox(frame2, width = 20, height = 10, font = ("Helvetica", 10), justify = tk.CENTER)
for title in cat_list_title:
    lb.insert("end", title)
lb.grid(column = 1, row = 3)


def add_cat():
    top = tk.Toplevel()
    top.minsize(width = 400, height = 200)

    cat_label = tk.Label(top, text = "Add your new category below: ", font = ("Helvetica", 15), pady = 5)
    cat_entry = tk.Entry(top, font = ("Helvetica", 15))

    def cat_but():
        lb.insert(1, cat_entry.get())
        top.destroy()
    cat_add_button = tk.Button(top, text = "Add category", command = cat_but)

    cat_label.grid(column = 1, row = 1, columnspan = 2, padx = 20)
    cat_entry.grid(column = 1, row = 2, padx = 20)
    cat_add_button.grid(column = 2, row = 2)



#Category information label
leb = tk.Label(frame2, width = 20)
leb.grid(column = 3, row = 3)

label_info = tk.Label(frame2, font = ("Helvetica", 10), bd = 1, relief = tk.SUNKEN, width = 25, height = 10, anchor = tk.NW, justify = tk.LEFT, padx = 5, pady = 5)
label_info.grid(column = 2, row = 3, columnspan = 2, rowspan = 2, sticky = tk.NW)

def select():
    x = lb.get(tk.ANCHOR)
    for key, value in json_file.items():
        if key == x:
            cat_list_info = value
    label_info.config(text = cat_list_info)

temp_frame = tk.Frame(frame2)
temp_frame.grid(column = 1, row = 4)
button3 = tk.Button(temp_frame, text = "Add category", command = add_cat)
button3.pack(side = tk.LEFT)
select_button = tk.Button(temp_frame, text = "Select", command = select)
select_button.pack(side = tk.RIGHT, padx = 5, pady = 5)


tk.mainloop()