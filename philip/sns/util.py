# -*- coding: utf-8 -*-
from django.db.models.query_utils import Q
from sns.dao.friend_dao import FriendDao
from sns.dao.group_dao import GroupDao
from sns.dao.user_dao import UserDao
from sns.models import Group, Message


def get_public():
    '''
    publicのUserとGroupを取得
    '''
    public_user = UserDao().select_list_by_username('public').first()
    public_group = GroupDao().select_list_by_owner(public_user).first()
    return (public_user, public_group)


def get_your_group_message(owner, group_list, find=None):
    '''
    GROUP及び、検索文字によるMessageの取得
    @param owner: 所有者
    @param group_list: グループリスト
    @param find: 検索文字列(未指定の場合、None)
    '''

    # publicの取得
    (public_user, public_group) = get_public()

    # チェックされたGroupの取得
    group_entity_list = Group.objects.filter(Q(owner=owner) | Q(owner=public_user))\
                                    .filter(title__in=group_list)

    # Groupに含まれるFriendの取得
    friend_entity_list = FriendDao().select_list_in_group(group_entity_list)

    # FriendのUserをリストにまとめる
    users = []
    for entity in friend_entity_list:
        users.append(entity.user)

    # UserリストのUserが作ったGroupの取得
    user_group_entity_list = GroupDao().select_list_in_owner_list(users)
    user_friend_entity_list = FriendDao().select_list_by_user_in_group(owner, user_group_entity_list)

    groups = []
    for entity in user_friend_entity_list:
        groups.append(entity.group)

    # Groupがgroup_entity_listに含まれるか、Groupに含まれるMessageの取得
    if find == None:
        message_entity_list = Message.objects.filter(Q(group__in=group_entity_list) \
                                                     | Q(group__in=groups))[:100]

    else:
        message_entity_list = Message.objects.filter(Q(group__in=group_entity_list) \
                                                     | Q(group__in=groups))\
                                                     .filter(content__contains=find)[:100]

    return message_entity_list
