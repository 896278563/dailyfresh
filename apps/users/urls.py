from django.conf.urls import url
from users import views

urlpatterns = [
    # 注册  http://127.0.0.1:8000/register
    url(r"^register$", views.RegisterView.as_view(), name='register'),
    # 邮件激活：
    # http://127.0.0.1:8000/users/active/!@#$&%^YTQRWEGE*&#@^#$!
    url(r"^active/(?P<token>.+)$", views.ActiveView.as_view(), name='active'),
]
