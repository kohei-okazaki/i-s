# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# Messageクラス
class Message(models.Model):

    # 投稿者情報
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_owner')
    # グループ情報
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    # 投稿内容
    content = models.TextField(max_length=1000)
    # share時のID
    share_id = models.IntegerField(default=-1)
    # いいね数
    good_count = models.IntegerField(default=0)
    # share数
    share_count = models.IntegerField(default=0)
    # 投稿日時
    pub_date = models.DateTimeField(auto_now_add=True)
    # 登録日時
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content) + ' (投稿者=' + str(self.owner) + ')'

    def get_share(self):
        return Message.objects.get(id=self.share_id)

    class Meta:
        ordering = ('-pub_date',)


# Groupクラス
class Group(models.Model):

    # 投稿者情報
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_owner')
    # グループタイトル
    title = models.CharField(max_length=100)
    # 登録日時
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


# Friendクラス
class Friend(models.Model):

    # 投稿者情報
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_owner')
    # ユーザ情報
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # グループ情報
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # 登録日時
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' (group:"' + str(self.group) + '")'


# Goodクラス
class Good(models.Model):

    # 投稿者情報
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_owner')
    # メッセージ情報
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    # 登録日時
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'good for "' + str(self.message) + '" (by ' + str(self.owner) + ')'

