import mysql.connector
from tkinter import ttk # Normal Tkinter.* widgets are not themed!
# from ttkthemes import ThemedTk
from tkinter import *
from tkinter import messagebox

try:
        db= mysql.connector.connect(host='localhost',user='root', password='root', database='medical_shop')
        cursor = db.cursor()
except Exception as e:
        print(e)
total=0
price = 0
flag = True
def add_item():
	mname=ent2.get()
	mqnty=ent3.get()
	global price
	global total
	global flag
	
	
	try:
		cursor.execute("select * from medicine_det where Mname = '{0}'".format(mname))
		data = cursor.fetchall()
		# print('{:15s}\t{:10s}\t{:15s}'.format('Itemnm','Itemqt','Itempr'))
		for row in data:
			itemnm = row[0] # Item name
			itemqt = row[1] # Item quantity	
			itempr = row[2] # Item price
			# print('{:15s}\t{:10d}\t{:15d}'.format(itemnm,itemqt,itempr))

		quantity = int(itemqt) - int(mqnty)

		cursor.execute("update medicine_det set Mquantity ={0} where Mname='{1}' ".format(quantity,mname))
		db.commit()
	
	except mysql.connector.errors.DataError:
		messagebox.showerror('!ERROR',' Only {0} quantity of {1} is availaible'.format(itemqt ,mname))

	except UnboundLocalError:
		messagebox.showerror('! ERROR','{0} not found in the database'.format(mname))
		ent2.delete(0,END)
		ent3.delete(0,END)

	except ValueError:
		messagebox.showerror('! ERROR',' Please enter proper quantity value ')

	else:
		p.set(itempr)
		price = itempr * int(mqnty)
		# Adding items in print list
		T1.insert(END, '\n   {0}\t\t\t\t\t\t\t  {1}'.format(mname,price))
		ent2.delete(0,END)
		ent3.delete(0,END)

		# Setting total price field's value
		total = total + price
		t.set(total)

def billing():
	mname=ent2.get()
	mqnty=ent3.get()
	# if (mname=='' and mqnty =='') :
	print(total)
	if total == 0:
		messagebox.showinfo('','Nothing to print Please add some items')
	else:
		try:
			T1.insert(END,'----------------------------------------------------------------------')
			T1.insert(END,'Total - \t\t\t\t\t\t\t     {0}'.format(total))
			T1.insert(END, '\n')
			T1.insert(END, '\n')
			T1.insert(END, '\n')
			T1.insert(END, '\n')
			T1.insert(END, '\t\t\tThankYou for visiting')
		except:
			pass
		else:
			T1.delete(0, END)


def submit():
	mname = ent6.get()
	mqnty = ent7.get()
	mprice= ent8.get()

	if mname == '':
		messagebox.showerror('! MySql Error','Please enter some contents to enter')
	elif mqnty == '':
		messagebox.showerror('! MySql Error','Please enter correct quantity')
	elif mprice == '':
		messagebox.showerror('! MySql Error','Please enter some price to save into database')
	
	cursor.execute("select Mname from medicine_det")
	data = cursor.fetchall()
	medicine_names = [i[0].lower() for i in data]
	print('Recieved value is -->',mname.lower())
	print(medicine_names)
	if mname.lower() in medicine_names:
		print('Its reacing here :) ')
		MsgBox = messagebox.askyesno('Data error', 'This medicine is already present in the database, press yes if you want to update this medicines quantity and price or else press No')
		if MsgBox:
			cursor.execute("update medicine_det set Mquantity={0}, Mprice={1} where Mname='{2}'".format(mqnty, mprice, mname))
			db.commit()
			messagebox.showinfo('!Updated Values',f"Values changed for medicine {mname} are Q = {mqnty} P ={mprice}. \n Please click on Check medicine details for confirmation")


	# try:
	cursor.execute("insert into medicine_det values('{0}',{1},{2})".format(mname,mqnty,mprice))
	db.commit()

	# # except mysql.connector.errors.ProgrammingError:
	# # 	messagebox.showerror('! MySql Error','Please enter some contents to enter')
	# except mysql.connector.errors.IntegrityError:
	# 	messagebox.showerror('! MySql Error', 'This medicine is already availaible' )

	# finally:
	ent6.delete(0, END)
	ent7.delete(0, END)
	ent8.delete(0, END)
	

def show_medicine_det():
	cursor.execute('select * from medicine_det')
	data = cursor.fetchall()
	T.delete(1.0, END)
	T.insert(END,'\t{0}\t\t{1}\t\t{2}\n'.format('Item name','Item Qty','Item price'))
	for row in data:
		itemnm = row[0]
		itemqt = row[1]
		itempr = row[2]
		T.insert(END,'\t{0}\t\t{1}\t\t{2}\n'.format(itemnm,itemqt,itempr))


# def enter(event):
# 	btn2.config(bg="#93DBF0")

# def leave(event):
# 	btn2.config(bg="#58ABE9")

win =Tk()
win.title('Freemum Medical software')
#win.iconbitmap(r'D:\data\icons\MSN.ico')
# win.set_theme('equilux')

headlbl=Label(win,text='Medical billing software FREEMUM VERSION 0.1',bg='lightblue',bd=1,relief=SOLID,font =('Bookman Old Style',14,'bold'))
headlbl.pack(fill=X)

f=Frame(win,bd=1,relief=SOLID,background='#1f304e')
f.pack(side=LEFT,fill=Y)

l1=Label(f,text='Select the medicine for billing',font=('Bookman Old Style',14),background='#1f304e',fg='white')
l1.grid(row=0,column=0,columnspan=2)
  
l2=Label(f,text='Medicine name:- ',font =('Consolas',12,'bold'),fg='lightblue',bg='#1f304e')
l2.grid(row=1,column=0,sticky=W,pady=5,padx=5)
ent2=Entry(f,width=60)
ent2.grid(row=1,column=1,sticky=W,padx=20)

q=StringVar()
l3 =Label(f,text='Quantity of medicine:- ',font =('Consolas',12,'bold'),fg='lightblue',bg='#1f304e')
l3.grid(row=2,column=0,sticky=W,pady=5,padx=5)
ent3 =Entry(f,width=60,textvariable=q)
ent3.grid(row=2, column=1,sticky=W,padx=20)

p=StringVar()
l4=Label(f,text='Price of medicine:- ',font =('Consolas',12,'bold'),fg='lightblue',bg='#1f304e')
l4.grid(row=3,column=0,sticky=W,pady=5,padx=5)
ent4 = Entry(f,width=60,state=DISABLED,textvariable=p)
ent4.grid(row=3,column=1,sticky=W,padx=20)

t=StringVar()
totlcst=Label(f,text='Total cost of all medicines:- ',font =('Consolas',12,'bold'),fg='lightblue',bg='#1f304e')
totlcst.grid(row=4,column=0,sticky=W,pady=5,padx=5)
ent5 = Entry(f,width=60,state=DISABLED,textvariable=t)
ent5.grid(row=4, column=1,sticky=W,padx=20)

btn=Button(f,text='Print for billing',command=billing)
btn.grid(row=5,column=0,columnspan=2,ipadx=30,pady=10,ipady=2)  

btn3 =Button(f, text='Add more item',command= add_item)
btn3.grid(row=5,column=0,pady=15,ipady=2,ipadx=25)

# lstbox=Listbox(f,width=70,height=28)
# lstbox.grid(row=6,column=0,columnspan=2,padx=20)
# lstbox.insert(END, '                                                MEDICAL GENERAL STORE ')
# lstbox.insert(END, '                                        Green Village Kashimira Kashigaon')
# lstbox.insert(END, '                                             Mira-Road (E) Thane- 401107')
# lstbox.insert(END, '                                                Phone no-022-8965-4589')
# lstbox.insert(END, '----------------------------------------------------------------------------------- ')
# lstbox.insert(END, '  Name of Product                                                                                                 Price')

T1 = Text(f,width=65,height=23,font=('Consolas',13))
T1.grid(row=6,column=0,columnspan=2,padx=25)
T1.insert(END,'\t\t\tMEDICAL GENERAL STORE\n')
T1.insert(END,'\t\t  Green Village Kashimira Kashigaon\n')
T1.insert(END,'\t\t     Mira-Road (E) Thane- 401107\n')
T1.insert(END,'\t\t\tPhone no-022-8965-4589\n')
T1.insert(END,'-----------------------------------------------------------------')
T1.insert(END,' Product name \t\t\t\t\t\t\t  Price \n')


###################################################################################################################
f1=Frame(win,bd=1,relief=SOLID,background='#1f304e')	
f1.pack(side=RIGHT,fill=Y)

l5=Label(f1,text='Section for inserting new medicines',font =('Bookman Old Style',14),background='#1f304e',fg='white')
l5.grid(row=0,column=0,pady=5,padx=5,columnspan=2)

l6=Label(f1,text='Enter new medicine name:- ',font =('Consolas',12,'bold'),fg='lightblue',bg='#1f304e')
l6.grid(row=1,column=0,sticky=W)
ent6=Entry(f1,width=40)
ent6.grid(row=1,column=1,padx=11,sticky=W)

l7=Label(f1,text='Enter Quantity of the medicines:- ',font =('Consolas',12,'bold'),fg='lightblue',bg='#1f304e')
l7.grid(row=2,column=0,sticky=W)
ent7=Entry(f1,width=40)
ent7.grid(row=2,column=1,padx=11,pady=11,sticky=W)

l8=Label(f1,text='Enter Price of the medicines:- ',font =('Consolas',12,'bold'),fg='lightblue',bg='#1f304e')
l8.grid(row=3,column=0,sticky=W)
ent8=Entry(f1,width=40)
ent8.grid(row=3,column=1,padx=11,pady=1,sticky=W)

btn2=Button(f1,text='Submit Entry',command=submit)
btn2.grid(row=4,column=1,pady=15,ipady=2,ipadx=25)
# btn2.bind("<Enter>",enter)
# btn2.bind("<Leave>",leave)

btn4 =Button(f1,text='Check Medicine Details',command=show_medicine_det)
btn4.grid(row=4,column=0,pady=20,ipady=2,ipadx=25)

T =Text (f1,width=60,height=23,font=('Consolas',13))
T.grid(row=6, column=0, columnspan = 2,padx=65)

# lstbox2 = Listbox(f1,width=90,height=29)
# lstbox2.grid(row=6, column=0,columnspan=2)

win.mainloop()

# from tkinter import ttk # Normal Tkinter.* widgets are not themed!
# from ttkthemes import ThemedTk
# window = ThemedTk(theme="arc")
# Button(window, text="Quit", command=window.destroy).pack()
# window.mainloop()




