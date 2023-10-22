from django.urls import path, include
from organization.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'register', OrganizationRegisterView)
# router.register(r'add-user', addMemberView)


urlpatterns = [
  path('', include(router.urls)),
  path('add-user/', addMemberView.as_view()),
  path('list/', OrganizationTotal.as_view()),
  path('register/<uid>/<token>/<organization_name>/', registerOrganizationVerify.as_view()),
  path('add-user/<uid>/<token>/<org_name>/', invitedActive.as_view()),
  
  path('member/<int:org_id>/', OrganizationMember.as_view()),
  
  path('member-remove/<int:pk>/', MemberRemoveView.as_view()),

  ########### Payment  #########
  path('payment/<int:pk>/', PlaceOrderPremiumView.as_view()),
  path('success/', successView.as_view()),
  
  ### org update  ###
  path('update/<int:pk>/', organizationUpdateView.as_view()),
  ### org Delete ###
  path('delete/<int:pk>/', organizationDeleteView.as_view()),
  
  ### Org Detaail ###
  path('detail/<slug:slug>/', organizationDetailView.as_view()),
  
  ### Payment History ###
  path('history/<slug:slug>/', PaymentHistoryView.as_view()),
  
]
