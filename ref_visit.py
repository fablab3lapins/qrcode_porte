import cv2
from time import sleep
from picamera import PiCamera
from tkinter import *
from datetime import *
import RPi.GPIO as GPIO
import db

#lieu = "a definir"  selon le lieu ou il sera placé
data=""

camera = PiCamera()
camera.resolution = (1024, 768)

id_client = ""

GPIO.setmode(GPIO.BCM)
LED = 21
GPIO.setup(LED, GPIO.OUT)


def scan(): #scan le qrcode en enregistre la valeur lu

    
    camera.start_preview(fullscreen=False, window=(50,50,650,650))

    sleep(5)

    camera.capture("/home/pi/Documents/qrcoed.jpeg")

    camera.stop_preview()

    img = cv2.imread("/home/pi/Documents/qrcoed.jpeg")

    detector = cv2.QRCodeDetector()
    swpr = False

    while True:   
        
        data, box, _ = detector.detectAndDecode(img)
        

        if (box is not None):
            for i in range(len(box)):
                cv2.line(img, tuple(box[i][0]), tuple(box[(i+1)% len(box)][0]), color=(255, 0, 0))
            

            if data:
                swpr= False
                print("data found:" + data)
                
        cv2.imshow("code detector" , img)
        sleep(0.1)
        cv2.destroyAllWindows()
        test(data, id_client)
        break


def test(data, id_client):     # regarde si le qrcode existe

    
    auxdata = data

    sql="SELECT * FROM client WHERE ( qr_code='"  # creation de la commande sql

    sql = "%s%s" % (sql, auxdata)

    sql = "%s%s" % (sql, "')")

    print(sql)

    qrcode = db.fetchone(sql)

    print(qrcode)

    id_client = qrcode[0] #recup la premieere colonne de la ligne

    print(id_client)
    

    if (qrcode == None):
        print('j\'ai pas celui la')
        

    else :
        print( ' got it ')
        change(data, id_client)



def change(data, id_client):       # regarde si le client peut entrée et si oui diminue de 1 le nombre d'entrée

    auxid = id_client

    sql="SELECT nb_visit FROM count WHERE ( id_client='"

    sql = "%s%s" % (sql, auxid)



    sql = "%s%s" % (sql, "')")
    print(sql)
    
    visit = db.fetchone(sql)

    nb_vis = visit[0]
    if (nb_vis == 0):
        root = Tk()

        lb = Label(root, text = ' t\'as pas le droit', fg = 'red', font = ('Courrier', 30))
        lb.pack()

        root.mainloop()

    else :

        nb_vis=nb_vis-1

        GPIO.output(LED, GPIO.HIGH)

        sleep(5)

        GPIO.output(LED, GPIO.LOW)

        sql="UPDATE count SET nb_visit="

        sql = "%s%s" % (sql, nb_vis)

        sql = "%s%s" % (sql, " WHERE id_client='")

        sql = "%s%s" % (sql, auxid)

        sql = "%s%s" % (sql, "' AND lieu ='")

        lieu = entry1.get()

        sql= "%s%s" % (sql, lieu)

        sql = "%s%s" % (sql, "'")

        print(sql)

        addref(id_client)

    db.execute(sql)



def addref(id_client):       #reference la visite

    heure = datetime.today().strftime('%H:%M')

    date = datetime.today().strftime('%Y-%m-%d')

    lieu = entry1.get()

    column = (id_client, date, heure, lieu)

    sql = "INSERT INTO ref_visit"

    sql = "%s%s" % (sql, " (id_client, date, heure, lieu) VALUES ")

    sql = "%s%s" % (sql, column)

    print(sql)
    db.execute(sql)



win = Tk()      # pour lancer le scan et entrée le lieu pour les tests

win.title("La tirelire magique ")
win.geometry("800x600")
win.config(background='#00ffe0')


label2 = Label(win, text='qr code test', font=('Courrier', 27), bg='#00ffe0')
label2.pack(side=TOP)

entry1 = Entry(win, width=45)
entry1.pack(expand=YES)

but = Button(win, text='tester', font=('Courrier', 20), bg='#00ffe0', command=scan)
but.pack(expand=YES)

win.mainloop()
