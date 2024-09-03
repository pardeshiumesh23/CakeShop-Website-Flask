# from main import app
from flask import render_template,request,redirect
import mysql.connector

def showAllCategories():
    con=mysql.connector.connect(host="localhost", username="root",password="pass123",database="cakeshopDB")
    cursor=con.cursor()
    sql='select * from Category'
    cursor.execute(sql)
    cats=cursor.fetchall()
    return render_template("Category/showAllCategories.html",cats=cats)

def addCategory():
    if request.method=="GET":
        return render_template("Category/addCategory.html")
    else:
        con=mysql.connector.connect(host="localhost", username="root",password="pass123",database="cakeshopDB")
        cursor=con.cursor()
        sql='insert into Category (cname) values (%s)'  
        val=(request.form["cname"],)
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showAllCategories")
    
def deleteCategory(cid):
    if request.method=="GET":
        return render_template("Category/deleteCategory.html")
    else:
        action= request.form["action"]
        if action=="Yes":
            con=mysql.connector.connect(host="localhost", username="root",password="pass123",database="cakeshopDB")
            cursor=con.cursor()
            sql='delete from Category where cid=%s'
            val=(cid,)
            cursor.execute(sql,val)
            con.commit()
        return redirect("/showAllCategories")
        
def editcategory(cid):
    con=mysql.connector.connect(host="localhost", username="root",password="pass123",database="cakeshopDB")
    cursor=con.cursor()
    if request.method=="GET":
        sql='select * from Category where cid=%s'
        val=(cid,)
        cursor.execute(sql,val)
        cats=cursor.fetchone()
        return render_template("Category/editCategory.html",cats=cats)
    else:
        cname=request.form["cname"]
        sql="update Category set cname=%s where cid=%s"
        val=(cname,cid)
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showAllCategories")
    

