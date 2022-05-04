from xml.dom import ValidationErr
from django.shortcuts import render, redirect
import mysql.connector
from .forms import employee_register_form, patient_register_form
from Receptionist import views


# Create your views here.

def landing_page(request):
    if request.method == "GET":
        return render(request, "landing_page.html")
    
    elif request.method == "POST":
        #register the account
        if "Register" in request.POST:
            return redirect(f"/register")
        
        elif "Login" in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]

            if username != "" and password != "":
                db = mysql.connector.connect(
                    host ='us-cdbr-east-05.cleardb.net',
                    user ='be6fd11e32efb5',
                    passwd='2e25d6f3',
                    database = 'heroku_7f02c0751957843')

                mycursor = db.cursor(buffered=True)
                
                mycursor.execute("SELECT * FROM user_table WHERE user_table.uname='" + username + "' AND user_table.pword='" + password + "';")

                for x in mycursor:
                    ssn = x[0]
                    acc_type = x[3]

                    if acc_type == "receptionist":
                        mycursor.close()
                        db.close()
                        return redirect(f"receptionist/{ssn}")

                    if acc_type == "Patient":
                        mycursor.close()
                        db.close()
                        return redirect(f"patient/{ssn}")

                    if acc_type == "dentist":
                        mycursor.close()
                        db.close()
                        return redirect(f"dentist/{ssn}")
                mycursor.close()
                db.close()
                return render(request, "landing_page.html")
            else:
                return render(request, "landing_page.html")
                    

def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    
    elif request.method == "POST":
        if "Proceed" in request.POST:
            
            if request.POST["account-type"] == "Patient":
                return redirect(f"/register/patient")
            
            elif request.POST["account-type"] == "Employee":
                return redirect(f"/register/employee")


def employee_register(request):
    if request.method == "GET":
        form = employee_register_form()
        return render(request, "employee_register.html", {"form" : form})

    if request.method == "POST":
        #check to make sure complete registration is pressed
        #validate all integers
        #will need to validate uniqueness for SSN
        
        if "Complete" in request.POST:
            form = employee_register_form(request.POST)
            if form.is_valid():

                db = mysql.connector.connect(
                    host ='us-cdbr-east-05.cleardb.net',
                    user ='be6fd11e32efb5',
                    passwd='2e25d6f3',
                    database = 'heroku_7f02c0751957843')

                mycursor = db.cursor(buffered=True)

                firstname = form.cleaned_data["firstname"]
                lastname = form.cleaned_data["lastname"]
                housenum = form.cleaned_data["housenum"]
                streetname = form.cleaned_data["streetname"]
                city = form.cleaned_data["city"]
                province = form.cleaned_data["province"]
                ssn = form.cleaned_data["ssn"]
                salary = form.cleaned_data["salary"]
                role = form.cleaned_data["role"]
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]


                check = "SELECT count(*) FROM user_table WHERE SSN = " + str(ssn) + ";"
                mycursor.execute(check)
                isValid = mycursor.fetchone()[0]
                mycursor.close()

                mycursor = db.cursor(buffered=True)
                check2 = "SELECT count(*) FROM user_table WHERE uname = '" + username + "';"
                mycursor.execute(check2)
                isValid2 = mycursor.fetchone()[0]

                if isValid > 0 or isValid2 > 0:
                    return render(request,"employee_register.html",{'form' : form, 'error' : "One or more fields are incorrect!"})

                mycursor.close()
                mycursor = db.cursor(buffered=True)

                #add into employee
                mycursor.execute("INSERT INTO employee VALUES ('" + firstname + "', '" + lastname + "', '" + str(housenum) + "', '" +
                                    streetname + "', '" + city + "', '" + province + "', '" + role + "', '" + str(salary) + "', '" + str(ssn) + "');")
                db.commit()
                mycursor.execute("INSERT INTO patient VALUES (%s, %s, %s, %s, %s, %s, NULL,NULL,NULL, %s)",
                (firstname, lastname, housenum, streetname, city, province, ssn))
                db.commit()

                mycursor.close()
                mycursor = db.cursor(buffered=True)

                
                mycursor.execute("INSERT INTO payement VALUES (%s,%s)",(ssn,0))
                db.commit()

                #add into user
                mycursor.execute("INSERT INTO user_table VALUES(%s, %s, %s, %s)", (ssn, username, password, role))
                db.commit()

                if role == "receptionist":
                    mycursor.close()
                    db.close()
                    return redirect(f"/receptionist/{ssn}")

                if role == "dentist":
                    mycursor.close()
                    db.close()
                    return redirect(f"/dentist/{ssn}")

            else:
                return render(request, "employee_register.html", {"form" : form})
                
                
def patient_register(request):
    if request.method == "GET":
        form = patient_register_form()
        return render(request, "patient_register.html", {"form": form})
    
    elif request.method == "POST":
        if "Complete" in request.POST:
            form = patient_register_form(request.POST)
            db = mysql.connector.connect(
                    host ='us-cdbr-east-05.cleardb.net',
                    user ='be6fd11e32efb5',
                    passwd='2e25d6f3',
                    database = 'heroku_7f02c0751957843')
            mycursor = db.cursor(buffered=True)

            if form.is_valid():
                db = mysql.connector.connect(
                    host ='us-cdbr-east-05.cleardb.net',
                    user ='be6fd11e32efb5',
                    passwd='2e25d6f3',
                    database = 'heroku_7f02c0751957843')
                mycursor = db.cursor(buffered=True)  

                firstname = form.cleaned_data["firstname"]
                lastname = form.cleaned_data["lastname"]
                housenum = form.cleaned_data["housenum"]
                streetname = form.cleaned_data["streetname"]
                city = form.cleaned_data["city"]
                province = form.cleaned_data["province"]
                gender = form.cleaned_data["gender"]
                email = form.cleaned_data["email"]
                Dob = form.cleaned_data["DOB"]
                ssn = form.cleaned_data["ssn"]
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]

                #validate date of birth
                DOBarr = Dob.split("-")
                error = False

                if len(DOBarr) == 3:
                    year = DOBarr[0]
                    month = DOBarr[1]
                    day = DOBarr[2]

                    if len(year) != 4:
                        error = True
                    
                    elif len(month) != 2:
                        error = True

                    elif len(day) != 2:
                        error = True
                    
                    try:
                        year = int(year)
                        month = int(month)
                        day  = int(day)
                    except ValueError:
                        error = True

                else:
                    error = True

                check = "SELECT count(*) FROM user_table WHERE SSN = " + str(ssn) + ";"
                mycursor.execute(check)
                isValid = mycursor.fetchone()[0]
                mycursor.close()
                db.close()

                db.reconnect()
                mycursor = db.cursor(buffered=True)
                check2 = "SELECT count(*) FROM user_table WHERE uname = '" + username + "';"
                mycursor.execute(check2)
                isValid2 = mycursor.fetchone()[0]
                mycursor.close()
                db.close()

                if isValid > 0 or isValid2 > 0 or error:
                    return render(request, "patient_register.html", {"form": form, "error" : "One or more fields are incorrect!"})

                db.reconnect()
                mycursor = db.cursor(buffered=True)
                mycursor.execute("INSERT INTO patient VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (firstname, lastname, housenum, streetname, city, province, gender, email, Dob, ssn))
                db.commit()
                mycursor.close()
                db.close()

                db.reconnect()
                mycursor = db.cursor(buffered=True)
                mycursor.execute("INSERT INTO user_table VALUES (%s, %s, %s, %s)", (ssn, username, password, "Patient"))
                db.commit()
                mycursor.close()
                db.close()
                
                db.reconnect()
                mycursor = db.cursor(buffered=True)
                mycursor.execute("INSERT INTO payement VALUES (%s,%s)",(ssn,0))
                db.commit()
                mycursor.close()
                db.close()
                return redirect(f"/patient/{ssn}")

