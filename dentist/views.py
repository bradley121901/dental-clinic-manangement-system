from django.shortcuts import redirect, render
from .form import SearchForm
import mysql.connector
from datetime import *
from django.http import HttpResponse

# db = mysql.connector.connect(
#     host ='us-cdbr-east-05.cleardb.net',
#     user ='be6fd11e32efb5',
#     passwd='2e25d6f3',
#     database = 'heroku_7f02c0751957843')

# mycursor = db.cursor()


def landing(request, ssn):
    if request.method == "GET":
        form = SearchForm()
        return render(request, "landing.html", {"form": form})

    elif request.method == "POST":
        if "appointment" in request.POST:
            print(1)
            return redirect(f"upcoming-appointments/{ssn}")
        elif "save" in request.POST:
            print(2)
            searchForm = SearchForm(request.POST)
            if searchForm.is_valid():
                patientFirstName = searchForm.cleaned_data["Patient_fname"]
                patientLastName = searchForm.cleaned_data["Patient_lname"]
                patientName = patientFirstName + "-" + patientLastName
                return redirect(f"patient-records/{patientName}")
        elif "branch" in request.POST:
            db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')

            mycursor = db.cursor()
            mycursor.execute("SELECT count(*) FROM Branches WHERE managerSSN = " + ssn + ";")
            isManager = mycursor.fetchone()[0]
            if isManager == 0:
                form = SearchForm()
                mycursor.close()
                db.close()
                return render(request,"landing.html",{'form' : form, 'error' : "You cannot access branch information if you are not the manager"})
            else:
                mycursor.close()
                db.close()
                return redirect(f"branch-details/{ssn}")
        elif "patient page" in request.POST:
            return redirect(f"/patient/{ssn}")


def appointment(request, ssn):
    db = mysql.connector.connect(
        host ='us-cdbr-east-05.cleardb.net',
        user ='be6fd11e32efb5',
        passwd='2e25d6f3',
        database = 'heroku_7f02c0751957843')

    mycursor = db.cursor()    
    query = '''
    Select date, startTime,endTime,P.first_name,P.last_name 
    FROM appointment as A, book_appointment as B, patient as P 
    WHERE A.appointment_ID = B.appointment_ID AND B.employee_SSN = 
    '''+ str(ssn)
    mycursor.execute("Select date, startTime,endTime,P.first_name,P.last_name FROM appointment as A, book_appointment as B, patient as P WHERE A.appointment_ID = B.appointment_ID AND B.employee_SSN ="+ str(ssn) +" AND date >'"+date.today().strftime('%Y-%m-%d')+"'AND B.patient_SSN =P.SSN;")

    string = '''
    <html>
        <head>
            <h1> Upcoming Appointment Dates </h1>
        </head>
        <body>
            <table border = 1 width = 100%>
                <tr>
                    <th>Appointment Date</th>
                    <th>Appointment Start Time</th>
                    <th>Appointment End Time (min)</th>
                    <th>Patient First Name</th>
                    <th>Patient Last Name</th>
                </tr>
    '''

    for x in mycursor:
        string += "<tr>"
        string +=  "<td><center>"+x[0].strftime("%m/%d/%Y")+"</center></td>"
        string +=  "<td><center>"+str(x[1])+"</center></td>"
        string +=  "<td><center>"+str(x[2])+"</center></td>"
        string +=  "<td><center>"+x[3]+"</center></td>"
        string +=  "<td><center>"+x[4]+"</center></td>"
        string += "</tr>"

    string += '''
            </table>
        </body>
    </html>
    
    '''
    mycursor.close()
    db.close()


    return HttpResponse(string)

def patientRecords(request,patientName):
    db = mysql.connector.connect(
    host ='us-cdbr-east-05.cleardb.net',
    user ='be6fd11e32efb5',
    passwd='2e25d6f3',
    database = 'heroku_7f02c0751957843')

    db = mysql.connector.connect(
        host ='us-cdbr-east-05.cleardb.net',
        user ='be6fd11e32efb5',
        passwd='2e25d6f3',
        database = 'heroku_7f02c0751957843')

    mycursor = db.cursor()   
    string = '''
        <html>
            <h1><center>Medical History</center></h1>
            <b1 style="font-weight: bold;">Patient Information</b1><br>'''

    patientFirst = patientName.split('-')[0]
    patientLast = patientName.split('-')[1]
    patientSSN = "None"

    # If more than one patient with same fName and lName, takes only the first one fetched
    counter = 0
    mycursor.execute("SELECT SSN,first_name,last_name,date_of_birth FROM Patient WHERE first_name = '" + patientFirst + "'AND last_name = '" + patientLast + "';")
    for patient in mycursor:
        if counter == 0:
            patientSSN = str(patient[0])
            string += "<b2><strong>Name:</strong> " + patient[1] + " " + patient[2] + " <strong><br>SSN:</strong> " + str(patient[0]) + " <strong><br>Date Of Birth:</strong> " + str(patient[3]) + "</b2><br>"
        counter += 1

    # If patient does not exist
    if patientSSN == "None":
        string2 = '''
            <html>
                <head>
                    <h1><center> No Patient With Such Name </center></h1>
                </head>
            </html>'''
        return HttpResponse(string2)
    else:
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

        mycursor.execute("SELECT first_name,last_name,role,treatmentLength,medicineRequired,patientCondition FROM Employee E,Records R WHERE R.employeeSSN = E.SSN AND R.patientSSN = " + patientSSN + ";")
        for record in mycursor:
                    string += "<tr>"
                    string +=  "<td><center>"+record[0]+" "+record[1]+"</center></td>"
                    string +=  "<td><center>"+record[2]+"</center></td>"
                    string +=  "<td><center>"+str(record[3])+"</center></td>"
                    string +=  "<td><center>"+record[4]+"</center></td>"
                    string +=  "<td><center>"+record[5]+"</center></td>"
                    string += "<tr>"
        string += "<table>"

        mycursor.close()
        db.close()
        return HttpResponse(string)


def branchDetails(request, ssn):
    db = mysql.connector.connect(
        host ='us-cdbr-east-05.cleardb.net',
        user ='be6fd11e32efb5',
        passwd='2e25d6f3',
        database = 'heroku_7f02c0751957843')

    mycursor = db.cursor()   
    string = '''
        <html>
            <h1><center>BRANCH INFORMATION</center></h1>'''

    mycursor.execute("SELECT first_name, last_name, branchNo, B.city, numOfClinics, numOfEmployees FROM Employee E, Branches B WHERE E.SSN = B.managerSSN AND E.SSN = " + ssn + ";")
    for branch in mycursor:
        string += "<b2><strong>Manager Name:</strong> " + branch[0] + " " + branch[1] + " <strong><br>Branch Number:</strong> " + str(branch[2]) + " <strong><br>Branch City:</strong> " + branch[3] + " <strong><br>Number of Clinics:</strong> " + str(branch[4]) + " <strong><br>Number of Employees:</strong> " + str(branch[5]) + "</b2><br>" + "</html"

    mycursor.close()
    db.close()
    return HttpResponse(string)