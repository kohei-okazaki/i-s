# -*- coding: utf-8 -*-
from sns.models import Good


class GoodDao:
    '''
    GOODテーブルのDaoクラス
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def insert(self, good):
        '''
        GOODテーブルを登録する
        @param good: GOOD
        '''
        good.save()

        # 登録成功時にTrueを返す
        return True

    def select_list_by_owner_and_message(self, user, message):
        '''
        userとmessageに一致するGOODのレコードを取得
        @param user: USER
        @param message: MESSAGE
        '''
        return Good.objects.filter(owner=user).filter(message=message)

    def count_by_owner_and_message(self, user, message):
        '''
        userとmessageに一致するGOODのレコードの件数を返す
        @param user: USER
        @param message: MESSAGE
        '''
        return self.select_list_by_owner_and_message(user, message).count()
