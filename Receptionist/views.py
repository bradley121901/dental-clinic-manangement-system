from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import mysql.connector

from Dental.views import patient
from .form import findPatient
from .form import patient_register_form
from .form import AppointmentForm
from datetime import *
# Create your views here.

db = mysql.connector.connect(
    host ='us-cdbr-east-05.cleardb.net',
    user ='be6fd11e32efb5',
    passwd='2e25d6f3',
    database = 'heroku_7f02c0751957843')

mycursor = db.cursor(buffered=True)

# retrieve patient details and return patientInfo.html page to client
# contains one url parameter ssn
def patientInfo(request, ssn, patientSSN):
    context = {}
    initial_dict ={}
    # define the returned patient as None
    patient = None
    db = mysql.connector.connect(
        host ='us-cdbr-east-05.cleardb.net',
        user ='be6fd11e32efb5',
        passwd='2e25d6f3',
        database = 'heroku_7f02c0751957843')

    mycursor = db.cursor(buffered=True)

    # sql query to retrive patient 
    mycursor.execute("SELECT * FROM patient WHERE SSN=" + patientSSN +";")

    # get the returned patient object
    if mycursor.rowcount > 0:
        # retrieves column attributes of patient with the specified ssn passed through url
        for x in mycursor:
            firstname = x[0]
            lastname = x[1]
            housenumber = x[2]
            streetname = x[3]
            city = x[4]
            province = x[5]
            gender = x[6]
            email = x[7]
            dob = x[8]
            SSN = x[9]


        # dictionary for initial data with field names as keys
        # stores retrieved data to pass onto form
        inital_dict = {
        "firstname" : firstname,
        "lastname" : lastname,
        "housenumber": housenumber,
        "streetname": streetname,
        "city": city,
        "province":  province,
        "gender": gender,
        "email": email,
        "dob": dob,
        "housenumber": housenumber,
        "SSN": SSN
        }
    else:
        patient = None

    # initialize form with dictionary during webpage intialization
    form = patient_register_form(inital_dict)
    context['form'] = form

    mycursor.close()
    db.close()

    # return the patientInfo.html  template file to client and pass form context
    if request.method == "GET":
        return render(request, 'patientInfo.html', context)  
    elif request.method == "POST":
        if "save" in request.POST:
            form = patient_register_form(request.POST)
            db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')

            mycursor = db.cursor(buffered=True)
            if form.is_valid():
                firstname = form.cleaned_data["firstname"]
                lastname = form.cleaned_data["lastname"]
                housenumber = form.cleaned_data["housenumber"]
                streetname = form.cleaned_data["streetname"]
                city = form.cleaned_data["city"]
                province = form.cleaned_data["province"]
                gender = form.cleaned_data["gender"]
                email = form.cleaned_data["email"]
                dob = form.cleaned_data["dob"]
                SSN = form.cleaned_data["SSN"]
                

                 # sql query to delete original patient data
                mycursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                mycursor.execute("DELETE FROM patient WHERE SSN=" + patientSSN +";")
                mycursor.execute("SET FOREIGN_KEY_CHECKS=1;")
                db.commit()
                # sql query to add new patient data
                mycursor.execute("INSERT INTO patient VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (firstname, lastname, housenumber, streetname, city, province, gender, email, dob, SSN))
                db.commit()
                mycursor.close()
                db.close()
               
            return redirect(f"/receptionist/{ssn}")
        return redirect(f"/receptionist/{ssn}")
        

# gets ssn input and passes through url
def reception(request, ssn):
    if request.method == "GET":
        return render(request, "reception.html")

    elif request.method == "POST":
        if "Find" in request.POST:
            form = findPatient(request.POST)
            db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')

            mycursor = db.cursor(buffered=True)
            if form.is_valid():
                #retrieving user input
                patientSSN = form.cleaned_data["patientSSN"]
                mycursor.execute("SELECT COUNT(*) FROM patient WHERE SSN = " + str(patientSSN))
                
                if(mycursor.fetchone()[0] == 1):
                    mycursor.close()
                    db.close()
                    return redirect(f"{ssn}/{patientSSN}")
                else:
                    mycursor.close()
                    db.close()
                    return render(request, "reception.html", {'error' :'Patient SSN not found'})

                #return render(request, 'patientInfo.html', {"ssn": patientSSN})
        elif "newAppointment" in request.POST:
            form = findPatient(request.POST)
            db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')

            mycursor = db.cursor(buffered=True)
            if form.is_valid():
                #retrieving user input
                patientSSN = form.cleaned_data["patientSSN"]
                mycursor.execute("SELECT COUNT(*) FROM patient WHERE SSN = " + str(patientSSN))
                if(mycursor.fetchone()[0] == 1):
                    mycursor.close()
                    db.close()
                    return redirect(f"appointment/{patientSSN}/{ssn}")
                else:
                    mycursor.close()
                    db.close()
                    return render(request, "reception.html", {'error' :'Patient SSN not found'})


# assign patient appointment
# contains one url parameter ssn
def bookAppointment(request, patientSSN, ssn):


    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')
        mycursor = db.cursor(buffered=True)

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


            # Retriving Dentist SSN from database
            mycursor.execute("Select SSN FROM employee WHERE first_name = '"+dentist_FN+"' AND last_name ='"+dentist_LN+"';")
            for x in mycursor:
                dentistSSN = x[0]
                break
            
            # Determining the appointment Id
            mycursor.execute("Select COUNT(*)FROM appointment")
            for i in mycursor:
                appointmentID = i[0]
                break
            appointmentID+=1
            

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
                mycursor.execute(query)


                for x in mycursor:
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
                mycursor.execute("Select first_name, last_name FROM employee WHERE role = \"Dentist\" or role = \"hygentist\";")
                
                #Creating list of dentists
                dentistList = []
                for x in mycursor:
                    name = x[0] + " " + x[1]
                    dentistList.append(name)
                return render(request, "book_appointment.html", {'ls': dentistList,'form': form, 'error': "One or more Incorrect Field"})    
            
            
            # Inserting appointment into db
            mycursor.execute("INSERT INTO appointment VALUES("+str(appointmentID)+",'"+appointment_date +"', '"+startTime+"', '"+endTime+"' , '"+ appointment_type+"');")
            db.commit()
            mycursor.execute("INSERT INTO book_appointment VALUES("+str(patientSSN)+","+ str(dentistSSN) +", "+str(appointmentID)+");")
            db.commit()

            mycursor.close()
            db.close()
            #redirecting to home page
            return redirect(f"/receptionist/{ssn}")

    else:   
        db = mysql.connector.connect(
                host ='us-cdbr-east-05.cleardb.net',
                user ='be6fd11e32efb5',
                passwd='2e25d6f3',
                database = 'heroku_7f02c0751957843')
        mycursor = db.cursor(buffered=True)
        # Retriving Dentist First  and Last Name from database
        mycursor.execute("Select first_name, last_name FROM employee WHERE role = \"Dentist\" or role = \"Hygentist\";")
        
        #Creating list of dentists
        dentistList = []
        for x in mycursor:
            name = x[0] + " " + x[1]
            dentistList.append(name)

        # Appointment Form
        form =  AppointmentForm()
        mycursor.close()
        db.close()


    return render(request, "newAppointment.html", {'ls': dentistList, 'form': form})
       
def inBetween(start_time, end_time, time):
    if(start_time <= time <= end_time):
        return True
    else:
        return False