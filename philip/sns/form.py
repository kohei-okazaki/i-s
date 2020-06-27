from django import forms
from django.forms.models import ModelForm
from django.forms.forms import Form
from sns.models import Message, Group, Friend, Good
from django.contrib.auth.models import User


# MessageのForm
class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ['owner', 'group', 'content']


# GroupのForm
class GroupForm(ModelForm):

    class Meta:
        model = Group
        fields = ['owner', 'title']


# FriendのForm
class FriendForm(ModelForm):

    class Meta:
        model = Friend
        fields = ['owner', 'user', 'group']


# GoodのForm
class GoodForm(ModelForm):

    class Meta:
        model = Good
        fields = ['owner', 'message']


# 検索Form
class SearchForm(Form):

    search = forms.CharField(max_length=100)


# GroupのチェックボックスForm
class GroupCheckboxForm(Form):

    def __init__(self, user, *args, **kwargs):
        f = super(GroupCheckboxForm, self)
        f.__init__(*args, **kwargs)

        # User.ユーザ名 = public で検索
        public = User.objects.filter(username='public').first()

        self.fields['group'] = forms.MultipleChoiceField(
            choices=[(item.title, item.title) for item in Group.objects.filter(owner__in=[user, public])],
            widget=forms.CheckboxSelectMultiple(),
        )


# Groupの選択メニューフォーム
class GroupSelectForm(Form):

    def __init__(self, user, *args, **kwargs):
        f = super(GroupSelectForm, self)
        f.__init__(*args, **kwargs)

        self.fields['groups'] = forms.ChoiceField(
            choices=[('-', '-')] + [(item.title, item.title) for item in Group.objects.filter(owner=user)]
        )


# Friendのチェックボックスフォーム
class FriendCheckboxForm(Form):

    def __init__(self, user, friends=[], vals=[], *args, **kwargs):
        f = super(FriendCheckboxForm, self)
        f.__init__(*args, **kwargs)

        self.fields['friends'] = forms.MultipleChoiceField(
            choices=[(item.user, item.user) for item in friends],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals,
        )


# Group作成フォーム
class CreateGroupForm(Form):

    group_name = forms.CharField(max_length=50)


# 投稿フォーム
class PostForm(Form):

    content = forms.CharField(max_length=500, widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        f = super(PostForm, self)
        f.__init__(*args, **kwargs)

        # User.ユーザ名 = public で検索
        public = User.objects.filter(username='public').first()

        self.fields['groups'] = forms.ChoiceField(
            choices=[('-', '-')] + [(item.title, item.title) for item in Group.objects.filter(owner__in=[user, public])]

        )

