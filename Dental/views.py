import string
from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import mysql.connector
import datetime
from .form import AppointmentForm,ReviewForm, CancelForm
from datetime import *


def patient(response, ssn):
    if response.method == "GET":
        db = mysql.connector.connect(
            host ='us-cdbr-east-05.cleardb.net',
            user ='be6fd11e32efb5',
            passwd='2e25d6f3',
            database = 'heroku_7f02c0751957843')
        mycursor1 = db.cursor(buffered = True)
        mycursor1.execute("SELECT COUNT(*) FROM employee WHERE SSN = "+ str(ssn))
        if(mycursor1.fetchone()[0] ==1):
            mycursor1.close()
            db.close()
            return render(response, "patientHomePage.html", {'error' : 'jdskkldas'})
        mycursor1.close()
        db.close()
        return render(response, "patientHomePage.html")
    
    elif response.method == "POST":
        #register the account
    
        if "Add Appointment" in response.POST:
            return redirect(f"/patient/appointment/{ssn}")
        elif "Cancel/View Upcoming Appointment" in response.POST:
            return redirect(f"/patient/appointment/view/{ssn}")
        elif "View Records" in response.POST:
            return redirect(f"/patient/records/{ssn}")
        elif "Leave a Review" in response.POST:
            return redirect(f"/patient/reviews/{ssn}")
        elif "View Invoices" in response.POST:
            return redirect(f"/patient/invoices/{ssn}")
        elif "Employee Page" in response.POST:
            return redirect(f"/dentist/{ssn}")
        
  
def invoices(response,ssn):

    if response.method == "GET":
        db = mysql.connector.connect(
            host ='us-cdbr-east-05.cleardb.net',
            user ='be6fd11e32efb5',
            passwd='2e25d6f3',
            database = 'heroku_7f02c0751957843')
        mycursor1 = db.cursor(buffered = True)
        mycursor1.execute("SELECT amount FROM payement WHERE ssn = " + str(ssn))
        money_owned  = mycursor1.fetchone()[0]
        mycursor1.close()
        db.close()
        return render(response, 'invoices.html', {'money':money_owned})

    elif response.method == "POST":
        if "Claim Insurance" in response.POST:
            db = mysql.connector.connect(
            host ='us-cdbr-east-05.cleardb.net',
            user ='be6fd11e32efb5',
            passwd='2e25d6f3',
            database = 'heroku_7f02c0751957843')
            mycursor1 = db.cursor(buffered = True)
            mycursor1.execute("SELECT amount From payement Where ssn = " + str(ssn))
            currentAmount = mycursor1.fetchone()[0] - 100
            if currentAmount < 0:
                mycursor1.execute("UPDATE payement SET amount = 0 WHERE ssn = " + str(ssn))
                db.commit()
                db.close()
                mycursor1.close()
                return render(response, 'invoices.html', {'money':0})
            else:
                mycursor1.execute("UPDATE payement SET amount = " + str(currentAmount) + " WHERE ssn = " + str(ssn))
                db.commit()
                db.close()
                mycursor1.close()
                return render(response, 'invoices.html', {'money':currentAmount})
        elif "Pay Now" in response.POST:
            return redirect(f"payement/{ssn}")


def payement(response, ssn):
    if response.method == "GET":
        db = mysql.connector.connect(
            host ='us-cdbr-east-05.cleardb.net',
            user ='be6fd11e32efb5',
            passwd='2e25d6f3',
            database = 'heroku_7f02c0751957843')
        mycursor1 = db.cursor(buffered = True)
        mycursor1.execute("SELECT amount From payement Where ssn = " + str(ssn))
        currentAmount = mycursor1.fetchone()[0]
        mycursor1.execute("UPDATE payement SET amount = 0 WHERE ssn = " + str(ssn))
        db.commit()
        mycursor1.close()
        db.close()
        return render(response, 'payement.html', {'money': currentAmount})
    elif response.method == 'POST':
        return redirect(f"/patient/{ssn}")

def appointment(response,ssn):
    if response.method == 'POST':
        db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')
        form = AppointmentForm(response.POST)
        if form.is_valid():
            #Retriving User Input From From
            dentist_FN = form.cleaned_data["dentist_FN"]
            dentist_LN = form.cleaned_data["dentist_LN"]
            appointment_type = form.cleaned_data["appointment_type"]
            appointment_date = form.cleaned_data["date"]
            startTime = form.cleaned_data["startTime"]
            endTime = form.cleaned_data["endTime"]
            dentistSSN = -1
            appointmentID = 0
            error = False
            
            mycursor1 = db.cursor(buffered = True)
            # Retriving Dentist SSN from database
            mycursor1.execute("Select SSN FROM employee WHERE first_name = '"+dentist_FN+"' AND last_name ='"+dentist_LN+"' AND SSN != "+ str(ssn))
            for x in mycursor1:
                dentistSSN = x[0]
                
            
            # Determining the appointment Id
            mycursor1.execute("Select max(appointment_ID) FROM appointment")
            for i in mycursor1:
                if i[0] != None:
                    appointmentID = i[0] + 1
            
            

            #Checking if date is valid
            dateArray = appointment_date.split("-")

            #Checking Time Format
            startTimeArray =  startTime.split(":")
            endTimeArray = endTime.split(":")

            if len(startTimeArray) != 2 or len(endTimeArray) != 2:
                error = True
            
            elif not startTimeArray[0].isdigit() or  not 0<=int(startTimeArray[0])<=23 or not startTimeArray[1].isdigit() or not 0<=int(startTimeArray[1])<=59:
                error = True
            
            elif not endTimeArray[0].isdigit() or not 0<=int(endTimeArray[0])<=23 or not endTimeArray[1].isdigit() or not 0<=int(endTimeArray[1])<=59:
                error = True

            elif datetime.strptime(startTime, '%H:%M') > datetime.strptime(endTime, '%H:%M'):
                error = True

            elif len(dateArray)!= 3:
                error = True

            elif len(dateArray[0]) != 4 or not str(dateArray[0]).isdigit():
                error = True

            elif len(dateArray[1]) !=2 or not str(dateArray[1]).isdigit() or not 1<=int(dateArray[1])<=12:
                error = True

            elif len(dateArray[2]) != 2 or not str(dateArray[2]).isdigit() or not 1<=int(dateArray[2])<=31:
                error = True

            elif (datetime.strptime(appointment_date +" " + startTime, '%Y-%m-%d %H:%M')<datetime.now()):
                error = True


            # Checking if dentist names are correct
            if dentistSSN == -1:
                error = True


            # Checking if there's exist conflicting appointment time
            if(not error):
                query = '''
                    select startTime, endTime
                    From book_appointment, appointment
                    where employee_SSN = '''+ str(dentistSSN) + " AND appointment.date = '" + appointment_date +"' AND book_appointment.appointment_ID = appointment.appointment_ID;"
                mycursor1.execute(query)
                for x in mycursor1:
                    if(inBetween(str(x[0]), str(x[1]), startTime)):
                        error = True 
                        
                    elif(inBetween(str(x[0]), str(x[1]), endTime)):
                        error= True
                        
                    elif(inBetween(startTime, endTime, str(x[0]))):
                        error = True
                        
                    elif (inBetween(startTime, endTime, str(x[1]))):
                        error = True
                    
                

            if error :
                # Retriving Dentist First  and Last Name from database
                mycursor1.execute("Select first_name, last_name FROM employee WHERE role = (\"dentist\" or role = \"hygentist\") AND SSN != " + str(ssn))
                
                #Creating list of dentists
                dentistList = []
                for x in mycursor1:
                    name = x[0] + " " + x[1]
                    dentistList.append(name)
                mycursor1.close()
                db.close()
                return render(response, "book_appointment.html", {'ls': dentistList,'form': form, 'error': "One or more Incorrect Field"})    
            
            # Inserting user infomation into db
            mycursor1.execute("INSERT INTO appointment VALUES("+str(appointmentID)+",'"+appointment_date +"', '"+startTime+"', '"+endTime+"' , '"+ appointment_type+"');")
            db.commit()
            mycursor1.execute("INSERT INTO book_appointment VALUES("+str(ssn)+","+ str(dentistSSN) +", "+str(appointmentID)+");")
            db.commit()
            mycursor1.execute("SELECT COUNT(*) FROM employee WHERE SSN = "+ str(ssn))
            if(mycursor1.fetchone()[0] == 0):

                mycursor1.execute("SELECT amount From payement Where ssn = " + str(ssn))

                currentAmount = mycursor1.fetchone()[0] + 500
                mycursor1.execute("UPDATE payement SET amount = " + str(currentAmount) + " WHERE ssn = " + str(ssn))
                db.commit()
            else:
                mycursor1.execute("SELECT amount From payement Where ssn = " + str(ssn))

                currentAmount = mycursor1.fetchone()[0] + 250
                mycursor1.execute("UPDATE payement SET amount = " + str(currentAmount) + " WHERE ssn = " + str(ssn))
                db.commit()

            #redirecting to home page
            db.close()
            mycursor1.close()
            return redirect(f"/patient/{ssn}")

    else:    
        db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')

        mycursor1 = db.cursor(buffered = True)
        # Retriving Dentist First  and Last Name from database
        mycursor1.execute("Select first_name, last_name FROM employee WHERE (role = \"dentist\" or role = \"hygentist\") AND SSN != " + str(ssn))
       
        #Creating list of dentists
        dentistList = []
        for x in mycursor1:
            name = x[0] + " " + x[1]
            dentistList.append(name)
        

        # Appointment Form
        form =  AppointmentForm()
        mycursor1.close()
        db.close()
        return render(response, "book_appointment.html", {'ls': dentistList, 'form': form})


def inBetween(start_time, end_time, time):
    if(start_time <= time <= end_time):
        return True
    else:
        return False


def viewAppointment(response, ssn):
    if response.method == "GET":
        db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')
        form = CancelForm()
        mycursor1 = db.cursor(buffered = True)
        mycursor1.execute("Select A.appointment_ID, date, startTime,endTime,first_name,last_name, appointment_type FROM appointment as A, book_appointment as B, employee as E WHERE A.appointment_ID = B.appointment_ID AND B.employee_SSN = E.SSN AND date >='"+date.today().strftime('%Y-%m-%d')+"'" + "AND B.patient_SSN = "+ str(ssn))
        appointmentInfoList = []
        for x in mycursor1:
            appointmentInfo = { "id" : str(x[0]),
                                "date"  : x[1].strftime("%m/%d/%Y"),
                                "startTime" : str(x[2]),
                                "endTime" : str(x[3]),
                                "firstName" : x[4],
                                "lastName" : x[5],
                                "type" : x[6]}
            
            appointmentInfoList.append(appointmentInfo)

        mycursor1.close()
        db.close()
        return render(response, "cancel_appointment.html", {"appointments" : appointmentInfoList , 'form': form})
    elif response.method == "POST":
        if "Cancel Button" in response.POST:
            db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')
            mycursor1 = db.cursor(buffered = True)
            form = CancelForm(response.POST)
            if(form.is_valid()):
                appointmentID = form.cleaned_data['appointment_ID']
                mycursor1.execute("SELECT startTime, endTime, date from appointment WHERE appointment_ID = " + str(appointmentID))
                for x in mycursor1:
                    appointmentDateTime = x[2].strftime("%m-%d-%Y") + " " + str(x[0])

                today = datetime. today()
                tmmr = today + timedelta(days=1)

                # Late Cancellation Fees
                if datetime.strptime(appointmentDateTime , '%m-%d-%Y %H:%M:%S')<tmmr:
                    mycursor1.close()
                    return redirect(f"/patient/appointments/view/late/{ssn}/{appointmentID}")
                else:
                    mycursor1.execute("SELECT COUNT(*) FROM employee WHERE SSN = "+ str(ssn))
                    if(mycursor1.fetchone()[0] == 0):
                        mycursor1.execute("SELECT amount From payement Where ssn = " + str(ssn))
                        currentAmount = mycursor1.fetchone()[0]  -500
                        mycursor1.execute("UPDATE payement SET amount = " + str(currentAmount) + " WHERE ssn = " + str(ssn))
                        mycursor1.execute("DELETE FROM book_appointment WHERE appointment_ID = " +str(appointmentID))
                        db.commit()
                        mycursor1.execute("DELETE FROM appointment WHERE appointment_ID = " +str(appointmentID))
                        db.commit()
                        mycursor1.execute("Select A.appointment_ID, date, startTime,endTime,first_name,last_name FROM appointment as A, book_appointment as B, employee as E WHERE A.appointment_ID = B.appointment_ID AND B.employee_SSN = E.SSN AND date >'"+date.today().strftime('%Y-%m-%d')+"'" + "AND B.patient_SSN = "+ str(ssn))
                        
                    else:
                        mycursor1.execute("SELECT amount From payement Where ssn = " + str(ssn))
                        currentAmount = mycursor1.fetchone()[0] -250
                        mycursor1.execute("UPDATE payement SET amount = " + str(currentAmount) + " WHERE ssn = " + str(ssn))
                        mycursor1.execute("DELETE FROM book_appointment WHERE appointment_ID = " +str(appointmentID))
                        db.commit()
                        mycursor1.execute("DELETE FROM appointment WHERE appointment_ID = " +str(appointmentID))
                        db.commit()
                        mycursor1.execute("Select A.appointment_ID, date, startTime,endTime,first_name,last_name FROM appointment as A, book_appointment as B, employee as E WHERE A.appointment_ID = B.appointment_ID AND B.employee_SSN = E.SSN AND date >'"+date.today().strftime('%Y-%m-%d')+"'" + "AND B.patient_SSN = "+ str(ssn))
                
                    mycursor1.execute("Select A.appointment_ID, date, startTime,endTime,first_name,last_name FROM appointment as A, book_appointment as B, employee as E WHERE A.appointment_ID = B.appointment_ID AND B.employee_SSN = E.SSN AND date >'"+date.today().strftime('%Y-%m-%d')+"'" + "AND B.patient_SSN = "+ str(ssn))
                    appointmentInfoList = []
                    for x in mycursor1:
                        appointmentInfo = { "id" : str(x[0]),
                                            "date"  : x[1].strftime("%m/%d/%Y"),
                                            "startTime" : str(x[2]),
                                            "endTime" : str(x[3]),
                                            "firstName" : x[4],
                                            "lastName" : x[5]}
                        
                        appointmentInfoList.append(appointmentInfo)
                    mycursor1.close()
                    db.close()
                    return render(response, "cancel_appointment.html", {"appointments" : appointmentInfoList , 'form': form})
        elif "Back Button" in response.POST:
            return redirect(f"/patient/{ssn}")


def cancellation(response, ssn, appointmentID):
    if response.method == "GET":
        return render(response,"cancellation.html")

    elif response.method == "POST":
        if "No" in response.POST:
            return redirect(f"/patient/{ssn}")
        elif "Yes" in response.POST:
            db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')  

            mycursor1 = db.cursor(buffered = True)
            mycursor1.execute("SELECT COUNT(*) FROM employee WHERE SSN = "+ str(ssn))
            if(mycursor1.fetchone()[0] == 0):
                mycursor1.execute("SELECT amount From payement Where ssn = " + str(ssn))
                currentAmount = mycursor1.fetchone()[0] + 14 -500
                mycursor1.execute("UPDATE payement SET amount = " + str(currentAmount) + " WHERE ssn = " + str(ssn))
                mycursor1.execute("DELETE FROM book_appointment WHERE appointment_ID = " +str(appointmentID))
                db.commit()
                mycursor1.execute("DELETE FROM appointment WHERE appointment_ID = " +str(appointmentID))
                db.commit()
                mycursor1.execute("Select A.appointment_ID, date, startTime,endTime,first_name,last_name FROM appointment as A, book_appointment as B, employee as E WHERE A.appointment_ID = B.appointment_ID AND B.employee_SSN = E.SSN AND date >'"+date.today().strftime('%Y-%m-%d')+"'" + "AND B.patient_SSN = "+ str(ssn))
                mycursor1.close()
                db.close()
                return redirect(f"/patient/{ssn}")
            else:
                mycursor1.execute("SELECT amount From payement Where ssn = " + str(ssn))
                currentAmount = mycursor1.fetchone()[0] + 14 -250
                mycursor1.execute("UPDATE payement SET amount = " + str(currentAmount) + " WHERE ssn = " + str(ssn))
                mycursor1.execute("DELETE FROM book_appointment WHERE appointment_ID = " +str(appointmentID))
                db.commit()
                mycursor1.execute("DELETE FROM appointment WHERE appointment_ID = " +str(appointmentID))
                db.commit()
                mycursor1.execute("Select A.appointment_ID, date, startTime,endTime,first_name,last_name FROM appointment as A, book_appointment as B, employee as E WHERE A.appointment_ID = B.appointment_ID AND B.employee_SSN = E.SSN AND date >'"+date.today().strftime('%Y-%m-%d')+"'" + "AND B.patient_SSN = "+ str(ssn))
                mycursor1.close()
                db.close()
                return redirect(f"/patient/{ssn}")

            


        

        



def viewRecords(response,ssn):
    db = mysql.connector.connect(
            host ='us-cdbr-east-05.cleardb.net',
            user ='be6fd11e32efb5',
            passwd='2e25d6f3',
            database = 'heroku_7f02c0751957843')
        
    mycursor1 = db.cursor(buffered = True)
    string = '''
    <html>
        <h1><center>Medical History</center></h1>
        <b1 style="font-weight: bold;">Patient Information</b1><br>'''

    # Query and Add Patient Information
    mycursor1.execute("SELECT SSN,first_name,last_name,date_of_birth FROM Patient WHERE SSN = " + ssn + ";")
    for patient in mycursor1:
        string += "<b2><strong>Name:</strong> " + patient[1] + " " + patient[2] + " <strong><br>SSN:</strong> " + str(patient[0]) + " <strong><br>Date Of Birth:</strong> " + str(patient[3]) + "</b2><br>"

    # Medical History Table Layout
    string += '''
        <br>
        <table border = 1 width = 100%>
        <tr>
            <th>Employee Name</th>
            <th>Employee Role</th>
            <th>Treatment Length (min)</th>
            <th>Medicine Required</th>
            <th>Patient Condition</th>
        </tr>'''

    # Query for Records
    mycursor1.execute("SELECT first_name,last_name,role,treatmentLength,medicineRequired,patientCondition FROM Employee E,Records R WHERE R.employeeSSN = E.SSN AND R.patientSSN = " + ssn + ";")

    # Populate Medical History table
    for record in mycursor1:
            string += "<tr>"
            string +=  "<td><center>"+record[0]+" "+record[1]+"</center></td>"
            string +=  "<td><center>"+record[2]+"</center></td>"
            string +=  "<td><center>"+str(record[3])+"</center></td>"
            string +=  "<td><center>"+record[4]+"</center></td>"
            string +=  "<td><center>"+record[5]+"</center></td>"
            string += "<tr>"
    string += "<table>"
    mycursor1.close()
    db.close()
    return HttpResponse(string)

def leaveReview(response, ssn):
    if response.method == 'POST':
        reviewForm = ReviewForm(response.POST)
        db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')
        mycursor1 = db.cursor(buffered = True)
        if reviewForm.is_valid():
            #User Inputs
            patientSSN = reviewForm.cleaned_data["patientSSN"]
            professionalism = reviewForm.cleaned_data["professionalism"]
            communication = reviewForm.cleaned_data["communication"]
            cleanliness = reviewForm.cleaned_data["cleanliness"]
            value = reviewForm.cleaned_data["value"]

            # Checking if the SSN exists in the database
            check = "SELECT count(*) FROM Patient WHERE SSN = " + str(patientSSN) + ";"
            mycursor1.execute(check)
            isValid = mycursor1.fetchone()[0]

            if isValid == 1 and patientSSN == int(ssn):
                # Creating Review for Database
                query = "INSERT INTO Reviews VALUES(" + str(patientSSN) + "," + str(professionalism) + "," + str(communication) + "," + str(cleanliness) + "," + str(value) + ");"
                mycursor1.execute(query)
                db.commit()

                # Home Page
                mycursor1.close()
                db.close()
                return redirect(f"/patient/{ssn}")

            else:
                mycursor1.close()
                db.close()
                # Stay in the same page
                return render(response,"leaveReview.html",{'review' : reviewForm, 'error' : "Invalid SSN"})
    else:
        # Stay in the same page
        reviewForm = ReviewForm()
        return render(response,"leaveReview.html",{'review' : reviewForm})
