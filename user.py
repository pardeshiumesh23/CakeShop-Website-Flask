from flask import request,redirect,render_template,session
import mysql.connector
from datetime import datetime
def homepage():
    con=mysql.connector.connect(host="localhost", username="root", database="cakeshopDB")
    cursor=con.cursor()
    sql='select * from Category'
    cursor.execute(sql)
    cats=cursor.fetchall()
    sql='select * from Cake'
    cursor.execute(sql)
    cakes=cursor.fetchall()
    return render_template("user/userHome.html",cats=cats,cakes=cakes)

def ShowCakes(cid):
    con=mysql.connector.connect(host="localhost", username="root", database="cakeshopDB")   
    cursor=con.cursor()
    if request.method=="GET": 
        sql='select * from Category'
        cursor.execute(sql)
        cats=cursor.fetchall()    
        
        sql="select * from Cake where cid=%s"
        val=(cid,)
        cursor.execute(sql,val)     
        cakes=cursor.fetchall()     
        
        sql="select cname from Category where cid=%s"
        val=(cid,)
        cursor.execute(sql,val)
        catname=cursor.fetchone()[0]
        return render_template("user/userHome.html",cats=cats,cakes=cakes,catname=catname)
    
def ViewDetails(cakeid): #name of the parameter should be same as in url section 
    con=mysql.connector.connect(host="localhost", username="root", database="cakeshopDB")
    cursor=con.cursor()
    if request.method=="GET":
        sql='select * from Category'
        cursor.execute(sql)
        cats=cursor.fetchall()    
        
        sql="select * from cake_cat_vw where cake_id=%s"
        val=(cakeid,)
        cursor.execute(sql,val)
        cake=cursor.fetchone()
        return render_template("user/ViewDetails.html",cats=cats,cake=cake)
    
    else:
        if "uname" in session:
            uname=session["uname"]
            cake_id=request.form["cid"]
            qty=request.form["qty"]
            sql="insert into mycart (cake_id,qty,status,username) values(%s,%s,%s,%s)"
            val=(cake_id,qty,'cart  ',uname)
            cursor.execute(sql,val)
            con.commit()
            return redirect("/ShowCart")
        else:
            return redirect("/login")

    
def register():
    con=mysql.connector.connect(host="localhost", username="root", database="cakeshopDB")
    cursor=con.cursor()
    if request.method=="GET":
        sql='select * from Category'
        cursor.execute(sql)
        cats=cursor.fetchall()   
        return render_template("user/register.html",cats)
    else:
        uname=request.form["uname"]
        pwd=request.form["pwd"]
        email=request.form["email"]
        sql='insert into userinfo values (%s,%s,%s)'
        val=(uname,pwd,email)
        try:
            cursor.execute(sql,val)
            con.commit()
            return redirect("/")
        except:
            return redirect("/register")
        
def login():
    con=mysql.connector.connect(host="localhost", username="root", database="cakeshopDB")
    cursor=con.cursor()
    if request.method=="GET":
        sql='select * from Category'
        cursor.execute(sql)
        cats=cursor.fetchall()   
        return render_template("user/login.html",cats=cats)
    else: 
        uname=request.form["uname"]
        pwd=request.form["pwd"]
        sql='select count(*) from userinfo where username=%s and password=%s'
        val=(uname,pwd)
        cursor.execute(sql,val)
        count=int(cursor.fetchone()[0])
        if count== 1:
            session["uname"]=uname
            return redirect("/")
        else:
            return redirect("/login")
        
def logout():
    session.clear()
    return redirect("/")

def ShowCart():
    con=mysql.connector.connect(host="localhost", username="root", database="cakeshopDB")
    cursor=con.cursor()
    if request.method=="GET":
        if "uname" in session:
            sql='select * from Category'
            cursor.execute(sql)
            cats=cursor.fetchall()   
            sql="select * from cart_vw where username=%s"
            val=(session["uname"],)
            cursor.execute(sql,val) 
            items=cursor.fetchall()

            sql='select sum(subtotal) from cart_vw where username = %s'
            cursor.execute(sql,val)
            total=cursor.fetchone()[0]
            session["total"] = total
            return render_template("user/ShowCart.html",items=items,total=total,cats=cats)
        
        else:
            return redirect("/login")
    else:
        action=request.form["action"]
        cart_id=request.form["cart_id"]
        if action == "edit":
            qty=request.form["qty"]    
            sql='update mycart set qty=%s where cart_id=%s'
            val=(qty,cart_id)
            cursor.execute(sql,val)
            con.commit()
        else:
            sql="delete from mycart where cart_id=%s"
            val=(cart_id,)
            cursor.execute(sql,val)
            con.commit()
        return redirect("/ShowCart")

def MakePayment():
    if request.method=="GET":
        return render_template("user/MakePayment.html")
    else:
        card_no=request.form["card_no"]
        cvv=request.form["cvv"]
        expiry=request.form["expiry"]
        con=mysql.connector.connect(host="localhost", username="root", database="cakeshopDB")
        cursor=con.cursor()
        sql='select count(*) from Payment where cardno=%s and cvv=%s and expiry=%s'
        val=(card_no,cvv,expiry)
        cursor.execute(sql,val)
        count=int(cursor.fetchone()[0])
        if count==1:
            sql1='update Payment set balance=balance+%s where cardno=%s'
            val1=(session['total'],'111')
            sql2='update Payment set balance=balance-%s where cardno=%s'
            val2=(session['total'],card_no)
            cursor.execute(sql1,val1)
            cursor.execute(sql2,val2)
            # Update cart status to 'order'
            # sql="update mycart set status='order' where username=%s"
            # val=(session['uname'],)
            # cursor.execute(sql,val)
            # con.commit()

            sql="insert into order_master (date_of_order,amount,username) values (%s,%s,%s)"
            val=(datetime.now(),session['total'],session['uname'])
            cursor.execute(sql,val)
            con.commit()

            dd=datetime.today().strftime('%Y-%m-%d') #strftime means string format time
            sql="select oid from order_master where date_of_order=%s and amount=%s and username=%s"
            val=(dd,session['total'],session['uname'])
            print(val)
            cursor.execute(sql,val)
            oid=cursor.fetchone()[0]            
            sql="update mycart set status='order',order_id=%s  where status='cart' and username=%s" 
            val=(oid,session["uname"])
            cursor.execute(sql,val)
            con.commit()
            return redirect("/")
            
        else:
            return redirect("/MakePayment")
      
def ShowOrder():
    con=mysql.connector.connect(host="localhost", username="root", database="cakeshopDB")
    cursor=con.cursor()
    sql="select * from order_vw where username=%s"
    val=(session["uname"],)
    cursor.execute(sql,val)
    order_details=cursor.fetchall()

    sql="select * from order_master where username=%s"
    val=(session["uname"],)
    cursor.execute(sql,val)
    order=cursor.fetchall()

    sql='select * from Category'
    cursor.execute(sql)
    cats=cursor.fetchall()
    return render_template("user/ShowOrder.html",order=order,order_details=order_details,cats=cats)
