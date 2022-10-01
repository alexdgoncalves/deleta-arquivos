import os
import smtplib,ssl
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


path = 'C:/Users/alex.goncalves/Downloads/backup'

sevenDaysAgo = (date.today() - timedelta(7))
fmt = '%d/%m/%Y'
log = ""
totalSize = 0


port = 465
smtp_server = "smtp.gmail.com"
sender_email = ""  # Enter your address
receiver_email = ""  # Enter receiver address
password = ""



message = MIMEMultipart("alternative")
message["Subject"] = "Arquivos backup deletados Allims"
message["From"] = sender_email
message["To"] = receiver_email



for root, directories, files in os.walk(path):
        for name in files:
            path_file = os.path.join(root, name)
            size = "{:.2f}".format(os.stat(path_file).st_size / (1024 * 1024))
            timestamp = os.path.getmtime(path_file)
            modificationTime = datetime.fromtimestamp(timestamp).date()
            if modificationTime < sevenDaysAgo :
                totalSize += os.stat(path_file).st_size / (1024 * 1024)
                log += "<tr><td align='center'>"+name+"</td><td align='center'>"+ modificationTime.strftime(fmt)+ "</td><td align='center'>"+size +" mb</td></tr>"
                ##os.remove(path_file)
              

# Create the plain-text and HTML version of your message

html = """\
<html>
	<body>
		<table cellpadding="0" cellspacing="0" width="640" align="center" border="1">
			<thead>
				<tr style="font-size:20px">
					<th>Nome do arquivo</th>
                    <th>Ultima modificação</th>
					<th>Tamanho do arquivo</th>
				</tr>
			</thead>
			<tbody>
				"""+log+"""	
                <tr><td colspan="3" align='center'><strong style="font-size:20px">Total liberado:<strong>    """+"{:.2f}".format(totalSize)+""" mb</td></tr>
			</tbody>
		</table>
	</tbody>
</html>
"""

# Turn these into plain/html MIMEText objects
part = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first

message.attach(part)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )