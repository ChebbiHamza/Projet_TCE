# Import modules
import smtplib
import ssl
# email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# The pandas library is only for generating the current date, which is not necessary for sending emails
import pandas as pd
# atttch
from email.mime.application import MIMEApplication
import csv
import urllib.request


def connect(host='http://google.com'):  # to check if there is internet acces
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


def send_mail():
    # Define the HTML document
    html = '''
        <html>
    
            <body>
                <h1><mark style="color:red">  TCE arrêté ! </mark> </h1>
                <h3>
                <p>TCE a atteint la limite des nombres des câbles partiels testés, une intervention est nécessaire, </p>
                <p>vérifier ci-dessous le nombre partiel et total atteint: </p>
                </h3>
            </body>
        </html>
        '''

    ########################################
    email_from = "raspberrypiTCE@gmail.com"
    password = "pi@raspberrypi"            #
    email_to = "chebihamza926@gmail.com"   #
    ########################################

# Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

# Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'Alerte sur létat du machine TCE - {date_str}'

# Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))


# next lines with convert the csv to html and attatch it
#a = pd.read_csv("/home/pi/Desktop/PFE_TCE/Main/csv_register/COMPTAGE.csv")
# a.to_html("COMPTAGE.html")
#email_message.attach(MIMEText(a, "html"))
#a = {}
#
#    csv_dict = csv.DictReader(csvfile)
#    a = {}
#    for i in csv_dict:
#        a.update(i)
#       # Define a function to attach files as MIMEApplication to the email
#      ##############################################################
# print(a)

    def attach_file_to_email(email_message, filename="/home/pi/Desktop/PFE_TCE/Main/csv_register/COMPTAGE.csv"):
        # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
        with open(filename, "rb") as f:
            file_attachment = MIMEApplication(f.read())

    # Add header/name to the attachments
        file_attachment.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
    # Attach the file to the message

        email_message.attach(file_attachment)


##############################################################
# call attach fct
    attach_file_to_email(email_message)

# Convert it as a string
    email_string = email_message.as_string()

# Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)
        server.sendmail(
            email_from, "mahfoudh.yassin2000@gmail.com", email_string)
