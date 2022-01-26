

import pyrebase as py
import pprint
import cv2
from base45 import b45decode
import cbor2
config = {
    'apiKey': "AIzaSyByJhZKkc9G0B-MrOOsnuDxIgUUELIEKyM",
  'authDomain': "covid19-e6bf1.firebaseapp.com",
  'databaseURL': "https://covid19-e6bf1-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "covid19-e6bf1",
  'storageBucket': "covid19-e6bf1.appspot.com",
  'messagingSenderId': "96661594726",
  'appId': "1:96661594726:web:d1dcb138c79bf3f4f1c3a7",
  'measurementId': "G-4QXVFPQ3PM"
}
fire = py.initialize_app(config)
auth = fire.auth()
ddbb = fire.database()


def conteo():

    qr_list = ddbb.child("CovidApp").get()
    moderna = 0
    janssen = 0
    pfizer = 0
    astra = 0
    
    for qr in qr_list.each(): ##RECORREMOS TODOS LOS QR QUE HAYA EN LA APP
        data = ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0/ma').get()
        
        if (data.val()) == 'ORG-100031184':
            moderna = moderna +1
            ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0').update({'ma':'Moderna'})
        if (data.val()) == 'ORG-100001699':
            astra = astra +1
            ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0').update({'ma':'Astra Zeneca'})
        if (data.val()) == 'ORG-100001417':
            janssen = janssen +1
            ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0').update({'ma':'Janssen'})
        if (data.val()) == 'ORG-100030215':
            pfizer = pfizer +1
            ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0').update({'ma':'Pfizer'})
        
        ##validamos los que ya estan dentro del programa para tener el conteo al tope
        if (data.val()) == 'Moderna':
            moderna = moderna +1
        if (data.val()) == 'Astra Zeneca':
            astra = astra +1
        if (data.val()) == 'Janssen':
            janssen = janssen +1
        if (data.val()) == 'Pfizer':
            pfizer = pfizer +1
      
        ddbb.child('CovidApp/ConteoVacunas').set({'Moderna': moderna,'Pfizer': pfizer,'Astra Zeneca': astra,'Janssen':janssen})

def QRDecoder(passport):
    qr_ = cv2.imread(passport)
    detector = cv2.QRCodeDetector()
    text, arr, deci = detector.detectAndDecode(qr_)
    data = text
    ## pablo qr data = "HC1:NCFOXN%TSMAHN-HXOCLGML-P8ZVHGJ-AH5*S1ROT$SD PL*IS2VF%G*H50E6TTNNO4*J8OX4W$C2VLWLIVO5ON1: BI$H1VO61Q/ZJGYBN-PT-J5Q1SGO/ROLTQKABAQ5/974CL395J4I-B5ET42HPPEPHCRCLAFDOAC5LGN1:6G16PCNQ+MBM6P846$AU47N/5QV4IV4:/6N9R%EPL8RU9DNKM*IK5C9A.D90I/EL6KKYHIL4ODJL8FF3DE0OA0D9E2LBHHGKLO-K%FGLIA5D8MJKQJK6HMMBIE2K5OI9YI:8D7A1SV81DOEA7IB65C94JB1IGV8OQZI+5IJXI*EMN8KH5HVTA6LF*KDPUKF6IOKE/*B6XB3Z0BUJZ0KVE0G%5TW5A 6+O67N6F7EUTMNU6DFJMZG6.G3T2RM6MZPE8N23L-8J9FL85UG/R-9RH65A3TC38K*2X97UB2+.CHCJA R9CUQ31A*5O/DFXD2BB8FBCKSL5RW4043CC1"
    ## sauco qr data = "HC1:NCFOXN%TSMAHN-HFSC41O/XMD/20MSM52VEL1WGTJPBBJRH5$JUQC0ZKLV/R2:O:ZH6I1$4JN:IN1MPK9V L9L69UEG%6ZZ1-Q6FB6-/E-$M846I.EH%6ZNMOWEJWEYYAEN932QZJDKK9%OC+G9QJPNF67J6UW6%PQNR66PPM4MP6FP8QD/9:G9%PPLTA8C9B212+P:S9HR9EB6*C2*$J+PEYMS:CSPZI$%P*$K3$OHBW24FAL86H0YQC:D9IE9WT0K3M9UVZSVV*001HW%8UE9.955B9-NT0 2$$0X4PCY0+-CVYCDEBD0HX2JR$4O1K8KE9.FMDQCY0CNNG.8M+87LPMIH-O92UQJLELV3Z/JNT28KGU*BNSG3UQ4F67%F$+NF1W7PG/UIGSU064P$6PORC.U9D2LOTT*QGTAAY7.Y7N31J4GD8VYDJ-IOJTAR4IJ9Q3+TOJUJGS0$V8*FW-HSXIL9K5CR24GB1F-BT% CX1NYURNV92$JN2E$JDJ8SC$A7E644RWUPDDWD7F%-FM404%213"
    data = data.replace("HC1:","")
    z_data = b45decode(data)
    databytes = bytes(z_data)
    decompress = zlib.decompress(databytes)
    decode = cbor2.loads(decompress)
    decodedData = cbor2.loads(decode.value[2])
    pprint.pprint(decodedData)
    num_qr = ddbb.child("CovidApp").get()
    lastvalorqr = 0
    for qr in num_qr.each(): ##RECORREMOS TODOS LOS QR QUE HAYA EN LA APP
        lastvalorqr = lastvalorqr + 1

    ddbb.child(f'CovidApp/QR{lastvalorqr}').set(decodedData) ## QR DINAMICO

def enviarCorreos():
    import smtplib, ssl
    import getpass
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    username = "trabajofinalpcd2022@gmail.com"
    password = getpass.getpass("Ingrese su password: ")
    destinatario = input("Ingrese destinatario: ")
    asunto= input("Ingrese el asunto: ")
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = asunto
    mensaje["From"] = username
    mensaje["To"] = destinatario
    html = f"""
<html>
<body>
    Hola <i>{destinatario}</i><br>
    Espero que estés <b>muy bien</b>
</body>
</html>
"""
    parte_html = MIMEText(html, "html")
    mensaje.attach(parte_html)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(username, password)
        print("Inicio Sesión")
        server.sendmail(username, destinatario, mensaje.as_string())
        print("Mensaje enviado")