# Djangoアプリケーションのメモ
## 1.Anacondaをインストール
https://www.anaconda.com/products/individual から64Bit版をDLし、解凍
 「Anaconda Prompt」を起動
 以下のコマンドを実行
>conda update conda
>conda update --all
>conda install django
>conda install sqlparse

## 2.EclipseのDjango環境構築手順
Eclipse を解凍
Eclipseを起動し、「メニュー」→「ウィンドウ」→「設定」を選択
左のペインから「PyDev」→「インタープリター」→「Python Interpreter」を選択
右のペインの「Python インタープリター」で、「Browse for python」を選択

### 2.1.Application 作成方法
「プロジェクトを右クリック」→「Django」→「Create Application」

### 2.2.Server 起動方法
「プロジェクトを右クリック」→「実行」→「Django」

### 2.3.Server ポート番号変更方法
  サーバ起動時の引数にポート番号をそのまま設定
  「プロジェクトを右クリック」→「実行」→「実行の構成」→「PyDev Django」→「引数」
 >runserver 8000

## 3.DBのマイグレーション
各アプリケーションからmodels.pyにEntity情報をclassとして追記.(IDは採番される)
各アプリケーションからadmin.pyにadmin.site.register(追記したクラス名)
>例：admin.site.register(Friend)

Anaconda Prompt を開いて、以下のコマンドを実行
>D:
>cd D:\philip-project\git\philip\philip
>python manage.py makemigrations
>python manage.py migrate

(注意.管理画面の管理者ユーザを作っていない場合、以下のコマンドを実行する必要がある)
>python manage.py createsuperuser
