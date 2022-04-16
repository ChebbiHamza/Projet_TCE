import csv
from pad4pi import rpi_gpio
import RPi.GPIO as GPIO
import time
from LCD_16_2 import LCD_I2C_DRIVER
from mail_send import mail_send_ssl

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
# setup LCD
lcd = LCD_I2C_DRIVER.lcd()

red_led = 20
green_led = 21
mail_state = False  # to sent mail just one time
mail_on_state = False  # to sent mail ON just one time
mail_warning_state = False
button = 17  # Button PIN BCM
RLin = 23
Limite_base = 60  # Nbr Limite
GPIO.setup(RLin, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)

listcp = ["Total:", "Partiel:"]
listli = ["Nblimite:"]

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button
# Setup Keypad
KEYPAD = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

# same as calling: factory.create_4_by_4_keypad, still we put here fyi:
ROW_PINS = [9, 11, 0, 5]  # BCM numbering
COL_PINS = [6, 13, 19, 26]  # BCM numbering

factory = rpi_gpio.KeypadFactory()

# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(
    keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)


password = ["1", "2", "3", "4"]


def NbPar_tot_CSV():
    with open("/home/pi/Desktop/PFE_TCE/Main/csv_register/COMPTAGE.csv") as file_csv:
        cmp = csv.DictReader(file_csv)
        a = []
        for i in cmp:                                                         # itirating trow a dicreader object
            for j in listcp:
                a.append(i[j])
        return a


def Nblimite_CSV():
    with open("/home/pi/Desktop/PFE_TCE/Main/csv_register/LIMITE.csv") as file_csv:
        cmp = csv.DictReader(file_csv)
        for i in cmp:
            for j in listli:
                return i[j]


def write_limite(limite):
    with open("/home/pi/Desktop/PFE_TCE/Main/csv_register/LIMITE.csv", "w") as file_csv:
        wrt = csv.DictWriter(file_csv, fieldnames=listli)
        wrt.writeheader()
        wrt.writerows(limite)


def write_csv(COMPTEUR):
    with open("/home/pi/Desktop/PFE_TCE/Main/csv_register/COMPTAGE.csv", "w") as file_csv:
        wrt = csv.DictWriter(file_csv, fieldnames=listcp)
        wrt.writeheader()
        wrt.writerows(COMPTEUR)


def read_display_csv():
    with open("/home/pi/Desktop/PFE_TCE/Main/csv_register/COMPTAGE.csv") as file_csv:
        cmp = csv.DictReader(file_csv)
        z = 1
        for i in cmp:
            for j in listcp:
                x = j + str(i[j])
                lcd.lcd_display_string(x, z, 0)
                z += 1


def RazPartiel(nombrepartiel, nombretotal):
    lcd.lcd_clear()
    lcd.lcd_display_string("Please enter    ", 1, 0)
    lcd.lcd_display_string("PIN PASSWRD:", 2, 0)
    seq = []

    for i in range(len(password)):
        digit = None
        while digit in ["A", "B", "C", "D", "*", "#"] or digit is None:
            digit = keypad.getKey()
        seq.append(digit)
        lcd.lcd_display_string('*', 2, i+12)
        time.sleep(0.4)
    if seq == password:
        lcd.lcd_clear()
        lcd.lcd_display_string("Termine", 2, 0)
        nombrepartiel = 0
        COMPTEUR = [{"Total:": nombretotal, "Partiel:": nombrepartiel}]
        write_csv(COMPTEUR)
        time.sleep(1)
        lcd.lcd_clear()
        read_display_csv()
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("incorrecte", 2, 0)

        time.sleep(1)
        lcd.lcd_clear()
        read_display_csv()


def Razlimite(Nblimite):
    seq = []
    digit = None
    lcd.lcd_clear()
    lcd.lcd_display_string("Please enter    ", 1, 0)
    lcd.lcd_display_string("PIN PASSWRD:", 2, 0)
    for i in range(len(password)):
        digit = None
        while digit in ["A", "B", "C", "D", "*", "#"] or digit is None:
            digit = keypad.getKey()
        seq.append(digit)
        lcd.lcd_display_string('*', 2, i+12)
        time.sleep(0.4)
    if seq == password:
        lcd.lcd_clear()
        lcd.lcd_display_string("RAZ termine", 2, 0)
        Nblimite = Limite_base
        limite = [{"Nblimite:": Nblimite}]
        write_limite(limite)
        time.sleep(1)
        lcd.lcd_clear()
        read_display_csv()
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("incorrecte", 2, 0)
        time.sleep(1)
        lcd.lcd_clear()
        read_display_csv()


def AddToLimite(Nblimite):
    seq = []
    st = ''
    lcd.lcd_clear()
    lcd.lcd_display_string("Please enter    ", 1, 0)
    lcd.lcd_display_string("PIN PASSWRD:", 2, 0)
    for i in range(len(password)):
        digit = None
        while digit in ["A", "B", "C", "D", "*", "#"] or digit is None:
            digit = keypad.getKey()
        seq.append(digit)
        lcd.lcd_display_string("*", 2, i+12)
        time.sleep(0.4)
    if seq == password:
        lcd.lcd_clear()
        lcd.lcd_display_string("Please enter    ", 1, 0)
        lcd.lcd_display_string("NBR to add: ", 2, 0)
        for i in range(4):
            digit = None
            while digit in ["A", "B", "C", "D", "*", "#"] or digit is None:
                digit = keypad.getKey()
            st += digit
            lcd.lcd_display_string(digit, 2, i+11)
            time.sleep(0.4)
        NB = int(st)
        Nblimite += NB
        limite = [{"Nblimite:": Nblimite}]
        write_limite(limite)
        lcd.lcd_clear()
        lcd.lcd_display_string("termine", 1, 0)
        time.sleep(1.5)
        read_display_csv()
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("incorrecte", 2, 0)
        time.sleep(1)
        lcd.lcd_clear()
        read_display_csv()


try:
    read_display_csv()

    while True:

        input_state = GPIO.input(button)
        nombretotal = int(NbPar_tot_CSV()[0])
        nombrepartiel = int(NbPar_tot_CSV()[1])
        Nblimite = int(Nblimite_CSV())

        if Nblimite > nombrepartiel:
            mail_state = False
            GPIO.output(RLin, GPIO.LOW)
            GPIO.output(green_led, GPIO.HIGH)
            GPIO.output(red_led, GPIO.LOW)
            if input_state == False:
                # print('ok')
                nombretotal += 1
                nombrepartiel += 1
                COMPTEUR = [{"Total:": nombretotal,
                            "Partiel:": nombrepartiel}]
                write_csv(COMPTEUR)
                time.sleep(0.2)

                read_display_csv()
            if nombrepartiel == 0 and mail_on_state == False:
                if mail_send_ssl.connect():
                    mail_send_ssl.send_mail_TCE_on()
                    lcd.lcd_clear()
                    lcd.lcd_display_string('mail alert!', 2, 0)
                    mail_on_state = True
                    time.sleep(2)
                    lcd.lcd_clear()
                    read_display_csv()
                else:
                    lcd.lcd_display_string('No Internet!', 2, 0)
                    mail_on_state = True
                    time.sleep(2)
                    lcd.lcd_clear()
                    read_display_csv()
            if Nblimite-5 == nombrepartiel and mail_warning_state == False:
                if mail_send_ssl.connect():
                    mail_send_ssl.send_mail_warning()
                    lcd.lcd_clear()
                    lcd.lcd_display_string('mail alert!', 2, 0)
                    mail_on_state = True
                    time.sleep(2)
                    lcd.lcd_clear()
                    read_display_csv()
                    mail_warning_state = True

        else:
            mail_warning_state = False
            mail_on_state = False
            GPIO.output(green_led, GPIO.LOW)
            GPIO.output(red_led, GPIO.HIGH)
            lcd.lcd_clear()
            lcd.lcd_display_string('TCE bloque', 1, 0)
            GPIO.output(RLin, GPIO.HIGH)
            time.sleep(0.2)
            # lcd.lcd_clear()
            # read_display_csv()
            # time.sleep(1.5)
            if mail_state == False:
                if mail_send_ssl.connect():
                    mail_send_ssl.send_mail()
                    lcd.lcd_clear()
                    lcd.lcd_display_string('mail alert!', 2, 0)
                    mail_state = True
                    time.sleep(2)
                else:
                    lcd.lcd_display_string('No Internet!', 2, 0)
                    mail_state = True
                    time.sleep(2)
        if keypad.getKey() == "A":  # RAZ
            RazPartiel(nombrepartiel, nombretotal)
        elif keypad.getKey() == "B":  # raz de limite
            Razlimite(Nblimite)
        elif keypad.getKey() == "C":  # ajoute a limite
            AddToLimite(Nblimite)


except KeyboardInterrupt:
    lcd.lcd_clear()
    GPIO.cleanup()
