from app.plugins import PluginBase, Menu, MountPoint
from app.models import Setting
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPDataError
from . import email
from . import config
from urllib import request as url_request, parse  # 重命名导入的request模块
from urllib.error import URLError, HTTPError  # 导入异常类

class ConfigurationForm(forms.Form):
    notification_app_name = forms.CharField(
        label='App name',
        max_length=100,
        required=True,
    )
    smtp_to_address = forms.CharField(
        label='Send Notification to Address',
        max_length=300,
        required=True
    )
    
    notify_task_completed = forms.BooleanField(
        label='Notify Task Completed',
        required=False,
    )
    notify_task_failed = forms.BooleanField(
        label='Notify Task Failed',
        required=False,
    )
    notify_task_removed = forms.BooleanField(
        label='Notify Task Removed',
        required=False,
    )

    def test_settings(self, django_request):  # 重命名参数避免冲突
        try:
            settings = Setting.objects.first()
            
            # 从表单获取实际数据
            app_name = self.cleaned_data.get('notification_app_name', settings.app_name)
            to_address = self.cleaned_data.get('smtp_to_address')
            
            # 构建GET请求参数
            params = {
                'app_name': app_name,
                'test_message': 'Hi, just testing if the API is working',
                'to_address': to_address
            }
            
            # 编码参数并构建完整URL
            encoded_params = parse.urlencode(params)
            api_url = f'https://jsonplaceholder.typicode.com/users?{encoded_params}'
            
            # 使用正确的url_request模块发送请求
            with url_request.urlopen(api_url) as response:
                if response.status == 200:
                    messages.success(django_request, f"API request sent successfully")
                else:
                    messages.error(django_request, f'HTTP error: {response.status}')
                    
        except URLError as e:
            messages.error(django_request, f'Network error: {e.reason}')
        except HTTPError as e:
            messages.error(django_request, f'HTTP error: {e.code}')
        except Exception as e:
            messages.error(django_request, f'An error occurred: {e}')
    
    def save_settings(self):
        config.save(self.cleaned_data)
                    
class Plugin(PluginBase):
    def main_menu(self):
        return [Menu(_("Task Notification"), self.public_url(""), "fa fa-envelope fa-fw")]
    
    def include_css_files(self):
        return ['style.css']

    def app_mount_points(self):

        @login_required
        def index(request):
            if request.method == "POST":
                form = ConfigurationForm(request.POST)
                test_configuration = request.POST.get("test_configuration")
                if form.is_valid() and test_configuration:
                    form.test_settings(request)  # 传递正确的request对象
                elif form.is_valid() and not test_configuration:
                    form.save_settings()
                    messages.success(request, "Notification settings applied successfully!")
            else:
                config_data = config.load()
                settings = Setting.objects.first()
                config_data['notification_app_name'] = config_data['notification_app_name'] or settings.app_name
                form = ConfigurationForm(initial=config_data)
            
            return render(request, self.template_path('index.html'), {'form': form, 'title': 'Task Notification Api'})
        
        return [
            MountPoint('$', index),
        ]