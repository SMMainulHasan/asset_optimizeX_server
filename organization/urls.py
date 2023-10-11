from django.urls import path, include
from organization.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'register', OrganizationRegisterView)
router.register(r'add-user', addMemberView)


urlpatterns = [
  path('', include(router.urls)),
  path('list/', OrganizationTotal.as_view()),
  path('register/<uid>/<token>/<organization_name>/', registerOrganizationVerify.as_view()),
  path('add-user/<uid>/<token>/<org_id>/', invitedActive.as_view()),
]
