from django.urls import path
from userapp.views import *
from order.views import *

urlpatterns = [
    
    # User Home
    path('user/dashboard', userDashboard, name='userDashboard'),
    
    # User Ticket URLS
    path('user/dashboard/tickets', ticketList, name='userTickets'),
    path('user/dashboard/ticket/create/', userTicketCreate, name='userTicketCreate'),
    path('user/dashboard/ticket/view/<int:id>', userticketView, name='userticketView'),
    path('user/dashboard/delete/ticket/<int:id>', userTicketDelete , name='userTicketDelete'),
    path('ajax/reply/<int:id>', ajax_reply, name='ajax_reply'),

    # User Project URLS
    path('user/dashboard/projects', userProjects, name='userProjects'),
    path('user/dashboard/project/details/<slug:slug>', projectDetail, name='userProjectDetail'),
    
    # User Invoice URLS
    path('user/dashboard/invoices' ,userInvoices, name='userInvoices'),
    path('user/dashboard/invoice/view/<slug:slug>', viewUserPDFInvoice, name='viewUserPDFInvoice'),
    
    # User Payments URLS
    path('user/dashboard/payments', userPayments, name='userPayments'),
    
    # User Profile URLS
    path('user/dashboard/profile', customUserProfile, name='customUserProfile'),
    path('user/dashboard/profile/edit/', profile_edit_view, name='profile_edit'),
    
    # User Agreement URLS
    path('user/dashboard/agreements', userAgreements, name='userAgreements'),
    path('user/dashboard/agreement/view/<int:id>', userAgreementDetail, name='userAgreementDetail'),
    path('user/dashboard/agreement/sign-agreement/', signAgreement, name='signAgreement'),
    
    # User Orders
    path('user/dashboard/orders', userOrders, name='userOrders'),
    path('user/dashboard/order/<str:order_id>', userOrderDetail, name='userOrderDetail')
]
