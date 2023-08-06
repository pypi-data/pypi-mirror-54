# reelib
頻繁に利用する処理を集めたライブラリ

## インストール方法

```sh
pip install reelib
```

## ライブラリの内容

### Timestamp

```python
from reelib import timestamp

# 現在時刻のタイムスタンプを取得
ts = timestamp.get_timestamp()
# ex) 20191025164844890916

# タイムスタンプをdatetimeに変換
t = timestamp.conv_time_from_timestamp(ts)
# ex) datetime.datetime(2019, 10, 25, 16, 48, 44, 890916, tzinfo=datetime.timezone(datetime.timedelta(0, 32400)))
```