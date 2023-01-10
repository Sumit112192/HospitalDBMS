from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,DateField,RadioField
from passlib.hash import sha256_crypt
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_wtf import Form

app=Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'hospital_management'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
Bootstrap(app)
datepicker(app)


class MyForm(Form):
    patient_id = StringField('Patient Id')
    doctor_id = StringField('Doctor Id')
    room_id = StringField('Room Id')
    disease = StringField('Disease')
    treatment_fee = StringField('Treatment Fee')
    date = StringField(id='datepick')
    description = StringField('Description')

class EditForm(Form):
    name = StringField('Name', [validators.DataRequired(),validators.Length(min=1,max=50)])
    sex = RadioField('Sex', choices=[('M','Male'),('F','Female'),('O','Other')])
    address = StringField('Address', [validators.DataRequired(),validators.Length(min=5,max=150)])
    city = StringField('City', [validators.DataRequired(),validators.Length(min=1,max=50)])
    pincode = StringField('Pincode', [validators.DataRequired(),validators.Length(min=1,max=50)])
    email = StringField('Email', [validators.DataRequired(),validators.Length(min=6,max=50)])
    contact = StringField('Contact', [validators.DataRequired(),validators.Length(min=1,max=50)])

@app.route('/home')
def index():
        return render_template('home.html')

@app.route('/')
def index2():
        return render_template('home.html')


@app.route('/about')
def about():
        return render_template('about.html')



class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1,max=50)])
    username = StringField('Username', [validators.Length(min=4,max=225)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [
                validators.DataRequired(),
                validators.EqualTo('confirm',message='Passwords do not match')
        ])
    confirm= PasswordField('Confirm Password')
    profession=StringField('Profession', [validators.Length(min=3,max=50)])


@app.route('/register',methods=['GET','POST'])
def register():
    form= RegisterForm(request.form)
    if request.method=='POST':
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
                
        cur.execute("INSERT INTO Patient(Name,Username,Email,Password) VALUES(%s, %s, %s, %s)",(name,username,email,password))
                
        mysql.connection.commit()

        cur.close()
        flash("You are now registered patient and can log in",'success')
        redirect(url_for('login'))
        return render_template('register.html',form=form)
    return render_template('register.html',form=form)
       

@app.route('/staffRegister',methods=['GET','POST'])
def staffRegister():
    form= RegisterForm(request.form)
    if request.method=='POST':
        name = form.name.data
        email = form.email.data
        username = form.username.data
        profession=form.profession.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
                
        if profession=="Doctor":
            cur.execute("INSERT INTO Doctor (Name,Username,Email) VALUES(%s, %s, %s)",(name,username,email))
        elif profession=="Nurse":
            cur.execute("INSERT INTO Nurse (Name,Username,Email) VALUES(%s, %s, %s)",(name,username,email))
        elif profession=="Receptionist":
            cur.execute("INSERT INTO Receptionist (Name,Username,Email) VALUES(%s, %s, %s)",(name,username,email))
                
        cur.execute("INSERT INTO Employee_credentials VALUES(%s, %s,%s)",(email,password,profession))
        mysql.connection.commit()

        cur.close()

        flash("You are now registered staff member and can log in",'success')
        redirect(url_for('login'))
        return render_template('staffRegister.html',form=form)
    return render_template('staffRegister.html',form=form)
        
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        userDetails = request.form
        email = userDetails['email']
        user_password = userDetails['password']
        cur = mysql.connection.cursor()
        result =cur.execute("SELECT * from Patient WHERE email=%s",[email])
        if result>0:
                data= cur.fetchone()
                password= data['Password']
                if sha256_crypt.verify(user_password,password):
                    app.logger.info('PASSWORD MATCHED')
                    session['logged_in'] = True
                    session['email'] = email
                    session['profession']="Patient"
                    flash('You are now logged in as Patient','success')
                    return redirect(url_for('dashboard',profession="Patient"))
                else:
                    error= 'Invalid Login'
                    return render_template('login.html',error=error)
        cur.close()
    return render_template('login.html')
            

@app.route('/staffLogin',methods=['GET','POST'])
def staffLogin():
    if request.method == "POST":
        userDetails = request.form
        if userDetails:
            email = userDetails['email']
            user_password = userDetails['password']
            cur = mysql.connection.cursor()
            result=cur.execute("SELECT * from Employee_credentials WHERE email=%s",[email])
        if result>0:
                data= cur.fetchone()
                password= data['Password']     #Make this small password
                profession=data['profession']
                session['profession']=profession
                mysql.connection.commit()
                cur.close()
                cur = mysql.connection.cursor()
                if profession=="Doctor":
                        cur.execute(" SELECT * FROM Doctor WHERE email=%s",[email])
                elif profession=="Nurse":
                        cur.execute(" SELECT * FROM Nurse WHERE email=%s",[email])
                elif profession=="Receptionist":
                        cur.execute(" SELECT * FROM Receptionist WHERE email=%s",[email])
                value=cur.fetchone()
                username=value['Username']
                if sha256_crypt.verify(user_password,password):
                    app.logger.info('PASSWORD MATCHED')
                    session['logged_in'] = True
                    session['email'] = email
                    session['username']=username
                    flash('You are now logged in as Staff Member','success')
                    return redirect(url_for('dashboard',profession=profession))
                else:
                    error= 'Invalid Login'
                    return render_template('staffLogin.html',error=error)
        else:
            flash("Not a user",'danger')
            return redirect(url_for('staffRegister'))
        cur.close()
    return render_template('staffLogin.html')

@app.route('/<profession>/dashboard')
def dashboard(profession):
    return render_template('dashboard.html',profession=profession)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

@app.route("/<profession>/<id>/detail", methods=['GET', 'POST'])
def detail(profession,id):
    cur = mysql.connection.cursor()
    profession=session['profession']
    if profession=="Patient":
        result=cur.execute("Select * from Patient Where pid=%s",[id])
        if result>0:
            user=cur.fetchone()
        cur.execute("SELECT Name,Timing,Description from Records natural join Doctor WHERE pid=%s",[id])
        appointment_details = cur.fetchone()
        cur.execute("SELECT Disease,Amount from Treatment where pid=%s",[id])
        treatment_detail = cur.fetchone()
        cur.execute("SELECT room_id,Joined_date from Room where pid=%s",[id])
        room_details = cur.fetchone()

        return render_template('detail.html',user=user,profession=profession,appointment_details=appointment_details,treatment_detail=treatment_detail,room_details=room_details)
    elif profession=="Doctor":
        result=cur.execute("Select * from Doctor Where did=%s",[id])
    elif profession=="Nurse":
        result=cur.execute("Select * from Nurse Where nid=%s",[id])
    elif profession=="Receptionist":
        result=cur.execute("Select * from Receptionist Where rid=%s",[id])
    if result>0:
        user = cur.fetchone()
    return render_template('detail.html',user=user,profession=profession)
            




@app.route("/<profession>/<id>/edit",methods=['GET','POST'])
def edit(profession,id):


    cur = mysql.connection.cursor()
    
    if profession == "Patient":
        cur.execute("Select Name,SEX,Address,City,Pincode,Email,Contact from Patient WHERE pid=%s",[id])
        
    elif profession == "Doctor":
        cur.execute("Select Name,SEX,Address,City,Pincode,Email,Contact from Doctor WHERE did=%s",[id])
        
    elif profession=="Nurse":
        
        cur.execute("Select Name,SEX,Address,City,Pincode,Email,Contact from Nurse WHERE nid=%s",[id])
        
    elif profession=="Receptionist":
        cur.execute("Select Name,SEX,Address,City,Pincode,Email,Contact from Receptionist WHERE rid=%s",[id])
    
    user = cur.fetchone()
    form= EditForm(request.form)
    if request.method=='POST':
        name = form.name.data
        sex = form.sex.data
        address=form.address.data
        city=form.city.data
        pincode=form.pincode.data
        email= form.email.data
        contact= form.contact.data



        cur = mysql.connection.cursor()
        VALUES= (name, sex, address, city, pincode, email, contact, id)
        if profession == "Patient":
            cur.execute("UPDATE Patient SET Name=%s, SEX=%s, Address=%s, City=%s, Pincode=%s,Email=%s,Contact=%s WHERE pid=%s",VALUES)
            result=cur.execute("Select * from Patient WHERE pid=%s",[id])
            records = cur.fetchone()
        elif profession == "Doctor":
            cur.execute("UPDATE Doctor SET Name=%s, SEX=%s, Address=%s, City=%s, Pincode=%s,Email=%s,Contact=%s WHERE did=%s",VALUES)
            result=cur.execute("Select * from Doctor WHERE did=%s",[id])
            records = cur.fetchone()
        elif profession=="Nurse":
            cur.execute("UPDATE Nurse SET Name=%s, SEX=%s, Address=%s, City=%s, Pincode=%s,Email=%s,Contact=%s WHERE nid=%s",VALUES)
            result=cur.execute("Select * from Nurse WHERE nid=%s",[id])
            records= cur.fetchone()
        elif profession=="Receptionist":
            cur.execute("UPDATE Receptionist SET Name=%s, SEX=%s, Address=%s, City=%s, Pincode=%s, Email=%s,Contact=%s WHERE rid=%s",VALUES)
            result=cur.execute("Select * from Receptionist WHERE rid=%s",[id])
            records = cur.fetchone()
                
        mysql.connection.commit()
        cur.close()
        if result > 0:
                    #records = cur.fetchone()
            return render_template('detail.html',user=records)
        else:
            return render_template('edit.html',form=form,user=user)
    
    return render_template('edit.html',form=form,user=user)

                




@app.route('/<profession>/profile', methods=['GET', 'POST'])
def profile(profession):
    cur = mysql.connection.cursor()
    email=session['email']
    if profession=="Patient":
        cur.execute("Select pid,Name,Email,Contact from Patient Where email=%s",[email])
        user=cur.fetchone()
        id = user['pid']
    elif profession=="Doctor":
        cur.execute("Select did,Name,Email,Username from Doctor Where email=%s",[email] )
        user=cur.fetchone()
        id=user['did']
    elif profession=="Nurse":
        cur.execute("Select nid,Name,Email,Username from Nurse Where email=%s",[email])
        user = cur.fetchone()
        id = user['nid']
    elif profession=="Receptionist":
        cur.execute("Select rid,Name,Email,Username from Receptionist Where email=%s",[email])
        user = cur.fetchone()
        id = user['rid']
    cur.close()

    if user:
        return render_template("profile.html",user=user,profession=profession,id=id)
    

    return render_template("profile.html")

@app.route('/<profession>/search', methods=['GET','POST'])
def search(profession):
    
    if request.method == 'POST':
        searchDetails = request.form
        cur = mysql.connection.cursor()
        if searchDetails['submit']=="patient_appointment":
            pid = searchDetails['patient_id']
            cur.execute("SELECT Timing,Name,Description from Records natural join Doctor  where pid=%s",[pid])
            record1 = cur.fetchall()
            cur.execute("SELECT * from Patient where pid=%s",[pid])
            record2 = cur.fetchall()
            if record2:

                return render_template('patient_appointment.html',record1=record1, record2=record2[0],profession=profession,id=id)
            else:
                return render_template('User_not_exist.html')
        elif searchDetails['submit']=='doctor_appointment':
            did = searchDetails['doctor_id']
            cur.execute("SELECT Timing,Name,Description from Records natural join Patient  where did=%s",[did])
            record1 = cur.fetchall()
            cur.execute("SELECT * from Doctor where did=%s",[did])
            record2 = cur.fetchall()
            if record2:
                return render_template('doctor_appointment.html',record1=record1, record2=record2[0],profession=profession,id=id)
            else:
                return render_template('User_not_exist.html',profession=profession,id=id)
        elif searchDetails['submit']=='patient_bill':
            pid = searchDetails['patient_id']
            cur.execute("SELECT pid,Amount,Disease from Treatment where pid=%s",[pid])
            record1 = cur.fetchone()
            cur.execute("SELECT Name,pid from Patient where pid=%s",[pid])
            record2 = cur.fetchone()
            if record2:
                return render_template('bill.html',record1=record1, record2=record2,profession=profession,id=id)
            else:
                return render_template("User_not_exist.html",profession=profession,id=id)
    return render_template('recep.html',profession=profession)

@app.route('/appointment/<whom>/<patient_doctor_id>', methods=['GET','POST'])    #Here id is for patient or doctor id
def appointment(whom,patient_doctor_id):
    form = MyForm()
    if request.method=='POST':
        patient_id = form.patient_id.data
        doctor_id = form.doctor_id.data
        timing = form.date.data
        description = form.description.data

        cur= mysql.connection.cursor()
        if whom=="Patient":
            cur.execute("SELECT * from Doctor where did=%s",[doctor_id])
            records = cur.fetchall()

            if not records:
                return render_template('not_exist.html',whom=whom,patient_doctor_id=patient_doctor_id, form=form)
        elif whom=="Doctor":
            cur.execute("SELECT * from Patient where pid=%s",[patient_id])  
            records = cur.fetchall()

            if not records:
                return render_template('not_exist.html',whom=whom,patient_doctor_id=patient_doctor_id, form=form)
        cur.close()
        timing = timing.split(" ")

        month_day = ''.join(list(timing[0])[0:5])
        year = ''.join(list(timing[0])[6:10])
        time = timing[1]
        am_pm = timing[2]
        hour = time.split(':')[0]
        minute = time.split(':')[1]
        if am_pm == 'PM':
            hour = int(hour)+12
            if int(hour)>=24:
                hour = int(hour)-24


        hour = str(hour)
        timing = year+'/'+month_day+' '+hour+':'+minute
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO  Records (pid,did,Timing,Description) VALUES (%s,%s,%s,%s)",[patient_id,doctor_id,timing,description])
        mysql.connection.commit()
        cur.close()
        

        return redirect( url_for('search',profession="Receptionist"))
    return render_template('appointment.html',whom=whom,patient_doctor_id=patient_doctor_id, form=form)

@app.route('/bill/create_bill/<patient_id>', methods=['GET','POST'])    #Here id is for patient or doctor id
def create_bill(patient_id):
    form = MyForm()
    if request.method=='POST':
        patient_id = form.patient_id.data
        disease = form.disease.data
        doctor_id = form.doctor_id.data
        treatment_fee = form.treatment_fee.data


        cur= mysql.connection.cursor()
        cur.execute("SELECT * from Doctor where did=%s",[doctor_id])
        records = cur.fetchall()
        if not records:
            return render_template("doctor_not_exist.html",patient_id=patient_id,form=form)
        
        cur.execute("INSERT INTO  Treatment (pid,did,Disease,Amount) VALUES (%s,%s,%s,%s)",[patient_id,doctor_id,disease,treatment_fee])
        mysql.connection.commit()
        cur.close()
        

        return redirect( url_for('search',profession="Receptionist"))
    return render_template('create_bill.html',patient_id=patient_id, form=form)

@app.route('/<profession>/room',methods=['GET','POST'])
def room(profession):
    if request.method == 'POST':
        searchDetails = request.form
        cur = mysql.connection.cursor()
        if searchDetails['submit']=="patient_id":
            pid = searchDetails['patient_id']
            cur.execute("SELECT room_id,Joined_date,Leaving_date from Room where pid=%s",[pid])
            record1 = cur.fetchall()
            cur.execute("SELECT * from Patient where pid=%s",[pid])
            record2 = cur.fetchall()
            if record2:
                return render_template('patient_room.html',record1=record1, record2=record2[0],profession=profession,id=id)
            else:
                return render_template('user1_not_exist.html',profession=profession)
        elif searchDetails['submit']=='room_id':
            room_id = searchDetails['room_id']
            cur.execute("SELECT room_id,Joined_date,Leaving_date,pid,Name from Room natural join Patient where room_id=%s",[room_id])
            records = cur.fetchone()        
            return render_template('room_search.html',records=records,room_id=room_id,profession=profession)

    return render_template('nurse.html',profession=profession)

@app.route('/room/<which_id>/<patient_room_id>',methods=['GET','POST'])
def room_allocation(which_id,patient_room_id):
    form = MyForm()
    if request.method=='POST':
        patient_id = form.patient_id.data
        room_id = form.room_id.data
        Joined_date = form.date.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from Room where room_id=%s or pid=%s",[room_id,patient_id])
        records = cur.fetchall()
        if records:
            return render_template('user_room_allocated.html',which_id=which_id,patient_room_id=patient_room_id,form=form)

        timing = Joined_date.split(" ")

        month_day = ''.join(list(timing[0])[0:5])
        year = ''.join(list(timing[0])[6:10])
        time = timing[1]
        am_pm = timing[2]
        hour = time.split(':')[0]
        minute = time.split(':')[1]
        if am_pm == 'PM':
            hour = int(hour)+12
            if int(hour)>=24:
                hour = int(hour)-24


        hour = str(hour)
        Joined_date = year+'/'+month_day+' '+hour+':'+minute
        
        cur.execute("INSERT INTO  Room (pid,room_id,Joined_date) VALUES (%s,%s,%s)",[patient_id,room_id,Joined_date])
        mysql.connection.commit()
        cur.close()
        

        return redirect( url_for('room',profession="Nurse"))
    return render_template('room_allocation.html',which_id=which_id,patient_room_id=patient_room_id, form=form)
    
@app.route('/<profession>/details',methods=['GET','POST'])
def doctor_appointment(profession):
    email = session['email']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from Doctor where Email=%s",[email])
    record = cur.fetchone()
    did = record['did']
    cur.execute("SELECT * from Patient natural join Records where did=%s",[did])
    record1 = cur.fetchall()

    cur.execute("SELECT * from Patient natural join Treatment where did=%s",[did])
    record2 = cur.fetchall()

    return render_template('doctor.html',record1=record1,record2=record2,profession=profession)

if __name__ == '__main__':
        app.secret_key='Harshad@123'
        app.run(debug=True)




"""
@app.route("/edit", methods=['GET', 'POST'])
def edit():
    cur = mysql.connection.cursor()
    email=session['email']
    profession = cur.execute("Select Profession from employee_credentials where email=%s",[email])
    if profession=="Patient":
        cur.execute("Select pid,Name,SEX,Address,City,Pincode,Email,Username from Patient Where pid=%s",[id])
    elif profession=="Doctor":
        cur.execute("Select did,Name,SEX,Address,City,Pincode,Email,Username from Doctor Where email=%s",[email])
    elif profession=="Nurse":
        cur.execute("Select nid,Name,SEX,Address,City,Pincode,Email,Username from Nurse Where nid=%s",id)
    elif profession=="Receptionist":
        cur.execute("Select rid,Name,SEX,Address,City,Pincode,Email,Username from Receptionist Where rid=%s",id)
    user = cur.fetchone()
    if request.method == "POST":
        userDetails = request.form
        name = userDetails['name']
        sex = 'Male'
        Address = userDetails['add']
        city = userDetails['city']
        pin = userDetails['pin']
        #eid = userDetails['eid']
        username = session['username']
        cur = mysql.connection.cursor()
        VALUES= (name, sex, Address, city, pin,  username, email)
        if profession == "Patient":
            cur.execute("UPDATE Patient SET Name=%s, SEX=%s, Address=%s, City=%s, Pincode=%s,Email=%s,\
                        Username=%s WHERE pid=%s",VALUES)
            cur.execute("Select * from Patient WHERE pid=%s",id)
            #records = cur.fetchone()
        elif profession == "Doctor":
            cur.execute("INSERT INTO Doctor VALUES (%s,%s,%s,%s,%s,%s) WHERE email=%s",VALUES)
            result=cur.execute("Select * from Doctor WHERE email=%s",[email])
            #records = cur.fetchone()
        elif profession=="Nurse":
            cur.execute("UPDATE Nurse SET Name=%s, SEX=%s, Address=%s, City=%s, Pincode=%s,Email=%s,\
                        Username=%s WHERE nid=%s",VALUES)
            cur.execute("Select * from Nurse WHERE nid=%s",id)
            # = cur.fetchone()
        else:
            cur.execute("UPDATE Receptionist SET Name=%s, SEX=%s, Address=%s, City=%s, Pincode=%s,\
                        Username=%s WHERE email=%s",VALUES)
            result=cur.execute("Select * from Receptionist WHERE email=%s",[email])
        #records = cur.fetchone()
        if result > 0:
            records = cur.fetchone()
            return render_template('detail.html',user=records)
        else:
            return render_template('edit.html')


    return render_template('edit.html',user=user)"""