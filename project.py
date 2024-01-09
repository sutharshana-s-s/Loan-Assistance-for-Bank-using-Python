import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import font as tkfont
import math
from tkinter import filedialog
import mysql.connector
from functools import partial

docu=[]
global image5
def insert(n,m,p,g,u,pa,base):
    base.destroy()
    vals=(n,m,p,g,u,pa)
    
    conn = mysql.connector.connect(user='root', password='sudeep2004', host='localhost', database='loanapp')
    cursor=conn.cursor()
    query="INSERT INTO DETAILS(NAME,EMAIL,CONTACT_NUMBER,GENDER,USERNAME,PASSWORD)VALUES(%s,%s,%s,%s,%s,%s)"

    cursor.execute(query,vals)
    conn.commit()
    messagebox.showinfo("Registered","You have been registered!!")
    conn.close()
    
def reg():
    base = tk.Tk()
    base.geometry("450x250")
    base.title("Registration form")
    
    name=StringVar()
    mail=StringVar()
    phno=IntVar()
    vars = IntVar()
    user=StringVar()
    passw=StringVar()
            
    lb1= Label(base, text="Enter Name:",width=10, font=("arial",12))
    lb1.grid(row=2, column=1)
    en1= Entry(base,textvariable=name)
    en1.grid(row=2, column=2)
    
    lb3= Label(base, text="Enter Email:", width=10, font=("arial",12))
    lb3.grid(row=3, column=1)
    en3= Entry(base,textvariable=mail)
    en3.grid(row=3, column=2)
    
    lb4= Label(base, text="Contact Number:", width=13,font=("arial",12))
    lb4.grid(row=4, column=1)
    en4= Entry(base,textvariable=phno)
    en4.grid(row=4, column=2)
    
    lb5= Label(base, text="Select Gender:", width=15, font=("arial",12))
    lb5.grid(row=5, column=1)
    Radiobutton(base, text="Male", padx=5,variable=vars, value="Male").grid(row=5, column=2)
    Radiobutton(base, text="Female", padx =10,variable=vars, value="Female").grid(row=5, column=3)
    Radiobutton(base, text="others", padx=15, variable=vars, value="Others").grid(row=5, column=4)
    
    lb2= Label(base, text="Enter username:", width=13,font=("arial",12))
    lb2.grid(row=6, column=1)
    en5=Entry(base,textvariable=user)
    en5.grid(row=6, column=2)
    
    lb6= Label(base, text="Enter Password:", width=13,font=("arial",12))
    lb6.grid(row=7, column=1)
    en6= Entry(base,textvariable=passw)
    en6.grid(row=7, column=2)
    
    lb7= Label(base, text="Re-Enter Password:", width=15,font=("arial",12))
    lb7.grid(row=8, column=1)
    en7 =Entry(base, show='*')
    en7.grid(row=8, column=2)
    
    regis=tk.Button(base, text="Register",width=10, command=lambda: insert(en1.get(), en3.get(), en4.get(), vars.get(), en5.get(), en6.get(),base)).grid(row=9, column=1,columnspan=2)
    base.mainloop()

def login():
    base1 = tk.Tk()
    base1.title("Login page")
    base1.geometry("260x150")
    
    user=StringVar()
    passw=StringVar()
    
    lb2= Label(base1, text="Enter username:", width=13,font=("arial",12))
    lb2.grid(row=2, column=1)
    en5=Entry(base1,textvariable=user)
    en5.grid(row=2, column=2)
    
    lb6= Label(base1, text="Enter Password:", width=13,font=("arial",12))
    lb6.grid(row=3, column=1)
    en6= Entry(base1,textvariable=passw,show="*")
    en6.grid(row=3, column=2)
    
    log=tk.Button(base1, text="Login", width=10,command=lambda: verify(en5.get(),en6.get(),base1))
    log.grid(row=4, column=1,columnspan=2)
    reg_button = tk.Button(base1, text="Register", command=lambda: reg())
    reg_button.grid(row=5,column=1,columnspan=2,pady=5)
    base1.mainloop()
    
def verify(userid,passwor,base1):
    vals=[userid,passwor]
    conn = mysql.connector.connect(user='root', password='sudeep2004', host='localhost', database='loanapp')
    cursor=conn.cursor()
    query="select USERNAME,PASSWORD from DETAILS where USERNAME = %s AND PASSWORD = %s"
    cursor.execute(query, vals)
    res=cursor.fetchall()

    if res:
        home(vals[0])
    else:
        messagebox.showwarning("Invalid Username or Password","Re-Enter Login credentials!!")
    conn.close()
    
def open_file_dialog(document_entry):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
    document_entry["state"]=tk.NORMAL
    file_name = file_path.split('/')[-1]
    docu.append(file_path)
    document_entry.delete(0, tk.END)
    document_entry.insert(tk.END, file_name)
    document_entry["state"]=tk.DISABLED
        
def submit(name,age,income,pan,loan,windows):
    # Get the values entered by the user
    
    conn = mysql.connector.connect(user='root', password='sudeep2004', host='localhost', database='sks')
    cursor=conn.cursor()
    query="Select Score from cibil where pan_number=%s"
    cursor.execute(query,[pan])
    res=cursor.fetchone()
    conn.commit() 
    
    if res[0]:
        vals=[name,age,income,pan,loan,docu[0],docu[1],docu[2]]
        # Check if all fields are filled
        if not name or not age or not income:
            messagebox.showwarning("Incomplete Application", "Please fill in all fields.")
            return

        db= mysql.connector.connect(host='localhost', user='root', passwd='sudeep2004', db='loanapp')
        cursor=db.cursor()
        cursor.execute('INSERT INTO applications (name,age,income,Pan_number,loan_type,id_proof,document_2,document_3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',vals)
        db.commit()
        db.close()
        # Show a success message
        messagebox.showinfo("Application Submitted", f"Your {loan} application has been submitted successfully!\nWe wil reach you out soon!!")
    else:
        messagebox.showwarning("Invalid Pan","The pan you have entered is not found!!")
    windows.destroy()
    
def apply(loan):   
    global pic1
    window=tk.Tk()
    window.title(f"{loan} Application")
    window.geometry("400x420")
    window.resizable(False,False)
    window.attributes("-topmost")
    name=StringVar()
    age=IntVar()
    income=IntVar()
    
    title_label=Label(window,text=f"SKS Bank {loan} Application",font=("bold",15))
    title_label.grid(row=1,column=1,columnspan=3)
    
    name_label = tk.Label(window, text="Name:")
    name_label.grid(row=3,column=1)
    age_label = tk.Label(window, text="Age:").grid(row=4,column=1)
    income_label = tk.Label(window, text="Income:").grid(row=5,column=1)

    name_entry = tk.Entry(window, textvariable=name)
    name_entry.grid(row=3, column=2)

    age_entry = tk.Entry(window, textvariable=age)
    age_entry.grid(row=4, column=2)

    income_entry = tk.Entry(window, textvariable=income)
    income_entry.grid(row=5, column=2)

    panLabel=tk.Label(window, text="PAN number:")
    panLabel.grid(row=6, column=1)
    panTextField=tk.Entry(window)
    panTextField.grid(row=6, column=2)
    
    document1_label = tk.Label(window, text="ID Proof:").grid(row=7,column=1)
    document1_entry = tk.Entry(window)
    document1_entry.grid(row=7,column=2)
    document1_entry.insert(tk.END,f"Upload Image")
    document1_entry["state"]=tk.DISABLED    
    document1_button = tk.Button(window, text="Browse", command=lambda: open_file_dialog(document1_entry)).grid(row=7,column=3)

    document2_label = tk.Label(window, text="Document 2:").grid(row=8,column=1)
    document2_entry = tk.Entry(window)
    document2_entry.grid(row=8,column=2)
    document2_entry.insert(tk.END,f"Upload Image")
    document2_entry["state"]=tk.DISABLED
    document2_button = tk.Button(window, text="Browse", command=lambda: open_file_dialog(document2_entry)).grid(row=8,column=3)

    document3_label = tk.Label(window, text="Document 3:").grid(row=9,column=1)
    document3_entry = tk.Entry(window)
    document3_entry.grid(row=9,column=2)
    document3_entry.insert(tk.END,f'Upload Image')
    document3_entry["state"]=tk.DISABLED
    document3_button = tk.Button(window, text="Browse", command=lambda: open_file_dialog(document3_entry)).grid(row=9,column=3)
    
    submit_button=tk.Button(window,text="Submit",command=lambda: submit(name_entry.get(),age_entry.get(),income_entry.get(),panTextField.get(),loan,window)).grid(row=10,column=2)
    window.mainloop()

def calculate_savings(irate,str):
    irate*=100
    def computeButtonAction():
        try:
            balance = float(balanceTextField.get())
            interest = float(irate)
            months = int(monthsTextField.get())
            anninc=float(annualincTextField.get())
            pan=panTextField.get()

            conn = mysql.connector.connect(user='root', password='sudeep2004', host='localhost', database='sks')
            cursor=conn.cursor()
            query="Select Score from cibil where pan_number=%s"
            cursor.execute(query,[pan])
            res=cursor.fetchone()
            conn.commit()            
            
            monthly_interest = interest / 1200
            if(interest==0):
                payment=balance/months
            else:
                multiplier=math.pow(1+monthly_interest,months)
                payment = (balance * monthly_interest*multiplier) / (multiplier-1)
            
            moninc=anninc/12
            
            
            loanBalance = balance
            for paymentNumber in range(1,months):
                loanBalance += loanBalance * monthly_interest - payment
            
            finalPayment = loanBalance
            if (finalPayment > payment):
                loanBalance += loanBalance * monthly_interest - payment
                finalPayment = loanBalance
                months+=1
            newLoanButton["state"] = tk.NORMAL
            
            diratio=(payment/moninc*100)
            
            outputTextArea["state"]=tk.NORMAL
            outputTextArea.insert(tk.END,f"Loan amount: Rs.{balance:.2f} \n")
            outputTextArea.insert(tk.END,f"Interest: {interest:.2f} %\n\n")
            outputTextArea.insert(tk.END,f"{months-1} Payments of Rs. {payment:.2f}\n")
            outputTextArea.insert(tk.END,f"Final payment of Rs. {finalPayment:.2f}\n")
            outputTextArea.insert(tk.END,f"Total Payment: Rs. {((months-1)*payment+ finalPayment):.2f}\n")
            outputTextArea.insert(tk.END,f"Interest paid: Rs. {((months - 1) * payment + finalPayment - balance):.2f}\n")
            outputTextArea.insert(tk.END,f"Monthly income: Rs.{moninc:.2f}\n")
            outputTextArea.insert(tk.END,f"Debt-Income ratio : {diratio:.2f} %\n")
            if(diratio>40):
                outputTextArea.insert(tk.END,f"You will be able to pay the monthly payment!!\n")
                if res:
                    if((str=="Personal" and res[0]>550) or (str=="Home" and res[0]>700) or (str=="Vehicle" and res[0]>600) or (str=="Education" and res[0]>650)):
                        outputTextArea.insert(tk.END,f"Your Cibil Score is {res[0]}.\nSo, You are Eligible for the loan.\n")           
                    else:
                        outputTextArea.insert(tk.END,f"You are not Eligible for the loan.\n")
                else:
                    outputTextArea.insert(tk.END,f"You are Pan number is not found.\n")
            else:
                outputTextArea.insert(tk.END,f"You will not be able to pay the monthly payment!!\n")
            outputTextArea["state"]=tk.DISABLED

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def newLoanButtonAction():
        balanceTextField.delete(0, tk.END)
        monthsTextField.delete(0, tk.END)
        annualincTextField.delete(0,tk.END)
        outputTextArea["state"]=tk.NORMAL
        outputTextArea.delete(1.0,tk.END)
        outputTextArea["state"]=tk.DISABLED
        newLoanButton["state"] = tk.DISABLED

    def quit():
        root.destroy()
        
    root = tk.Tk()
    root.title("Loan Assistant")
    root.geometry("800x500")
    root.resizable(False, False)
    
    # Fonts
    myFont = tkfont.Font(family="Arial", size=16)

    # Labels
    title_label=Label(root,text=f"SKS Bank {str} Loan Application",font=("bold",15))
    title_label.grid(row=0,column=0,columnspan=3)
    
    Enterlabel=tk.Label(root, text="Enter Details:", font=myFont)
    Enterlabel.grid(row=1, column=0, sticky="w", padx=10, pady=10)

    balanceLabel = tk.Label(root, text="Loan Balance:", font=myFont)
    balanceLabel.grid(row=2, column=0, sticky="w", padx=10, pady=10)

    interestLabel = tk.Label(root, text="Interest Rate:", font=myFont)
    interestLabel.grid(row=3, column=0, sticky="w", padx=10, pady=10)

    monthsLabel = tk.Label(root, text="Number of Payments:", font=myFont)
    monthsLabel.grid(row=4, column=0, sticky="w", padx=10, pady=10)

    analysisLabel = tk.Label(root, text=str+" Loan Analysis:", font=myFont)
    analysisLabel.grid(row=0, column=3, sticky="w", padx=10, pady=5)

    annualincLabel=tk.Label(root, text="Annual Income:", font=myFont)
    annualincLabel.grid(row=5, column=0, sticky="w", padx=10, pady=10)

    panLabel=tk.Label(root, text="PAN number:", font=myFont)
    panLabel.grid(row=6, column=0, sticky="w", padx=10, pady=10)

    # Text Fields
    balanceTextField = tk.Entry(root, width=10, font=myFont)
    balanceTextField.grid(row=2, column=1, padx=10, pady=10)

    interestTextField = tk.Entry(root, width=10, font=myFont)
    interestTextField.insert(0,f"{irate:.2f}")
    interestTextField["state"]=tk.DISABLED
    interestTextField.grid(row=3, column=1, padx=10, pady=10)

    monthsTextField = tk.Entry(root, width=10, font=myFont)
    monthsTextField.grid(row=4, column=1, padx=10, pady=10)

    annualincTextField=tk.Entry(root, width=10, font=myFont)
    annualincTextField.grid(row=5, column=1, padx=10, pady=10)
    
    panTextField=tk.Entry(root, width=10, font=myFont)
    panTextField.grid(row=6, column=1, padx=10, pady=10)

    #Buttons

    computeButton = tk.Button(root, text="Compute Monthly Payment", command=computeButtonAction)
    computeButton.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    newLoanButton = tk.Button(root, text="New Loan Analysis", state=tk.DISABLED, command=newLoanButtonAction)
    newLoanButton.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
    
    exitButton= tk.Button(root, text="Exit",command=quit)
    exitButton.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    # Text Area
    outputTextArea = scrolledtext.ScrolledText(root, width=35, height=13, font=myFont)
    outputTextArea.grid(row=1, column=3, rowspan=6, padx=10, pady=10)

    # Main loop
    root.mainloop()
    
def home(name):
    global image1,image2,image3,image4,image5
    window=Toplevel()
    window.geometry("600x600")
    window.title("Loan Assistance")

    header_label = tk.Label(window, text="Select a Loan Type:")
    
    l1=Label(window, text=f"Hi {name}, Welcome to SKS bank!!",font=("bold", 15))
    l1.grid(rows=1,column=1,columnspan=4,rowspan=2)
    

    personal_loan_interest=0.1049
    personal_savings_button = tk.Button(window, text="Calculate Savings", command=lambda: calculate_savings(personal_loan_interest,"Personal")).grid(row=3,column=1,padx=5,pady=5)
    personal_apply_button = tk.Button(window, text="Apply Now", command=partial(apply,"Personal loan")).grid(row=3,column=2,padx=10,pady=5)

    home_loan_interest=0.069
    home_savings_button = tk.Button(window, text="Calculate Savings", command=lambda: calculate_savings(home_loan_interest,"Home"))
    home_savings_button.grid(row=3,column=3,padx=5,pady=5)
    home_apply_button = tk.Button(window, text="Apply Now", command=partial(apply,"Home Loan"))
    home_apply_button.grid(row=3,column=4,padx=5,pady=5)

    car_loan_interest=0.07
    car_savings_button = tk.Button(window, text="Calculate Savings", command=lambda: calculate_savings(car_loan_interest,"Vehicle"))
    car_savings_button.grid(row=5,column=1,padx=5,pady=5)
    car_apply_button = tk.Button(window, text="Apply Now", command=partial(apply,"Vehicle loan"))
    car_apply_button.grid(row=5,column=2,padx=5,pady=5)

    education_loan_interest=0.08
    education_savings_button = tk.Button(window, text="Calculate Savings", command=lambda: calculate_savings(education_loan_interest,"Education"))
    education_savings_button.grid(row=5,column=3,padx=5,pady=5)
    education_apply_button = tk.Button(window, text="Apply Now", command=partial(apply,"Education Loan"))
    education_apply_button.grid(row=5,column=4,padx=5,pady=5)

    photo1 = Image.open("D:\sem 4\Corporate finance\project\plloan.jpg")
    resized_image1 = photo1.resize((150, 150))
    image1 = ImageTk.PhotoImage(resized_image1)
    image_label1 = tk.Label(window, image=image1)
    image_label1.grid(row=2,columnspan=2,column=1)

    photo2 = Image.open("D:\sem 4\Corporate finance\project\hl.jpg")
    resized_image2 = photo2.resize((150, 150),Image.LANCZOS)
    image2 = ImageTk.PhotoImage(resized_image2)
    image_label2 = tk.Label(window, image=image2)
    image_label2.grid(row=2,columnspan=2,column=3)

    photo3 = Image.open("D://sem 4//Corporate finance//project//vl.jpg")
    resized_image3 = photo3.resize((150, 150))
    image3 = ImageTk.PhotoImage(resized_image3)
    image_label3 = tk.Label(window, image=image3)
    image_label3.grid(row=4,columnspan=2,column=1)

    photo4 = Image.open("D:\sem 4\Corporate finance\project\edl.jpg")
    resized_image4 = photo4.resize((150, 150))
    image4 = ImageTk.PhotoImage(resized_image4)
    image_label4 = tk.Label(window, image=image4)
    image_label4.grid(row=4,columnspan=2,column=3)
    
    photo5 = Image.open("D://sem 4//Corporate finance//project//bank.jpg")
    resized_image5 = photo5.resize((100, 100))
    image5 = ImageTk.PhotoImage(resized_image5)
    image_label5 = tk.Label(window, image=image5)
    image_label5.grid(row=1,column=0)

    # Start the application
    window.mainloop()
login()