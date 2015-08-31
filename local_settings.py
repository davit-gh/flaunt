DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "b3212423-e4fe-4e90-a8cd-f25e482c8cd828c5d18b-2264-4d6d-849a-932b5fa33b2f9404e08d-a85a-4a5b-a5ba-70ed3c8ee1b4"
NEVERCACHE_KEY = "82605bbd-169e-4a3a-9ce3-ae4978ae5d130a6030c4-f243-43b9-a614-294dd44e04f09cd0b9f6-23c4-4786-a7b9-8b5fc9b4abb0"
ALLOWED_HOSTS = ["cpupanda.com", "www.cpupanda.com"]
DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "orqacle".
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # DB name or path to database file if using sqlite3.
        "NAME": "prod",
        # Not used with sqlite3.
        "USER": "prod",
        # Not used with sqlite3.
        "PASSWORD": "thisisaproductiondatabase",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "localhost",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "5432",
    }
}

FABRIC = {
     "SSH_USER": "flaunt", # SSH username
     "SSH_PASS":  "", # SSH password (consider key-based authentication)
     "SSH_KEY_PATH":  "/home/hero/.ssh/id_rsa.pub", # Local path to SSH key file, for key-based auth
     "HOSTS": ['cpupanda.com'], # List of hosts to deploy to
     "VIRTUALENV_HOME":  "/home/flaunt", # Absolute remote path for virtualenvs
     "PROJECT_NAME": "real_project", # Unique identifier for project
     "REQUIREMENTS_PATH": "req_new.txt", # Path to pip requirements, relative to project
     "GUNICORN_PORT": 8000, # Port gunicorn will listen on
     "LOCALE": "en_US.UTF-8", # Should end with ".UTF-8"
     "LIVE_HOSTNAME": "cpupanda.com", # Host for public site.
     "REPO_URL": "https://github.com/davit-gh/flaunt.git", # Git or Mercurial remote repo URL for the project
     "DB_PASS": "scanyoga", # Live database password
     "ADMIN_PASS": "scanyoga", # Live admin user password
     "SECRET_KEY": SECRET_KEY,
     "NEVERCACHE_KEY": NEVERCACHE_KEY,
 }
