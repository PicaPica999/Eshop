from django import forms
from captcha.fields import CaptchaField
from .models import comments, seller, buyer
from ckeditor.fields import RichTextFormField


class login_form(forms.Form):
    captcha = CaptchaField()


class AddForm(forms.Form):
    # account = forms.CharField()
    headimg = forms.FileField()
    verbose_name = '上传图片'


class CommentForm(forms.ModelForm):
    # owner = forms.CharField()
    # time = forms.DateField()
    content = RichTextFormField(label='内容')

    class Meta:
        model = comments
        fields = ['content', ]


class ImageFormSeller(forms.ModelForm):
    class Meta:
        model = seller
        fields = ['headimg', ]


class ImageFormBuyer(forms.ModelForm):
    class Meta:
        model = buyer
        fields = ['headimg', ]
