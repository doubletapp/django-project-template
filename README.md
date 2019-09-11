```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`sudo -u postgres psql`
```
CREATE DATABASE confapp;
CREATE USER confapp_admin WITH PASSWORD 'confapp_admin';
GRANT ALL PRIVILEGES ON DATABASE confapp TO confapp_admin;
```
