from tkinter import *
import qrcode
import random
import db

check=0

def lettre():   #creer le qrcode    
    nbChar = random.randint(4,13)
    qr_code =""
    for i in range(nbChar):
        aux = random.randint(97, 122)
        aux = chr(aux)
        qr_code = "%s%s" % (qr_code, aux)


    sql = "SELECT * FROM client WHERE qrcode ='"  #verif que le qrcode est unique

    sql = "%s%s" % (sql, qr_code)

    sql = "%s%s" % (sql, "'")

    result = db.fetchone(sql)  # recup la ligne si elle existe sinon none

    if (result != None):
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

    sql = "SELECT * FROM client WHERE id_client ='"  #verif que l'id est unique

    sql = "%s%s" % (sql, id_client)

    sql = "%s%s" % (sql, "'")

    result = db.fetchone(sql)

    if (result != None):
        return id_client
    else:
        id()

    


def edit(check):   # ajoute un ligne avec les coordonnées de l'utilisateur


    mailverif(check)
    
    new_user = (id(),nom.get(),prenom.get(),mail.get(),tel.get(),adresse.get(),lettre())

    if (check == 1):
        sql = "INSERT INTO client"        #création de la commande sql

        sql = "%s%s" % (sql, " (id_client, nom, prenom, mail, telephone, adresse,  qr_code) VALUES ")

        sql = "%s%s" % (sql, new_user)

        print(sql)
        db.execute(sql)

        

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


    if (check == 1):
        save()

def mailverif(check):  #verif que le mail n'existe pas et que le client n'a pas été créer
    
    sql ="SELECT * FROM client WHERE mail='"

    sql = "%s%s" % (sql ,mail.get())

    sql = "%s%s" % (sql, "'")

    result = db.fetchone(sql)
    print(sql)

    if (result == None):
        check = 1
    else:
        check = 0


def save():     # enrigstre le qrcode dans un dossier (nom de l'image compose du nom prenom et id)

    sql ="SELECT * FROM client WHERE mail='"

    sql = "%s%s" % (sql ,mail.get())

    sql = "%s%s" % (sql, "'")


    result = db.fetchone(sql)

    print(result)

    name = result[1]

    surname = result[2]

    id_user = result[0]

    qr_code = result[6]

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

but = Button(win, text='créer utilisateur', font=('Courrier', 20), bg='#00ffe0', command=edit(check))
but.pack(expand=YES)

win.mainloop()
