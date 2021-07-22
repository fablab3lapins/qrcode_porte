from tkinter import *
import qrcode
import random
import db


varVerif=0


def lettre():   #creer le qrcode    
    nbChar = random.randint(4,13)
    qr_code =""
    for i in range(nbChar):
        aux = random.randint(97, 122)
        aux = chr(aux)
        qr_code = "%s%s" % (qr_code, aux)


    sqlStr = "SELECT * FROM client WHERE qrcode ='"  #verif que le qrcode est unique

    sqlStr = "%s%s" % (sqlStr, qr_code)

    sqlStr = "%s%s" % (sqlStr, "'")




    recep = db.fetchone(sqlStr)  # recup la ligne si elle existe sinon none

    if (recep != None):
        return qr_code
    else:
        lettre()
    

def id():       #créer un id unique
    a, d ,e, f = random.randint(0, 9), random.randint(0, 9) , random.randint(0, 9),random.randint(0, 9)
    b ,c = random.randint(97,122), random.randint(97,122)

    b, c= chr(b), chr(c)        

    id_client = "%s%s" % (a, d)
    id_client = "%s%s" % (id_client, e)
    id_client = "%s%s" % (id_client, f)
    id_client = "%s%s" % (id_client, b)

    id_client = "%s%s" % (id_client, c)

    sqlStr = "SELECT * FROM client WHERE id_client ='"  #verif que l'id est unique

    sqlStr = "%s%s" % (sqlStr, id_client)

    sqlStr = "%s%s" % (sqlStr, "'")





    recep = db.fetchone(sqlStr)

    if (recep != None):
        return id_client
    else:
        id()

    


def edit():   # ajoute un ligne avec les coordonnées de l'utilisateur
    global varVerif

    mailverif()
    
    new_user = (id(),nom.get(),prenom.get(),mail.get(),tel.get(),adresse.get(),lettre())

    if (varVerif == 1):
        sqlStr = "INSERT INTO client"        #création de la commande sql

        sqlStr = "%s%s" % (sqlStr, " (id_client, nom, prenom, mail, telephone, adresse,  qr_code) VALUES ")

        sqlStr = "%s%s" % (sqlStr, new_user)

        print(sqlStr)
        db.execute(sqlStr)

        

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


    if (varVerif == 1):
        save()

def mailverif():  #verif que le mail n'existe pas et que le client n'a pas été créer
    global varVerif


    sqlStr ="SELECT * FROM client WHERE mail='"

    sqlStr = "%s%s" % (sqlStr ,mail.get())

    sqlStr = "%s%s" % (sqlStr, "'")




    recep = db.fetchone(sqlStr)
    print(sqlStr)
    


    if (recep == None):
        varVerif = 1
    else:
        varVerif = 0


def save():     # enrigstre le qrcode dans un dossier (nom de l'image compose du nom prenom et id)

    sqlStr ="SELECT * FROM client WHERE mail='"

    sqlStr = "%s%s" % (sqlStr ,mail.get())

    sqlStr = "%s%s" % (sqlStr, "'")

    


    recep = db.fetchone(sqlStr)

    print(recep)

    name = recep[1]

    surname = recep[2]

    id_user = recep[0]

    qr_code = recep[6]

    qr = qrcode.QRCode(version=3, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4)


    qr.add_data(qr_code)

    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="#FFD800")

    imgq='qrcode_list/'

    imgq = "%s%s" % (imgq,name)
    imgq = "%s%s" % (imgq,surname)
    imgq = "%s%s" % (imgq,id_user)

    imgq = "%s%s" % (imgq,".png")

    

    

    img.save(imgq)
                       


win = Tk()

win.title("creer un utilisateur")
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
