import smtplib, ssl
import os

#Change Email and Password for emails for errors on the site
email = "3760team11testing@gmail.com"
password = "yoloswagxd11"



port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = email
receiver_email = email


#change subject and body variables for custom text
Subject = "Error Testing Team 11\n"
Body = "Custom Body"
file = open('results.txt', 'r')
data = file.read()
file.close()

if not data:
    print("No email sent.")
else:
    message = """\
    Subject: """ + str(Subject) + "\n" + str(data)
    print(message)

    #sends email to specified account
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)