import cv2
from time import sleep
from picamera import PiCamera
from tkinter import *
import json
import MySQLdb
from datetime import *
import RPi.GPIO as GPIO

txt = json.loads()

iphost = txt["iphost"]

hostname = txt["hostname"]

password = txt["password"]

database = txt["database_name"]


#lieu = "a definir"  selon le lieu ou il sera placé
data=""

camera = PiCamera()
camera.resolution = (1024, 768)

id_client = ""

GPIO.setmode(GPIO.BCM)

LED = 21

GPIO.setup(LED, GPIO.OUT)


def execute(k):
    connection = MySQLdb.connect(iphost, hostname, password, database)

    cursor = connection.cursor()

    cursor.execute(k)

    connection.commit()

    connection.close()


def fetch(k):
    connection = MySQLdb.connect(iphost, hostname, password, database)

    cursor = connection.cursor()

    cursor.execute(k)

    b = cursor.fetchone()

    connection.commit()

    connection.close()

    return b


def scan(): #scan le qrcode en enregistre la valeur lu

    
    camera.start_preview(fullscreen=False, window=(50,50,650,650))

    sleep(5)

    camera.capture("/home/pi/Documents/qrcoed.jpeg")

    camera.stop_preview()

    img = cv2.imread("/home/pi/Documents/qrcoed.jpeg")

    

    detector = cv2.QRCodeDetector()
    swpr = False

    global data
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
        test()
        break


        

        if cv2.waitKey(1) == ord("q"):
            break

    





def test():     # regarde si le qrcode existe
    global data
    global id_client
    
    a = data
    print(a)

    k="SELECT * FROM client WHERE ( qr_code='"  # creation de la commande sql

    k = "%s%s" % (k, a)

    v = "')"

    k = "%s%s" % (k, v)

    print(k)
    


    b =fetch(k)

    print(b)

    id_client = b[0] #recup la premieere colonne de la ligne

    print(id_client)
    

    if (b == None):
        print('j\'ai pas celui la')
        
        

    else :
        print( ' got it ')
        change()



def change():       # regarde si le client peut entrée et si oui diminue de 1 le nombre d'entrée
    global data
    global id_client
    


    a = id_client

    k="SELECT nb_visit FROM count WHERE ( id_client='"

    k = "%s%s" % (k, a)

    v = "')"

    k = "%s%s" % (k, v)


    
    print(k)
    
    b = fetch(k)

    c = b[0]
    if (c == 0):
        root = Tk()

        lb = Label(root, text = ' t\'as pas le droit', fg = 'red', font = ('Courrier', 30))
        lb.pack()

        root.mainloop()

    else :

        c=c-1

        GPIO.output(LED, GPIO.HIGH)

        sleep(5)

        GPIO.output(LED, GPIO.LOW)

        
        l="UPDATE count SET nb_visit="

        l = "%s%s" % (l, c)

        w = " WHERE id_client='"

        l = "%s%s" % (l, w)

        l = "%s%s" % (l, a)

        s = "' AND lieu ='"

        l = "%s%s" % (l, s)

        lieu = entry1.get()

        l = "%s%s" % (l, lieu)

        r = "'"

        l = "%s%s" % (l, r)

        print(l)

        addref()

    execute(l)





def addref():       #reference la visite 
    global id_client


    heure = datetime.today().strftime('%H:%M')

    date = datetime.today().strftime('%Y-%m-%d')

    lieu = entry1.get()

    al = (id_client, date, heure, lieu)

    k = "INSERT INTO ref_visit"

    e = " (id_client, date, heure, lieu) VALUES "

    k = "%s%s" % (k, e)

    k = "%s%s" % (k, al)

    print(k)
    execute(k)




    

    


    




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
