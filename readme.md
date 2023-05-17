# 動画検証ツール

このスクリプトは、動画ファイルを検証し、有効な動画を集計するためのツールです。また、有効な動画はWebM形式からMP4形式に変換します。

## 前提条件

- Python 3.6以上がインストールされていること
- FFmpegがシステムにインストールされていること

## インストールとセットアップ

1. 仮想環境を作成します。ターミナルで以下のコマンドを実行します：

   ```shell
   conda create -n video-validator
   ```

2. 作成した仮想環境にアクティベートします：

   ```shell
   conda activate video-validator
   ```

3. 必要なライブラリをインストールします：

   ```shell
   conda install pip
   pip install opencv-python
   ```

## ファイル構成

```
Videovalidator.py
README.md
```

- `Videovalidator.py`: 動画検証ツールのメインスクリプトです。
- `README.md`: この説明ファイルです。

```
root/
├── VideoValidator/
│   ├── videovalidator.py
│   └── README.md
├── data/
│   ├── ユーザID1/
│   │   ├── 動画ID1.webm
│   │   ├── 動画ID2.webm
│   │   └── ...
│   ├── ユーザID2/
│   │   ├── 動画ID1.webm
│   │   └── ...
│   └── ...
└── processed_data/
    ├── ユーザID1/
    │   ├── 動画ID1.mp4
    │   ├── 動画ID2.mp4
    │   └── ...
    ├── ユーザID2/
    │   ├── 動画ID1.mp4
    │   └── ...
    └── ...
```

- `VideoValidator/`: プロジェクトのルートディレクトリです。このディレクトリは "VideoValidator" という名前であり、プロジェクトのファイルが格納されます。
- `VideoValidator/videovalidator.py`: 動画検証ツールのメインスクリプトです。このスクリプトは "VideoValidator" ディレクトリ内に配置してください。
- `VideoValidator/README.md`: この説明ファイルです。同様に "VideoValidator" ディレクトリ内に配置してください。
- `data/`: 入力となる動画ファイルが格納されるディレクトリです。"VideoValidator" ディレクトリと同じ階層にあります。各ユーザごとにサブディレクトリが作成され、その中に動画ファイルが配置されます。
- `processed_data/`: 変換後の動画ファイルが格納されるディレクトリです。同様に "VideoValidator" ディレクトリと同じ階層にあります。入力ディレクトリと同様に、各ユーザごとにサブディレクトリが作成され、その中に変換後の動画ファイルが配置されます。

このディレクトリ構造に従って、"VideoValidator" ディレクトリ内にスクリプトファイル `videovalidator.py` と説明ファイル `README.md` を配置してください。また、入力動画ファイルは `data/` ディレクトリに、変換後の動画ファイルは `processed_data/` ディレクトリに配置してください。

## 使用法

1. `Videovalidator.py` スクリプトを開きます。
2. `DATA_DIR` 変数を適切なデータディレクトリのパスに設定します。データディレクトリは、ユーザごとにサブディレクトリが作成され、各サブディレクトリ内に動画ファイルが格納されている想定です。
3. `PROCESSED_DATA_DIR` 変数を変換後の動画を格納するディレクトリのパスに設定します。このディレクトリは事前に作成しておく必要があります。
4. その他の定数を必要に応じて変更します（解像度、ファイルサイズ制限など）。
5. ターミナルで以下のコマンドを実行して、スクリプトを実行します：

   ```shell
   python Videovalidator.py
   ```

6. スクリプトはデータディレクトリ内の各ユーザの動画を検証し、有効な動画を変換し、日付ごとに動画の総合計時間を出力します。

## ライセンス

MITライセンスのもとで公開されています。詳細については、[LICENSE](LICENSE) ファイルを参照してください。