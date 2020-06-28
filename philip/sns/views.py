# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from sns.form import SearchForm, GroupCheckboxForm, GroupSelectForm, FriendCheckboxForm, CreateGroupForm, PostForm
from sns.models import Group, Friend, Message, Good
from sns import util


@login_required(login_url='/admin/login/')
def index(request):
    '''
    index画面の処理
    @param request リクエスト情報
    '''

    # public userの取得
    (public_user, public_group) = util.get_public()

    if request.method == 'POST':

        if request.POST['mode'] == '__check_form__':
            # Groupsのチェックを更新した場合

            # フォームの用意
            search_form = SearchForm()
            check_form = GroupCheckboxForm(request.user, request.POST)

            # チェックされたGroup名をリストにまとめる
            glist = []
            for group in request.POST.getlist('groups'):
                glist.append(group)

            # Messageの取得
            message_entity_list = util.get_your_group_message(request.user, glist)

        if request.POST['mode'] == '__search_form__':
            # Groupsのメニューを更新した場合

            # フォームの用意
            search_form = SearchForm(request.POST)
            check_form = GroupCheckboxForm(request.user)

            # Groupのリストを取得
            group_entity_list = Group.objects.filter(owner=request.user)
            glist = [public_group]
            for entity in group_entity_list:
                glist.append(entity)

            # Messageの取得
            message_entity_list = util.get_your_group_message(request.user, glist, request.POST['search'])

    else:
        # Formの用意
        search_form = SearchForm()
        check_form = GroupCheckboxForm(request.user)

        # Groupリストの取得
        group_entity_list = Group.objects.filter(owner=request.user)
        group_list = [public_group]
        for entity in group_entity_list:
            group_list.append(entity)

        # メッセージの取得
        message_entity_list = util.get_your_group_message(request.user, group_list)

    params = {
        'login_user': request.user,
        'contents': message_entity_list,
        'check_form': check_form,
        'search_form': search_form,
    }

    return render(request, 'sns/index.html', params)


@login_required(login_url='/admin/login/')
def groups(request):
    '''
    Group画面の処理
    @param request リクエスト情報
    '''

    # 自分が登録したFriendを取得
    friend_entity_list = Friend.objects.filter(owner=request.user)

    # POST送信時の場合
    if request.method == 'POST':

        # Groupメニュー選択肢の処理
        if request.POST['mode'] == '__groups_form__':

            # 選択したGroup名を取得
            select_group = request.POST['groups']

            # Groupを取得
            group_entity = Group.objects.filter(owner=request.user).filter(title=select_group).first()

            # Groupに含まれるFriendを取得
            friend_entity_list = Friend.objects.filter(owner=request.user).filter(group=group_entity)

            # FriendのUserリストにまとめる
            list = []
            for entity in friend_entity_list:
                list.append(entity.user.username)

            # フォームの用意
            groups_form = GroupSelectForm(request.user, request.POST)
            friends_form = FriendCheckboxForm(request.user, friends=friend_entity_list, vals=list)

        # Friendsのチェック更新時の処理
        if request.POST['mode'] == '__friends_form__':

            # 選択したGroupの取得
            select_group = request.POST['groups']
            group_entity = Group.objects.filter(title=select_group).first()

            # チェックしたFriendsを取得
            select_friends = request.POST.getlist('friends')

            # Friendsのユーザを取得
            select_users = User.objects.filter(username__in=select_friends)

            # userのリストに含まれるユーザが登録したFriendを取得
            fds = Friend.objects.filter(owner=request.user).filter(user__in=select_users)

            # すべてのFriendにGroupを設定し保存する
            list = []
            for entity in fds:
                entity.group = group_entity
                entity.save()
                list.append(entity.user.username)

            # メッセージを設定
            messages.success(request, 'チェックされたFriendを ' + select_group + ' に登録しました')

            # フォームの用意
            groups_form = GroupSelectForm(request.user, {'groups': select_group})
            friends_form = FriendCheckboxForm(request.user, friends=friend_entity_list, vals=list)

    else:

        # フォームの用意
        groups_form = GroupSelectForm(request.user)
        friends_form = FriendCheckboxForm(request.user, friends=friend_entity_list, vals=[])

        select_group = '-'

    create_form = CreateGroupForm()
    params = {
        'login_user': request.user,
        'groups_form': groups_form,
        'friends_form': friends_form,
        'create_form': create_form,
        'group': select_group,
    }

    return render(request, 'sns/groups.html', params)


@login_required(login_url='/admin/login/')
def add(request):
    '''
    User追加画面の処理
    @param request リクエスト情報
    '''

    # 追加するUserを取得
    add_name = request.GET['name']
    add_user = User.objects.filter(username=add_name).first()

    if add_user == request.user:
        # Userが本人の場合
        messages.info(request, "自分自身を追加する事はできません")
        return redirect(to='/sns')

    # public userの取得
    (public_user, public_group) = util.get_public()
    # add_userのFriendの数を調べる
    friend_cnt = Friend.objects.filter(owner=request.user).filter(user=add_user).count()

    # 0より大きければ既に登録済
    if friend_cnt > 0:
        messages.info(request, add_user.username + "は既に追加されています")
        return redirect(to='/sns')

    # Friendを登録
    friend_entity = Friend()
    friend_entity.owner = request.user
    friend_entity.user = add_user
    friend_entity.group = public_group
    friend_entity.save()

    # メッセージの設定
    messages.info(request, add_user.username + "を追加しました。 groupページに移動して追加したFriendをメンバーに設定してください")
    return redirect(to='/sns')


@login_required(login_url='/admin/login/')
def creategroup(request):
    '''
    Group作成画面の処理
    @param request リクエスト情報
    '''

    # Groupを作り、Userとtitleを設定して保存する
    group_entity = Group()
    group_entity.owner = request.user
    group_entity.title = request.POST['group_name']
    group_entity.save()

    messages.info(request, '新しいグループを作成しました')

    return redirect(to='/sns/groups')


@login_required(login_url='/admin/login/')
def post(request):
    '''
    Message投稿画面の処理
    @param request リクエスト情報
    '''

    # POST送信の処理
    if 'POST' == request.method:
        # 送信内容の取得
        group_name = request.POST['groups']
        content = request.POST['content']

        # Groupの取得
        group_entity = Group.objects.filter(owner=request.user).filter(title=group_name).first()

        if group_entity == None:
            (public_user, group_entity) = util.get_public()

        # Messageを作成し、設定して保存
        message_entity = Message()
        message_entity.owner = request.user
        message_entity.group = group_entity
        message_entity.content = content
        message_entity.save()

        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました')
        return redirect(to='/sns')

    # GETアクセス時の処理
    form = PostForm(request.user)

    params = {
        'login_user': request.user,
        'form': form,
    }
    return render(request, 'sns/post.html', params)


@login_required(login_url='/admin/login/')
def share(request, share_id):
    '''
    share処理
    @param request リクエスト情報
    @param share_id shareID
    '''

    # シェアするMessageの取得
    share_message = Message.objects.get(id=share_id)

    # POST送信時の処理
    if 'POST' == request.method:
        # 送信内容を取得
        group_name = request.POST['groups']
        content = request.POST['content']

        # Groupの取得
        group_entity = Group.objects.filter(owner=request.user).filter(title=group_name).first()

        if group_entity == None:
            (pub_user, group_entity) = util.get_public()

        # Messageを作成
        message_entity = Message()
        message_entity.owner = request.user
        message_entity.group = group_entity
        message_entity.content = content
        message_entity.share_id = share_message.id
        message_entity.save()

        # 応答メッセージを設定
        messages.info(request, 'メッセージをシェアしました')
        return redirect(to='/sns')

    form = PostForm()
    params = {
        'login_user': request.user,
        'form': form,
        'share': share_message,
    }

    return render(request, 'sns/share.html', params)


@login_required(login_url='/admin/login/')
def good(request, good_id):
    '''
    Goodボタン押下時の処理
    @param request リクエスト情報
    @param good_id GoodID
    '''

    # GoodするMESSAGEを取得
    good_message = Message.objects.get(id=good_id)

    # 自身がメッセージにgoodした数を調べる
    is_good = Good.objects.filter(owner=request.user).filter(message=good_message).count()
    # 0より大きければ既にgood済
    if is_good > 0:
        messages.success(request, '既にメッセージにGoodしています')
        return redirect(to='/sns')

    # Messageのgood数をインクリメント
    good_message.good_count += 1
    good_message.save()

    # Goodを作成
    good = Good()
    good.owner = request.user
    good.message = good_message
    good.save()

    # 応答メッセージを設定
    messages.success(request, 'メッセージにGoodしました')

    return redirect(to='/sns')

