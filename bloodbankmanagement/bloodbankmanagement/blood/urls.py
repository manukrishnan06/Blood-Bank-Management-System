from django.urls import path
from blood import views



urlpatterns = [

    path('indexfn/',views.indexfn,name="indexfn"),
    path('donorfn/',views.donorfn,name="donorfn"),
    path('davedonorfn/',views.davedonorfn,name="davedonorfn"),
    path('displaydonorfn/',views.displaydonorfn,name="displaydonorfn"),
    path('displaypatientfn/',views.displaypatientfn,name="displaypatientfn"),
    path('editpatientfn/<int:pid>/',views.editpatientfn,name="editpatientfn"),
    path('updatepatientfn/<int:pid>/',views.updatepatientfn,name="updatepatientfn"),
    path('editdonorfn/<int:did>/',views.editdonorfn,name="editdonorfn"),
    path('updatedonorfn/<int:did>/',views.updatedonorfn,name="updatedonorfn"),
    path('displaydonations/',views.displaydonations,name="displaydonations"),
    path('displaybloodRequests/',views.displaybloodRequests,name="displaybloodRequests"),
    path('approverequest/<int:sid>/',views.approverequest,name="approverequest"),
    # path('savedapproverequest/<int:sid>/',views.savedapproverequest,name="savedapproverequest")
    path('deletedonorfn/<int:did>/', views.deletedonorfn, name='deletedonorfn'),

]