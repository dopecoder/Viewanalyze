import re, hashlib
from django.contrib.auth.models import User

def validateUsername(username):
    if re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$", username):
        users = User.objects.all()
        for user in users:
            if username == user.username:
                return "Username already exists"
        return "True"
    else:
        return "False"

def validateUniqueEmail(email):
    users = User.objects.all()
    for user in users:
        if user.email == email:
            return False
    return True

def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def passwordMatch(password, re_password):
    if password == re_password:
        return True
    else:
        return False

def generateActivationCode(email_username, email, timeObject):
    activation_intermediate = email_username + email + timeObject
    hash = hashlib.sha256(activation_intermediate).hexdigest()
    return hash

def generateResetCode(username, timeObject):
    reset_intermediate = username + timeObject
    hash = hashlib.sha256(reset_intermediate).hexdigest()
    return hash

def getActivationLink(activation_code):
    link = 'http://www.viewanalyse.com/registration/activation/'+ activation_code
    return link    

def send_email(A_SUBJECT, A_BODY, A_FROM, A_TO):
    import smtplib

    gmail_user = "nitzzyhr@gmail.com"
    gmail_pwd = "proton1024"
    FROM = A_FROM #'nitzzyhr@gmail.com'
    TO = A_TO #['nithinhr@outlook.com'] #must be a list
    SUBJECT = A_SUBJECT #"Testing sending using gmail"
    TEXT = A_BODY #"Testing sending mail using gmail servers"

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        #server = smtplib.SMTP(SERVER) 
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        #return render(request, 'registration/mail.html', {'error':'successfully sent the mail'})
        return True
    except:
        #return render(request, 'registration/mail.html', {'error':'failed to send the mail'})
        return False     