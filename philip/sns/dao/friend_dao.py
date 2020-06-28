# -*- coding: utf-8 -*-
from sns.models import Friend


class FriendDao:
    '''
    FRIENDテーブルのDaoクラス
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def select_list_in_group(self, group_list):
        '''
        FRIENDから指定されたGROUPのリストが含まれるレコードを検索する
        @param group_list: GROUPのリスト
        '''
        return Friend.objects.filter(group__in=group_list)

    def select_list_by_user_in_group(self, in_user, group_list):
        '''
        FRIENDから指定されたUSERかつGROUPのリストが含まれるレコードを検索する
        @param in_user: USER
        @param group_list: GROUPのリスト
        '''
        return Friend.objects.filter(user=in_user).filter(group__in=group_list)
