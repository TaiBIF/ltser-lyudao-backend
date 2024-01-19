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


#### Database Schema Migration

改了Database Schema (通常是models.py)，需要做migration。

Docker compose跑起來後，執行以下：

```
sudo docker compose exec app bash
```

進入Django docker的環境，然後執行

```
python manage.py makemigrations
```

產生migration檔案後，就可以`exit`退出，回到開發主機環境。

重新啟動，執行`docker compose down`，`docker compose up`，entrypoint.sh會自動跑`migrate`。

## Deployment部署

目前放在AWS EC2上，https已經用certbot跟`init-letsencrypt.sh`處理好，之後會自動更新。

開啟只要執行:

```
sudo docker compose -f compose.yml -f compose.prod.yml up -d
```


還沒設定自動部署(branch有更動的話會自動部署到EC2)，目前都是手動到AWS EC2 去更新跟重新 docker restart，之後可以考慮使用bitbucket的pipeline。
### 前端程式

已透過Nginx把`/`的連線導到`frontend`目錄，所以前端執行`yarn build`後的build目錄就直接複製到`ltser-lyudao-volumes/frontend`目錄即可。

## 資料庫

增加一個`ltserLyudao/initdb`目錄，可以把dump出來的xxx.sql.gz檔放在這個目錄裡，如果資料庫是空的就會自動import這個匯出檔。

如果要清空資料庫，可以執行：

```
sudo docker volume rm postgres_data
```

正式站沒有對外開DB port (5432)，所以如果要從csv匯入postgres的話就要到正式站進去docker環境去處理

```
sudo docker compose -f compose.yml -f compse.prod.yml exec db bash
```

## Notice

- django後端的static url跟前端的static url會衝突，剛好目前沒用到django的static，所以目前nginx是設定`/stati/admin`才會指向volumes的static folder。
