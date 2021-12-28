# FastAPIテスト

## 起動方法

Dockerコンテナを起動
```
docker-compose build
docker-compose up
```

## 依存パッケージのインストール

```
docker-compose run --entrypoint "poetry install" shushukun-api
```

## テスト方法
```
docker-compose run --entrypoint "poetry run pytest" shushukun-api
```

## VSCodeのpylanceがパッケージを読み込んでくれない時
- ルート直下に`.vscode`というディレクトを生成
- その中に`.settings.json`を作成  
- 内容を以下のように編集

```json
{
  "python.analysis.extraPaths": [
    // ルート直下に生成された.dockervenv/lib/python3.9/site-packagesのパス
  ]
}
```