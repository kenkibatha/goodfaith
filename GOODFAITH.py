from flask import Flask, render_template, request, Response, redirect, url_for, session, flash
from functools import wraps
app = Flask(__name__)
app.secret_key = 'wewe'
import pymysql
import pygal

#  login_required decorator
def login_required(f):
    print('hrtyy')
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please log in First!!')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
        error = None
        if request.method == "POST":
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':

                error = 'Invalid Login, Please Try Again'
            else:
                session['logged_in'] = True
                flash('You were just logged in!')
                return redirect(url_for('students'))
        return render_template('index.html',error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('login'))


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/student', methods=['GET', 'POST'])
@login_required
def students():
    if request.method == "POST":  # this checks the method used
        regno = request.form['regno']
        surname = request.form['surname']
        name = request.form['name']
        other = request.form['other']
        dob = request.form['dob']
        gender = request.form['gender']
        sclass = request.form['class']

        if regno == "":
            return render_template("students.html", msg="Check your fields!!!")
        else:
            con = pymysql.connect("localhost", "root", "", "goodfaith_db")
            cursor = con.cursor()  # to execute our sql
            sql = "INSERT INTO `tblstudents`(`regno`, `surname`, `name`, `other`, `dob`, `gender`, `class`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            data = (regno, surname, name, other, dob, gender, sclass)
            cursor.execute(sql, data)
            con.commit()
            return render_template("students.html", msg1="Student Registered Successfully")
    else:
        return render_template('students.html')

@app.route('/payments', methods=['GET', 'POST'])
def payements():
    if request.method == "POST":  # this checks the method used
        regno = request.form['regno']
        amount = request.form['amount']

        if regno == "" :
            return render_template("payments.html", msg="Check above field!")
        else:
            con = pymysql.connect("localhost", "root", "", "goodfaith_db")
            cursor = con.cursor()  # to execute our sql
            sql = "INSERT INTO `tblpayments`(`regno`, `amount`) VALUES (%s,%s)"
            data = (regno, amount)
            cursor.execute(sql, data)
            con.commit()
            return render_template("payments.html", msg1="Payment Made Successfully")
    else:
        return render_template('payments.html')

@app.route('/marks', methods=['GET', 'POST'])
def marks():
    if request.method == "POST":  # this checks the method used
        regno = request.form['regno']
        term_1 = request.form['term_1']
        term_2 = request.form['term_2']
        term_3 = request.form['term_3']

        if regno == "" :
            return render_template("marks.html", msg="Check above field!")
        else:
            con = pymysql.connect("localhost", "root", "", "goodfaith_db")
            cursor = con.cursor()  # to execute our sql
            sql = "INSERT INTO `tblmarks`(`regno`, `term_1`, `term_2`, `term_3`) VALUES (%s,%s,%s,%s)"
            data = (regno, term_1, term_2, term_3 )
            cursor.execute(sql, data)
            con.commit()
            return render_template("marks.html", msg1="Marks Updated Successfully")
    else:
        return render_template('marks.html')


@app.route('/sstudents', methods=['GET', 'POST'])
def sstudents():
    if request.method =='POST':
       regno = request.form['regno']
       if regno == '':
         return render_template('search_student.html', msg = 'Enter Reg No.!!!')

       else:
            con = pymysql.connect('localhost', 'root','', 'goodfaith_db')
            cursor = con.cursor()
            sql = 'SELECT * FROM tblstudents WHERE regno=%s'
            data = (regno)
            cursor.execute(sql, data)
            if cursor.rowcount < 1:
                return render_template('search_student.html', msg1 = 'Student not Found!!')
            else:
             results = cursor.fetchall()
            return render_template('search_student.html', results = results)
    else:
          return render_template('search_student.html')

@app.route('/spayments', methods=['GET', 'POST'])
def spayments():
    if request.method =='POST':
       regno = request.form['regno']
       if regno == '':
         return render_template('search_payment.html', msg = 'Enter Reg No.!!!')

       else:
            con = pymysql.connect('localhost', 'root','', 'goodfaith_db')
            cursor = con.cursor()
            sql = 'SELECT tblstudents.regno,tblstudents.surname, tblstudents.name,tblstudents.other,tblpayments.amount,(20000-amount) AS balance ' \
                  'FROM tblstudents ' \
                  'JOIN tblpayments ON ' \
                  'tblstudents.regno = tblpayments.regno ' \
                  'WHERE tblstudents.regno=%s'
            data = (regno)
            cursor.execute(sql,data)
            if cursor.rowcount < 1:
                return render_template('search_payment.html', msg1 = 'Student not Found!!')
            else:
             results = cursor.fetchall()
            return render_template('search_payment.html', results = results)
    else:
          return render_template('search_payment.html')


@app.route('/smarks', methods=['GET','POST'])
def smarks():
    if request.method =='POST':
       regno = request.form['regno']
       if regno == '':
         return render_template('search-marks.html', msg = 'Enter Reg No.!!!')

       else:
            con = pymysql.connect('localhost', 'root','', 'goodfaith_db')
            cursor = con.cursor()
            sql = 'SELECT tblstudents.regno,tblstudents.surname, tblstudents.name,tblstudents.other,tblmarks.term_1, tblmarks.term_2, tblmarks.term_3 ' \
                  'FROM tblstudents ' \
                  'JOIN tblmarks ON ' \
                  'tblstudents.regno = tblmarks.regno ' \
                  'WHERE tblstudents.regno=%s'
            data = (regno)
            cursor.execute(sql,data)
            if cursor.rowcount < 1:
                return render_template('search-marks.html', msg1 = 'Student not Found!!')
            else:
             results = cursor.fetchall()
            return render_template('search-marks.html', results = results)
    else:
          return render_template('search-marks.html')

@app.route('/graph')

def graph():
    return """
        <html>
            <body>
               
                 <Embed type='image/svg+xml' src='/bar' style='max-width:1000px'>
                 <Embed type='image/svg+xml' src='/bar2' style='max-width:1000px'>
            </body>
        </html>
        """

#@app.route('/line')
#def lgraph():
  #  lgraph = pygal.Line()
  #  lgraph.title = 'Evolution of Programming Languages Overtime'
  #  lgraph.x_labels = map(str, range(2004,2010))
  #  lgraph.add('Python', [12, 23, 45, 78, 97])
   # lgraph.add('Java', [13, 34, 45, 67, 76])
   # lgraph.add('C++', [32, 45, 56, 33, 34])
   # lgraph.add('Others', [12, 45, 56, 78, 79])
   # return Response (response= lgraph.render(), content_type= "image/svg+xml")

@app.route('/bar')
def bar():
    bgraph = pygal.Bar()
    con = pymysql.connect("localhost", "root", "", "goodfaith_db")
    cursor = con.cursor()
    sql = "SELECT tblstudents.name,tblpayments.amount, 20000-amount as Balance FROM tblstudents JOIN tblpayments ON tblstudents.regno = tblpayments.regno"

    cursor.execute(sql)
    results = cursor.fetchall()
    x = []
    y = []
    z = []

    for row in results:
        x.append(row[0])
        y.append(row[1])
        z.append(row[2])

    bgraph.title = "Student Salaries"
    bgraph.x_labels = (map(str, x))
    bgraph.add('Amount Paid', y)
    bgraph.add('Balance', z)

    return Response(response=bgraph.render(), content_type="image/svg+xml")

# @app.route('/bar2')
# def bar2():
#     b2graph = pygal.Bar()
#     con = pymysql.connect("localhost", "root", "", "goodfaith_db")
#     cursor = con.cursor()
#     sql = "SELECT tblstudents.name, tblstudents.surname,tblstudents.other, (tblmarks.term_1 + tblmarks.term_2 + tblmarks.term_3)/3 as mean_grade FROM tblstudents JOIN tblmarks ON tblstudents.regno = tblmarks.regno  where class = 'Class 1'"
#
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     x = []
#     y = []
#     z = []
#
#     for row in results:
#         x.append(row[3])
#         y.append(row[0])
#         z.append(row[3])
#
#     b2graph.title = "Class 1 Students Mean Grade "
#     b2graph.x_labels = (map(str, y))
#     b2graph.add('Mean Grade', x)
#     b2graph.add('Class Mean', sum(z)/5)
#
#     return Response(response=b2graph.render(), content_type="image/svg+xml")


if __name__ == '__main__':
  app.run()
