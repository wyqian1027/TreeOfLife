from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
	path('', views.index, name='homepage'),
	path('register/', views.register_request, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path('acount/', views.account, name='login'),
	path('category/<cat_name>', views.find_category, name='findCat'),
	path('new_category', views.add_new_category, name='addCat'),
	path('category/new/<parent_name>', views.add_new_category_by_parent, name='addCatByParent'),
	path('category/del/<cat_name>', views.delete_category, name='delCat'),
	path('category/edit/<cat_name>', views.edit_category, name='editCat'),
	path('all_category', views.show_all, name='showAll'),
]

