# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

class UserDao:
    '''
    User関連のDaoクラス
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def select_list_by_username(self, in_username):
        '''
        USERをusernameで検索する
        @param in_username 検索対象のユーザ名
        '''
        return User.objects.filter(username=in_username)

    def select_list_in_username_list(self, in_username):
        '''
        USERをusernameで複数指定して検索する
        @param in_username 検索対象のユーザ名
        '''
        return User.objects.filter(username=in_username)
