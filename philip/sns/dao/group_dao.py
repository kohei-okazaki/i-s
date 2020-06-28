# -*- coding: utf-8 -*-
from sns.models import Group


class GroupDao:
    '''
    GROUPのDaoクラス
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def insert(self, group):
        '''
        GROUPを登録する
        @param group GROUP
        '''
        group.save()

        # 登録成功時にTrueを返す
        return True

    def select_list_by_owner(self, in_owner):
        '''
        Userを指定してGROUPを検索する
        @param in_owner 投稿者情報
        '''
        return Group.objects.filter(owner=in_owner)

    def select_list_by_owner_and_title(self, in_owner, in_title):
        '''
        ownerとtitleからGROUPを検索する
        @param in_owner 投稿者情報
        @param in_title グループタイトル
        '''
        return Group.objects.filter(owner=in_owner).filter(title=in_title)

    def select_list_in_owner_list(self, in_owner):
        '''
        Userを複数指定してGROUPを検索する
        @param in_owner 投稿者情報
        '''
        return Group.objects.filter(owner__in=in_owner)

    def select_list_by_title(self, in_title):
        '''
        titleを指定してGROUPを検索する
        @param in_title グループタイトル
        '''
        return Group.objects.filter(title=in_title)



