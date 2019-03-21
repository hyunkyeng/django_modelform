from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Board

# class BoardForm(forms.Form):
#     title = forms.CharField(label="제목", widget=forms.TextInput(attrs={
#                                                         'placeholder': 'THE TITLE!',
#                                              }))
#     content =  forms.CharField(label="내용", 
#                               error_messages={'required': '내용을 입력해주세요!'},
#                               widget=forms.Textarea(attrs={
#                                                         'class': 'Content-input',
#                                                         'rows': 5,
#                                                         'cols': 50,
#                                                         'placeholder': 'Fill the Content~'
#                                              }))

class BoardForm(forms.ModelForm):
    # Model 의 정보를 작성하는 곳
    class Meta:
        model = Board
        # models.py 에 지정해놓은 필드를 사용한다.
        fields = '__all__'
        widgets = {'title': forms.TextInput(attrs={
                                                'placeholder': '제목을 입력하세요.',
                                                'class': 'title'}),
                'content': forms.Textarea(attrs={
                                                'placeholder': '내용을 입력하세요.',
                                                'class': 'content',
                                                'rows': 5,
                                                'cols': 50,})}
        error_messages = {'title': {
                                        'required': '제목을 입력하세요'
                                    },
                        'content': {
                                        'required': '내용을 입력하세요'
                                    },
                          }
                          
    # 밑에는 안외워도 된다. 문서에 나와있음
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', '작성!'))