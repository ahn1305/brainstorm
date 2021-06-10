

def send_email_register(user_code,email,usr):
	import smtplib, ssl
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart

	code_r = user_code

	sender_email = "ab7710850@gmail.com"
	receiver_email = email
	password = "cr712345"

	message = MIMEMultipart("alternative")
	message["Subject"] = "Otp from brainstrom"
	message["From"] = sender_email
	message["To"] = receiver_email

	# Create the plain-text and HTML version of your message
	html = ("""\
			<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
  <div style="margin:50px auto;width:70%;padding:20px 0">
    <div style="border-bottom:1px solid #eee">
      <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Brainstrom</a>
    </div>
    <p style="font-size:1.1em">Welcome {},</p>
    <p>Thank you for choosing Us. Use the following OTP to complete your Sign up procedures.
	<br> OTP is valid for 2 minutes</p>
    <h2 style="background: #00466a;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{}</h2>
    <p style="font-size:0.9em;">Regards,<br />Team Brainstrom</p>
    <hr style="border:none;border-top:1px solid #eee" />
    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
      <p>Brainstrom</p>
      <p>1600 Amphitheatre Parkway</p>
      <p>California</p>
    </div>
  </div>
</div>
	
	""").format(usr,code_r)

	# Turn these into plain/html MIMEText objects
	part1 = MIMEText(html, "html")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(
			sender_email, receiver_email, message.as_string()
		)

def send_email_login(user_code,email,usr):
	import smtplib, ssl
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart

	code_l = user_code

	sender_email = "ab7710850@gmail.com"
	receiver_email = email
	password = "cr712345"

	message = MIMEMultipart("alternative")
	message["Subject"] = "Otp from brainstrom"
	message["From"] = sender_email
	message["To"] = receiver_email

	# Create the plain-text and HTML version of your message
	html = ("""\
		<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
  <div style="margin:50px auto;width:70%;padding:20px 0">
    <div style="border-bottom:1px solid #eee">
      <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Brainstrom</a>
    </div>
    <p style="font-size:1.1em">Hi {},</p>
    <p>Use the following OTP to complete your Login. 
    <br>OTP is valid for 2 minutes</p>
    <h2 style="background: #00466a;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{}</h2>

	<p>If you didn't request this, you can ignore this email or let us know.</p>
    <p style="font-size:0.9em;">Regards,<br />Team Brainstrom</p>
    <hr style="border:none;border-top:1px solid #eee" />
    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
      <p>Brainstrom</p>
      <p>1600 Amphitheatre Parkway</p>
      <p>California</p>
    </div>
  </div>
</div>	
	""").format(usr,code_l)

	# Turn these into plain/html MIMEText objects
	part1 = MIMEText(html, "html")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(
			sender_email, receiver_email, message.as_string()
		)