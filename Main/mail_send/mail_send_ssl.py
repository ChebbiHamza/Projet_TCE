# Importer les modules
import smtplib
import ssl
# email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# La bibliothèque pandas sert uniquement à générer la date actuelle, ce qui n'est pas nécessaire pour envoyer des e-mails
import pandas as pd
# atttch
from email.mime.application import MIMEApplication
import csv
import urllib.request


def connect(host='http://google.com'):  # vérifier l'accés internet
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


def send_mail():

    a = pd.read_csv("/home/pi/Desktop/PFE_TCE/Main/csv_register/COMPTAGE.csv")
    a.to_html("/home/pi/Desktop/PFE_TCE/Main/csv_register/Table.html")
    html_file = a.to_html()
    with open("/home/pi/Desktop/PFE_TCE/Main/csv_register/Table.html", 'r') as html_file:
        html_file_content = html_file.read()

    # defenir le document HTML
    html = """\
        <html>
            
            </head>
            <body>
                <h1><mark style="color:red">  TCE arrêté ! </mark> </h1>
                <h3>
                <p>TCE a atteint la limite des nombres des câbles partiels testés, une intervention est nécessaire, </p>
                <p>vérifier ci-dessous le nombre partiel et total atteint: </p>
                </h3>
                {html_file_content}
            </body>
        </html>
        """.format(html_file_content=html_file_content)

    ########################################
    email_from = "raspberrypiTCE@gmail.com"
    password = "pi@raspberrypi"            #
    email_to = "chebihamza926@gmail.com"  #
    ########################################

# Générez la date d'aujourd'hui à inclure dans l'objet de l'e-mail
    date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

# Créez une classe MIMEMultipart et configurez les champs From, To, Subject
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'Alerte sur létat du machine TCE - {date_str}'

# Joignez le document html défini précédemment, en tant que type de contenu html MIMEText au message MIME
    email_message.attach(MIMEText(html, "html"))
    #email_message.attach(MIMEText(filecontent, "html"))


# Convertez le message comme string
    email_string = email_message.as_string()

# Connecter au serveur SMTP de Gmail et envoyez un e-mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)
