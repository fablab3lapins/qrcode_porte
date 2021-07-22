from tkinter import *
import qrcode
import json
import random
import MySQLdb

txt = json.loads()

iphost = txt["iphost"]

hostname = txt["hostname"]

password = txt["password"]

database = txt["database name"]

vr=0


def lettre():   #creer le qrcode    
    a = random.randint(4,13)
    k =""
    for i in range(a):
        b = random.randint(97, 122)
        b = chr(b)
        k = "%s%s" % (k, b)


    f = "SELECT * FROM client WHERE qrcode ='"  #verif que le qrcode est unique

    f = "%s%s" % (f, a)

    b ="'"

    f = "%s%s" % (f, b)

    connection = MySQLdb.connect("192.168.0.15","admin","fablab70300","set_client")

    cursor = connection.cursor()

    cursor.execute(f) 

    m = cursor.fetchone  # recup la ligne si elle existe sinon none

    if (m!= None):
        return k
    else:
        lettre()
    

def id():       #créer un id unique
    a, d ,e, f = random.randint(0, 9), random.randint(0, 9) , random.randint(0, 9),random.randint(0, 9)
    b ,c = random.randint(97,122), random.randint(97,122)

    b, c= chr(b), chr(c)        

    a = "%s%s" % (a, d)
    a = "%s%s" % (a, e)
    a = "%s%s" % (a, f)
    a = "%s%s" % (a, b)

    a = "%s%s" % (a, c)

    f = "SELECT * FROM client WHERE id_client ='"  #verif que l'id est unique

    f = "%s%s" % (f, a)

    b ="'"

    f = "%s%s" % (f, b)

    connection = MySQLdb.connect("192.168.0.15","admin","fablab70300","set_client")

    cursor = connection.cursor()

    cursor.execute(f)

    m = cursor.fetchone

    if (m!= None):
        return a
    else:
        id()

    


def edit():   # ajoute un ligne avec les coordonnées de l'utilisateur
    global vr

    mailverif()
    
    connection = MySQLdb.connect("192.168.0.15","admin","fablab70300","set_client")

    cursor = connection.cursor()    #recuperation des entrée
    b= lettre()
    a = nom.get()
    c = mail.get()
    d = prenom.get()
    e = adresse.get()
    f = tel.get()
    g = id()
    

    
    new_user = (g,a,d,c,f,e,b)
    if (vr == 1):
        k = "INSERT INTO client"        #création de la commande sql

        e = " (id_client, nom, prenom, mail, telephone, adresse,  qr_code) VALUES "

        k = "%s%s" % (k, e)

        k = "%s%s" % (k, new_user)

        print(k)
        cursor.execute(k)

        

    else :
        win = Tk()              #fenetre de refus

        win.configure(bg='red')

        label = Label(win, text='cet utilisateur existe deja', font=('Courrier', 120), bg='red', fg='white')
        label.pack(side=TOP)

        """label1 = Label(win, text='www.pourdebon.com', font=('Courrier', 120), bg='red', fg='white')
        label1.pack(side=TOP)

        label2 = Label(win, text='(-10%) avec le code\'a mort\'', font=('Courrier', 120), bg='red', fg='white')
        label2.pack(side=TOP)"""

        win.mainloop()
                
    connection.commit()

    connection.close()

    if (vr == 1):
        save()

def mailverif():  #verif que le mail n'existe pas et que le client n'a pas été créer
    global vr

    a = mail.get()
    k="SELECT * FROM client WHERE mail='"

    k = "%s%s" % (k,a)

    e = "'"

    k = "%s%s" % (k, e)

    connection = MySQLdb.connect("192.168.0.15","admin","fablab70300","set_client")

    cursor = connection.cursor()
    cursor.execute(k)

    b = cursor.fetchone()
    print(k)
    
    connection.commit()

    connection.close()

    if (b == None):
        vr = 1
    else:
        vr = 0


def save():     # enrigstre le qrcode dans un dossier (nom de l'image compose du nom prenom et id)

    a = mail.get()
    k="SELECT * FROM client WHERE mail='"

    k = "%s%s" % (k,a)

    e = "'"

    k = "%s%s" % (k, e)

    
    connection = MySQLdb.connect("192.168.0.15","admin","fablab70300","set_client")

    cursor = connection.cursor()

    cursor.execute(k)

    b = cursor.fetchone()

    print(b)

    a = b[1]

    c = b[2]

    i = b[0]

    q = b[6]
    
    
    connection.commit()

    connection.close()
    



    qr = qrcode.QRCode(version=3, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4)


    qr.add_data(q)

    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="#FFD800")

    k='qrcode_list/'

    k = "%s%s" % (k,a)
    k = "%s%s" % (k,c)
    k = "%s%s" % (k,i)

    r = ".png"

    k = "%s%s" % (k,r)

    

    

    img.save(k)
                       

        
    

win = Tk()

win.title("La tirelire magique ")
win.geometry("800x600")
win.config(background='#00ffe0')


label = Label(win, text='mail', font=('Courrier', 27), bg='#00ffe0')
label.pack(side=TOP)

mail = Entry(win, width=45)
mail.pack(expand=YES)

label1 = Label(win, text='nom', font=('Courrier', 27), bg='#00ffe0')
label1.pack(side=TOP)

nom = Entry(win, width=45)
nom.pack(expand=YES)

label3 = Label(win, text='prenom', font=('Courrier', 27), bg='#00ffe0')
label3.pack(side=TOP)

prenom = Entry(win, width=45)
prenom.pack(expand=YES)

label4 = Label(win, text='telephone', font=('Courrier', 27), bg='#00ffe0')
label4.pack(side=TOP)

tel = Entry(win, width=45)
tel.pack(expand=YES)

label5 = Label(win, text='adresse', font=('Courrier', 27), bg='#00ffe0')
label5.pack(side=TOP)

adresse = Entry(win, width=45)
adresse.pack(expand=YES)

but = Button(win, text='créer utilisateur', font=('Courrier', 20), bg='#00ffe0', command=edit)
but.pack(expand=YES)

win.mainloop()
