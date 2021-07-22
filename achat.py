from tkinter import *
import random
from datetime import *
import db



ref = 0



def refachat():   #creer une ref pour l'achat (annee, mois, jours, random number de 4 chiffres
    global ref
    heure = datetime.today().strftime('%H:%M')

    date = datetime.today().strftime('%Y-%m-%d')
    
    a, d ,e, f = random.randint(0, 9), random.randint(0, 9) , random.randint(0, 9),random.randint(0, 9)

    ref = "%s%s" % (a, d)
    ref = "%s%s" % (ref, e)
    ref = "%s%s" % (ref, f)

    ref = "%s%s" % ( "-", ref)

    ref = "%s%s" % (date, ref)

    verif()

    



def verif():
    global ref

    

    sqlStr ="SELECT * FROM achat WHERE ref_achat ='"      #creer la commande sql

    sqlStr = "%s%s" % (sqlStr, ref)


    sqlStr = "%s%s" % (sqlStr, "'")

    print(sqlStr)
    


    recep = db.fetchone(sqlStr) #recup la ligne si elle existe sinon recup none

    print(recep)
    

    if (recep == None):
        print('j\'ai pas celui la')
        id()
        achat()
        
    else :
        print( ' got it ')




def id():       # recuper l'id
    global id_client

    sqlStr ="SELECT * FROM client WHERE ( nom='"

    sqlStr = "%s%s" % (sqlStr, nom.get())

    sqlStr = "%s%s" % (sqlStr, "'")

    sqlStr = "%s%s" % (sqlStr, " AND prenom='")

    sqlStr = "%s%s" % (sqlStr, prenom.get())

    sqlStr = "%s%s" % (sqlStr, "')")

    print(sqlStr)
    

    
    


    recep = db.fetchone(sqlStr)

    print(recep)

    id_client = recep[0]

    print(id_client)





def achat():        # ajoute la ligne de l'achat avec le nb de visit , la ref de l'achat, l'id et le lieu
    global id_client

    global ref

    date = datetime.today().strftime('%Y-%m-%d')

    column = (int(nb.get()), ref, id_client, lieu.get())

    sqtStr  = "INSERT INTO achat"

    sqtStr = "%s%s" % (sqtStr, " (nb_visit_achat, ref_achat, id_client, lieu) VALUES ")

    sqtStr = "%s%s" % (sqtStr, column)

    print(sqtStr)
    db.execute(sqtStr)


    upcount()




def upcount():      # met a jour si le client a deja effectuer un achat dans le lieu sinon créer la ligne
    global id_client

    
    sqlStr ="SELECT * FROM count WHERE id_client='"

    sqlStr = "%s%s" % (sqlStr, id_client)

    sqlStr = "%s%s" % (sqlStr, "'")

    sqlStr = "%s%s" % (sqlStr, " AND lieu='")

    sqlStr = "%s%s" % (sqlStr,lieu.get())

    sqlStr = "%s%s" % (sqlStr, "'")

    print(sqlStr)

    recep = db.fetchone(sqlStr)

    if (recep == None):
        pass
    else :
        nbvisit = recep[0]



    if (recep == None):
        print('j\'ai pas celui la')


        column = (nb.get(), id_client, lieu.get())

        sqlStr = "INSERT INTO count"

        sqlStr = "%s%s" % (sqlStr, " (nb_visit, id_client, lieu) VALUES ")

        sqlStr = "%s%s" % (sqlStr, column)

        db.execute(sqlStr)

    else:
        print( ' got it ')


        nbvis= int(nb.get()) + nbvisit

        sqlStr = " UPDATE count SET nb_visit = "

        sqlStr = "%s%s" % (sqlStr, nbvis)
        

        x =

        sqlStr = "%s%s" % (sqlStr, " WHERE id_client ='")

        sqlStr = "%s%s" % (sqlStr, id_client)
        
        sqlStr = "%s%s" % (sqlStr, "'")

        sqlStr = "%s%s" % (sqlStr, " AND lieu='")

        sqlStr = "%s%s" % (sqlStr, lieu.get())

        sqlStr = "%s%s" % (sqlStr, "'")

        print(sqlStr)

        db.execute(sqlStr)



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



    
