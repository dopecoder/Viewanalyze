from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms, models
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.contrib.auth.models import User
from registration import formProcessor
from django.core.urlresolvers import reverse
from registration.forms import MailForm
from django.core.exceptions import ObjectDoesNotExist
import datetime
# Create your views here.

nextLink = ''

class LoginFormView(View):

    def __init__(self, *args, **kwargs):
        super(LoginFormView, self).__init__(**kwargs)
        self.nextLink = ''

    def get(self, request):
        if 'next' in request.GET:
            print request.GET['next']
            global nextLink
            nextLink = request.GET['next']
            #request.sessions['next'] = request.GET['next']
        else:
            nextLink = ''

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))
        form = forms.LoginForm
        return render(request, 'authentication/login_form.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            cleanForm = form.cleaned_data
            print "Cleaned from"
            try:
                user = User.objects.get(email=cleanForm['email'])
                if user.check_password(cleanForm['password']):
                    if user.is_active:
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        if cleanForm.get('remember_me'):
                            request.session.set_expiry((60 * 60 * 24 * 30))
                        else:
                            request.session.set_expiry(0)

                        login(request, user)

                        global nextLink
                        if nextLink != '':
                            print "nextLink -> %s" % nextLink
                            return HttpResponseRedirect(nextLink)
                        return HttpResponseRedirect('/discussion/')
                    else:
                        return render(request, 'authentication/login_form.html', {'form':form, 'errors':['You have not confirmed you email address.',]})
                else:
                    return render(request, 'authentication/login_form.html', {'form':form, 'errors':['This is an invalid email or password.',]})
            
            except ObjectDoesNotExist:
                return render(request, 'authentication/login_form.html', {'form':form, 'errors':['Please register.',]})

def log_out(request):
    logout(request)
    return render(request, 'authentication/login_form.html',{'form':forms.LoginForm})

class PasswordResetView(View):

    def get(self, request):

        form = MailForm()
        return render(request, 'authentication/reset_password.html', {'form':form,})


    def post(self, request):

        form = MailForm(request.POST)

        if form.is_valid():
            cleanedForm = form.cleaned_data
            try:
                user = User.objects.get(email = cleanedForm.get('email'))
                #generate a reset passcode
                reset_code = formProcessor.generateResetCode(user.username, str(datetime.datetime.now()))
                #send the main to the email with reset passcode
                link = 'http://www.viewanalyse.com/authentication/password/reset/' + reset_code
                subject = 'Password reset for viewanalyse.com'
                body = 'A password reset request was sent to this email. If you have sent it, please click on the link ' + link + ' Or please ignore it and we are sorry for the inconvienience we have caused you.'
                formProcessor.send_email(subject, body, 'registration@viewanalyse.com', [cleanedForm.get('email')])
                #save the details in ResetPassword db
                passwordReset = models.PasswordReset(user = user, email = cleanedForm.get('email'), reset_code = reset_code, reset_status = "True")
                passwordReset.save()
                #return render with message giving them instructions
                return render(request, 'authentication/reset_password.html', {'message':['We have sent you a password reset link to your email address.',]})
            except ObjectDoesNotExist:
                #return render with message "Please check the entered email."
                return render(request, 'authentication/reset_password.html', {'form': form, 'message':['Make sure you have entered a registered email address.',]})
        else:
            return render(request, 'authentication/reset_password.html', {'form': form, 'message':['Make sure you have entered a valid email address.',]})


class PasswordResetActivationView(View):
    
    def get(self, request, *args, **kwargs):
        reset_code = self.kwargs['resetcode']
        try:
            passwordReset = models.PasswordReset.objects.get(reset_code = reset_code)
            form = forms.PasswordResetForm()
            return render(request, 'authentication/password_reset.html', {'form':form})
        except ObjectDoesNotExist:
            return render(request, 'authentication/password_reset.html', {'form':form, 'message':['Please reset the password again',]})

    def post(self, request, *args, **kwargs):
        form = forms.PasswordResetForm(request.POST)

        if form.is_valid():
            cleanedForm = form.cleaned_data

            if not formProcessor.passwordMatch(cleanedForm.get('password'), cleanedForm.get('re_password')):
                return render(request, 'authentication/password_reset.html', {'form':form, 'message':['You passwords don\'t match.']}) 
            try:
                passwordReset = models.PasswordReset.objects.get(reset_code = self.kwargs['resetcode'])
                if passwordReset.email == cleanedForm.get('email'):
                    user = User.objects.get(email = cleanedForm.get('email'))
                    user.set_password(cleanedForm.get('password'))
                    user.save()
                    return render(request, 'authentication/password_reset_successful.html')
                else:
                    return render(request, 'authentication/password_reset.html', {'form':form, 'message':['You have to enter the email address associated with the account.']})
            except ObjectDoesNotExist:
                return render(request, 'authentication/password_reset.html', {'form':form, 'message':['Something went wrong! make sure you have enter valid email address and try again.']})
        else:
            return render(request, 'authentication/password_reset.html', {'form':form, 'message':['Make sure you have entered valid email and password.']})        
