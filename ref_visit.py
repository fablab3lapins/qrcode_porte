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
    
    auxdata = data

    sqlStr="SELECT * FROM client WHERE ( qr_code='"  # creation de la commande sql

    sqlStr = "%s%s" % (sqlStr, auxdata)

    sqlStr = "%s%s" % (sqlStr, "')")

    print(sqlStr)

    


    recep = db.fetchone(sqlStr)

    print(recep)

    id_client = recep[0] #recup la premieere colonne de la ligne

    print(id_client)
    

    if (recep == None):
        print('j\'ai pas celui la')
        
        

    else :
        print( ' got it ')
        change()



def change():       # regarde si le client peut entrée et si oui diminue de 1 le nombre d'entrée
    global data
    global id_client
    


    auxid = id_client

    sqlStr="SELECT nb_visit FROM count WHERE ( id_client='"

    sqlStr = "%s%s" % (sqlStr, auxid)



    sqlStr = "%s%s" % (sqlStr, "')")


    
    print(sqlStr)
    
    recep = db.fetchone(sqlStr)

    nb_vis = recep[0]
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

        
        sqlStr="UPDATE count SET nb_visit="

        sqlStr = "%s%s" % (sqlStr, nb_vis)

        sqlStr = "%s%s" % (sqlStr, " WHERE id_client='")

        sqlStr = "%s%s" % (sqlStr, auxid)

        sqlStr = "%s%s" % (sqlStr, "' AND lieu ='")

        lieu = entry1.get()

        sqlStr= "%s%s" % (sqlStr, lieu)

        sqlStr = "%s%s" % (sqlStr, "'")

        print(sqlStr)

        addref()

    db.execute(sqlStr)





def addref():       #reference la visite 
    global id_client


    heure = datetime.today().strftime('%H:%M')

    date = datetime.today().strftime('%Y-%m-%d')

    lieu = entry1.get()

    column = (id_client, date, heure, lieu)

    sqlStr = "INSERT INTO ref_visit"

    e =

    sqlStr = "%s%s" % (sqlStr, " (id_client, date, heure, lieu) VALUES ")

    sqlStr = "%s%s" % (sqlStr, column)

    print(sqlStr)
    db.execute(sqlStr)



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
