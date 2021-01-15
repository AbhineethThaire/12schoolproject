#Tkinter is the module i use to give my program a GUI
from tkinter import *
#PIL or python image library is used to put images in my program. this is PPillow, a fork of PIL, since PIL is outdated
from PIL import ImageTk,Image
#datetime is used for getting data in the date or time fformats for SQL
import datetime
#mysql connector, for intergrating python into the sql server
import mysql.connector as sql
#this is a drop down calendar to choose dates
import tkcalendar
#this is the module that gives you messa
import tkinter.messagebox
'''
To DO list:
Page1 - DONE
Page 2 -DONE
Page 3 - DONE
page 4 - not done yet. it's like nothing, jsut gotta display patient details with PID as input, it'll be done in 30 mins. i'll do it tomorrow :D
page 5 and 6 have been cancelled because this thing is almost 400 fucking lines already and it's way too much code it'll take like 30 pages if i complete it
'''
'''
set up code for making the database in SQL: you can't copy paste it all unfortunately, but just like, type it in there or smth idk

#come on, do i really need to explain this? it's just making a database man.
create database hospital;

#login table holds all the usernames and passwords
CREATE TABLE login(
	username varchar primary key
	password varchar NOT NULL);

#these are just easy to use login credentials. replace them with actual credentials if you dont want your hospital database to be hacked
INSERT INTO login VALUES('admin','admin');

#PatientData table, it contains the name, ID, sex, and other relevant details of patients
CREATE TABLE PatientData(
	OID int PRIMARY KEY,
	Name varchar NOT NULL,
	Sex varchar,
	DOB date,
	BloodGroup varchar,
	Contact int,
	Email varchar,
	Address varchar);

#appointments table, it contains all the details for appointments. primary key is appointment number, but PID is a foreign key connected to Patientdata(PID)
 CREATE TABLE appointments(
    -> Appointment_num int PRIMARY KEY,
    -> Name varchar(20) NOT NULL,
    -> PID  int NOT NULL,
    -> DrID int NOT NULL,
    -> Apt_date date,
    -> Apt_time time,
    -> Description varchar(100),
    -> FOREIGN KEY (PID) REFERENCES PatientData(PID));

aaaand that's it, all the set up you need to do to be able to use this program!
'''
#connecting to sql, replace user and password with whatever is on your personal home server
conn = sql.connect(user = 'Abhi', password = 'abhi', host = '127.0.0.1', database = 'hospital')
cursor = conn.cursor()

#The Frame objects are tkinter objects that can hold any other widget inside of them. Here, we make a Page class that inherits all the features of the Frame class, and adds a new function, show()
#There are a bunch of frames or, in this case, page objects, stacked on top of each other. show() lifts a specific one to the top. it's more convenient than using dictionaries and stuff.
#i'm too lazy to explain what *args and **kwargs do, just look it up. skip to the MainView class to see the main loop of the program
class Page(Frame):
	def __init__(self, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
	def show(self):
		self.lift()

#This is the first page object, it's our login page
class Page1(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)

		#This function just gets the login values from the entry widget. in hindsight i could have just put this into the LoginCheck function, since this is pretty dumb, but hey, it works :p
		def GetLoginValues():
			self.password = self.PasswordEntry.get()
			self.username = self.UsernameEntry.get()

		#This function compares the inputted username and password to the logi table in the database, and only allows you to access the rest of the program if the username exists in the login table,
		#and if the Password matches the username. username is primary key so you can only have one result, which is why we only need a fetchone()
		def LoginCheck(user,code):
			#access and cursor will be globalised in most functions because those two are not class variables, and are used in every page
			global access, cursor
			cursor.execute('SELECT * FROM login WHERE username = %s', (user,))
			LoginDetails = cursor.fetchone()
			if (user,code) == LoginDetails:
				access = True
				tkinter.messagebox.showinfo("Login", "Logged In Successfully")
			elif LoginDetails == None:
				access = False
				tkinter.messagebox.showinfo("Login", "Your username is not registered in the database. Contact your IT department")			
			else:
				access = False
				tkinter.messagebox.showinfo("Login", "Your password is Incorrect")
			

		#Assigning each of the images used in this page to variables
		self.LoginButtonImg = ImageTk.PhotoImage(Image.open("./Assets/ButtonImages/login.png"),)
		self.ExitButtonImg = ImageTk.PhotoImage(Image.open("./Assets/ButtonImages/exit.png"))
		self.ImgLogin = ImageTk.PhotoImage(Image.open("./Assets/BGImages/Login.jpg"), Image.ANTIALIAS)

		#Background image and the grey frame arround the buttons and entry widgets
		self.background=Label(self, image=self.ImgLogin)
		self.LoginBg = Label(self,bg = '#151414')
		self.loginlabel = Label(self.LoginBg,text = "Enter your login information", bg = 'black', fg = "white", font = ('Helvetica', 11, "bold"))

		#Login and Exit Buttons for Login Page. Currently, both the buttons just exit the program, havent gotten around to making login verification code yet
		self.Quit = Button(self, image = self.ExitButtonImg, borderwidth = 0, command = root.quit, width = 80, height = 30)
		self.Login = Button(self, image = self.LoginButtonImg, borderwidth = 0, command = lambda: [GetLoginValues(),LoginCheck(self.username,self.password)], width = 80, height = 30)

		#enntry fields for username and password. these give the values to the "username" and "password" variables, which i've globalised
		self.UsernameEntry = Entry(self.LoginBg, bd = 0)
		self.PasswordEntry = Entry(self.LoginBg, bd = 0, show = "*",)
		self.UsernameLabel = Label(self.LoginBg, bd = 0, text = "Username:", bg = "black", fg = "white")
		self.PasswordLabel = Label(self.LoginBg, bd = 0, text = "Password:", bg = "black", fg = "white")


		#placing each widget
		self.background.place(x=0,y=0,relwidth=1, relheight=1)
		self.LoginBg.place(relx = 0.4,rely = 0.15, width = 250, height = 500)
		self.loginlabel.place(relx = 0.09, rely =0.15)

		self.Quit.place(relx = 0.42, rely = 0.78)
		self.Login.place(relx = 0.514, rely = 0.78)

		self.UsernameEntry.place(relx = 0.16, rely = 0.29, height = 30, width = 170)
		self.PasswordEntry.place(relx = 0.16, rely = 0.48, height = 30, width = 170)
		self.UsernameLabel.place(relx = 0.16, rely = 0.25, height = 20, width = 170)
		self.PasswordLabel.place(relx = 0.16, rely = 0.45, height = 20, width = 170)


class Page2(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		
		#This function Updates the table records to whatever you input into the fields
		def UpdatePatientData():
			global cursor
			PID = self.GetPatientID.get()
			Name = self.GetPatientName.get()
			Sex = self.GetPatientSex.get()
			DOB = self.GetPatientDOB.get()
			BloodGroup = self.GetPatientBloodGroup.get()
			Contact = self.GetPatientContactNumber.get()
			Email = self.GetPatientEmail.get()
			Address = self.GetPatientAddress.get()
			cursor.execute('''UPDATE PatientData
				              SET NAME = %s, Sex = %s, DOB = %s, Bloodgroup = %s, Contact = %s, Email = %s, Address = %s
				              WHERE PID = %s;''',(Name,Sex,DOB,BloodGroup,Contact,Email,Address,PID))
			#this is just as a sort of confirmation that yes, something actually happened.
			# i want to put in a try except block to catch any errors arising from incorrect data types, i'll do that in the final draft
			tkinter.messagebox.showinfo("Hospital Database System", "Patient data updated successfully")
			

		#This function adds the data given in the entry widgets into the PatientData table. also need a try except block for this.
		def SubmitPatientData():
			global cursor
			PID = self.GetPatientID.get()
			Name = self.GetPatientName.get()
			Sex = self.GetPatientSex.get()
			DOB = self.GetPatientDOB.get()
			BloodGroup = self.GetPatientBloodGroup.get()
			Contact = self.GetPatientContactNumber.get()
			Email = self.GetPatientEmail.get()
			Address = self.GetPatientAddress.get()
			cursor.execute("INSERT INTO PatientData VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(PID,Name,Sex,DOB,BloodGroup,Contact,Email,Address))
			conn.commit()
			tkinter.messagebox.showinfo("Hospital Database System", "Patient data submitted successfully")

		#This function deletes patient data, you only need to put in the primary key, i.e the PID for it. the askyesno messagebox is just confirmation so you dont accidentally delete things
		def DeletePatientData():
			global cursor
			PID = self.GetPatientID.get()
			if tkinter.messagebox.askyesno("Deleting data", "are you sure you wish to delete this patient's data?"):
				cursor.execute("DELETE FROM PatientData WHERE PID = %s", (PID,))
			conn.commit()
			tkinter.messagebox.showinfo("Hospital Database System", "Data has been deleted successfully")


		#Loading images for buttons and backgrounds
		self.BGImage = ImageTk.PhotoImage(Image.open("./Assets/BGImages/PatientRegistrationBG.jpg"), Image.ANTIALIAS)
		self.UpdateButtonImage = ImageTk.PhotoImage(Image.open("./Assets/ButtonImages/update.png"))
		self.DeleteButtonImage = ImageTk.PhotoImage(Image.open("./Assets/ButtonImages/delete.png"))
		self.SubmitButtonImage = ImageTk.PhotoImage(Image.open("./Assets/ButtonImages/submit.png"))

		#Miscellaneous Text and image labels
		self.Background = Label(self, image=self.BGImage)
		self.TextLabel = Label(self.Background, bg = "#151414")
		self.Heading = Label(self.TextLabel, text = "Patient Registration", bg = "black", fg = "white", font = ('Roboto', 22, "bold"))

		#Labels placed above entry widgets
		self.PatientIDLabel = Label(self.TextLabel, bd = 0, text = "Patient ID", bg = "black", fg = "white")
		self.PatientNameLabel = Label(self.TextLabel, bd = 0, text = "Patient Name", bg = "black", fg = "white")
		self.PatientSexLabel = Label(self.TextLabel, bd = 0, text = "Sex", bg = "black", fg = "white")
		self.PatientDOBLabel = Label(self.TextLabel, bd = 0, text = "Date Of Birth", bg = "black", fg = "white")
		self.PatientBloodGroupLabel = Label(self.TextLabel, bd = 0, text = "Blood Group", bg = "black", fg = "white")
		self.PatientContactNumberLabel = Label(self.TextLabel, bd = 0, text = "Contact Number", bg = "black", fg = "white")
		self.PatientEmailLabel = Label(self.TextLabel, bd = 0, text = "Email Address", bg = "black", fg = "white")
		self.PatientAddressLabel = Label(self.TextLabel, bd = 0, text = "Home Address", bg = "black", fg = "white")

		#buttons
		self.UpdateButton = Button(self.TextLabel,image = self.UpdateButtonImage, borderwidth = 0, command = UpdatePatientData, width = 80, height = 30)
		self.SubmitButton = Button(self.TextLabel,image = self.SubmitButtonImage, borderwidth = 0, command = SubmitPatientData, width = 80, height = 30)
		self.DeleteButton = Button(self.TextLabel,image = self.DeleteButtonImage, borderwidth = 0, command = DeletePatientData, width = 80, height = 30)

		#Entry Widgets for patient data
		self.GetPatientID = Entry(self.TextLabel, bd = 0)
		self.GetPatientName = Entry(self.TextLabel, bd = 0)
		self.GetPatientSex = Entry(self.TextLabel, bd = 0)
		self.GetPatientDOB = tkcalendar.DateEntry(self.TextLabel, bd = 0, date_pattern = 'yyyy/MM/dd')
		self.GetPatientBloodGroup = Entry(self.TextLabel, bd = 0)
		self.GetPatientContactNumber = Entry(self.TextLabel, bd = 0)
		self.GetPatientEmail = Entry(self.TextLabel, bd = 0)
		self.GetPatientAddress = Entry(self.TextLabel, bd = 0)
						

		#Placing everything
		#i use place because it's much more precise than pack, even though its a bit of a pain in the ass. relwith, relx/y etc. are just size and position decided relative to the main
		#widget theyre placed on, whether its the background widget or the grey box.
		self.Background.place(relx=0,rely=0,relwidth=1, relheight=1)
		self.TextLabel.place(relx = 0.34375,rely = 0, width = 400, height = 700)
		self.Heading.place(relx = 0.15, rely = 0)

		self.GetPatientID.place(relx = 0.2, rely = 0.1, height = 30, width = 170)
		self.GetPatientName.place(relx = 0.2, rely = 0.2, height = 30, width = 170)
		self.GetPatientSex.place(relx = 0.2, rely = 0.3, height = 30, width = 170)
		self.GetPatientDOB.place(relx = 0.2, rely = 0.4, height = 30, width = 170)
		self.GetPatientBloodGroup.place(relx = 0.2, rely = 0.5, height = 30, width = 170)
		self.GetPatientContactNumber.place(relx = 0.2, rely = 0.6, height = 30, width = 170)
		self.GetPatientEmail.place(relx = 0.2, rely = 0.7, height = 30, width = 170)
		self.GetPatientAddress.place(relx = 0.2, rely = 0.8, height = 30, width = 170)

		self.PatientIDLabel.place(relx = 0.2, rely = 0.07, height = 20, width = 170)
		self.PatientNameLabel.place(relx = 0.2, rely = 0.17, height = 20, width = 170)
		self.PatientSexLabel.place(relx = 0.2, rely = 0.27, height = 20, width = 170)
		self.PatientDOBLabel.place(relx = 0.2, rely = 0.37, height = 20, width = 170)
		self.PatientBloodGroupLabel.place(relx = 0.2, rely = 0.47, height = 20, width = 170)
		self.PatientContactNumberLabel.place(relx = 0.2, rely = 0.57, height = 20, width = 170)
		self.PatientEmailLabel.place(relx = 0.2, rely = 0.67, height = 20, width = 170)
		self.PatientAddressLabel.place(relx = 0.2, rely = 0.77, height = 20, width = 170)

		self.UpdateButton.place(relx = 0.7,rely = 0.4)
		self.SubmitButton.place(relx = 0.7,rely = 0.5)
		self.DeleteButton.place(relx = 0.7,rely = 0.6)


class Page3(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)

		#This function adds appointment data to the appointments table. needs a try except block for when you add PIDs that don't already exist
		def SetAppointmen():
			tkinter.messagebox.showinfo("Hospital Database System", "Appointment has been set")

		def SetAppointment():
			global cursor
			Name = self.GetPatientName.get()
			PID = self.GetPatientID.get()
			DrID = self.GetDoctorID.get()
			AptNum = self.GetAppointmentNumber.get()
			AptDate = self.GetAppointmentDate.get()
			AptTime = datetime.datetime.strptime(self.GetAppointmentTime.get(), '%H:%M:%S')
			AptDesc = self.GetAppointmentDesc.get()
			cursor.execute("INSERT INTO appointments VALUES(%s,%s,%s,%s,%s,%s,%s);",(Name,PID,DrID,AptNum,AptDate,AptTime,AptDesc))
			conn.commit()
			tkinter.messagebox.showinfo("Hospital Database System", "Appointment has been set")

		#Deletes appointments. only need to put in the appointment number for this.
		def DeleteAppointment():
			global cursor
			num = self.GetAppointmentNumber.get()
			if tkinter.messagebox.askyesno("Deleting Appointment", "are you sure you wish to cancel this appointment?"):
				try:
					cursor.execute("DELETE FROM PatientData WHERE Appointment_num = %s", (num,))
				except:
					tkinter.messagebox.showerror("Hospital Database System", "Appointments can only be deleted if patient is already registered")
					return None
			conn.commit()
			tkinter.messagebox.showinfo("Hospital Database System", "Appointment Cancelled Successfully")


		#Images used in this page
		self.BGImage = ImageTk.PhotoImage(Image.open("./Assets/BGImages/appointmentbg.jpg"), Image.ANTIALIAS)
		self.set_appimg = ImageTk.PhotoImage(Image.open("./Assets/ButtonImages/set_app.png"))
		self.delete_appimg = ImageTk.PhotoImage(Image.open("./Assets/ButtonImages/delete_app.png"))

		#Background and the grey box
		self.background = Label(self,image = self.BGImage)
		self.TextLabel= Label(self.background, bg = '#151414')
		self.Heading = Label(self.TextLabel, text = "Appointment Booking", bg = "black", fg = "white", font = ('Roboto', 22, "bold"))

		#buttons
		self.set_app = Button(self.TextLabel,image = self.set_appimg, borderwidth = 0, command = SetAppointmen, width = 80, height = 30)
		self.delete_app = Button(self.TextLabel,image = self.delete_appimg, borderwidth = 0, command = DeleteAppointment, width = 80, height = 30)

		#Labels above the entry widgets
		self.PatientNameLabel = Label(self.TextLabel, text = "PatientName", bd = 0, bg = "black", fg = "white")
		self.PatientIDLabel = Label(self.TextLabel, text = "Patient ID", bd = 0, bg = "black", fg = "white")
		self.DoctorIDLabel = Label(self.TextLabel, text = "Doctor ID", bd = 0, bg = "black", fg = "white")
		self.AppointmentNumberLabel = Label(self.TextLabel, text = "Appointment Number", bd = 0, bg = "black", fg = "white")
		self.AppointmentDateLabel = Label(self.TextLabel, text = "Appointment Date", bd = 0, bg = "black", fg = "white")
		self.AppointmentTimeLabel = Label(self.TextLabel, text = "Appointment Time", bd = 0, bg = "black", fg = "white")
		self.AppointmentDescriptionLabel = Label(self.TextLabel, text = "Description", bd = 0, bg = "black", fg = "white")

		#Entry widgets
		self.GetPatientName = Entry(self.TextLabel, bd = 0)
		self.GetPatientID = Entry(self.TextLabel, bd = 0)
		self.GetDoctorID = Entry(self.TextLabel, bd = 0)
		self.GetAppointmentNumber = Entry(self.TextLabel, bd = 0)
		self.GetAppointmentDate = tkcalendar.DateEntry(self.TextLabel, bd = 0, date_pattern = 'yyyy/MM/dd')
		self.GetAppointmentTime = Entry(self.TextLabel, bd = 0)
		self.GetAppointmentDesc = Entry(self.TextLabel, bd = 0)


		#placing all of the widgets
		self.background.place(relx=0,rely=0,relwidth=1, relheight=1)
		self.TextLabel.place(relx = 0.34375,rely = 0, width = 400, height = 700)
		self.Heading.place(relx = 0.11, rely = 0)

		self.GetPatientID.place(relx = 0.2875, rely = 0.1, height = 30, width = 170)
		self.GetPatientName.place(relx = 0.2875, rely = 0.2, height = 30, width = 170)
		self.GetDoctorID.place(relx = 0.2875, rely = 0.3, height = 30, width = 170)
		self.GetAppointmentNumber.place(relx = 0.2875, rely = 0.4, height = 30, width = 170)
		self.GetAppointmentDate.place(relx = 0.2875, rely = 0.5, height = 30, width = 170)
		self.GetAppointmentTime.place(relx = 0.2875, rely = 0.6, height = 30, width = 170)
		self.GetAppointmentDesc.place(relx = 0.2875, rely = 0.7, height = 30, width = 170)


		self.PatientNameLabel.place(relx = 0.2875, rely = 0.07, height = 20, width = 170)
		self.PatientIDLabel.place(relx = 0.2875, rely = 0.17, height = 20, width = 170)
		self.DoctorIDLabel.place(relx = 0.2875, rely = 0.27, height = 20, width = 170)
		self.AppointmentNumberLabel.place(relx = 0.2875, rely = 0.37, height = 20, width = 170)
		self.AppointmentDateLabel.place(relx = 0.2875, rely = 0.47, height = 20, width = 170)
		self.AppointmentTimeLabel.place(relx = 0.2875, rely = 0.57, height = 20, width = 170)
		self.AppointmentDescriptionLabel.place(relx = 0.2875, rely = 0.67, height = 20, width = 170)


		self.set_app.place(relx = 0.2875, rely = 0.8, height = 30, width = 170)
		self.delete_app.place(relx = 0.2875, rely = 0.9, height = 30, width = 170)


class Page4(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)

		#this function searches and displays patient info
		def SearchInformation():
			global cursor
			#this nested function converts tuples to strings so that they get displayed correctly
			def ConvertTuple(tup): 
				string =  ''.join(tup) 
				return string
			PID = self.GetPatientID.get()
			#we keep making SQL Queries and assign them to StringVars. i realised halfway through typing this that i could just use a loop but eh whatever
			cursor.execute("SELECT Name FROM PatientData WHERE PID = %s", (PID,))
			name = ConvertTuple(cursor.fetchone())
			cursor.execute("SELECT Sex FROM PatientData WHERE PID = %s", (PID,))
			sex = ConvertTuple(cursor.fetchone())
			cursor.execute("SELECT DOB FROM PatientData WHERE PID = %s", (PID,))
			dob = cursor.fetchone()
			cursor.execute("SELECT BloodGroup FROM PatientData WHERE PID = %s", (PID,))
			blood = ConvertTuple(cursor.fetchone())
			cursor.execute("SELECT Contact FROM PatientData WHERE PID = %s", (PID,))
			contact = cursor.fetchone()
			cursor.execute("SELECT Email FROM PatientData WHERE PID = %s", (PID,))
			email = ConvertTuple(cursor.fetchone())
			cursor.execute("SELECT Address FROM PatientData WHERE PID = %s", (PID,))
			address = ConvertTuple(cursor.fetchone())
			self.ShowPatientName.configure(text = name)
			self.ShowPatientSex.configure(text = sex)
			self.ShowPatientDOB.configure(text = dob)
			self.ShowPatientBloodGroup.configure(text = blood)
			self.ShowPatientContact.configure(text = contact)
			self.ShowPatientEmail.configure(text = email)
			self.ShowPatientAddress.configure(text = address)

		#Images used in this page
		self.BGImage = ImageTk.PhotoImage(Image.open("./Assets/BGImages/SearchBG.jpg"), Image.ANTIALIAS)
		self.SearchImage= ImageTk.PhotoImage(Image.open("./Assets/ButtonImages/search.png"))

		#Background and the grey box
		self.background = Label(self,image = self.BGImage)
		self.TextLabel= Label(self.background, bg = '#151414')
		self.Heading = Label(self.TextLabel, text = "Patient Data", bg = "black", fg = "white", font = ('Roboto', 22, "bold"))

		#button
		self.SearchButton = Button(self.TextLabel,image = self.SearchImage, borderwidth = 0, command = SearchInformation, width = 80, height = 30)

		#Labels above the widgets
		self.PatientIDLabel = Label(self.TextLabel, text = "Enter Patient ID", bd = 0, bg = "black", fg = "white")
		self.PatientNameLabel = Label(self.TextLabel, text = "Name", bd = 0, bg = "black", fg = "white")
		self.PatientSexLabel = Label(self.TextLabel, text = "Sex", bd = 0, bg = "black", fg = "white")
		self.PatientDOBLabel = Label(self.TextLabel, text = "Date Of Birth", bd = 0, bg = "black", fg = "white")
		self.PatientBloodGroupLabel = Label(self.TextLabel, text = "Blood Group", bd = 0, bg = "black", fg = "white")
		self.PatientContactLabel = Label(self.TextLabel, text = "Contact Number", bd = 0, bg = "black", fg = "white")
		self.PatientEmailLabel = Label(self.TextLabel, text = "Email Address", bd = 0, bg = "black", fg = "white")
		self.PatientAddressLabel = Label(self.TextLabel, text = "Address", bd = 0, bg = "black", fg = "white")

		#widgets
		self.GetPatientID = Entry(self.TextLabel, text = "")
		self.ShowPatientName = Entry(self.TextLabel, text = "", bg = '#151414', fg = "white")
		self.ShowPatientSex = Label(self.TextLabel, text = "", bg = '#151414', fg = "white")
		self.ShowPatientDOB = Label(self.TextLabel, text = "", bg = '#151414', fg = "white")
		self.ShowPatientBloodGroup = Label(self.TextLabel, text = "", bg = '#151414', fg = "white")
		self.ShowPatientContact = Label(self.TextLabel, text = "", bg = '#151414', fg = "white")
		self.ShowPatientEmail = Label(self.TextLabel, text = "", bg = '#151414', fg = "white")
		self.ShowPatientName = Label(self.TextLabel, text = "", bg = '#151414', fg = "white")		
		self.ShowPatientAddress = Message(self.TextLabel, text = "", bg = '#151414', fg = "white")

		#placing all of the widgets
		self.background.place(relx=0,rely=0,relwidth=1, relheight=1)
		self.TextLabel.place(relx = 0.34375,rely = 0, width = 400, height = 700)
		self.Heading.place(relx = 0.11, rely = 0)

		self.GetPatientID.place(relx = 0.2875, rely = 0.1, height = 30, width = 170)
		self.ShowPatientName.place(relx = 0.2875, rely = 0.2, height = 30, width = 170)
		self.ShowPatientSex.place(relx = 0.2875, rely = 0.3, height = 30, width = 170)
		self.ShowPatientDOB.place(relx = 0.2875, rely = 0.4, height = 30, width = 170)
		self.ShowPatientBloodGroup.place(relx = 0.2875, rely = 0.5, height = 30, width = 170)
		self.ShowPatientContact.place(relx = 0.2875, rely = 0.6, height = 30, width = 170)
		self.ShowPatientEmail.place(relx = 0.2875, rely = 0.7, height = 30, width = 170)
		self.ShowPatientAddress.place(relx = 0.2875, rely = 0.8, height = 60, width = 170)


		self.PatientIDLabel.place(relx = 0.2875, rely = 0.07, height = 20, width = 170)
		self.PatientNameLabel.place(relx = 0.2875, rely = 0.17, height = 20, width = 170)
		self.PatientSexLabel.place(relx = 0.2875, rely = 0.27, height = 20, width = 170)
		self.PatientDOBLabel.place(relx = 0.2875, rely = 0.37, height = 20, width = 170)
		self.PatientBloodGroupLabel.place(relx = 0.2875, rely = 0.47, height = 20, width = 170)
		self.PatientContactLabel.place(relx = 0.2875, rely = 0.57, height = 20, width = 170)
		self.PatientEmailLabel.place(relx = 0.2875, rely = 0.67, height = 20, width = 170)
		self.PatientAddressLabel.place(relx = 0.2875, rely = 0.77, height = 20, width = 170)


		self.SearchButton.place(relx = 0.2875, rely = 0.9, height = 30, width = 170)

'''
This is the class for the base/main frame, that displays all the other frames on top of itself. the "root" window is the 
main window, and This one's a frame that always draws on top of root, so it basically does the same exact thing


The way this works is, the moment you start up the program, all the frames are placed one by one into a frame inside the Main frame, and then the first frame,
page1, is displayed. each page is given a variable, and everytime a page button is clicked, the command first checks if you have logged in properly through the
"access" variable, then it does page.lift() to bring up that frame. the frames are kept constantly loaded, which sometimes causes issues with everything glitching
out and disappearing when you move the main window, but it gets fixed if you go to another frame then back to the one you were on. not fixing that bug.
'''
class MainView(Frame):
	def __init__(self, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)

		def CheckPageAccess(access,page):
			AccessDeniedLabel = Label(self, text = "Please enter your login details to proceed", bd = 2)
			if access == 1:
				page.lift()
			else:
				AccessDeniedLabel.place(relx = 0.41, rely = 0.7)


		#assigning each one of the previous frame classes to a variable
		p1 = Page1(self)
		p2 = Page2(self)
		p3 = Page3(self)
		p4 = Page4(self)

		buttonframe = Frame(self)
		container = Frame(self)
		buttonframe.pack(side="top", fill="x", expand=False)
		container.pack(side="top", fill="both", expand=True)

		p1.place(in_=container, x=0, y=0, relwidth=1, relheight= 1)
		p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)


		b1 = Button(buttonframe, text="Login", command=p1.lift)
		b2 = Button(buttonframe, text="Patient Registration", command=lambda: [CheckPageAccess(access,p2)])
		b3 = Button(buttonframe, text="Appointment Booking", command=lambda: [CheckPageAccess(access,p3)])
		b4 = Button(buttonframe, text="Patient Data", command=lambda: [CheckPageAccess(access,p4)])


		b1.pack(side="left")
		b2.pack(side="left")
		b3.pack(side="left")
		b4.pack(side="left")


		p1.show()

#defining access first so our login checks can use it. it resets to false everytime the program closes.
access = False

#here we make root into a TK class object, which is just a window to put all the widgets in.
root = Tk()

#assigning the MainView frame object to a variable so we can then pack it into the root window
main = MainView(root)
main.pack(side="top", fill="both", expand=True)

#these are just the dimensions of the window. you COULD make it 1920x1080 or smth but that's gonna break literally all the widgets since those were based on pixel count.
root.wm_geometry("1280x720")

#the main loop that keeps going on. it's basically just your program. exiting the window is just stopping this loop.
root.mainloop()

#closing connection to SQL
conn.close()
