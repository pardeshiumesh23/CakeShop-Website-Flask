from flask import render_template,request,redirect
import mysql.connector,os
from main import app
from werkzeug.utils import secure_filename
app.secret_key = 'supersecretkey'  # Needed for flash messages
def showAllCake():
    con=mysql.connector.connect(host="localhost", username="root",password="pass123",database="cakeshopDB")
    cursor=con.cursor()
    sql='select * from cake_cat_vw;'
    cursor.execute(sql)
    cakes=cursor.fetchall()
    return render_template("Cake/showAllCakes.html",cakes=cakes) 

def addCake():
    con=mysql.connector.connect(host="localhost", username="root",password="pass123",database="cakeshopDB")
    cursor=con.cursor()
    if request.method=="GET":
        sql="select * from Category"
        cursor.execute(sql)
        cats=cursor.fetchall()
        return render_template("Cake/addCake.html",cats=cats)
    else:
        cname=request.form["cname"]
        price=request.form["price"]
        description=request.form["description"]
        cid=request.form["cat"]
        f=request.files["image_url"]
        filename=secure_filename(f.filename)
        filename="static/Images/"+f.filename
        f.save(filename)
        filename="Images/"+f.filename
        
        sql='insert into Cake (cake_name,price,description,image_url,cid) values (%s,%s,%s,%s,%s)'
        val=(cname,price,description,filename,cid)
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showAllCakes")



def editCake(cake_id):
    con = mysql.connector.connect(host="localhost", username="root",password="pass123",database="cakeshopDB")
    cursor = con.cursor()
    
    if request.method == "GET":
        sql = "SELECT * FROM Cake WHERE cake_id=%s"
        val = (cake_id,)
        cursor.execute(sql, val)
        cake = cursor.fetchone()
        return render_template("Cake/editCake.html", cake=cake)
    else:
        cname = request.form["cname"]
        price = request.form["price"]
        description = request.form["description"]
        f = request.files["image_url"]
        
        # Ensure secure filename
        filename = secure_filename(f.filename)
        
        # Define the directory and file path
        directory = 'static/Images/'
        file_path = os.path.join(directory, filename)
        
        # Print debug information
        print(f"Filename: {filename}")
        print(f"File path: {file_path}")
        
        # Check if the directory exists
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            except Exception as e:
                print(f"Failed to create directory: {directory}")
                print(f"Error: {e}")
                flash(f"Error creating directory: {e}", "error")
                return redirect(request.url)
        else:
            print(f"Directory already exists: {directory}")
        
        # Save the file to the specified path
        try:
            f.save(file_path)
            print(f"File saved to: {file_path}")
        except IsADirectoryError as e:
            print(f"IsADirectoryError: {e}")
            flash(f"Error saving file: {e}", "error")
            return redirect(request.url)
        except Exception as e:
            print(f"Unexpected error: {e}")
            flash(f"Unexpected error: {e}", "error")
            return redirect(request.url)
        
        # Update the file path to be relative for storing in the database
        relative_file_path = "Images/" + filename
        
        sql = 'UPDATE Cake SET cake_name=%s, price=%s, image_url=%s, description=%s WHERE cake_id=%s'
        val = (cname, price, relative_file_path, description, cake_id)
        cursor.execute(sql, val)
        con.commit()
        
        return redirect("/showAllCakes")    

def deleteCake(cake_id):
    if request.method=="GET":
        return render_template("Cake/deleteCake.html")
    else:
        action=request.form["action"]
        if action=="Yes":
            con=mysql.connector.connect(host="localhost",username="root",password="pass123",database="cakeshopDB")
            cursor=con.cursor()
            sql="delete from Cake where cake_id=%s"
            val=(cake_id,)
            cursor.execute(sql,val)
            con.commit()
        return redirect("/showAllCakes")
  








