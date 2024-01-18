# LTSER Lyudao

## Development開發

### Docker環境

1. 安裝Docker與docker compose
Docker 最好更新到24版之後，預設會有`docker compose`指令，而不是舊版的script: `docker-compose`。新版的執行docker也會需要用sudo權限。

2. Build docker images

```
sudo docker compose build
```

不用特別指定設定檔，預設會讀`compose.yml`跟`compose.override.yml`2個檔案。


3. 啟動 docker compose

```
sudo docker compose up
```

Notice:

- Django 預設使用port 8000
- 如果需要在開發端安裝管理資料庫的網頁界面(adminer.php)，就可以把`compose.override.yml`裡的adminer拿掉註解。
- 會自動產生一個`ltser-lyudao-volumes`目錄，放置跟docker volumes的對應，之後static活pgdata的檔案也可以設定在這邊比較方便備份



## Deployment部署

目前放在AWS EC2上，https已經用certbot跟`init-letsencrypt.sh`處理好，之後會自動更新。

開啟只要執行:

```
sudo docker compose -f compose.yml -f compose.prod.yml up -d
```

### 前端程式

已透過Nginx把`/`的連線導到`frontend`目錄，所以前端執行`yarn build`後的build目錄就直接複製到`ltser-lyudao-volumes/frontend`目錄即可。

## 資料庫

增加一個`ltserLyudao/initdb`目錄，可以把dump出來的xxx.sql.gz檔放在這個目錄裡，如果資料庫是空的就會自動import這個匯出檔。

如果要清空資料庫，可以執行：
```
sudo docker volume rm postgres_data
```
