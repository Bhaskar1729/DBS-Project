from tkinter import *
import tkinter.messagebox
import tkinter.font as font
import mysql.connector as sqltor
import tkinter as tk

mainWindow = None

databaseRootPassword = "Password" # TODO: change to your mySQL root user password

studentId = ""  # Global variable for tracking studentId

mydb = sqltor.connect(
    user = "root",
    host = "localhost",
    password = databaseRootPassword,
    database = "assignment_manager")

root = Tk()
cursor = mydb.cursor()

myfont = font.Font(size = 15)

student = 0
id = 0

def window():
    global root
    root.destroy()
    root=Tk()
    
    
    root.geometry('800x800')
    root.configure(bg='white')
    root.resizable(False, False)


def chooseLogin():
    global root
    window()

    Student = Button(root, background = "white", command = studentLogin, text = "Student", font = myfont)
    Student.pack(anchor = "center", pady = 100)
    Admin = Button(root, background = "white", command = TeacherLogin, text = "Teacher", font = myfont)
    Admin.pack(anchor = "center")

    

def TeacherLogin():
    global root
    global id
    id = 0
    window()
    Label(root, text = "Username", background = "white", font = myfont).pack(pady = (100, 20), anchor = "center")
    user = Entry(root, text = "1")
    user.pack(pady = 20, anchor = "center")
    Label(root, text = "Password", background = "white", font = myfont).pack(pady = (50, 20), anchor = "center")
    pwd = Entry(root, show = "*", text="bob")
    pwd.pack(pady = 20, anchor = "center")

    frame = Frame(root, background = "white")
    frame.pack()
    Button(frame, text = "Back", command = chooseLogin, font = myfont).pack(side = LEFT, padx = 5, pady = 20)
    

    def action1():
        global id
        userid = user.get()
        password = pwd.get()
        cursor.execute("Select instructor_auth(%s, %s)", (int(userid), password))
        a = cursor.fetchall()
        if a[0][0] == 1:
            student = 0
            id = userid
            TeacherMainPage()
        
        else:
            tkinter.messagebox.showinfo("Error", "Userid and password do not match")
            

    
    Button(frame, text = "Login", command = action1, font = myfont).pack(side = LEFT, padx = 5)
    Button(frame, text = "Register new teacher", command = createNewTeacher, font = myfont).pack(side = LEFT, padx = 10)
    

def TeacherMainPage():
    global root
    window()
    cursor.execute("Select InstructorName from Instructor where InstructorID = %s", (id,))
    name = cursor.fetchall()[0][0]
    Label(root, text = "Welcome " + name, font = myfont).pack(pady = (20, 50))
    Button(root, text = "Add assignment", font = myfont, command = AddAssignment).pack(pady = (30, 0), anchor = CENTER)
    Button(root, text = "Edit assignment", font = myfont, command = editAssignment).pack(pady = (30, 0))
    Button(root, text = "View Assignment Statistics", font = myfont, command = assignmentstats).pack(pady = (30, 0), anchor = CENTER)
    Button(root, text = "Grade submissions", font = myfont, command = gradeSubmissions).pack(pady = (30, 0), anchor = CENTER)
    Button(root, text = "View Submissions", font = myfont, command = viewSubmission).pack(pady = (30, 0))
    Button(root, text = "Update details", font = myfont, command = UpdateDetails).pack(pady = (30, 0))
    Button(root, text = "Log out", font = myfont, command = TeacherLogin).pack(pady = (30, 0))

def AddAssignment():
    global root
    window()
    Label(root, text = "Enter Assignment Name", font = myfont).pack(pady = (100, 0))
    aname = Entry(root)
    aname.pack(pady = 20)
    Label(root, text = "Enter the assignment's course's code", font = myfont).pack(pady = 20)
    cvar = StringVar()
    
    cursor.execute("Select CourseCode from Course where instructorid = %s", (id,))
    temp = cursor.fetchall()
    cOptions = []
    for i in temp:
        cOptions.append(i[0])
    if cOptions == []:
        cOptions = ["hi"]
    c_code = OptionMenu(root, cvar, *cOptions)
    c_code.pack(pady = 20)
    if cOptions == ["hi"]:
        c_code['menu'].delete(0, 'end')
    Label(root, text = "Enter deadline", font = myfont).pack(pady = 20)


    frame = Frame(root, background = "white")
    frame.pack(pady = 20, anchor = CENTER)
    dvar = StringVar()
    dateOptions = [i for i in range(1, 32)]
    date = OptionMenu(frame, dvar, *dateOptions)
    date.pack(side = LEFT, padx = 10)

    mvar = StringVar()
    monthOptions = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    month = OptionMenu(frame, mvar, *monthOptions)
    month.pack(side = LEFT, padx = 10)

    yvar = StringVar()
    yearOptions = [i for i in range(2000, 2030)]
    year = OptionMenu(frame, yvar, *yearOptions)
    year.pack(side = LEFT, padx = 10)

    def action1():
        if cvar.get() == "":
            tkinter.messagebox.showerror("Error", "Enter the details corretly")
            return None
        d = dvar.get()
        m = mvar.get()
        m = str(monthOptions.index(m)+1)
        y = yvar.get()
        if len(m) == 1:
            m = "0" + m
        
        if d == "" or m == "" or y == "":
            tkinter.messagebox.showerror("Error", "Enter the details corretly")
            return None

        cursor.execute("call create_assignment(%s, %s, %s)", (aname.get(), y + "-" + m + "-" + d + " " + "23:59:59", int(cvar.get())))
        mydb.commit()
        
        cursor.execute("select assignmentid from assignment where assignmentname = %s, coursecode = %s", (aname.get(), int(cvar.get())))
        a = cursor.fetchall()[0][0]
        tkinter.messagebox.showinfo("Info", "Assignment created successfully. The assignment id is " + str(a))
        #TeacherMainPage()
                        
    frame2 = Frame(root, background = "white")
    frame2.pack(pady = 20)
    Button(frame2, text = "Add assignment", command = action1, font = myfont).pack(padx = 10, side = LEFT)
    Button(frame2, text = "Back", command = TeacherMainPage, font = myfont).pack(padx = 10, side = LEFT)


def gradeSubmissions():
    global root
    window()
    cursor.execute("Select InstructorName from Instructor where InstructorID = %s", (id,))
    name = cursor.fetchall()[0][0]
    Label(root, text = "Welcome " + name, font = myfont).pack(pady = (20, 50))
    
    frame1 = Frame(root, background="white")
    frame1.pack(pady = 20)
    Label(frame1, text = "Choose the course code", font = myfont).pack(padx = 10, side = LEFT)
    varccode = StringVar()
    cursor.execute("Select coursecode from course where instructorId = %s", (id, ))
    courseOptions = cursor.fetchall()
    for i in range(len(courseOptions)):
        courseOptions[i] = courseOptions[i][0]
    
    
    c_code = OptionMenu(frame1, varccode, *courseOptions)
    c_code.pack(padx = 10, side = LEFT)
    assignmentOptions = ["NULL"]

    def action1():
        #global aid, varaid
        #global assignmentOptions
        course = varccode.get()
        cursor.execute("Select assignmentid from assignment where coursecode = %s", (course,))
        assignmentOptions = cursor.fetchall()
        aid['menu'].delete(0, 'end')
        submissionId['menu'].delete(0, 'end')
        varaid.set('')
        varsid.set("")

        content.configure(text = "")
        for i in range(len(assignmentOptions)):
            aid['menu'].add_command(label=assignmentOptions[i][0], command=tkinter._setit(varaid, assignmentOptions[i][0]))
    
    frame2 = Frame(root, background="white")
    frame2.pack(pady = 20)
    Label(frame2, text = "Choose the assignment id", font = myfont).pack(padx = 10, side = LEFT)
    varaid = StringVar()
    aid = OptionMenu(frame2, varaid, *assignmentOptions)
    aid.pack(padx = 10, side = LEFT)
    aid['menu'].delete(0, 'end')
    submissionOptions = [' ']
    b1 = Button(frame1, text = "Select", command = action1, font = myfont).pack(side = LEFT)

    def action2():
        #global varsid, submissionId
        cursor.execute("select submissionid from submission where assignmentid = %s", (varaid.get(),))
        submissionId['menu'].delete(0, 'end')
        varsid.set('')
        content.configure(text = "")
        submissionOptions = cursor.fetchall()
        for i in range(len(submissionOptions)):
            submissionId['menu'].add_command(label=submissionOptions[i][0], command=tkinter._setit(varsid, submissionOptions[i][0]))

    
    frame3 = Frame(root, background="white")
    frame3.pack(pady = 20)
    Label(frame3, text = "Choose Submission id", font = myfont).pack(padx = 10, side = LEFT)
    varsid = StringVar()
    submissionId = OptionMenu(frame3, varsid, *submissionOptions)
    submissionId.pack(padx = 10, side = LEFT)
    submissionId['menu'].delete(0, 'end')
    content = Label(root, text = "", font = myfont)
    content.pack(pady = 20)
    Button(frame2, text = "Select", font = myfont, command = action2).pack(padx = 10, side = LEFT)

    
    def action3():
        cursor.execute("Select SubmissionContent from Submission where submissionid = %s", (varsid.get(), ))
        contentText = cursor.fetchall()
        if len(contentText) == 0:
            return None
        content.configure(text = contentText[0][0])
    
    Button(frame3, command = action3, text = "Select", font = myfont).pack(side = LEFT, padx = 10)

    frame4 = Frame(root, background="white")
    frame4.pack(pady = 20)
    Label(frame4, text = "Grade", font = myfont).pack(padx = 10, side = LEFT)
    grade = Entry(frame4)
    grade.pack(padx = 10, side = LEFT)

    def action4():
        if (grade.get().isnumeric == False or grade.get() == ""):
            tkinter.messagebox.showinfo("Error", "Enter integer grade between 0 and 10")
            return None
        
        elif (int(grade.get()) < 0 or int(grade.get()) > 10):
            tkinter.messagebox.showinfo("Error", "Enter integer grade between 0 and 10")
            return None
        
        if (varsid.get() == ""):
            tkinter.messagebox.showinfo("Error", "Choose submission first")
            return None
        
        cursor.execute("call grade_assignment(%s, %s)", (varsid.get(), grade.get()))
        mydb.commit()

    Button(frame4, text = "Assign", font = myfont, command = action4).pack(side = LEFT, padx = 10)
    
    frame5 = Frame(root, background="white")
    frame5.pack(pady = 20)
    Label(frame5, text = "Feedback", font = myfont).pack(side = LEFT, padx =10)
    feedback = Text(frame5, width = 30, height = 4)
    feedback.pack(padx = 10, side = LEFT)

    def action5():
        if (varsid.get() == ""):
            tkinter.messagebox.showinfo("Error", "Choose submission first")
            return None
        
        cursor.execute("call give_feedback(%s, %s)", (varsid.get(), feedback.get("1.0", END)))
        mydb.commit()
    Button(frame5, text = "Give feedback", font = myfont, command = action5).pack(padx =10, side = LEFT)
    Button(root, text = "Back", command = TeacherMainPage, font = myfont).pack()

def assignmentstats():
    global root
    window()
    cursor.execute("Select InstructorName from Instructor where InstructorID = %s", (id,))
    name = cursor.fetchall()[0][0]
    Label(root, text = "Welcome " + name, font = myfont).pack(pady = (20, 50))
    
    frame1 = Frame(root, background="white")
    frame1.pack(pady = 20)
    Label(frame1, text = "Choose the course code", font = myfont).pack(padx = 10, side = LEFT)
    varccode = StringVar()
    cursor.execute("Select coursecode from course where instructorId = %s", (id, ))
    courseOptions = cursor.fetchall()
    for i in range(len(courseOptions)):
        courseOptions[i] = courseOptions[i][0]
    
    
    c_code = OptionMenu(frame1, varccode, *courseOptions)
    c_code.pack(padx = 10, side = LEFT)
    assignmentOptions = ["NULL"]

    def action1():
        course = varccode.get()
        cursor.execute("Select assignmentid from assignment where coursecode = %s", (course,))
        assignmentOptions = cursor.fetchall()
        aid['menu'].delete(0, 'end')
        varaid.set("")
        stats.config(text= "")
        for i in range(len(assignmentOptions)):
            aid['menu'].add_command(label=assignmentOptions[i][0], command=tkinter._setit(varaid, assignmentOptions[i][0]))
    
    frame2 = Frame(root, background="white")
    frame2.pack(pady = 20)
    Label(frame2, text = "Choose the assignment id", font = myfont).pack(padx = 10, side = LEFT)
    varaid = StringVar()
    aid = OptionMenu(frame2, varaid, *assignmentOptions)
    aid.pack(padx = 10, side = LEFT)
    aid['menu'].delete(0, 'end')
    submissionOptions = [' ']
    b1 = Button(frame1, text = "Select", command = action1, font = myfont).pack(side = LEFT)

    def action2():
        if (varaid.get() == ""):
            tkinter.messagebox.showinfo("Error", "Choose assignment first")
            return None
    
        cursor.execute("Select completion_statistic(%s)", (varaid.get(),))
        compRate = cursor.fetchall()[0][0]
        cursor.execute("Select average_grade_statistic(%s)", (varaid.get(), ))
        ag = cursor.fetchall()[0][0]
        if (ag is None):
            ag = 0
        stats.config(text = "The completion rate of this assignment is " + str(compRate) + " and the average grade is " + str(ag))

    
    Button(frame2, text = "Select", font = myfont, command = action2).pack(side = LEFT, padx = 10)

    stats = Label(root, font = myfont, wraplength=300, justify=CENTER)
    stats.pack(pady = 20)

    Button(root, text = "Back", command = TeacherMainPage, font = myfont)

def viewSubmission():
    global root
    window()
    cursor.execute("Select InstructorName from Instructor where InstructorID = %s", (id,))
    name = cursor.fetchall()[0][0]
    Label(root, text = "Welcome " + name, font = myfont).pack(pady = (20, 50))
    
    frame1 = Frame(root, background="white")
    frame1.pack(pady = 20)
    Label(frame1, text = "Choose the course code", font = myfont).pack(padx = 10, side = LEFT)
    varccode = StringVar()
    cursor.execute("Select coursecode from course where instructorId = %s", (id, ))
    courseOptions = cursor.fetchall()
    for i in range(len(courseOptions)):
        courseOptions[i] = courseOptions[i][0]
    
    
    c_code = OptionMenu(frame1, varccode, *courseOptions)
    c_code.pack(padx = 10, side = LEFT)
    assignmentOptions = ["NULL"]

    def action1():
        course = varccode.get()
        cursor.execute("Select assignmentid from assignment where coursecode = %s", (course,))
        assignmentOptions = cursor.fetchall()
        aid['menu'].delete(0, 'end')
        varaid.set("")
        varsid.get("")
        submissionId['menu'].delete(0, 'end')
        for i in range(len(assignmentOptions)):
            aid['menu'].add_command(label=assignmentOptions[i][0], command=tkinter._setit(varaid, assignmentOptions[i][0]))
    
    frame2 = Frame(root, background="white")
    frame2.pack(pady = 20)
    Label(frame2, text = "Choose the assignment id", font = myfont).pack(padx = 10, side = LEFT)
    varaid = StringVar()
    aid = OptionMenu(frame2, varaid, *assignmentOptions)
    aid.pack(padx = 10, side = LEFT)
    aid['menu'].delete(0, 'end')
    submissionOptions = [' ']
    b1 = Button(frame1, text = "Select", command = action1, font = myfont).pack(side = LEFT)

    def action2():
        cursor.execute("select submissionid from submission where assignmentid = %s", (varaid.get(),))
        submissionId['menu'].delete(0, 'end')
        submissionOptions = cursor.fetchall()
        for i in range(len(submissionOptions)):
            submissionId['menu'].add_command(label=submissionOptions[i][0], command=tkinter._setit(varsid, submissionOptions[i][0]))

    
    frame3 = Frame(root, background="white")
    frame3.pack(pady = 20)
    Label(frame3, text = "Choose Submission id", font = myfont).pack(padx = 10, side = LEFT)
    varsid = StringVar()
    submissionId = OptionMenu(frame3, varsid, *submissionOptions)
    submissionId.pack(padx = 10, side = LEFT)
    submissionId['menu'].delete(0, 'end')
    content = Label(root, text = "", font = myfont)
    content.pack(pady = 20)
    Button(frame2, text = "Select", font = myfont, command = action2).pack(padx = 10, side = LEFT)

    
    def action3():
        cursor.execute("Select SubmissionContent from Submission where submissionid = %s", (varsid.get(), ))
        contentText = cursor.fetchall()
        if len(contentText) == 0:
            return None
        content.configure(text = contentText[0][0])
    
    Button(frame3, command = action3, text = "Select", font = myfont).pack(side = LEFT, padx = 10)
    Button(root, text = "Back", font = myfont, command = TeacherMainPage).pack()


def editAssignment():
    global root
    window()
    cursor.execute("Select InstructorName from Instructor where InstructorID = %s", (id,))
    name = cursor.fetchall()[0][0]
    Label(root, text = "Welcome " + name, font = myfont).pack(pady = (20, 50))
    
    frame1 = Frame(root, background="white")
    frame1.pack(pady = 20)
    Label(frame1, text = "Choose the course code", font = myfont).pack(padx = 10, side = LEFT)
    varccode = StringVar()
    cursor.execute("Select coursecode from course where instructorId = %s", (id, ))
    courseOptions = cursor.fetchall()
    for i in range(len(courseOptions)):
        courseOptions[i] = courseOptions[i][0]
    
    if courseOptions == []:
        courseOptions = ["NULL"]

    c_code = OptionMenu(frame1, varccode, *courseOptions)
    c_code.pack(padx = 10, side = LEFT)
    c_code['menu'].delete(0, 'end')

    assignmentOptions = ["NULL"]

    def action1():
        course = varccode.get()
        cursor.execute("Select assignmentid from assignment where coursecode = %s", (course,))
        assignmentOptions = cursor.fetchall()
        aid['menu'].delete(0, 'end')
        varaid.set("")
        
        for i in range(len(assignmentOptions)):
            aid['menu'].add_command(label=assignmentOptions[i][0], command=tkinter._setit(varaid, assignmentOptions[i][0]))
    
    frame2 = Frame(root, background="white")
    frame2.pack(pady = 20)
    Label(frame2, text = "Choose the assignment id", font = myfont).pack(padx = 10, side = LEFT)
    varaid = StringVar()
    aid = OptionMenu(frame2, varaid, *assignmentOptions)
    aid.pack(padx = 10, side = LEFT)
    aid['menu'].delete(0, 'end')
    submissionOptions = [' ']
    b1 = Button(frame1, text = "Select", command = action1, font = myfont).pack(side = LEFT)

    Label(root, text = "Set new deadline as:", font = myfont).pack(pady = 20)
    frame = Frame(root, background = "white")
    frame.pack(pady = 20, anchor = CENTER)
    dvar = StringVar()
    dateOptions = [i for i in range(1, 32)]
    date = OptionMenu(frame, dvar, *dateOptions)
    date.pack(side = LEFT, padx = 10)

    mvar = StringVar()
    monthOptions = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    month = OptionMenu(frame, mvar, *monthOptions)
    month.pack(side = LEFT, padx = 10)

    yvar = StringVar()
    yearOptions = [i for i in range(2000, 2030)]
    year = OptionMenu(frame, yvar, *yearOptions)
    year.pack(side = LEFT, padx = 10)

    def action1():
        d = dvar.get()
        m = mvar.get()
        m = str(monthOptions.index(m)+1)
        y = yvar.get()
        if len(m) == 1:
            m = "0" + m

        cursor.execute("Update assignment set assignmentDeadline = %s where assignmentId = %s", (y + "-" + m + "-" + d + " " + "23:59:59", varaid.get()))
        mydb.commit()

    frame3 = Frame(root, background = "white")
    frame3.pack(pady = 20)
    Button(frame3, text = "Edit assignment", command = action1, font = myfont).pack(padx = 10, side = LEFT)
    Button(frame3, text = "Back", command = TeacherMainPage, font = myfont).pack(padx = 10, side = LEFT)
    

def UpdateDetails():
    global root
    window()
    cursor.execute("Select InstructorName from Instructor where InstructorID = %s", (id,))
    name = cursor.fetchall()[0][0]
    Label(root, text = "Welcome " + name, font = myfont).pack(pady = (20, 50))

    Label(root, text = "Enter name: ", font = myfont).pack(pady = 20)
    name = Entry(root)
    name.pack(pady = 20)

    Label(root, text = "Enter new password: ", font = myfont).pack(pady = 20)
    pwd = Entry(root)
    pwd.pack(pady = 20)
    
    Label(root, text = "Enter new phone number: ", font = myfont).pack(pady = 20)
    phnum = Entry(root)
    phnum.pack(pady = 20)

    Label(root, text = "Enter new email address", font = myfont).pack(pady = 20)
    email = Entry(root)
    email.pack(pady = 20)

    def action1():
        if email.get() == "" or phnum.get() == "" or phnum.get().isnumeric == False:
            tkinter.messagebox.showinfo("Error", "Enter appropriate details")
            return None
        
        cursor.execute("Update instructor set instructorPhone = %s, instructorEmail = %s, instructorName = %s, instructorPassword = %s where instructorID = %s", (email.get(), phnum.get(), name.get(), pwd.get(), id))
        mydb.commit()

    frame3 = Frame(root, background = "white")
    frame3.pack(pady = 20)
    Button(frame3, text = "Update details", command = action1, font = myfont).pack(padx = 10, side = LEFT)
    Button(frame3, text = "Back", command = TeacherMainPage, font = myfont).pack(padx = 10, side = LEFT)
    
def createNewTeacher():
    global root
    window()
    frame1 = Frame(root, background="white")
    frame1.pack(pady = (50, 20))
    Label(frame1, text = "Enter name: ", font = myfont).pack(padx = 10, side = LEFT)
    name = Entry(frame1)
    name.pack(padx = 10, side = LEFT)

    frame2 = Frame(root, background="white")
    frame2.pack(pady = 20)
    Label(frame2, text = "Enter password: ", font = myfont).pack(padx = 10, side = LEFT)
    password = Entry(frame2)
    password.pack(padx = 10, side = LEFT)

    frame3 = Frame(root, background="white")
    frame3.pack(pady = 20)
    Label(frame3, text = "Enter phone number: ", font = myfont).pack(padx = 10, side = LEFT)
    phonenum = Entry(frame3)
    phonenum.pack(padx = 10, side = LEFT)
    
    frame4 = Frame(root, background="white")
    frame4.pack(pady = 20)
    Label(frame4, text = "Enter email: ", font = myfont).pack(padx = 10, side = LEFT)
    email = Entry(frame4)
    email.pack(pady = 10, side = LEFT)

    frame5 = Frame(root, background = "white")
    frame5.pack(pady = 20)

    def action1():
        if (name.get() == "" or phonenum.get == "" or email.get() == "" or password.get() == "" or phonenum.get().isnumeric == False):
            tkinter.messagebox.showinfo("Error", "Enter all info correctly")
            return None

        cursor.execute("Insert into Instructor(instructorName, instructorphone, instructoremail, instructorpassword) values(%s, %s, %s, %s);", (name.get(), phonenum.get(), email.get(), password.get()))
        mydb.commit()
        cursor.execute("Select instructorid from instructor where instructorname = %s and instructorphone = %s", (name.get(), phonenum.get()))
        a = cursor.fetchall()[0][0]
        tkinter.messagebox.showinfo("Info", "Teacher created successfully. The Instructor ID is " + str(a))

    Button(frame5, text = "Create new teacher", command = action1, font = myfont).pack(padx = 10, side = LEFT)
    Button(frame5, text = "Back", command = TeacherLogin, font = myfont).pack(padx = 10, side = LEFT)
    cursor.execute("Select InstructorId from Instructor where InstructorName = %s and InstructorPhone = %s and InstructorEmail = %s", (name.get(), phonenum.get(), email.get()))
    a = cursor.fetchall()
    a = a[0][0]
    tkinter.messagebox.showinfo("Info", "Teacher has been created. The Instructor ID is " + str(a))





def connectToDb(password):
    database = sqltor.connect(
        host="localhost",
        user="root",
        password=password,
        database="assignment_manager"
    )

    return database


# mydb = connectToDb(databaseRootPassword)
cursor = mydb.cursor()


def registerStudentSql(name, passwd, email, phone, window):

    try:
        cursor.execute(f'call register_student("{name}", "{passwd}", "{email}", "{phone}");')
        mydb.commit()
        tk.messagebox.showinfo("Registered successfully!")
        window.destroy()
    except:
        tk.messagebox.showerror("Error in registering student.")

def resetPasswordSql(mail, password, window):

    try:
        if mail != "" and mail is not None:
            cursor.execute(f'call reset_student_password("{mail}", "{password}")')
            cursor.fetchall()
            mydb.commit()
        tk.messagebox.showinfo("Updated Successfully!")
        window.destroy()
    except:
        tk.messagebox.showerror("Error in updating details.")

def updateProfileSql(mail, phone, window):
    try:
        if mail != "" and mail is not None:
            cursor.execute(f'Update Student set StudentEmail = "{mail}" where StudentId = {studentId};')
            cursor.fetchall()
            mydb.commit()
        if phone != "" and phone is not None:
            cursor.execute(f'Update Student set StudentPhone = "{phone}" where StudentId = {studentId};')
            cursor.fetchall()
            mydb.commit()
        tk.messagebox.showinfo("Updated Successfully!")
        window.destroy()
    except:
        tk.messagebox.showerror("Error in updating details.")


def submitAssignmentSql(id, content, window):

    try:
        global cursor, mydb
        cursor.close()

        if (not mydb.is_connected()):
            mydb = connectToDb(databaseRootPassword)

        cursor = mydb.cursor()

        cursor.execute(f'call submit_assignment("{content}", {studentId}, {id});')
        cursor.fetchall()
        mydb.commit()
        tk.messagebox.showinfo("Submitted Successfully!")
        window.destroy()
    except:
        tk.messagebox.showerror("Error in submitting assignment.")


def loginStudentSql(id, passwd):
    global studentId, mydb, cursor

    if not mydb.is_connected():
        mydb = connectToDb(databaseRootPassword)
        cursor = mydb.cursor()

    cursor.execute(f'select student_auth({id}, "{passwd}");')

    check_value = cursor.fetchall()[0][0]
    mydb.commit()
    print(check_value)

    if check_value == 1:
        studentId = id
        choicePage()
    else:
        tk.messagebox.showerror("Invalid login.")


def viewSubmissionsSql():

    try:
        global cursor, mydb
        cursor.close()

        if (not mydb.is_connected()):
            mydb = connectToDb(databaseRootPassword)

        cursor = mydb.cursor()

        cursor.execute(f'call view_submissions_by_student_id({studentId});')
        result = cursor.fetchall()

        submissionList = []

        for record in result:
            if (record[0] == None):
                grade = "Not Graded"
            else:
                grade = record[0]
            if (record[1] == None):
                feedback = "No Feedback."
            else:
                feedback = record[1]
            datetime = record[3]
            assignment_id = record[-1]

            recordList = [assignment_id, datetime, grade, feedback]
            print(recordList)
            submissionList.append(recordList)

        return submissionList

    except:
            tk.messagebox.showerror("Error in fetching submissions.")
            return []


def activeAssignmentsSql():
    try:
        global cursor, mydb
        cursor.close()

        if (not mydb.is_connected()):
            mydb = connectToDb(databaseRootPassword)

        cursor = mydb.cursor()

        cursor.execute(f'call filter_assignment_by_student_id({studentId});')
        result = cursor.fetchall()

        assignmentList = []

        for record in result:
            id = record[0]
            name = record[1]
            deadline = record[2]
            course_code = record[3]

            recordList = [id, name, course_code, deadline]
            print(recordList)
            assignmentList.append(recordList)

        return assignmentList

    except:
        tk.messagebox.showerror("Error in fetching active assignments.")
        return []


def studentRegister():
    window = tk.Toplevel(mainWindow)

    mainHeading = tk.Label(window, text="Assignment Manager", font=("Times new roman", 26, "bold"), background="cyan")
    mainHeading.pack(side=tk.TOP, fill=tk.X, pady=20)

    detailsFrame = tk.LabelFrame(window, text="Register Student", font=("Times new roman", 20, "bold"),
                                 background="lightblue")
    detailsFrame.pack(side=tk.TOP, fill=tk.X)
    dataFrame = tk.Frame(window)
    dataFrame.pack(side=tk.TOP, fill=tk.X)

    name = tk.StringVar()
    email = tk.StringVar()
    phone = tk.StringVar()
    password = tk.StringVar()

    nameLabel = tk.Label(detailsFrame, text="Name", font=("Times new roman", 16), width=20)
    nameLabel.grid(row=1, column=0, padx=2, pady=2)
    nameEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=name)
    nameEntry.grid(row=1, column=1, padx=5, pady=2)

    emailLabel = tk.Label(detailsFrame, text="Email", font=("Times new roman", 16), width=20)
    emailLabel.grid(row=2, column=0, padx=2, pady=2)
    emailEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=email)
    emailEntry.grid(row=2, column=1, padx=5, pady=2)

    phoneLabel = tk.Label(detailsFrame, text="Phone", font=("Times new roman", 16), width=20)
    phoneLabel.grid(row=3, column=0, padx=2, pady=2)
    phoneEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=phone)
    phoneEntry.grid(row=3, column=1, padx=5, pady=2)

    passLabel = tk.Label(detailsFrame, text="Password", font=("Times new roman", 16), width=20)
    passLabel.grid(row=4, column=0, padx=2, pady=2)
    passEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=password)
    passEntry.grid(row=4, column=1, padx=5, pady=2)

    submitButton = tk.Button(detailsFrame, text="Submit", bd=3, font=("Times new roman", 15), width=15,
                             command=lambda: registerStudentSql(name.get(), password.get(), email.get(),
                                                                phone.get(), window))
    submitButton.grid(row=5, column=0, padx=2, pady=2)

    backButton = tk.Button(detailsFrame, text="Back", bd=3, font=("Times new roman", 15), width=15,
                           command=window.destroy)
    backButton.grid(row=5, column=1, padx=2, pady=2)


def studentLogin():
    global root
    root.destroy()
    global mainWindow
    mainWindow = tk.Tk()
    mainWindow.title("Assignment Manager")
    window = mainWindow

    mainHeading = tk.Label(window, text="Assignment Manager", font=("Times new roman", 26, "bold"), background="cyan")
    mainHeading.pack(side=tk.TOP, fill=tk.X, pady=20)

    detailsFrame = tk.LabelFrame(window, text="Student Login", font=("Times new roman", 20, "bold"),
                                 background="lightblue")
    detailsFrame.pack(side=tk.TOP, fill=tk.X)
    dataFrame = tk.Frame(window)
    dataFrame.pack(side=tk.TOP, fill=tk.X)

    id = tk.StringVar()
    password = tk.StringVar()

    idLabel = tk.Label(detailsFrame, text="Student ID", font=("Times new roman", 16))
    idLabel.grid(row=0, column=0, padx=2, pady=2)
    idEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=id)
    idEntry.grid(row=0, column=1, padx=5, pady=2)

    passLabel = tk.Label(detailsFrame, text="Password", font=("Times new roman", 16))
    passLabel.grid(row=1, column=0, padx=2, pady=2)
    passEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=password)
    passEntry.grid(row=1, column=1, padx=5, pady=5)

    loginButton = tk.Button(detailsFrame, text="Login", bd=3, font=("Times new roman", 15), width=15,
                            command=lambda: loginStudentSql(id.get(), password.get()))
    loginButton.grid(row=2, column=0, padx=2, pady=10)

    registerButton = tk.Button(detailsFrame, text="Register", bd=3, font=("Times new roman", 15), width=15,
                               command=studentRegister)
    registerButton.grid(row=2, column=1, padx=2, pady=10)

    resetPassButton = tk.Button(detailsFrame, text="Reset Password", bd=3, font=("Times new roman", 15), width=15,
                                command=resetPassword)
    resetPassButton.grid(row=2, column=2, padx=2, pady=10)


def resetPassword():
    window = tk.Toplevel(mainWindow)

    mainHeading = tk.Label(window, text="Assignment Manager", font=("Times new roman", 26, "bold"), background="cyan")
    mainHeading.pack(side=tk.TOP, fill=tk.X, pady=20)

    detailsFrame = tk.LabelFrame(window, text="Reset Password", font=("Times new roman", 20, "bold"),
                                 background="lightblue")
    detailsFrame.pack(side=tk.TOP, fill=tk.X)
    dataFrame = tk.Frame(window)
    dataFrame.pack(side=tk.TOP, fill=tk.X)

    email = tk.StringVar()
    password = tk.StringVar()

    idLabel = tk.Label(detailsFrame, text="Email", font=("Times new roman", 16))
    idLabel.grid(row=0, column=0, padx=2, pady=2)
    idEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=email)
    idEntry.grid(row=0, column=1, padx=5, pady=2)

    passLabel = tk.Label(detailsFrame, text="New Password", font=("Times new roman", 16))
    passLabel.grid(row=1, column=0, padx=2, pady=2)
    passEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=password)
    passEntry.grid(row=1, column=1, padx=5, pady=5)

    submitButton = tk.Button(detailsFrame, text="Submit", bd=3, font=("Times new roman", 15), width=15,
                             command=lambda : resetPasswordSql(email.get(), password.get(), window))
    submitButton.grid(row=2, column=0, padx=2, pady=10)

    backButton = tk.Button(detailsFrame, text="Back", bd=3, font=("Times new roman", 15), width=15,
                           command=window.destroy)
    backButton.grid(row=2, column=1, padx=2, pady=10)


def choicePage():
    window = tk.Toplevel(mainWindow)

    mainHeading = tk.Label(window, text="Assignment Manager", font=("Times new roman", 26, "bold"), background="cyan")
    mainHeading.pack(side=tk.TOP, fill=tk.X, pady=10)

    detailsFrame = tk.LabelFrame(window, text="Select Action", font=("Times new roman", 20, "bold"),
                                 background="lightblue")
    detailsFrame.pack(side=tk.TOP, fill=tk.X)
    dataFrame = tk.Frame(window)
    dataFrame.pack(side=tk.TOP, fill=tk.X)

    viewActiveButton = tk.Button(detailsFrame, text="View Active Assignments", bd=3, font=("Times new roman", 15),
                                 width=25, command=activeAssignments)
    viewActiveButton.grid(row=1, column=0, padx=10, pady=10, ipady=10)

    viewSubmissionsButton = tk.Button(detailsFrame, text="View My Submissions", bd=3, font=("Times new roman", 15),
                                      width=25, command=viewSubmissions)
    viewSubmissionsButton.grid(row=2, column=0, padx=10, pady=10, ipady=10)

    updateProfileButton = tk.Button(detailsFrame, text="Update Profile", bd=3, font=("Times new roman", 15), width=25,
                                    command=updateProfile)
    updateProfileButton.grid(row=3, column=0, padx=10, pady=10, ipady=10)

    logoutButton = tk.Button(detailsFrame, text="Log Out", bd=3, font=("Times new roman", 15), width=25,
                             command=window.destroy)
    logoutButton.grid(row=4, column=0, padx=10, pady=10, ipady=10)


def updateProfile():
    window = tk.Toplevel(mainWindow)

    mainHeading = tk.Label(window, text="Assignment Manager", font=("Times new roman", 26, "bold"), background="cyan")
    mainHeading.pack(side=tk.TOP, fill=tk.X, pady=20)

    detailsFrame = tk.LabelFrame(window, text="Update Profile", font=("Times new roman", 20, "bold"),
                                 background="lightblue")
    detailsFrame.pack(side=tk.TOP, fill=tk.X)
    dataFrame = tk.Frame(window)
    dataFrame.pack(side=tk.TOP, fill=tk.X)

    email = tk.StringVar()
    phone = tk.StringVar()

    emailLabel = tk.Label(detailsFrame, text="Update Email", font=("Times new roman", 16))
    emailLabel.grid(row=1, column=0, padx=2, pady=2)
    emailEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=email)
    emailEntry.grid(row=1, column=1, padx=5, pady=2)

    phoneLabel = tk.Label(detailsFrame, text="Update Phone", font=("Times new roman", 16))
    phoneLabel.grid(row=2, column=0, padx=2, pady=2)
    phoneEntry = tk.Entry(detailsFrame, bd=2, font=("Times new roman", 14), width=20, textvariable=phone)
    phoneEntry.grid(row=2, column=1, padx=5, pady=10)

    submitButton = tk.Button(detailsFrame, text="Submit", bd=3, font=("Times new roman", 15), width=15,
                             command=lambda : updateProfileSql(email.get(), phone.get(), window))
    submitButton.grid(row=3, column=0, padx=2, pady=10)

    backButton = tk.Button(detailsFrame, text="Back", bd=3, font=("Times new roman", 15), width=15,
                           command=window.destroy)
    backButton.grid(row=3, column=1, padx=2, pady=10)


def activeAssignments():
    window = tk.Toplevel(mainWindow)

    mainHeading = tk.Label(window, text="Assignment Manager", font=("Times new roman", 26, "bold"), background="cyan")
    mainHeading.pack(side=tk.TOP, fill=tk.X, pady=10)

    detailsFrame = tk.LabelFrame(window, text="Active Assignments", font=("Times new roman", 20, "bold"),
                                 background="lightblue")
    detailsFrame.pack(side=tk.TOP, fill=tk.X)
    dataFrame = tk.Frame(window)
    dataFrame.pack(side=tk.TOP, fill=tk.X)

    nameLabel = tk.Label(detailsFrame, text="Assignment Name", font=("Times new roman", 16, "bold"), width=15)
    nameLabel.grid(row=0, column=0, padx=2, pady=2)

    courseCodeLabel = tk.Label(detailsFrame, text="Course Code", font=("Times new roman", 16, "bold"), width=15)
    courseCodeLabel.grid(row=0, column=1, padx=2, pady=2)

    deadlineLabel = tk.Label(detailsFrame, text="Submission Deadline", font=("Times new roman", 16, "bold"), width=15)
    deadlineLabel.grid(row=0, column=2, padx=2, pady=2)

    submitLabel = tk.Label(detailsFrame, text="Submit", font=("Times new roman", 16, "bold"), width=15)
    submitLabel.grid(row=0, column=3, padx=2, pady=2)

    assignmentList = activeAssignmentsSql()

    for i in range(len(assignmentList)):
        assignmentRow(assignmentList[i][0], assignmentList[i][1], assignmentList[i][2], assignmentList[i][3], i + 1,
                      detailsFrame)

    backButton = tk.Button(detailsFrame, text="Back", bd=3, font=("Times new roman", 15), width=15,
                           command=window.destroy)
    backButton.grid(row=len(assignmentList) + 1, column=0, padx=2, pady=10, columnspan=4)


def assignmentRow(id, name, code, deadline, rowNum, detailsFrame):
    nameLabel = tk.Label(detailsFrame, text=name, font=("Times new roman", 14), width=15)
    nameLabel.grid(row=rowNum, column=0, padx=2, pady=2)

    courseCodeLabel = tk.Label(detailsFrame, text=code, font=("Times new roman", 14), width=15)
    courseCodeLabel.grid(row=rowNum, column=1, padx=2, pady=2)

    deadlineLabel = tk.Label(detailsFrame, text=deadline, font=("Times new roman", 14), width=15)
    deadlineLabel.grid(row=rowNum, column=2, padx=2, pady=2)

    submitButton = tk.Button(detailsFrame, text="Submit", bd=3, font=("Times new roman", 14), width=15,
                             command=lambda: submitAssignment(id, name, code, deadline))
    submitButton.grid(row=rowNum, column=3, padx=2, pady=2)


def submitAssignment(id, name, code, deadline):
    window = tk.Toplevel(mainWindow)

    mainHeading = tk.Label(window, text="Assignment Manager", font=("Times new roman", 26, "bold"), background="cyan")
    mainHeading.pack(side=tk.TOP, fill=tk.X, pady=20)

    detailsFrame = tk.LabelFrame(window, text="Submit Assignment", font=("Times new roman", 20, "bold"),
                                 background="lightblue")
    detailsFrame.pack(side=tk.TOP, fill=tk.X)
    dataFrame = tk.Frame(window)
    dataFrame.pack(side=tk.TOP, fill=tk.X)

    nameLabel = tk.Label(detailsFrame, text="Assignment Name", font=("Times new roman", 16, "bold"), width=20)
    nameLabel.grid(row=0, column=0, padx=2, pady=2)

    nameLabel2 = tk.Label(detailsFrame, text=name, font=("Times new roman", 16), width=20)
    nameLabel2.grid(row=0, column=1, padx=2, pady=2)

    codeLabel = tk.Label(detailsFrame, text="Course Code", font=("Times new roman", 16, "bold"), width=20)
    codeLabel.grid(row=1, column=0, padx=2, pady=2)

    codeLabel2 = tk.Label(detailsFrame, text=code, font=("Times new roman", 16), width=20)
    codeLabel2.grid(row=1, column=1, padx=2, pady=2)

    deadlineLabel = tk.Label(detailsFrame, text="Deadline", font=("Times new roman", 16, "bold"), width=20)
    deadlineLabel.grid(row=2, column=0, padx=2, pady=2)

    deadlineLabel2 = tk.Label(detailsFrame, text=deadline, font=("Times new roman", 16), width=20)
    deadlineLabel2.grid(row=2, column=1, padx=2, pady=2)

    contentLabel = tk.Label(detailsFrame, text="Assignment Content", font=("Times new roman", 16, "bold"), width=20)
    contentLabel.grid(row=3, column=0, padx=2, pady=2)

    content = tk.Text(detailsFrame, font=("Times new roman", 12), height=5)
    content.grid(row=4, columnspan=2, padx=2, pady=2)

    submitButton = tk.Button(detailsFrame, text="Submit", bd=3, font=("Times new roman", 15), width=15,
                             command=lambda: submitAssignmentSql(id, content.get("1.0", "end-1c"), window))
    submitButton.grid(row=5, column=0, padx=2, pady=10, columnspan=2)


def viewSubmissions():
    window = tk.Toplevel(mainWindow)

    mainHeading = tk.Label(window, text="Assignment Manager", font=("Times new roman", 26, "bold"), background="cyan")
    mainHeading.pack(side=tk.TOP, fill=tk.X, pady=10)

    detailsFrame = tk.LabelFrame(window, text="My Submissions", font=("Times new roman", 20, "bold"),
                                 background="lightblue")
    detailsFrame.pack(side=tk.TOP, fill=tk.X)
    dataFrame = tk.Frame(window)
    dataFrame.pack(side=tk.TOP, fill=tk.X)

    courseCodeLabel = tk.Label(detailsFrame, text="Assignment ID", font=("Times new roman", 16, "bold"), width=15)
    courseCodeLabel.grid(row=0, column=0, padx=2, pady=2)

    deadlineLabel = tk.Label(detailsFrame, text="Time Submitted", font=("Times new roman", 16, "bold"), width=15)
    deadlineLabel.grid(row=0, column=1, padx=2, pady=2)

    gradeLabel = tk.Label(detailsFrame, text="Grade", font=("Times new roman", 16, "bold"), width=15)
    gradeLabel.grid(row=0, column=2, padx=2, pady=2)

    feedbackLabel = tk.Label(detailsFrame, text="Feedback", font=("Times new roman", 16, "bold"), width=15)
    feedbackLabel.grid(row=0, column=3, padx=2, pady=2, columnspan=2)

    submissionList = viewSubmissionsSql()

    for i in range(len(submissionList)):
        submissionRow(submissionList[i][0], submissionList[i][1], submissionList[i][2], submissionList[i][3], i + 1,
                      detailsFrame)

    backButton = tk.Button(detailsFrame, text="Back", bd=3, font=("Times new roman", 15), width=15,
                           command=window.destroy)
    backButton.grid(row=len(submissionList) + 1, column=0, padx=2, pady=10, columnspan=5)


def submissionRow(code, deadline, grade, feedback, rowNum, detailsFrame):
    assignmentIdLabel = tk.Label(detailsFrame, text=code, font=("Times new roman", 14), width=15)
    assignmentIdLabel.grid(row=rowNum, column=0, padx=2, pady=2)

    deadlineLabel = tk.Label(detailsFrame, text=deadline, font=("Times new roman", 14), width=15)
    deadlineLabel.grid(row=rowNum, column=1, padx=2, pady=2)

    gradeLabel = tk.Label(detailsFrame, text=grade, font=("Times new roman", 14), width=15)
    gradeLabel.grid(row=rowNum, column=2, padx=2, pady=2)

    feedbackLabel = tk.Label(detailsFrame, text=feedback, font=("Times new roman", 14))
    feedbackLabel.grid(row=rowNum, column=3, padx=2, pady=2, columnspan=2)


#studentLogin()
chooseLogin()

#mainWindow.mainloop()
root.mainloop()

    