from flask import request,redirect,render_template,session
import mysql.connector

def adminlogin():
    if request.method== "GET":
        return render_template("Admin/adminlogin.html")
    else:
        uname=request.form["uname"]
        pwd=request.form["pwd"]
        sql='select count(*) from adminuser where username=%s and password=%s'
        val=(uname,pwd)
        con=mysql.connector.connect(host="localhost", username="root",password="pass123",database="cakeshopDB")
        cursor=con.cursor()
        cursor.execute(sql,val)
        count=cursor.fetchone()
        count=int(count[0])
        if count==1:
            session["uname"]=uname
            return redirect("/adminHome")
        else:
            return redirect("/adminlogin")
        
def adminHome():
    if "uname" in session:
        return render_template("Admin/adminHome.html")
    else:
        return redirect("/adminlogin")

def adminLogout():
    session.clear()
    return redirect("/adminlogin")