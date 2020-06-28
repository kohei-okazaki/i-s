# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from sns.models import Group, Friend, Message
from django.db.models.query_utils import Q

def get_public():
    public_user = User.objects.filter(username='public').first()
    public_group = Group.objects.filter(owner=public_user).first()
    return (public_user, public_group)


def get_your_group_message(owner, group_list, find=None):
    # 指定されたグループ及び、検索文字によるMessageの取得

    # publicの取得
    (public_user, public_group) = get_public()

    # チェックされたGroupの取得
    group_entity_list = Group.objects.filter(Q(owner=owner) | Q(owner=public_user))\
                                    .filter(title__in=group_list)
    print(group_entity_list)

    # Groupに含まれるFriendの取得
    friend_entity_list = Friend.objects.filter(group__in=group_entity_list)
    print(friend_entity_list)

    # FriendのUserをリストにまとめる
    users = []
    for entity in friend_entity_list:
        users.append(entity.user)

    # UserリストのUserが作ったGroupの取得
    user_group_entity_list = Group.objects.filter(owner__in=users)
    user_friend_entity_list = Friend.objects.filter(user=owner)\
                                    .filter(group__in=user_group_entity_list)

    groups = []
    for entity in user_friend_entity_list:
        groups.append(entity.group)

    # groupがgroup_entity_listに含まれるか、groupsに含まれるMessageの取得
    if find == None:
        message_entity_list = Message.objects.filter(Q(group__in=group_entity_list) \
                                                     | Q(group__in=groups))[:100]

    else:
        message_entity_list = Message.objects.filter(Q(group__in=group_entity_list) \
                                                     | Q(group__in=groups))\
                                                     .filter(content__contains=find)[:100]

    return message_entity_list
