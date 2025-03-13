



from django.urls import path

from users.views import PaymentListAPIView
app_name = 'users'
urlpatterns = [
                  path('pay/', PaymentListAPIView.as_view(), name='pay')]