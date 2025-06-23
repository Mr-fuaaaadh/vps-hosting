
# 🛰️ Deploying Django Project to VPS

## 📋 Prerequisites

**Generate `requirements.txt`:**
```bash
pip freeze > requirements.txt
```

**Set up static files with Whitenoise:**
1. Install:
   ```bash
   pip install whitenoise
   pip freeze > requirements.txt
   ```

2. In `settings.py`, add to `MIDDLEWARE` (at the top):
   ```python
   'whitenoise.middleware.WhiteNoiseMiddleware',
   ```

3. Add static file settings:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

4. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

5. Push your project to GitHub.

## 🖥️ SSH Into Server

```bash
ssh username@server_ip_address
# Enter your password when prompted
```

## 🔧 Update & Upgrade the Server

```bash
sudo apt-get update
sudo apt-get upgrade
```

## 🐍 Install Python & pip

```bash
sudo apt install python3
sudo apt install python3-pip
```

## 🧪 Set Up Virtual Environment

```bash
sudo apt install virtualenv
virtualenv /opt/myproject
source /opt/myproject/bin/activate
```

## 📦 Clone Your Repository

```bash
mkdir myproject
cd myproject
```

1. Check Git:
   ```bash
   git status
   sudo apt-get install git  # if needed
   ```

2. Clone your repo:
   ```bash
   git clone <your-repo-url>
   ```

3. Install dependencies:
   ```bash
   cd <repo-name>
   pip install -r requirements.txt
   pip install gunicorn
   ```

## 🌐 Configure Nginx

**Install:**
```bash
sudo apt install nginx
```

**Create config file:**
```bash
sudo nano /etc/nginx/sites-available/myproject
```

**Paste:**
```nginx
server {
    listen 80;
    server_name your_server_ip;

    access_log /var/log/nginx/website-name.log;

    location /static/ {
        alias /opt/myproject/myproject/path-to-static-files/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        add_header P3P 'CP="ALLDSP COR PSAa PSDa OURNOR ONL UNI COM NAV"';
    }
}
```

**Enable site:**
```bash
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/myproject
```

**Uncomment in `/etc/nginx/nginx.conf`:**
```nginx
server_names_hash_bucket_size 64;
```

**Restart Nginx:**
```bash
sudo service nginx restart
```

## 🔥 Adjust Firewall

```bash
sudo apt-get install ufw
sudo ufw allow 8000
sudo service nginx restart
```

## 🧪 Test Gunicorn

```bash
cd /opt/myproject/myproject/<repo-name>
gunicorn --bind 0.0.0.0:8000 demopro.wsgi
```

Visit:  
`http://your_server_ip:8000`

## 🌍 Connect a Domain

1. Go to your domain DNS settings.
2. Add an **A record**:
   - **Name**: `@`
   - **Points to**: your server IP
3. Edit Nginx config:
   ```bash
   sudo nano /etc/nginx/sites-available/demopro
   ```

**Update server block:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    access_log /var/log/nginx/website-name.log;

    location /static/ {
        alias /opt/myproject/myproject/path-to-static-files/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
    }
}
```

**Restart Nginx:**
```bash
sudo service nginx restart
```

Wait for DNS changes to propagate.

## 🔐 Add SSL with Let’s Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**Test and reload Nginx:**
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 🔁 Run Gunicorn in Background

```bash
gunicorn --bind 0.0.0.0:8000 demopro.wsgi
# OR background:
nohup gunicorn --bind 0.0.0.0:8000 demopro.wsgi &
```

**To stop:**
```bash
pkill gunicorn
```

## 🔄 Making Changes

- Pull updates from GitHub
- Restart Gunicorn
- Recollect static if needed

## 📚 References

- [DigitalOcean Django Deployment](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-local-django-app-to-a-vps)
- [Django + PostgreSQL + Gunicorn + Nginx](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)
- [Stack Overflow: Troubleshooting](https://stackoverflow.com/questions/37339383/nginx-gunicorn-django-not-working)
