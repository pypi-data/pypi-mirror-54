# packaging
- clickコマンドを使ったパッケージングの練習
[必要なモジュールについて(requirements.txt Pipfile Pipfile.lockの必要性)]
- 利用者はこのリポジトリをクローンしたらpipenvまたはvenv環境内で利用することが可能である
- pipenvで使用するときはhelloName/packaging/helloNameに入り込みpipenv run [コマンド] (ここではpipenv run ./helloworld.py -n miyabi)で利用
- pipenvが入っていない場合は入れてあげる
- venvの仮想環境を利用する場合はhelloName/packagingに入り込みpython3 -m venv venvを実行
- 仮想環境を構築したら . ./venv/bin/activate を実行し、仮想環境内に入り込む
- pip install -r requirements.txtを仮想環境の中で実行し、仮想環境内に必要なモジュールをインストールする
- venvで実行する場合は仮想環境に入り込んだまま ./helloworld.py -n [NAME] で実行
- venvは仮想環境に入り込んでいないと必要なモジュールがグローバル環境にない可能性があるため、コマンドが実行できない可能性がある

