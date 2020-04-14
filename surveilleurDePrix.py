# This script checks the price of an article on the LDLC website, and send it by mail if it's under a certain value.
# Each article page on the website has the same structure.


# YOU JUST NEED TO FILL THE VARIABLE WITH YOUR MAILING INFORMATIONS. (and you have to allow connection here if you're using gmail: https://www.google.com/settings/security/lesssecureapps)
myMail = "" # Your mail.
myPASSWORD = "" # Your password.
mailTo = "" # Receiver.
subject = "Daily price of the article" # Message's subject.
msgContent = "The daily price of the article is : " # Message's content.
cc = "" # Attached receivers.
maxValue = 1500 # The value from which you want to be notified.


from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Get the url of the page. (Change it to get the article you want)
url = "https://www.ldlc.com/fr-be/fiche/PB00260401.html"

# Create the request to send.
request = requests.get(url)

# We want the content of the targeted page.
page = request.content

# We now need to parse that content.
soup = BeautifulSoup(page, "html.parser")

# We want the price of the article. (no id for the price here, we have to get all the price classed elements...)
htmlTag = soup.findAll("div", {"class":"price"})
elemPriceHtml = str(htmlTag[4]) # Retrieves the price at the right side of the web page.

# Extract the price.

i = 0
priceValues = []
while (i < len(elemPriceHtml)):
    number = ""
    while(ord(elemPriceHtml[i]) >= 48 and ord(elemPriceHtml[i]) <= 57):
        number += elemPriceHtml[i]
        i += 1
    if(number != ""):
        priceValues.append(number)
    i += 1

price = ".".join(priceValues)
msgContent += str(price) # Add the price in the message to send.

# Define the value that interests us.
maxValue = 1500

# Send a mail if the value is smaller or equal to the wanted price.
if (float(price) <= maxValue):
    message = MIMEMultipart()
    message["From"] = myMail
    message["To"] = mailTo
    message["Subject"] = subject
    message.attach(MIMEText(msgContent.encode('utf-8'), 'plain', 'utf-8'))


    serveur = smtplib.SMTP('smtp.gmail.com', 587)
    serveur.starttls() 
    serveur.login(myMail, myPASSWORD)
    text = message.as_string().encode('utf-8')
    receivers = mailTo
    serveur.sendmail(myMail, receivers, text)
    serveur.quit()



    


