import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import datetime
import pygubu
from tkinter import messagebox  

sqlite3.register_converter("BOOLEAN", lambda v: v != '0')
db = "blood_bank.db"  



def connect():
    cursor_obj= None
    con = None
    try:
        con = sqlite3.connect(f'{db}')
        cursor_obj = con.cursor()
        print("connection to "+db+" is successful")
    except Exception as error:
        print("Error "+error+" occured while connecting database")
        return cursor_obj, con
    return cursor_obj, con


def user(user_name, mobile_no, email, blood_type, quantity, date, is_donor):
    avail_quant = get_quantity(blood_type)
    cursor_obj, con = connect()
    if is_donor == False and avail_quant[0] >= quantity:
        if cursor_obj != None and con != None:
            insert = f"INSERT INTO user_info VALUES (?, ?, ?, ?, ?, ?, ?)" 
            val1= (user_name, mobile_no, email, blood_type, quantity, date, is_donor)
            update(is_donor, blood_type, quantity)
            try:
                cursor_obj.execute(insert, val1)
                con.commit()
                con.close()
            except:
                con.rollback()
                con.close()
        else:
            print("Something went wrong")    
    elif is_donor == True:
        insert = f"INSERT INTO user_info VALUES (?, ?, ?, ?, ?, ?, ?)" 
        val1= (f'{user_name}', f'{mobile_no}', f'{email}', f'{blood_type}', quantity, f'{date}', is_donor)
        update(is_donor, blood_type, quantity)
        try:
            cursor_obj.execute(insert, val1)
            con.commit()
            con.close()
        except:
            con.rollback()
            con.close()
    else:

        messagebox.showinfo("ALERT!",f"Sorry, insufficient Blood balance. Blood available is {avail_quant[0]}")
        con.close()
        
def get_quantity(blood_type):
    cursor_obj, con = connect()
    avail_quant = 0
    # print("i am here loser")
    try:
       select = f"SELECT avail_quant FROM blood_info WHERE blood_type = ?"
       val2 = (f'{blood_type}',)
    #    print(select)
       cursor_obj.execute(select, val2)
       avail_quant = cursor_obj.fetchone()
    except:
        con.close()
        return None
    # print(avail_quant)
    return avail_quant
    

def update(is_donor, blood_type, quantity):
    cursor_obj, con = connect()
    avail_quant = get_quantity(blood_type)
    temp = avail_quant[0]
    update = "UPDATE blood_info SET avail_quant = ? WHERE blood_type = ?"
    
    try:
        if is_donor == False:
            temp -= quantity
        else:
            temp += quantity
        val3 = (temp, f'{blood_type}')
        cursor_obj.execute(update, val3)
        con.commit()
        con.close
    except:
        con.rollback()
        con.close()
    messagebox.showinfo("Message","Details recorded")
    
class Form:

    def __init__(self):
        
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('FORM.ui')
        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)
        # self.username.set("")
    
    def printvar(self):
        print(type(self.builder.tkvariables['is_donor'].get()))
        if self.builder.tkvariables['is_donor'].get() == "":
            print("empty")

    def run(self):
        self.mainwindow.mainloop()

    def on_click(self):
        user_name = self.builder.tkvariables['user_name'].get()
        mobile_no = self.builder.tkvariables['mobile_no'].get()
        email = self.builder.tkvariables['email'].get()
        blood_type = self.builder.tkvariables['blood_type'].get()
        quantity = self.builder.tkvariables['quantity'].get()
        date = self.builder.tkvariables['date'].get()
        is_donor = self.builder.tkvariables['is_donor'].get()
        lst = [user_name, mobile_no, email, blood_type, quantity, date, is_donor]
        flag = 1
        for x in lst:
            if x == "":
                flag = 0
                #print("empty")
        if flag == 0:
            messagebox.showinfo("Error","Information missing")
        quantity = int(quantity)
        if is_donor == "True":
            is_donor = True
        else:
            is_donor = False 
        user(user_name, mobile_no, email, blood_type, quantity, date, is_donor)

if __name__ == '__main__':
    app = Form()
    app.run()
