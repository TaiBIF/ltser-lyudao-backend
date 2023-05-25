# 使用 Python 3.9 作為基礎映像
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製專案文件到容器內
COPY . /app

# 安裝所需的依賴庫
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN python manage.py migrate

# 設定環境變數
ENV SECRET_KEY=${SECRET_KEY}

# 開放 Django 服務的預設端口
EXPOSE 8000

# 執行 Django 服務
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
