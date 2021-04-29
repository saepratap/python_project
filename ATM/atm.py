from flask import Flask,render_template,request,jsonify,json,redirect,url_for;
import pymongo


app = Flask(__name__)

obj = pymongo.MongoClient();
#print("obj:",obj)
mydb = obj["AccountDetailsDB"]
testcol = mydb["CustomerAccountColl"]
#print(mydb.testdata.find({"name":"John"}))
#mydict = { "Account_Number": "1212-1111-1414-1001", "Account_id": 1001,"Customer_id":"2001","Customer_Name":"Mahesh","Cust_Contact_Num":7050581987,"PIN":1213,"Min_Amt":1000,"Amt_Due_Remaining":120000,"Account_Type":"Savings","last_update_date":"2020 June 02" }
#print(mydb.testcol.count({"Account_Number":"1212-1111-1414-1000"}))
#x = testcol.insert_one(mydict)
#print("Collection:",x)

print("databases list...",obj.list_database_names())
#print("Collections list...",obj.list_collection_names())
collist = mydb.list_collection_names()
if "CustomerAccountColl" in collist:
  print("The collection exists.")
#x = testcol.find_one({"Account_Number":"1212-1111-1414-1000"})
#print(x)


@app.route("/")
def index():
    return render_template("atm.html")

@app.route("/",methods=['GET','POST'])
def main():
    global cnumber1
    cnumber = request.form["fname"]
    cnumber1 = cnumber
    print("cnumber1",cnumber1)
    x = testcol.count({"Account_Number":cnumber1})
    print("x:",x)
    if x == 1:
        return redirect(url_for("index_login"))
    elif x > 1:
        return "duplicates."
    else:
        return "Validation failed."

@app.route("/login")
def index_login():
    return render_template("login.html")

@app.route("/login",methods=['GET','POST'])
def login():
    global cpin
    try:
        cpin = int(request.form["fpin"])
        x = testcol.find_one({"Account_Number":cnumber1})
        print("Pin Value is ",x)
        if x["PIN"]==cpin:
            return redirect(url_for("index_selection"))
    except Exception as e:
        print("Err",e)
    else:
        return "Not Valid PIN"


@app.route("/selection")
def index_selection():
    return render_template("selection.html")

@app.route("/Balance")
def balance():
    x = testcol.find_one({"Account_Number":cnumber1})
    global Amount
    Amount = x["Amt_Due_Remaining"]
    Cust_Name = x["Customer_Name"]
    pin_num =x["PIN"]
    if pin_num == int(cpin):
        return "Hey "+Cust_Name+" the Amount Balance in ur Account is :"+str(Amount)


@app.route("/Withdraw")
def Withdraw():
    return render_template("withdraw.html")

@app.route("/Withdraw",methods=['GET','POST'])
def Withdraw_amt():
    amt = request.form["bal"]
    x = testcol.find_one({"Account_Number":cnumber1})
    balance_rem = x["Amt_Due_Remaining"]
    if abs(balance_rem - int(amt)) <= 1000:
        return "ur not allow to withdraw entire amount."
    elif balance_rem < int(amt):
        return "u dont have enough amount to withdraw"
    elif balance_rem - int(amt) > 1000:
        Amount = balance_rem - int(amt)
        testcol.update_one({"Account_Number":cnumber1},{"$set":{"Amt_Due_Remaining":Amount}})
        print("Amount:",Amount)
        x = testcol.find_one({"Account_Number":cnumber1})
        print("details",x)
        return "balance Available after withdraw is : "+str(Amount)

@app.route("/Phone")
def ChangePhoneNo_cmob():
    return render_template("Phone.html")

@app.route("/Phone",methods=['GET','POST'])
def ChangePhoneNo():
    x = testcol.find_one({"Account_Number":cnumber1})
    phone_num = int(x["Cust_Contact_Num"])
    pin_num = int(x["PIN"])
    oldmobnum = int(request.form["omobno"])
    newmobnum = int(request.form["nmobno"])
    conformmobno = int(request.form["cnmobno"])
    pin_num_val = int(request.form["cpin"])
    print("Conform:",conformmobno)
    print("MObile Number:",phone_num)
    if pin_num == pin_num_val:
        if phone_num ==oldmobnum:
            if newmobnum != phone_num:
                if newmobnum == conformmobno:
                    try:
                        testcol.update_one({"Account_Number":cnumber1},{"$set":{"Cust_Contact_Num":conformmobno}})
                    except Exception as e:
                        print("User Exception : ",e)
                else:
                    return "Conformation Contact Num and the New Contact Num are not Matching"
            else:
                return "Old and new Contact Numbers should not be same"
        else:
            return "Contact u entered is incorrect and ur not allowed to Change the Contact Number.."
    else:
        return "Not a Valid PIN"

    print(oldmobnum,newmobnum,conformmobno)
    return "Mobile Number Changed...."
    #return render_template("Phone.html")

@app.route("/ChangePIN")
def ChangePIN_cpin():
    return render_template("Pinchange.html")

@app.route("/ChangePIN",methods=['GET','POST'])
def ChangePIN():
    x = testcol.find_one({"Account_Number":cnumber1})
    pin_num = int(x["PIN"])
    oldpin = int(request.form["opin"])
    newpin = int(request.form["npin"])
    conformpin = int(request.form["cpin"])
    print("Conform:",conformpin)
    if pin_num ==oldpin:
        if newpin != pin_num:
            if newpin == conformpin:
                try:
                    testcol.update_one({"Account_Number":cnumber1},{"$set":{"PIN":conformpin}})
                except Exception as e:
                    print("User Exception : ",e)
            else:
                return "Conformation PIN and the New PIN are not Matching"
        else:
            return "Old and new PIN Number should not be same"
    else:
        return "PIN u entered is incorrect and ur not allowed to Change the PIN.."

    print(oldpin,newpin,conformpin)
    return "Amount Balance in ur Account"

app.run(port=5010)

#https://www.youtube.com/watch?v=lUCmVNGs5gw
#https://www.youtube.com/watch?v=AEM8_4NBU04
