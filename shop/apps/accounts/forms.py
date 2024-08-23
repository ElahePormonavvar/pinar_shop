from typing import Any
from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# فرم ساخت ودرج کاربر- و یکی هم فرم تغییر کاربر
class UserCreateForm(ModelForm):
    # فیلدهای ما:
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Repassword',widget=forms.PasswordInput)
    class Meta:
        model=CustomUser
        fields=['mobile_number','email','name','family','gender']

    # مقایسه های ما که برای بقیه هم میشه نوشت
    def clean_password2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن با هم مغایرت دارند")
        return pass2
    
    # همه فرم های ما سیو داشتن اما اینجا لازمه دوباره نویسی کنیم
    # چون رمز گرفته شده به طول معمول سیو میشد باید هش شده سیو بشه
    # دوباره نویسی تابع سیو مدل فرم:
    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
# ----------------------------------------------------------------------
class UserChangeForm(ModelForm):
    # اینجا هم فیلد پسورد باید تحت کنترل باشه-هش بشه
    # برای همین نمونه ای از کلاس ReadOnlyPasswordHashFields
    # اینکار باعث میشه پسورد در صفحه تغغیر کاربر بصورت فقط خواندنی باشه
    password=ReadOnlyPasswordHashField(help_text='برای تغییر رمز عبور روی این <a href="../password">لینک</a> کلیک کنید')
    class Meta:
        model=CustomUser
        fields=['mobile_number','password','email','name','family','gender','is_active','is_admin']
# ----------------------------------------------------------------------
class RegisterUserForm(ModelForm):

    password1=forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمزعبور را وارد کنید'}))
    password2=forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمزعبور را وارد کنید'}))

    class Meta:
        model=CustomUser
        fields=['mobile_number',]

        widgets={
             'mobile_number':forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل را وارد کنید'})
        }

    def clean_password2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن با هم مغایرت دارند")
        return pass2
# -------------------------------------------------------
class VerifyRegisterForm(forms.Form):
    active_code=forms.CharField(label='',
                                error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کدفعال سازی را وارد کنید'})
                                )
# -----------------------------------------------------------
class LoginUserForm(forms.Form):
        mobile_number=forms.CharField(label='',
                                error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل  را وارد کنید'})
                                )
        password=forms.CharField(label='',
                                error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'})
                                )
# ---------------------------------------------------------------
class ChangePasswordForm(forms.Form):
        
    password1=forms.CharField(label='',
                            error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                            widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'})
                            )
    password2=forms.CharField(label='',
                            error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                            widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'})
                            )
        
    def clean_password2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن با هم مغایرت دارند")
        return pass2
# ------------------------------------------------------------------
class RememberPasswordForm(forms.Form):
    mobile_number=forms.CharField(label='',
                            error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل  را وارد کنید','readonly':'readonly'},)
                            )
# ------------------------------------------------------------------
class UpdateProfileForm(forms.Form):
    mobile_numbe=forms.CharField(label='',
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل  را وارد کنید'})
                            )
    name=forms.CharField(label='',
                            error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام  را وارد کنید'})
                            )
    family=forms.CharField(label='',
                            error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خانوادگی  را وارد کنید'})
                            )
    email=forms.CharField(label='',
                            error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                            widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل  را وارد کنید'})
                            )
    phone_number=forms.CharField(label='',
                            error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'تلفن  را وارد کنید'})
                            )
    address=forms.CharField(label='',
                            error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                            widget=forms.Textarea(attrs={'class':'form-control','placeholder':'آدرس  را وارد کنید'})
                            )
    image=forms.ImageField(required=False)