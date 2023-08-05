====================
インベントリ
====================
hive-builder のインベントリは以下の2つからなります。

hive 定義
  サーバやネットワークで構成される基盤（infrastructure）を定義する

サービス定義
  コンテナイメージ、ボリューム、内部ネットワークで構成されるサービスを定義する

.. _defineHive:

hive 定義
====================
hive 定義では基盤を構成するサーバやネットワークを記述します。

IaaS 上にサイトを構築する場合、コンテナ収容サーバは3つの Availability Zone
に分かれて配置されます。以下にその例を示します。

.. image:: imgs/infra.png
   :align: center


hive 定義のフォーマット
---------------------------
hive 定義のフォーマットは以下の通り。

============  ==============  ============  ================================================
パラメータ    選択肢/例       デフォルト    意味
============  ==============  ============  ================================================
plugin        hive_inventory  必須          このファイルがhive定義で有ることを示す
name          pdns            必須          hive の名前
stages        ..              ..            | ステージオブジェクトへの辞書
                                            | private, staging, production の3つが定義できる
============  ==============  ============  ================================================

stages の下にステージ名をキーとしてステージオブエクトを指定します。以下に例を
示します。

::

  plugin: hive_inventory
  stages:
    private:
      provider: vagrant
      separate_repository: False
      cidr: 192.168.0.96/27
      memory_size: 4096
      mirrored_disk_size: 10
      number_of_hosts: 1
    production:
      provider: aws
      separate_repository: False
      cidr: 192.168.0.0/24
      instance_type: t3.medium
      region: ap-northeast-1
      mirrored_disk_size: 20
      repository_instance_type: t3.large
      subnets:
      - cidr: 192.168.0.0/26
        name: subnet-a
        available_zone: ap-northeast-1d
      - cidr: 192.168.0.64/26
        name: subnet-b
        available_zone: ap-northeast-1b
      - cidr: 192.168.0.128/26
        name: subnet-c
        available_zone: ap-northeast-1c

この例では、private ステージと production ステージが定義されています。
private ステージは vagrant で VirtualBox 上に 4G のメモリの
サーバ1台を構築します。

production ステージでは aws 上に t3.medium のサーバ3台を
東京リージョンの3つの可用性ゾーンに分けて構築します。
リポジトリサーバは3台目のコンテナ収容サーバと兼用し、
t3.large で構築します。

ステージオブジェクト
-----------------------------
ステージオブジェクトのフォーマットは以下の通り。

..  list-table::
    :widths: 18 18 18 50
    :header-rows: 1

    * - パラメータ
      - 選択肢/例
      - デフォルト
      - 意味
    * - provider
      - - aws
        - azure
        - gcp
        - prepared
        - vagrant
      - 必須
      - 基盤を提供するシステム
    * - cidr
      - 192.168.1.0/24
      - 必須
      - ネットワークのアドレス
    * - number_of_hosts
      - 1
      - 3
      - コンテナ収容サーバの台数
    * - separate_repository
      - - True
        - False
      - True
      - リポジトリサーバをコンテナ収容サーバとは別に建てるか否か
    * - subnets
      - 後述
      -
      - サブネットの定義のリスト
    * - ip_address_list
      - ["192.168.20.5","192.168.20.6"]
      -
      - IPアドレスのリスト
    * - disk_size
      - 16
      - プロバイダによる
      - コンテナ収容サーバの起動ディスクのサイズ（GBytes)
    * - repository_disk_size
      - 16
      - プロバイダによる
      - リポジトリサーバの起動ディスクのサイズ（GBytes)
    * - mirrored_disk_size
      - 16
      - 必須
      - drbdで複製同期するディスクのサイズ（GBytes)
    * - root_password
      - X12bv5riykfid
      - ""
      - 最初に ssh でログインするためのユーザを作成する必要がある場合に root のパスワードを指定する


上記はプロバイダ共通の属性ですが、プロバイダ固有の属性もあります。
以下にプロバイダ固有の属性をプロバイダごとに説明します。

IPアドレスと可用性ゾーンの割当
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
IPアドレスと可用性ゾーンの割当は以下のルールで行われます。
ただし、subnet 属性はプロバイダごとに指定できなかったり、
必須であったりしますので、プロバイダごとに割当方法が
異なります。

subnets が指定されている場合：
サーバは subnets に指定されたsubnetオブジェクトに順に割り振られます。
サーバの台数のほうがsubnetオブジェクトの数よりも大きい場合は、
先頭に戻ります。
サーバのIPアドレスは subnetオブジェクトに指定されたCIDR から
自動的に割り振ります。サーバはsubnetオブジェクトの
available_zone属性で指定された可用性ゾーンに配備されます。

ip_address_list が指定されている場合：
サーバのIPアドレスは ip_address_list から順に割り当てられます。
ip_address_listの要素数はサーバの台数と一致しなければなりません。
アベラブルゾーンは自動的にできるだけ分散するように割り振ります。

上記以外の場合：
サーバのIPアドレスは cidr 属性から自動的に割り振ります。
アベラブルゾーンは自動的にできるだけ分散するように割り当てます。


vagrant プロバイダ
^^^^^^^^^^^^^^^^^^^
vagrant プロバイダを利用するには、 Vagrant がインストールされていて、 virtualbox か libvirt の Vagrant プロバイダ
がセットアップされている必要があります。
vagrant プロバイダ固有の属性には以下のものがあります。

..  list-table::
    :widths: 18 18 18 50
    :header-rows: 1

    * - パラメータ
      - 選択肢/例
      - デフォルト
      - 意味
    * - memory_size
      - 4096
      - Vagrant のデフォルト
      - コンテナ収容サーバに割り当てるメモリのサイズで(MBytes)
    * - repository_memory_size
      - 4096
      - Vagrant のデフォルト
      - リポジトリサーバに割り当てるメモリのサイズで(MBytes)
    * - cpus
      - 2
      - Vagrant のデフォルト
      - サーバに割り当てる仮想CPUの個数
    * - bridge
      - brHive
      - ''
      - 外部のネットワークへブリッジ経由で接続するための仮想ブリッジをこの名前で生成する
    * - dev
      - brHive
      - ''
      - この名前の既設の仮想ブリッジに接続する（Vagrantプロバイダが libvirt である場合のみ利用できる）

- disk_size, repository_disk_size を省略した場合、Vagrant のデフォルトのサイズになります。
- subnets 属性は指定できません
- bridge, dev のどちらも指定しない場合、ホストオンリーネットワークに接続されます。


aws プロバイダ
^^^^^^^^^^^^^^^^^^^
aws プロバイダ固有の属性には以下のものがあります。

..  list-table::
    :widths: 18 18 18 50
    :header-rows: 1

    * - パラメータ
      - 選択肢/例
      - デフォルト
      - 意味
    * - instance_type
      - t3.medium
      - 必須
      - コンテナ収容サーバのインスタンスタイプ
    * - repository_instance_type
      - t3.medium
      - 必須
      - リポジトリサーバのインスタンスタイプ
    * - region
      - ap-northeast-1
      - 必須
      - 構築先のリージョン

prepared プロバイダ
^^^^^^^^^^^^^^^^^^^
prepared プロバイダは OS がインストール済みのホストが
事前に用意されている場合に使用します。
以下に prepared プロバイダの hive 定義の例を示します。

::

  staging:
    provider: prepared
    separate_repository: False
    cidr: 192.168.0.96/27
    ip_address_list:
    - 192.168.0.98
    - 192.168.0.99
    - 192.168.0.100
    root_password: mzYY3qjdvBiD

root_password が指定された場合は、build-infra フェーズは
鍵認証ではなく root ユーザでパスワードでログインして実行されます。
build-infra フェーズで ssh 鍵を生成し、 hive_admin で指定された
ユーザを作成して、 authorized_keys を設定します。

.. 台数をへらす方法：リポジトリサーバの分割、1台だけで動作

サービス定義
====================
サービス定義には、サービスをどのように構築するかが書かれます。

image属性
-----------------------------

image 属性には、そのサービスを構成する docker コンテナのイメージの取得方法を
記載してください。image 属性には、イメージのタグを記載する以外に、
イメージのビルド方法を書くことができます。

タグ指定
^^^^^^^^^^^^^^^^^^^
image 属性に文字列を指定すると、それはイメージのタグとみなされます。
サービスの起動時には、 docker pull により、タグに対応するイメージを
ダウンロードします。

ビルド方法指定
^^^^^^^^^^^^^^^^^^^
image 属性にオブジェクトを指定すると、イメージのビルド方法の指定とみなされます。
この場合、その内容に従って、 build-images フェーズでコンテナ
イメージがビルドされ、リポジトリサーバのプライベートリポジトリに push されます。
ビルド方法指定には以下の属性が指定できます。


..  list-table::
    :widths: 18 18 18 50
    :header-rows: 1

    * - パラメータ
      - 選択肢/例
      - デフォルト
      - 意味
    * - from
      - mariadb:10.4
      - 必須
      - ビルドのもととなるイメージのタグ
    * - roles
      - ['python-aptk', 'powerdns']
      - 必須
      - ビルド時に適用する role のリスト（対応する role が roles ディレクトリ配下に定義されていなければならない）
    * - standalone
      - - True
        - False
      - False
      - ビルド時にスタンドアローン型としてビルドするか否か
    * - env
      - {"HTTPD_USER": "admin"}
      - {}
      - イメージの設定：ビルドで追加される環境変数
    * - stop_signal
      - "2"
      - "15"
      - イメージの設定：コンテナを終了させる場合にルートプロセスに送られるシグナルの番号
    * - user
      - admin
      - root
      - イメージの設定：コンテナでルートプロセスを起動する際のユーザID
    * - working_dir
      - /home/admin
      - /
      - イメージの設定：コンテナでルートプロセスを起動する際の作業ディレクトリ
    * - entrypoint
      - /docker_entrypoint.sh
      - "[]"
      - イメージの設定：コンテナの entrypoint
    * - command
      - ["--api-port","5000"]
      - "[]"
      - イメージの設定：コンテナのデフォルト command
    * - privileged
      - - True
        - False
      - False
      - イメージの設定：コンテナのプロセスに特権を与えるか否か

ビルトインrole
^^^^^^^^^^^^^^^^^^^
python-aptk はビルトイン role であり、イメージのビルド時に role 定義を行わずに使用できます。
build-images フェーズでは、 ansible で中身を構築するため、
ビルド用に起動したコンテナに python がインストールされていなければなりません。
しかし、 ubuntu や alpine をベースとしたイメージには python がインストールされていないものが
多々あります。このような場合、ビルドの最初の roleとして python-aptk を指定してください。
python-aptk には以下のようにタスクが定義されており、ubuntu や alpine をベースとした
コンテナに python をインストールできます。

::

    - name: install python
      raw: if [ -x /usr/bin/apt-get ]; then (apt-get update && apt-get -y install python); else (apk update && apk add python); fi
      changed_when: False


スタンドアローン型とマイクロサービス型
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

docker のコンテナはスタンドアローン型とマイクロサービス型の2種類に分類することができます。
どちらのイメージをビルドするかによって、ビルド時のコンテナのルートプロセスが
変わります。

=================== =================================================================================
型                  説明
=================== =================================================================================
スタンドアローン型  - centos:7 などスーパバイザ機能を持った OS のイメージをベースとして構築する
                    - 実行時には /sbin/init を起動する
                    - systemd により内部のプロセスが管理される
マイクロサービス型  - dockerhub のオフィシャルイメージをベースとして構築する
                    - ベースの OS はUbuntuやalpineなどの軽量 OS を採用する
                    - 実行時にはサービスを提供するプロセス1個を起動する
=================== =================================================================================

image属性の standalone 属性に True が指定されると、そのfrom に指定された
元イメージがスタンドアローン型であるとみなされます。
build-images フェーズでスタンドアローン型のコンテナをビルドする際は、
デフォルトのentrypoint, command でコンテナを起動します。
これにより、 /sbin/init が起動され、
コンテナに対して ansible を実行してイメージをビルドすることができます。

build-images フェーズでマイクロサービス型のコンテナをビルドする際は、
ルートプロセスとして、以下のような sleep をし続ける1行のシェルスクリプトが
起動されます。

::

     /bin/sh -c 'trap "kill %1" int;sleep 2400 &wait'

このコマンドでルートプロセスが 40分間sleepするため、その間に
コンテナに対して ansible 実行でき、イメージをビルドすることができます。

プライベートリポジトリ上のタグとイメージの共有
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
build-images でビルドされたイメージはプライベートリポジトリに push
されます。このときのタグは、以下のようになります。

リポジトリサーバ名:5000/image_サービス名

例：separate_repository=True の production ステージの powerdns サービスのイメージの場合

::

    hive3.pdns:5000/image_powerdns

build-images でビルドするイメージを複数のサービスで共有するためには、
最初のサービス定義で image 属性にオブジェクトを指定してビルドし、
二個目以降のサービスではimage 属性にプライベートリポジトリ上のタグを
指定してイメージを参照する必要があります。

(サービス定義の他の属性については未執筆)