# -*- coding: utf-8 -*-
from sns.models import Message


class MessageDao:
    '''
    MESSAGEテーブルのDaoクラス
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def insert(self, message):
        '''
        MESSAGEを登録する
        @param message: MESSAGE
        '''
        message.save()

        # 登録成功時にTrueを返す
        return True

    def good_increment(self, message):
        '''
        MESSAGEのgood_countの件数を1件増やす
        @param message: MESSAGE
        '''
        message.good_count += 1
        message.save()

    def select_by_id(self, message_id):
        '''
        MESSAGEをIDから取得する
        @param message_id: ID
        '''
        return Message.objects.get(id=message_id)

