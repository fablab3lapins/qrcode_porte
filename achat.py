from tkinter import *
import random
from datetime import *
import db

ref = 0

def refachat():   #creer une ref pour l'achat (annee, mois, jours, random number de 4 chiffres
    global ref
    heure = datetime.today().strftime('%H:%M')

    date = datetime.today().strftime('%Y-%m-%d')

    ref = "%s%s%s%s" % (
        random.randint(0, 9), 
        random.randint(0, 9), 
        random.randint(0, 9), 
        random.randint(0, 9)
    )
    
    ref = "%s%s" % ( "-", ref)

    ref = "%s%s" % (date, ref)

    verif()


def verif():
    global ref

    sql ="SELECT * FROM achat WHERE ref_achat ='"      #creer la commande sql

    sql = "%s%s" % (sql, ref)


    sql = "%s%s" % (sql, "'")

    print(sql)
    

    recep = db.fetchone(sql) #recup la ligne si elle existe sinon recup none

    print(recep)
    

    if (recep == None):
        print('j\'ai pas celui la')
        id()
        achat()
        
    else :
        print( ' got it ')



def id():       # recuper l'id
    global id_client

    sql ="SELECT * FROM client WHERE ( nom='"

    sql = "%s%s" % (sql, nom.get())

    sql = "%s%s" % (sql, "'")

    sql = "%s%s" % (sql, " AND prenom='")

    sql = "%s%s" % (sql, prenom.get())

    sql = "%s%s" % (sql, "')")

    print(sql)

    client = db.fetchone(sql)

    print(client)

    id_client = client[0]

    print(id_client)



def achat():        # ajoute la ligne de l'achat avec le nb de visit , la ref de l'achat, l'id et le lieu
    global id_client

    global ref

    date = datetime.today().strftime('%Y-%m-%d')

    column = (int(nb.get()), ref, id_client, lieu.get())

    sql  = "INSERT INTO achat"

    sql = "%s%s" % (sql, " (nb_visit_achat, ref_achat, id_client, lieu) VALUES ")

    sql = "%s%s" % (sql, column)

    print(sql)
    db.execute(sql)


    upcount()




def upcount():      # met a jour si le client a deja effectuer un achat dans le lieu sinon créer la ligne
    global id_client

    
    sql = "SELECT * FROM count WHERE id_client='"

    sql = "%s%s" % (sql, id_client)

    sql = "%s%s" % (sql, "'")

    sql = "%s%s" % (sql, " AND lieu='")

    sql = "%s%s" % (sql,lieu.get())

    sql = "%s%s" % (sql, "'")

    print(sql)

    count = db.fetchone(sql)

    if (count == None):
        pass
    else :
        nbvisit = count[0]

    if (count == None):
        print('j\'ai pas celui la')


        column = (nb.get(), id_client, lieu.get())

        sql = "INSERT INTO count"

        sql = "%s%s" % (sql, " (nb_visit, id_client, lieu) VALUES ")

        sql = "%s%s" % (sql, column)

        db.execute(sql)

    else:
        print( ' got it ')


        nbvis= int(nb.get()) + nbvisit

        sql = " UPDATE count SET nb_visit = "

        sql = "%s%s" % (sql, nbvis)

        sql = "%s%s" % (sql, " WHERE id_client ='")

        sql = "%s%s" % (sql, id_client)
        
        sql = "%s%s" % (sql, "'")

        sql = "%s%s" % (sql, " AND lieu='")

        sql = "%s%s" % (sql, lieu.get())

        sql = "%s%s" % (sql, "'")

        print(sql)

        db.execute(sql)



    win = Tk()

    win.configure(bg='red')

    label = Label(win, text='bravo t\'es moins riche maintenant', font=('Courrier', 40), bg='red', fg='white')
    label.pack(side=TOP)

    win.mainloop()



win = Tk()

win.title("faire un achat")
win.geometry("800x600")
win.config(background='#00ffe0')


label2 = Label(win, text='nom', font=('Courrier', 27), bg='#00ffe0')
label2.pack(side=TOP)

nom = Entry(win, width=45)
nom.pack(expand=YES)

label1 = Label(win, text='prenom', font=('Courrier', 27), bg='#00ffe0')
label1.pack(side=TOP)

prenom = Entry(win, width=45)
prenom.pack(expand=YES)

label = Label(win, text='nombre de entrez, faites comme chez vous', font=('Courrier', 27), bg='#00ffe0')
label.pack(side=TOP)

nb = Entry(win, width=45)
nb.pack(expand=YES)

label4 = Label(win, text='lieu de visite', font=('Courrier', 27), bg='#00ffe0')
label4.pack(side=TOP)

lieu = Entry(win, width=45)
lieu.pack(expand=YES)

but = Button(win, text='réaliser l\'achat', font=('Courrier', 20), bg='#00ffe0', command=refachat)
but.pack(expand=YES)

win.mainloop()



    
