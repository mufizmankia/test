from flask import *
import pymysql


app = Flask(__name__)

def main_data():
    connection = pymysql.connect(
        host ="localhost",
        user = "root",
        password = "root",
        db ='mysql',
        cursorclass = pymysql.cursors.DictCursor
    )
    return connection

@app.route('/')
def load_page():
    return render_template("register.html")

@app.route('/register',methods=['POST'])
def insert_data():
    first_name= request.form.get("firstName")
    last_name = request.form.get("lastName")
    user_name = request.form.get("userName")
    password = request.form.get("password")
    address = request.form.get("address")
    country = request.form.get("country")
    gender = request.form.get('gender')
    hobbies = request.form.getlist("hobbies")
    hobbies = ",".join(hobbies)
    connection = main_data()
    cursor1 = connection.cursor()
    cursor1.execute("INSERT INTO contacts(firstName,lastName,userName,password,address,country,gender,hobbies) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(first_name,last_name,user_name,password,address,country,gender,hobbies )
                    )
    # data = cursor1.fetchall()
    connection.commit()
    cursor1.close()
    return redirect(url_for('view_data'))

@app.route("/view",methods=["GET","POST"])
def view_data():

    connection = main_data()
    cursor2 = connection.cursor()
    cursor2.execute("SELECT * FROM contacts ")
    data = cursor2.fetchall()
    print(data)
    print(type(data))
    cursor2.close()
    connection.close()
    return render_template("view.html", data = data)

@app.route("/delete_data",methods=["GET","POST"])
def delete_data():
    connection = main_data()
    cursor3 = connection.cursor()
    user_id = request.args.get('did')
    cursor3.execute("DELETE FROM contacts WHERE registrationId ='{}'".format(user_id))
    connection.commit()
    cursor3.close()
    connection.close()
    print("done")
    return redirect (url_for('view_data'))
@app.route("/edit_data",methods=["GET","POST"])
def edit_data():
        connection = main_data()
        cursor4= connection.cursor()
        user_id = request.args.get('eid')
        cursor4.execute("SELECT * FROM contacts WHERE registrationId='{}'".format(user_id))
        data = cursor4.fetchall()
        connection.commit()
        return render_template('update_data.html', data =data)
@app.route("/update_data", methods=['GET','POST'])
def update_data():
        connection = main_data()
        registration_id = request.form.get("eid")
        new_first_name= request.form.get("new_first_name")
        new_last_name = request.form.get("new_last_name")
        new_user_name = request.form.get("new_user_name")
        new_password = request.form.get("new_password")
        new_address = request.form.get("new_address")
        new_country = request.form.get("new_country")
        new_gender = request.form.get('new_gender')
        new_hobbies = request.form.getlist("new_hobbies")
        new_hobbies = ",".join(new_hobbies)
        cursor5 = connection.cursor()
        cursor5.execute("UPDATE contacts SET  firstName='{}', lastName='{}', userName='{}', password ='{}', address='{}', gender='{}', country='{}', hobbies='{}' WHERE registrationId='{}'".format(
                        new_first_name,new_last_name,new_user_name,new_password,new_address,new_gender,new_country,new_hobbies,registration_id))
        new_data = cursor5.fetchall()
        print(new_data)
        connection.commit()
        cursor5.close()
        connection.close()
        return redirect('/view')
if __name__ == '__main__':
   app.run(threaded = True,debug= True, host='localhost')
