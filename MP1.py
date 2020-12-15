import sqlite3
import datetime
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
        print("Sorry, insufficient Blood balance. Blood available is" +avail_quant[0])
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

# user("anushka aseet", "9172827887", "anushkagarode@gmail.com", "O+ve", 2, "12-10-2020", True)
# con = sqlite3.connect(f'{db}')
# cursor_obj = con.cursor()
# user_name = "anushka aseet"
# mobile_no = "8421873831"
# email = "aseet10800@gmail.com"
# blood_type = "O +ve"
# quantity = 2
# is_donor = False
# # # cursor_obj, con = connect()
# insert = f"INSERT INTO user_info VALUES (?, ?, ?, ?, ?, ?)" 
# val1= (f'{user_name}', f'{mobile_no}', f'{email}', f'{blood_type}', quantity, is_donor)
# cursor_obj.execute(insert, val1)
# con.commit()
# con.close()
