# guild-manager
A web portal for managing WOW Guild rosters, loot distribution, viewing statistics (and for me to get my feet wet with Django :smile:)

Built using:
 * [django](https://www.djangoproject.com/)
 * [PostgreSQL](https://www.postgresql.org/)
 * [Heroku](https://www.heroku.com/)

Contributions and feedback welcome!

Please use the [Issues](https://github.com/rob-lynch/guild-manager/issues) page for filing feature requests and bugs, but be sure to check the [Projects](https://github.com/rob-lynch/guild-manager/projects/1) page first to make sure it's not already on the road-map.

Admin/User documentation can be found here:

### Key Features
* Utilizes [Discord OAUTH2](https://discordapp.com/developers/docs/topics/oauth2) for authentication/login to reduce admin overhead and accountability.
* Allows importing/exporting guild rosters and raid attendance (See [here](import_examples) for examples)
* Can manage multiple realms and guilds (no multi-tenancy/siloing as of yet)

### Local Development Setup
**Pre-reqs:** Python 3.x, Pip, PostgreSQL (recommended via Docker)

**Create a virtual environment, install the dependencies and configure to use the local settings file:***
```
pip install virtualenv 
virtualenv env

pip install -r requirements.txt

#For Bash:
    export DJANGO_SETTINGS_MODULE="guild_manager.settings.local" 
#For Powershell: 
    $Env:DJANGO_SETTINGS_MODULE = "guild_manager.settings.local"
```

**Start up a postgres db using Docker:**
```
docker run -p 5432:5432 --name guild_manager -e POSTGRES_PASSWORD=password -e POSTGRES_USER=guild_manager -d postgres
```

**Make and Run the migrations to create/populate the tables:**
```
python manage.py makemigrations
python manage.py migrate
```

**Import some stock data (classes, races, etc.):**
```
python manage.py loaddata boostrap_data.json
```

**Create a super user**
```
python manage.py createsuperuser
```

**Start up the server:**
```
python manage.py runserver
```

### Setting up OAUTH
* Navigate to `/admin/sites/site/1/change/` to update the Domain and Display name accordingly.
* Navigate to `/admin/socialaccount/socialapp/add/` and set the Provider, Name, Client ID, and Secret key that correlates to your Discord App. Select site setup in step 1 and save your changes.
* Go to `/accounts/discord/login/?process=login` to attempt to login.
  
Note, the OAUTH user will not be able to access the admin portal until another admin grants at least "staff status" to the newly created account.

### Initial Provisioning to Heroku
Use the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) to create, manager and deploy the solution.
Details here outlining steps in detail

After deploying the code, be sure to set a super user, import stock data and start up a dyno:
```
heroku run python manage.py createsuperuser
heroku run python manage.py loaddata boostrap_data.json
heroku ps:scale web=1
```

### Deploying Updates
Details here - likely to be automated on merge to master