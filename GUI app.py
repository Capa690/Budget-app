import tkinter as tk
import json


#Create the window 600 by 400 px which is not resizeable
window = tk.Tk()
window.resizable(width = False, height = False)

#Budget class
class Budget:
    whole_budget = tk.IntVar()
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

#Create a frame 600x400 px inside the window
frame1 = tk.LabelFrame(window, width = 600, height = 400)
frame1.pack()
#Create another frame for another page with all the interactions
frame2 = tk.LabelFrame(window, width = 600, height = 400)
#Create third frame for changeing the amount
frame3 = tk.LabelFrame(window, width = 600, height = 400)

#Create label and entry box where the budget amount is introduced inside frame 1
label1 = tk.Label(frame1, text = "Enter your amount below", font = (25))
entry1 = tk.Entry(frame1, font = (25))
#Placing the label and the entry box inside the window
label1.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)
entry1.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)


#Function for changeing to another page(frame 1 to frame 2)
def next_page():
    a = entry1.get()
    if not a.isdigit():
        label1.config(text = "This is not a number!", fg = "red")
        return
    Budget.whole_budget.set(entry1.get())
    frame2.pack(padx = 10, pady = 10)
    frame1.pack_forget()


#Create a button that changes the sets the amount introduced
button1 = tk.Button(frame1, text = "ADD", command = next_page)
button1.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)


#Create a label for showing the total amount left
temp2_frame = tk.Frame(frame2)
label2_1 = tk.Label(temp2_frame, text = "Your budget is: ", font = (45))
label2 = tk.Label(temp2_frame, textvariable = Budget.whole_budget, font = (45))
#Placing the label inside the window
temp2_frame.grid(column = 1, row = 1)
label2_1.pack(side = tk.LEFT)
label2.pack(side = tk.RIGHT, padx = 2)


#Function for changing to another page where amount is added(frame 2 to frame 1)
def change_budget_page():
    top = tk.Toplevel()
    top.minsize(width = 400, height = 200)

    amount_label = tk.Label(top, text = "Enter amount below: ", font = ("Helvetica", 15), pady = 5)
    amount_entry = tk.Entry(top, font = ("Helvetica", 15))

    def addAmount():
        x = int(amount_entry.get()) + Budget.whole_budget.get()
        Budget.whole_budget.set(x)
        top.destroy()
    def changeAmount():
        Budget.whole_budget.set(int(amount_entry.get()))
        top.destroy()
    add_but = tk.Button(top, text = "Add amount", command = addAmount)
    change_but = tk.Button(top, text = "Change to", command = changeAmount)

    amount_label.pack()
    amount_entry.pack()
    add_but.pack()
    change_but.pack()

#Create button for changing amount
button2 = tk.Button(frame2, text = "Add amount", command = change_budget_page)
button2.grid(column = 2, row = 1, padx = 10, pady = 10)


#Label with all the categories inside
label_cat = tk.Label(frame2, text = "Your categories are:", font = (25))
label_cat.grid(column = 1, row = 2, padx = 10, pady = 10)


#Function that gets the data from the json file
def get_json():
    with open("data.json", "r") as f:
        return json.load(f)
json_file = get_json()
#Saves the names of the categories in a list
cat_list_title = [key for key, value in json_file.items()]


#List of all the categories
lb = tk.Listbox(frame2, width = 20, height = 10, font = ("Helvetica", 10), justify = tk.CENTER)
for title in cat_list_title:
    lb.insert("end", title)
lb.grid(column = 1, row = 3)

def write_json(cat_name):
    with open("data.json", "w") as f:
        json_file.update({cat_name:{"Name":cat_name, "Deposited": 0, "Percentage": 0}})
        return json.dump(json_file, f)

#Function for adding a new category
def add_cat():
    #Creating a new window for adding category
    top = tk.Toplevel()
    top.minsize(width = 400, height = 200)

    #Creating new label and entry box for adding category
    cat_label = tk.Label(top, text = "Add your new category below: ", font = ("Helvetica", 15), pady = 5)
    cat_entry = tk.Entry(top, font = ("Helvetica", 15))

    #Function for confirming the addition of new category
    def cat_add():
        write_json(cat_entry.get())
        lb.insert(1, cat_entry.get())
        top.destroy()
    #Button for adding the new category
    cat_add_button = tk.Button(top, text = "Add category", command = cat_add)

    #Placing all the elements inside the window
    cat_label.grid(column = 1, row = 1, columnspan = 2, padx = 20)
    cat_entry.grid(column = 1, row = 2, padx = 20)
    cat_add_button.grid(column = 2, row = 2)


#------Separation label------
leb = tk.Label(frame2, width = 20)
leb.grid(column = 3, row = 3)
#----------------------------
#Label for showing all the information about a selected category
label_info = tk.Label(frame2, font = ("Helvetica", 10), bd = 1, relief = tk.SUNKEN, width = 25, height = 10, anchor = tk.NW, justify = tk.LEFT, padx = 5, pady = 5)
label_info.grid(column = 2, row = 3, columnspan = 2, rowspan = 2, sticky = tk.NW)

#Function for getting the information from the json file
def select():
    x = lb.get(tk.ANCHOR)
    jim = ""
    for key, value in json_file.items():
        if key == x:
            for key1, value1 in value.items():
                jim += str(key1) + ":\t" + str(value1) + "\n"
                label_info.config(text = jim)
    

#Creating a frame for the "Add category" button and "Select" button
temp_frame = tk.Frame(frame2)
button3 = tk.Button(temp_frame, text = "Add category", command = add_cat)
select_button = tk.Button(temp_frame, text = "Select", command = select)
#Placing all the element above inside the window
temp_frame.grid(column = 1, row = 4)
button3.pack(side = tk.LEFT)
select_button.pack(side = tk.RIGHT, padx = 5, pady = 5)


def dep_cat():
    an = lb.get(tk.ANCHOR)
    if an != "":
        top1 = tk.Toplevel()
        top1.minsize(width = 400, height = 200)

        dep_label = tk.Label(top1, text = "Enter the amount you want to deposit:", font = ("Helvetica", 15), pady = 5)
        dep_entry = tk.Entry(top1, font = ("Helvetica", 15))
        dep_label.pack()
        dep_entry.pack()

        def finish_deposit():
            for k, v in json_file.items():
                if k == an:
                    for i, j in v.items():
                        if i == "Deposited":
                            v[i] += int(dep_entry.get())
                            b = Budget.whole_budget.get() - int(dep_entry.get())
                            Budget.whole_budget.set(b)
            with open("data.json", "w") as f:
                json.dump(json_file, f)
            
            top1.destroy()
        cat_button = tk.Button(top1, text = "Deposit", command = finish_deposit)
        cat_button.pack()

def del_cat():
    an2 = lb.get(tk.ANCHOR)
    if an2 != "":
        for k, v in json_file.items():
            if k == an2:
                json_file.pop(k)
                break
        with open("data.json", "w") as f:
            json.dump(json_file, f)
        
        lb.delete(tk.ANCHOR)
#A frame for the category deposit button
temp3_frame = tk.Frame(frame2)
cat_dep_button = tk.Button(temp3_frame, text = "Deposit", command = dep_cat)
cat_del_button = tk.Button(temp3_frame, text = "Delete", command = del_cat)
#Placing the elements
temp3_frame.grid(column = 2, columnspan = 2, row = 4)
cat_dep_button.pack(side = tk.RIGHT)
cat_del_button.pack(side = tk.LEFT)



tk.mainloop()
