from tkinter import *
import random
from datetime import *
import db



a = 0



def refachat():   #creer une ref pour l'achat (annee, mois, jours, random number de 4 chiffres

    global a

    
    heure = datetime.today().strftime('%H:%M')

    date = datetime.today().strftime('%Y-%m-%d')
    
    a, d ,e, f = random.randint(0, 9), random.randint(0, 9) , random.randint(0, 9),random.randint(0, 9)

    a = "%s%s" % (a, d)
    a = "%s%s" % (a, e)
    a = "%s%s" % (a, f)

    b= "-"
    a = "%s%s" % ( b, a)

    a = "%s%s" % (date, a)

    verif()

    



def verif():
    global a

    

    k="SELECT * FROM achat WHERE ref_achat ='"      #creer la commande sql 

    k = "%s%s" % (k, a)

    v = "'"
    
    k = "%s%s" % (k, v)

    print(k)
    


    b = db.fetchone(k) #recup la ligne si elle existe sinon recup none

    print(b)
    

    if (b == None):
        print('j\'ai pas celui la')
        id()
        achat()
        
    else :
        print( ' got it ')




def id():       # recuper l'id
    global id_client
    
    nm = nom.get()

    pm= prenom.get()

    

    k="SELECT * FROM client WHERE ( nom='"

    k = "%s%s" % (k, nm)

    v = "'"

    g = " AND prenom='"

    w = "')"

    k = "%s%s" % (k, v)

    k = "%s%s" % (k, g)

    k = "%s%s" % (k, pm)

    k = "%s%s" % (k, w)

    print(k)
    

    
    


    b = db.fetchone(k)

    print(b)

    id_client = b[0]

    print(id_client)





def achat():        # ajoute la ligne de l'achat avec le nb de visit , la ref de l'achat, l'id et le lieu
    global id_client

    global a


    nbvis = int(nb.get())

    li = lieu.get()

    

    date = datetime.today().strftime('%Y-%m-%d')
    


    al = (nbvis, a, id_client, li)

    k = "INSERT INTO achat"

    e = " (nb_visit_achat, ref_achat, id_client, lieu) VALUES "

    k = "%s%s" % (k, e)

    k = "%s%s" % (k, al)

    print(k)
    db.execute(k)


    upcount()




def upcount():      # met a jour si le client a deja effectuer un achat dans le lieu sinon créer la ligne
    global id_client

    
    k="SELECT * FROM count WHERE id_client='"

    k = "%s%s" % (k, id_client)

    v = "'"

    g = " AND lieu='"
    
    k = "%s%s" % (k, v)

    k = "%s%s" % (k, g)

    li = lieu.get()

    k = "%s%s" % (k, li)

    k = "%s%s" % (k, v)

    

    

    print(k)

    b = db.fetchone(k)

    if (b == None):
        truc = 0
    else :
        c = b[0]



    if (b == None):
        print('j\'ai pas celui la')

        nbvis = nb.get()

        li = lieu.get()

        al = (nbvis, id_client, li)

        k = "INSERT INTO count"

        e = " (nb_visit, id_client, lieu) VALUES "

        k = "%s%s" % (k, e)

        k = "%s%s" % (k, al)


        db.execute(k)


            
        
    else :
        print( ' got it ')


        nbvis= int(nb.get()) + c
        v = "'"

        k = " UPDATE count SET nb_visit = "

        k = "%s%s" % (k, nbvis)
        

        x = " WHERE id_client ='"

        k = "%s%s" % (k, x)

        k = "%s%s" % (k, id_client)

        

        g = " AND lieu='"
        
        k = "%s%s" % (k, v)

        k = "%s%s" % (k, g)

        li = lieu.get()

        k = "%s%s" % (k, li)

        k = "%s%s" % (k, v)

        print(k)

        db.execute(k)



    win = Tk()

    win.configure(bg='red')

    label = Label(win, text='bravo t\'es moins riche maintenant', font=('Courrier', 40), bg='red', fg='white')
    label.pack(side=TOP)

    win.mainloop()

        


            


        

    





win = Tk()

win.title("La tirelire magique ")
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



    
