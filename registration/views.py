from django.shortcuts import render
import datetime, hashlib
import re
from django.http import HttpResponseRedirect
from personalization import views as personalize
from django.views.generic.base import View
from . import forms, models, formProcessor
from discussion.models import Analyser
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class RegistrationView(View):

    def get(self, request):
        form = forms.RegistrationForm
        return render(request, 'registration/registrationform.html', {'form':form})

    def post(self, request):
        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            cleanedForm = form.cleaned_data
            print "form is valid"

            if not formProcessor.passwordMatch(cleanedForm.get('password'), cleanedForm.get('re_password')):
                return render(request, 'registration/registrationform.html', {'form':form, 'errors':['Your passwords don\'t match.']})
            else:
                validateusername = formProcessor.validateUsername(cleanedForm.get('email'))
                if validateusername == "False":
                    return render(request, 'registration/registrationform.html', {'form':form, 'errors':['enter a valid email.']})               
                elif validateusername == "Username already exists":
                    return render(request, 'registration/registrationform.html', {'form':form, 'errors':['The email already exists.']})
                else:
                    if not formProcessor.validateUniqueEmail(cleanedForm.get('email')):
                        return render(request, 'registration/registrationform.html', {'form':form, 'errors':['You have already registered with this email',]})
                    else:
                        user = User.objects.create_user(cleanedForm.get('email'), cleanedForm.get('email'), cleanedForm.get('password'))
                        user.first_name = cleanedForm.get('first_name')
                        user.last_name = cleanedForm.get('last_name')
                        user.is_active = False
                        user.save()

                        name = cleanedForm.get('first_name') + ' ' + cleanedForm.get('last_name')
                        analyser = Analyser(user = user,
                                            name = name,
                                            email = cleanedForm.get('email'),
                                            #country = cleanedForm.get('country'),
                                            #dob = cleanedForm.get('dob'),
                                            )
                        analyser.save()

                        activation_code = formProcessor.generateActivationCode(cleanedForm.get('email'), cleanedForm.get('email'), str(datetime.datetime.now()))
                        #activation_code = cleanedForm.get('username') + cleanedForm('email') + datetime.datetime()

                        tempregistration = models.TempRegistration(user = user, email = cleanedForm.get('email'), activation_code = activation_code, activation_status="False")   
                        tempregistration.save() 

                        activation_link = formProcessor.getActivationLink(tempregistration.activation_code)

                        subject = 'Account activation for viewanalyse.com'
                        body = 'Thank you for registering with viewanalyse.com\n' + cleanedForm.get('first_name') + 'your link is ' + activation_link + '\nThank You.'

                        formProcessor.send_email(subject, body, 'registration@viewanalyse.com', [cleanedForm.get('email')])

                        #send_mail(subject, body, 'registration@viewanalyse.com', cleanedForm.get('email'), fail_silently=False)
                        url = 'http://10.252.16.244' + '/registration/registration-successful'
                        return HttpResponseRedirect(url)
        else:
            print form.data['first_name']
            print form.data['last_name']
            #print form.data['username']
            print form.data['email']
            print form.data['password']
            print form.data['re_password']
            #print form.data['dob']
            #print form.data['country']
            return render(request, 'registration/registrationform.html', {'form':form, 'errors':['The form is not valid.']})


class ActivationView(View):

    def get(self, request, *args, **kwargs):
        activation_code = self.kwargs['activationcode']
        try:
            registrar = models.TempRegistration.objects.get(activation_code = activation_code)
            if registrar.activation_status == 'False':
                delta = datetime.date.today() - registrar.registered_on 
                if(delta.days <= settings.ACCOUNT_ACTIVATION_DAYS):
                    user = User.objects.get(pk = registrar.user.pk)
                    user.is_active = True
                    user.save()

                    registrar.activation_status = 'True'
                    registrar.save()

                    url = 'http://10.252.16.244' + '/registration/activation-successful'
                    return HttpResponseRedirect(url)
                else:
                    return render(request, 'registration/registration_failure.html', {'reasons':['Your registration has expired. please register again!',]})
            else:
                    return render(request, 'registration/registration_failure.html', {'reasons':['Your have already registered!',]})

        except ObjectDoesNotExist:
            return render(request, 'registration/registration_failure.html', {'reasons':['You have not registered! Please register.',]})


def registation_successful(request):
    return render(request, 'registration/registration_successful.html')

def activation_successful(request):
    return render(request, 'registration/activation_successful.html')

#Need to configure resend_email
class resend_email(View):

    def get(self, request):

        form = forms.MailForm()
        return render(request, 'registration/resend_email.html', {'form':form})

    def post(self, request):
        form = forms.MailForm(request.POST)

        if form.is_valid():
            cleanedForm = form.cleaned_data
            try:
                registrar = models.TempRegistration.objects.get(email = cleanedForm.get('email'))
                if registrar.activation_status == 'False':
                    subject = 'Account activation for viewanalyse.com'
                    body = 'Thank you for registering with viewanalyse.com\n' + registrar.user.first_name + 'your link is ' + registrar.activation_code + '\nThank You.'
                    formProcessor.send_email(subject, body, 'registration@viewanalyse.com', [registrar.email])
                    return render(request, 'registration/resend_email.html', {'message':['The activation link has been sent to email!',]})
                else:
                    return render(request, 'registration/resend_email.html', {'message':['Your account has already been activated.',]})    

            except ObjectDoesNotExist:
                return render(request, 'registration/resend_email.html', {'form':form, 'message':['Please enter the valid email you have registered with!',]})

        else:
            return render(request, 'registration/resend_email.html', {'form':form, 'message':['Something went wrong! please make sure you have entered a valid email address.',]})
 


