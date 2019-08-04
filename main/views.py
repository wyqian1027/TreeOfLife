from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import Q


from .models import Category, Hierarchy
from .forms import NewUserForm, NewCatForm, NewCatFormByParent


# aux functions
def displayHierarchy(cat_name):
	s = ""
	cat_objects = Category.objects.filter(category_name=cat_name)
	if len(cat_objects) == 1:
		cat_object = cat_objects[0]
		cur   = cat_object
		count = 0
		while cur.category_name != "root":
			cur = cur.category_parent
			count += 1

		cur   = cat_object
		# arrow = " -> "
		arrow = " <i class='material-icons'>subdirectory_arrow_right</i> "

		delim = "&nbsp;&nbsp;&nbsp;"
		if cur.category_name != "root":
			url = "<a href='/category/tmp'>tmp</a>".replace("tmp", cur.category_name)
			s += delim*count + arrow + url + "(" + cur.hierarchy.hierarchy_name + ")"
			count -= 1

		while cur.category_parent.category_name != "root":
			cur = cur.category_parent
			url = "<a href='/category/tmp'>tmp</a>".replace("tmp", cur.category_name)
			s = delim*count + arrow + url + "(" + cur.hierarchy.hierarchy_name + ")" + "<br>" + s
			count -= 1
	return s


# We use RESTFUL framework in realizing CRUD operations:
#
#  - INDEX
#  - NEW
#  - ADD
#  - SHOW
#  - EDIT
#  - UPDATE
#  - DELETE

############## Category Model  ##############

def existsCategory(cat_name):
	return Category.objects.filter(category_name=cat_name).count() > 0

def getSubCounts(cat_name):
	return Category.objects.filter(category_parent__category_name=cat_name).count()


# INDEX: index page for rendering all related categories
def index(request):
	return render(request=request,
				  template_name="main/index.html",
				  context={"cats"     : Category.objects.filter(category_parent__category_name="root"),
						   "current"  : Category.objects.filter(category_name="root")[0],
						   "subCounts": len(Category.objects.filter(category_parent__category_name="root"))})

# INDEX: find sub-categories of cat_name and rendering via index route
def find_category(request, cat_name):

	if not cat_name or cat_name == "root": 
		return redirect("main:homepage")

	if not existsCategory(cat_name):
		messages.error(request, f"Category {cat_name} does not exist.")
		return redirect("main:homepage")

	matching_items = Category.objects.filter(category_parent__category_name=cat_name)
	current_item   = Category.objects.filter(category_name=cat_name)[0]
	subCounts = len(Category.objects.filter(category_parent__category_name=current_item))
	return render(request,
				"main/index.html",
				{"cats"     : matching_items,
				 "current"  : current_item,
				 "subCounts": subCounts,
				 "evoPath"  : displayHierarchy(cat_name)})	


# NEW/ADD: add any category anywhere in the tree
def add_new_category(request):

	if request.method == "POST":
		form = NewCatForm(request.POST)
		if form.is_valid():
			print("form is valid")
			newCat = form.save(commit=False)
			newCatName = newCat.category_name
			newCatParent = newCat.category_parent.category_name
			
			# checking cur category is duplicated
			if existsCategory(newCatName):
				messages.error(request, f"Category {newCatName} is already present.")
				dupParent = Category.objects.get(category_name=newCatName).category_parent.category_name
				return redirect(f"/category/{dupParent}")

			newCat.created_by = request.user
			newCat.description = form.cleaned_data.get('description')
			newCat.save()
			messages.success(request, f"Category {newCatName} added.") 
			return redirect(f"/category/{newCatParent}")
		else:
			print("form is NOT valid")
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")
			return redirect("main:homepage")	    	

	form = NewCatForm()
	return render(request=request,
				template_name="main/cat_add_form.html",
				context={"form": form})


# NEW/ADD: add only category to parent category one clicked
def add_new_category_by_parent(request, parent_name):
	if request.method == "POST":
		form = NewCatFormByParent(request.POST)
		if form.is_valid():
			newCat = form.save(commit=False)
			newCatName = newCat.category_name

			# checking parent category
			if not existsCategory(parent_name):
				messages.error(request, f"Parent {parent_name} is not valid.")
				messages.error(request, f"Using general form for adding category.")
				return redirect("main:addCat")

			# if valid, set parent
			newCat.category_parent = Category.objects.get(category_name=parent_name)
			
			# checking cur category is duplicated
			if existsCategory(newCatName):
				messages.error(request, f"Category {newCatName} is already present.")
				dupParent = Category.objects.get(category_name=newCatName).category_parent.category_name
				return redirect(f"/category/{dupParent}")

			newCat.created_by = request.user
			newCat.description = form.cleaned_data.get('description')
			newCat.save()
			messages.success(request, f"Category {newCatName} added to {parent_name}.") 
			return redirect(f"/category/{parent_name}")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")
			return redirect(f"/category/{parent_name}")	    	

	form = NewCatFormByParent()
	return render(request=request,
				template_name="main/cat_add_form_by_parent.html",
				context={"form"		  : form,
						 "parent_name": parent_name})

# DELETE
def delete_category(request, cat_name):

	# check existence
	if not existsCategory(cat_name):
		messages.error(request, f"Category {cat_name} does not exist.")
		return redirect("main:homepage")

	catObj = Category.objects.get(category_name=cat_name)
	catParent = catObj.category_parent.category_name

	# check not root
	if catParent == "root":
		messages.error(request, f"Category is protected.")
		return redirect(f"/category/{cat_name}")
	
	# make sure no sub categories
	if getSubCounts(cat_name) > 0:
		messages.error(request, f"Cannot delete {cat_name}. Must delete all sub-categories first.")
		return redirect(f"/category/{cat_name}")

	# verify username
	if catObj.created_by.username == request.user.username or request.user.is_superuser:
		catObj.delete()
		messages.success(request, f"Category {cat_name} is deleted by {request.user.username}")
		return redirect(f"/category/{catParent}")
	else:
		messages.error(request, f"You are not authorized to DELETE {cat_name}")
		return redirect(f"/category/{cat_name}")


# EDIT/UPDATE
def edit_category(request, cat_name):

	# check existence
	if not existsCategory(cat_name):
		messages.error(request, f"Category {cat_name} does not exist.")
		return redirect("main:homepage")	

	catObj = Category.objects.get(category_name=cat_name)

	# check authorization:
	if catObj.created_by.username != request.user.username and not request.user.is_superuser:
		messages.success(request, f"You are not authorized to EDIT {cat_name}")
		return redirect(f"/category/{cat_name}")

	if request.method == "POST":
		form = NewCatForm(request.POST)
		if form.is_valid():
			print("form is valid")
			newCat = form.save(commit=False)
			newCatName = newCat.category_name

			# checking cur category is duplicated
			if cat_name != newCatName and existsCategory(newCatName):
				messages.error(request, f"Category {newCatName} is already used. Please use another name.")
				return redirect(f"/category/{cat_name}")

			catObj.category_name = newCat.category_name
			catObj.category_parent = newCat.category_parent
			catObj.hierarchy = newCat.hierarchy
			catObj.description = newCat.description
			catObj.image_description = newCat.image_description
			catObj.image_address = newCat.image_address
			catObj.created_by = request.user
			catObj.create_date = now()
			catObj.save()

			messages.success(request, f"Successfully editted Category {newCatName}.") 
			return redirect(f"/category/{newCatName}")
		else:
		
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")
			return redirect(f"/category/{cat_name}")


	data_dict = {"category_name"    : catObj.category_name,
				"category_parent"   : catObj.category_parent.pk,
				"hierarchy"			: catObj.hierarchy.pk,
				"description"		: catObj.description,
				"image_address"		: catObj.image_address,
				"image_description"	: catObj.image_description}

	form = NewCatForm(initial=data_dict)
	return render(request=request,
				template_name="main/cat_edit_form.html",
				context={"form"		: form,
						 "cat_name" : cat_name})


# SHOWALL
def show_all(request):
	allObjs = Category.objects.filter(~Q(category_name="root")).order_by('-create_date')
	return render(request=request,
				  template_name="main/index.html",
				  context={"cats"   : allObjs,
				  		   "display": "none",
				  		   "total"  : allObjs.count()})
	







############## User Authentication, Login, Logout  ##############

def account(request):
	catCounts = len(Category.objects.filter(created_by__username=request.user.username))
	return render(request, 
		'main/account.html', 
		{"catCounts" : catCounts})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New Account created {username}")
			login(request, user)
			messages.info(request, f"You are now logged in as {username}")
			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")

	form = NewUserForm() 
	return render(request=request,
				template_name="main/register.html",
				context={"form": form})
def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("main:homepage")


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid username or password")
		else:
			messages.error(request, "Invalid username or password")

	form = AuthenticationForm()
	return render(request, 
				"main/login.html", 
				{"form": form})
