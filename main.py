import cx_Oracle
import os
import logging
from configparser import ConfigParser
from flask import Flask,render_template,request


LOCATION = r"C:\Oracle\instantclient_12_1"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]
logging.basicConfig(level=logging.DEBUG)
config = ConfigParser()
config.read(r'.\venv\config.ini')


def databaseConn(instance):
    try:
        user = config['password']['USER']
        password = config['password'][instance]
        database = config['host'][instance]
        # logging.debug(password,user,database)
        #print("-->",user,password,database)
        con = cx_Oracle.connect(user, password, database)
    except Exception as e:
        print("Error is :",e)
    return con

def compassfd(re2,re4,re5,res6,res7,res8,res9,res10,rec11,res12,res13,res14,res15,cursor):
    num = cursor.execute("""select batchid_update.NEXTVAL from dual""")
    for i in num:
        val = i
    actval = str(val[0])
    seq = "TE" + actval
    cursor.execute("""insert into xxsa.xxsa_stg_batch_header(batch_id,business_segment,bu_id,total_credit,total_debit,total_trxns,batch_date,status,provider,currency,
                                    div_num,creation_date,CREATED_BY,LAST_UPDATE_DATE,LAST_UPDATE_BY)
                                    values(:Batchid,:BS,:BID,:TC,:TD,:TND,sysdate,'NEW',:prov,:CUR,:DIVNO,sysdate,-1,sysdate,-1)""",
                                    Batchid=seq,BS=re2,BID=re5,TC=res6,TD=res7,TND=res8,prov=re4,CUR=res9,DIVNO=res10)
    if res15 == 'CAPTURE':
        amt = res6
    elif res15 == 'REFUND':
        amt = res7

    cursor.execute("""insert into xxsa.xxsa_stg_batch_details(SA_TRANSACTION_ID,BATCH_ID,PROVIDER_NAME,ORDER_CODE,CARD_TYPE,ORDER_NUMBER,INVOICE_NUMBER,BU_ID,BUSINESS_SEGMENT,
                      SALES_CHANNEL,CURRENCY,TRXN_TYPE,DEMAND_AMOUNT,RECEIVED_AMOUNT,STATUS,BATCH_DATE,DIV_NUM,TRXN_STATUS,CREATion_DATE,CREATED_BY,
                      LAST_UPDATE_DATE,ATTRIBUTE5,ATTRIBUTE6,ATTRIBUTE3) values(:satrxid,:Batchid,:prov,:OC,:CT,:ONo,:TNum,:BID,:BS,:SC,:CUR,:TType,:DAmt,:RAmt,'NEW',sysdate,
                      :DIVNO,'SUCCESS',sysdate,-1,sysdate,to_char(sysdate,'MM/DD/YYYY'),to_char(sysdate,'DDMMYYYY')||'FD','Credit/Deb.Card')""",
                   satrxid=actval,Batchid=seq,prov=re4,OC=rec11,CT=res12,ONo=res13,TNum=res14,BID=re5,BS=re2,SC=re2,CUR=res9,TType=res15,DAmt=amt,RAmt=amt,DIVNO=res10)

    print("Inserted....CC.....")
    return seq

def paypal(re2,re4,re5,res6,res7,res8,res9,rec11,res12,res13,res14,res15,cursor):
    num = cursor.execute("""select batchid_update.NEXTVAL from dual""")
    print("sales_channel:",re2)
    for i in num:
        val = i
    actval = str(val[0])
    seq = "PP" + actval
    cursor.execute("""insert into xxsa.xxsa_stg_batch_header(batch_id,bu_id,total_credit,total_debit,total_trxns,batch_date,status,provider,currency,
                                        div_num,creation_date,CREATED_BY,LAST_UPDATE_DATE,LAST_UPDATE_BY)
                                        values(:Batchid,:BID,:TC,:TD,:TND,sysdate,'NEW',:prov,:CUR,:DIVNO,sysdate,-1,sysdate,-1)""",
                   Batchid=seq, BID=re5, TC=res6, TD=res7, TND=res8, prov=re4, CUR=res9, DIVNO=re2)
    if res15 == 'CAPTURE':
        amt = res6
    elif res15 == 'REFUND':
        amt = res7

    cursor.execute("""insert into xxsa.xxsa_stg_batch_details(SA_TRANSACTION_ID,BATCH_ID,PROVIDER_NAME,ORDER_CODE,CARD_TYPE,ORDER_NUMBER,INVOICE_NUMBER,BU_ID,
                      SALES_CHANNEL,CURRENCY,TRXN_TYPE,DEMAND_AMOUNT,RECEIVED_AMOUNT,STATUS,BATCH_DATE,DIV_NUM,TRXN_STATUS,CREATion_DATE,CREATED_BY,
                      LAST_UPDATE_DATE,ATTRIBUTE5,ATTRIBUTE6,ATTRIBUTE3) values(:satrxid,:Batchid,:prov,:OC,:CT,:ONo,:TNum,:BID,:SC,:CUR,:TType,:DAmt,:RAmt,'NEW',sysdate,
                      :DIVNO,'SUCCESS',sysdate,-1,sysdate,sysdate,sysdate,'PayPal')""",
                   satrxid=actval,Batchid=seq,prov=re4,OC=rec11,CT=res12,ONo=res13,TNum=res14,BID=re5,SC=re2,CUR=res9,TType=res15,DAmt=amt,RAmt=amt,DIVNO=re2)

    print("Inserted...PayPal......")
    return seq

def trustly():
    return "TRUSTLY"

def cbcbr(res12,res13,res14,res15,res16,res17,res18,res19,res20,cursor):
    print("I m Here..")
    print("response :", res12, res13, res14, res15, res16, res17, res18, res19, res20)
    try:
        num1 = cursor.execute("""select batchid_update.NEXTVAL from dual""")
        print("Value :",num1)
    except Exception as e:
        print("Error :",e)
    for i in num1:
        val = i
    actval = str(val[0])
    seq = "1." + actval
    cursor.execute("""insert into xxsa.XXSA_STG_CB_HDR(batch_id,report_Date_from,report_date_to,report_generation_date,dfr_file_name,creation_Date,created_by,last_update_date,
                      last_updated_by,status,payment_type,record_count,record_type,org_id) values(:Batchid,sysdate,sysdate,sysdate,'FD.DFM.AU.TEST.01052020.CB.LS - test.txt',sysdate,
                      '-1',sysdate,'-1','NEW',:prov,1,'CHARGEBACKS',:org_id)""",Batchid=seq,prov='CompassFD',org_id=529)


    cursor.execute("""insert into xxsa.XXSA_STG_CB_LINE(batch_id,record_id,record_type,entity_number,presentment_currency,sequence_number,merchant_order_code,
                      mop_code,chargeback_amount,status,creation_Date,created_by,last_update_date,last_updated_by,reference_number,org_id,attribute5,attribute6)
                      values(:Batchid,:record_id,'CHARGEBACK',:MID,:CURR,1,'ABX3TXAWM35','VI',-10,'NEW',sysdate,-1,sysdate,-1,910015258,389,'01/05/2021','05012021FD')""",
                      Batchid=seq,record_id=actval,MID='311177132884',CURR='USD',)

    print("Inserted....CC.....")
    return seq


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/",methods=['POST','GET'])
def home():
    if request.method =='POST':
        #res2 = request.form.get("resp2")
        res3 = request.form.get("insta")                       # get the value for the instance
        res4 = request.form.get("provider")                    # get the value for the provider
        res5 = request.form.get("country")
        res2 = request.form.get("resp2")
        res6 = request.form.get("Credit")
        res7 = request.form.get("Debit")
        res8 = request.form.get("lines")
        res9 = request.form.get("curr")
        res10 = request.form.get("dno")
        res11 = request.form.get("OCode")
        res12 = request.form.get("CType")
        res13 = request.form.get("ONo")
        res14 = request.form.get("TNo")
        res15 = request.form.get("trxStatus")
        res16 = request.form.get("flow")
        print("response :",res2,res3,res4,res5,res16)
        con = databaseConn(res3)
        cursor = con.cursor()
        if res4 in ('CompassFD','Amex'):
            data = compassfd(res2,res4,res5,res6,res7,res8,res9,res10,res11,res12,res13,res14,res15,cursor)
            con.commit()
        elif res4 == 'PAYPAL':
            data = paypal(res2,res4,res5,res6,res7,res8,res9,res11,res12,res13,res14,res15,cursor)
            #con.commit()
        elif res4 == 'TRUSTLY':
            data = trustly()
        else:
            data = "Nothing selected for Provider"
        print("selected provider is :",data)
        return "Done"

@app.route("/CBCBR")
def IndexCB():
    return render_template('CBCBR.html')

@app.route("/CBCBR",methods=['POST','GET'])
def HomeCB():
    if request.method == 'POST':
        #res2 = request.form.get("resp2")
        res11 = request.form.get("insta")  # get the value for the instance
        res12 = request.form.get("provider")  # get the value for the provider
        res13 = request.form.get("country")
        res14 = request.form.get("Debit")
        res15 = request.form.get("curr")
        res16 = request.form.get("mid")
        res17 = request.form.get("OCode")
        res18 = request.form.get("mop")
        res19 = request.form.get("refno")
        res20 = request.form.get("trxStatus")
        print("response :",res11,res12, res13, res14, res15, res16,res17, res18, res19, res20)
        con1 = databaseConn(res11)
        cursor = con1.cursor()
        if res12 in ('CompassFD', 'Amex'):
            num = cbcbr(res12,res13,res14,res15,res16,res17,res18,res19,res20,cursor)
            print("Inserted and the batch_id is : {}:".format(num))
            con1.commit()
        return "None"

if __name__ == '__main__':
    app.run(debug=True)