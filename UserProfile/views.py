from django.shortcuts import render
from django.contrib.auth.models import User
from discussion.models import Analyser, Follow
from django.views.generic.base import View
from django.views.generic.edit import UpdateView

# Create your views here.

class UserProfile(View):

	def get(self, request):
		user = self.request.user
		analyser = Analyser.objects.get(user=user)
		following = Follow.objects.filter(follower = analyser)
		return render(request, 'UserProfile/profile.html', {'user':user, 'analyser':analyser, 'following':following})

 


