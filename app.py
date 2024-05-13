import flask
import pymysql 

app = flask.Flask(__name__)

app.secret_key="hjgjhgfdhgf"

@app.route('/')
def role():
    

    return flask.render_template('first.html')


@app.route('/home')
def home():
    

    return flask.render_template('home.html')




import hashlib

def hash_password_salt(password):
    salt = "QW66HJk(994634vv)"
    salted_password = salt + password
    md5_hasher = hashlib.md5()
    md5_hasher.update(salted_password.encode('utf-8'))
    hashed_password = md5_hasher.hexdigest()
    return hashed_password

def verify_password_salt(hashed_password, input_password):
    salt = "QW66HJk(994634vv)"
    salted_input_password = salt + input_password
    hashed_input_password = hashlib.md5(salted_input_password.encode('utf-8')).hexdigest()
    return hashed_password == hashed_input_password

# # Upload employee route
@app.route('/register', methods=['POST', 'GET'])
def register():
    if flask.request.method == 'POST':
        full_name = flask.request.form["full_name"]
        username = flask.request.form["username"]
        email = flask.request.form["email"]
        phone = flask.request.form["phone"]
        department = flask.request.form["department"]
        password = flask.request.form["password"]

        # Hash the password before storing
        hashed_password = hash_password_salt(password)

        connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
        cursor = connection.cursor()
        data = (full_name, username, email, phone, department, hashed_password)
        
        if password != flask.request.form["password"]:
            return flask.render_template('signup.html', error='Passwords do not match')
        elif len(password) < 8:
            return flask.render_template('signup.html', error='Password must be at least 8 characters long')
        else:
            sql = "INSERT INTO employees (full_name, username, email, phone, department, password) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, data)
            connection.commit()
            return flask.render_template("signup.html", message="Registered Successfully")
    else:
        return flask.render_template("signup.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html', message='Please Enter Information')
    elif flask.request.method == 'POST':
        username = flask.request.form["username"]
        password = flask.request.form["password"]

        connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
        cursor = connection.cursor()
        data = (username)

        sql = "SELECT * FROM employees WHERE username = %s"
        cursor.execute(sql, data)

        if cursor.rowcount == 0:
            return flask.render_template('login.html', Warning="Username dont exist")
        else:
            user = cursor.fetchone()
            stored_password = user[6]  # Assuming password is stored in the 7th column
            if verify_password_salt(stored_password, password):
                flask.session["key"] = user[2]
                flask.session["password"] = user[6]
                return flask.redirect('/taskDashboard')
            else:
                return flask.redirect('/taskDashboard', Warning="Invalid Credentials")

@app.route('/profile')
def profile():
    if 'username' in flask.session:
        user = {
            'username': flask.session['username'],
            'email': flask.session['email'],
            'full_name': flask.session['full_name']
        }
        return flask.render_template('profile.html', user=user)
    else:
        return flask.redirect('/profile')
    
    
#emp log out session
@app.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect('/')
            
    
@app.route('/taskDashboard')
def task():
    #step 1. DATABASE CONNECTION
    import pymysql
    connection = pymysql.connect(host='localhost', user='root', password='', database= 'task_Management_db')
    
    #step 2. cursor()->Added to the connection used to execute sql queries
    cursor = connection.cursor()
    
    #Fetch Products based on categories
    #1. tasks
    sql_tasks = "select * from task"
    cursor.execute(sql_tasks)
    data_task = cursor.fetchall()

    return flask.render_template('taskDashboard.html', task = data_task)

@app.route('/taskCreation', methods = ['POST', 'GET'])
def taskCreation():
    if flask.request.method == 'POST':
        # step 1. request data from the form
        task_name = flask.request.form["task_name"]
        task_desc = flask.request.form["task_desc"]
        start_date = flask.request.form["start_date"]
        due_date = flask.request.form["due_date"]
        status = flask.request.form["status"]
        attachment = flask.request.files["attachment"]
        
        #save img ->static/images/
        attachment.save('static/images/' + attachment.filename)
        
        
        #database connection
        import pymysql
        connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
        
        #create cursor(): to execute spl codes
        cursor = connection.cursor()
        data = (task_name, task_desc, start_date, due_date, status, attachment.filename)
        
        # sql query
        sql = "insert into task (task_name, task_desc, start_date, due_date, status, attachment) values (%s, %s, %s, %s, %s, %s)"
        
        #use cursor to execute sql then provide data on the placeholders
        cursor.execute(sql, data)
        
        #updating(committing) changes to the database
        connection.commit()
        
        #return success message
        return flask.render_template('taskCreation.html', message = 'Task uploaded Successfully')
        employees
    else:
        return flask.render_template('taskCreation.html', message = 'Input Task Details')


@app.route('/single/<task_id>')
def single(task_id):
    # step 1. Database connection
    import pymysql
    connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
    
    #step 2. Create a connection cursor():SQL Execute
    cursor = connection.cursor()
    
    # Write the sql Query
    sql = 'select * from task where task_id = %s'
    
    #Execute
    cursor.execute(sql, (task_id))
    data = cursor.fetchone()
    
    #Run server response
    return flask.render_template('test.html', single = data)

#task submission sql
@app.route('/submit', methods = ['POST', 'GET'])
def submit():
    if flask.request.method == 'POST':
        # step 1. request data from the form
        task_name = flask.request.form["task_name"]
        
        start_date = flask.request.form["start_date"]
        Completed_date = flask.request.form["Completed_date"]
        
        attachment = flask.request.files["attachment"]
        
        #save img ->static/images/
        attachment.save('static/images/' + attachment.filename)
        
        
        #database connection
        import pymysql
        connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
        
        #create cursor(): to execute spl codes
        cursor = connection.cursor()
        data = (task_name, start_date, Completed_date, attachment.filename)
        
        # sql query
        sql = "insert into task_done (task_name, start_date, Completed_date, attachment) values (%s, %s, %s, %s)"
        
        #use cursor to execute sql then provide data on the placeholders
        cursor.execute(sql, data)
        
        #updating(committing) changes to the database
        connection.commit()
        
        #return success message
        return flask.render_template('taskSubmission.html', message = 'Task uploaded Successfully')
        employees
    else:
        return flask.render_template('taskSubmission.html', message = 'Submit Task Info')




@app.route('/admin1', methods = ['POST', 'GET'])
def admin_signup():
    if flask.request.method == 'POST':
        # step 1. request data from the form
        name = flask.request.form["name"]
        username = flask.request.form["username"]
        email = flask.request.form["email"]
        phone = flask.request.form["phone"]        
        password = flask.request.form["password"]
        
        
        
        #Connect to the data base
        import pymysql
        connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
        
        #step 2. Create a connection cursor():SQL Execute
        cursor = connection.cursor()
        data = (name, username, email, phone, password)
        
        if password != password:
            return flask.render_template('/admin_signup.html', error='Password Dont Match')
        elif len(password) < 8:
            return flask.render_template('/admin_signup.html', error = 'Password is less than 8 Characters')
        
        
        
        else:
            sql = "insert into admin (name, username, email, phone, password) values (%s, %s, %s, %s, %s)"
            cursor.execute(sql, data)
            connection.commit()
            return flask.render_template("/admin_signup.html", message = "Registered Successfully")
    else:
        return flask.render_template("/admin_signup.html")
    
@app.route('/admin2', methods = ['POST', 'GET'])
def admin_login():
    if flask.request.method == 'GET':
        return flask.render_template('admin_login.html', message = 'Please Enter Information')
        
    elif flask.request.method == 'POST':
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        
        #Connect to the data base
        import pymysql
        connection = pymysql.connect(host='localhost', user='root', password='', database= 'task_Management_db')
        
        cursor = connection.cursor()
        data = (username, password)
        
        sql = "select * from admin where username = %s and password = %s"
        cursor.execute(sql, data)
        
        #make a decision
        #cursor.rowcount
        
        if cursor.rowcount == 0:
            return flask.redirect('/admin2') #Warning = "Invalid Credentials")
        
        else:
            # fetch info
            user = cursor.fetchone()
            flask.session["key"] = user[1]
            flask.session["password"] = user[4]
            return flask.redirect('/one')

@app.route('/error')
def error():
    

    return flask.render_template('error.html')


# total items
@app.route('/totalItems')
def total_items():
    # Step 1: DATABASE CONNECTION
    connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
    
    # Step 2: Create a cursor for executing SQL queries
    cursor = connection.cursor()
    
    # Fetch the total counts from each table
    counts = {}
    
    # Query for Admins count
    cursor.execute("SELECT COUNT(*) FROM admin")
    counts['admins'] = cursor.fetchone()[0]
    
    # Query for Employees count
    cursor.execute("SELECT COUNT(*) FROM employees")
    counts['employees'] = cursor.fetchone()[0]
    
    # Query for Tasks count
    cursor.execute("SELECT COUNT(*) FROM task")
    counts['tasks'] = cursor.fetchone()[0]
    
    # Query for Task_done count
    cursor.execute("SELECT COUNT(*) FROM task_done")
    counts['done'] = cursor.fetchone()[0]
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Pass counts dictionary to the template
    return flask.render_template('totalItems.html', counts=counts)



#updates (employees table)
# Database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'task_Management_db'

@app.route('/employees')
def employees_list():
    # Step 1: Database Connection
    connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
    
    # Step 2: Create a cursor for executing SQL queries
    cursor = connection.cursor()
    
    # Query to fetch all items from the employees table
    cursor.execute("SELECT * FROM employees")
    employees_data = cursor.fetchall()
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Pass employee data to the template
    return flask.render_template('employees.html', employees_data=employees_data)

@app.route('/update_employee/<int:employee_id>', methods=['POST'])
def update_employee(employee_id):
    if flask.request.method == 'POST':
        # Get form data
        full_name = flask.request.form["full_name"]
        username = flask.request.form["username"]
        email = flask.request.form["email"]
        phone = flask.request.form["phone"]
        department = flask.request.form["department"]
        password = flask.request.form["password"]
        
        # Update employee information in the database
        connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
        cursor = connection.cursor()
        update_query = "UPDATE employees SET full_name=%s, username=%s, email=%s, phone=%s, department=%s, password=%s WHERE id=%s"
        cursor.execute(update_query, (full_name, username, email, phone, department, password))
        connection.commit()
        cursor.close()
        connection.close()
        
        # Redirect to the employees list page
        return flask.redirect('/employees')

@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    if flask.request.method == 'POST':
        # Delete employee from the database
        connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
        cursor = connection.cursor()
        delete_query = "DELETE FROM employees WHERE id=%s"
        cursor.execute(delete_query, (employee_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        # Redirect to the employees list page
        return flask.redirect('/employees')
    
    
#tsk page(admin)
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'task_Management_db'

@app.route('/task')
def task_view():
    # Step 1: Database Connection
    connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
    
    # Step 2: Create a cursor for executing SQL queries
    cursor = connection.cursor()
    
    # Query to fetch all items from the employees table
    cursor.execute("SELECT * FROM task")
    task_data = cursor.fetchall()
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Pass task data to the template
    return flask.render_template('task.html', task_data=task_data)

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if flask.request.method == 'POST':
        # Get form data
        task_name = flask.request.form["task_name"]
        task_desc = flask.request.form["task_desc"]
        start_date = flask.request.form["start_date"]
        due_date = flask.request.form["due_date"]
        status = flask.request.form["status"]
        
        
        # Update task information in the database
        connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
        cursor = connection.cursor()
        update_query = "UPDATE task SET task_name=%s, task_desc=%s WHERE id=%s"
        cursor.execute(update_query, (task_name, task_desc, start_date, due_date, status))
        connection.commit()
        cursor.close()
        connection.close()
        
        # Redirect to the employees list page
        return flask.redirect('/task')

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if flask.request.method == 'POST':
        # Delete employee from the database
        connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
        cursor = connection.cursor()
        delete_query = "DELETE FROM task WHERE id=%s"
        cursor.execute(delete_query, (task_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        # Redirect to the employees list page
        return flask.redirect('/task')
    
@app.route('/done')
def done():
    # Step 1: Database Connection
    connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
    
    # Step 2: Create a cursor for executing SQL queries
    cursor = connection.cursor()
    
    # Query to fetch all items from the employees table
    cursor.execute("SELECT * FROM task_done")
    complete_data = cursor.fetchall()
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Pass task data to the template
    return flask.render_template('completed_task.html', complete_data=complete_data)

# admin dashboard
@app.route('/one')
def one():
    # Step 1: DATABASE CONNECTION
    connection = pymysql.connect(host='localhost', user='root', password='', database='task_Management_db')
    
    # Step 2: Create a cursor for executing SQL queries
    cursor = connection.cursor()
    
    # Fetch the total counts from each table
    counts = {}
    
    # Query for Admins count
    cursor.execute("SELECT COUNT(*) FROM admin")
    counts['admins'] = cursor.fetchone()[0]
    
    # Query for Employees count
    cursor.execute("SELECT COUNT(*) FROM employees")
    counts['employees'] = cursor.fetchone()[0]
    
    # Query for Tasks count
    cursor.execute("SELECT COUNT(*) FROM task")
    counts['tasks'] = cursor.fetchone()[0]
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Pass counts dictionary to the template
    return flask.render_template('admin.html', counts=counts)
    
@app.route('/about')
def about():
    return flask.render_template('about.html')



@app.route('/terms')
def terms():
    return flask.render_template('terms.html')





app.run(debug=True)



