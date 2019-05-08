from __future__ import unicode_literals
import os
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.views.static import serve
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from .search_song import accuracy_calculator


def music_retrieval(request):
	if request.method == 'POST':
		data = request.POST
		try:
			myfile = request.FILES['image']
		except:
			messages.warning(request, 'Invalid Question')
			return redirect(request.META.get('HTTP_REFERER'))
		
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		l, scores = accuracy_calculator()
		if l is not None:
			for i, j in zip(l, scores):
				messages.success(request, i+" \t\tScore: " + str(j))
		fs.delete(myfile.name)
	return render(request, 'project/music_retrieval.html')