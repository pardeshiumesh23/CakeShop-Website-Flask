import category_op as cat
import cake_op as cake
from main import app
import admin
import user

app.add_url_rule("/showAllCategories",view_func=cat.showAllCategories)
app.add_url_rule("/addCategory",view_func=cat.addCategory,methods=["GET","POST"])
app.add_url_rule("/delete/<cid>",view_func=cat.deleteCategory,methods=["GET","POST"])
app.add_url_rule("/edit/<cid>",view_func=cat.editcategory,methods=["GET","POST"])
app.add_url_rule("/addCake",view_func=cake.addCake,methods=["GET","POST"])
app.add_url_rule("/showAllCakes",view_func=cake.showAllCake)
app.add_url_rule("/editCake/<cake_id>",view_func=cake.editCake,methods=["GET","POST"])
app.add_url_rule("/deleteCake/<cake_id>",view_func=cake.deleteCake,methods=["GET","POST"])
app.add_url_rule("/adminlogin",view_func=admin.adminlogin,methods=["GET","POST"])
app.add_url_rule("/adminHome",view_func=admin.adminHome)    
app.add_url_rule("/adminlogout",view_func=admin.adminLogout)
app.add_url_rule("/",view_func=user.homepage)
app.add_url_rule("/ShowCakes/<cid>",view_func=user.ShowCakes)
app.add_url_rule("/ViewDetails/<cakeid>",view_func=user.ViewDetails,methods=["GET","POST"])
app.add_url_rule("/register",view_func=user.register,methods=["GET","POST"])
app.add_url_rule("/login",view_func=user.login,methods=["GET","POST"])
app.add_url_rule("/logout",view_func=user.logout,methods=["GET","POST"])
app.add_url_rule("/ShowCart",view_func=user.ShowCart,methods=["GET","POST"])
app.add_url_rule("/MakePayment",view_func=user.MakePayment,methods=["GET","POST"])
app.add_url_rule("/ShowOrder",view_func=user.ShowOrder)