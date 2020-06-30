#YouTube Helper
A YouTube Helper application allows users to search videos from YouTube and add them to favorite video list.
##Installation
All dependencies locate in `pyproject.toml`, so you can use [poetry](https://github.com/python-poetry/poetry)
1.  You need to download all files from this repository
`git clone https://github.com/HolyDorus/youtube_helper`

2. Use this command to install all dependencies
```
cd youtube_helper
poetry install
```

3. You need to create file `.env`  with filled values (see `.env.example`) or manually add values in your enviroment variables

4. Next, you need to make migrations and migrate
```s
cd YouTubeHelper
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

5. Use this command to create a super user
`poetry run python manage.py createsuperuser`

6. Next, run application
`poetry run python manage.py runserver`

7. Visit [localhost:8000](localhost:8000)

##Screenshots
**Index page:**
![Index page](https://drive.google.com/uc?export=view&id=155TuY9_6Fzl-p9hC3LZ1Z03cCZWY9vf1 "Index page")

**Search page:**
![Search page](https://drive.google.com/uc?export=view&id=1usO1vYSqZUEJp1ngO8meuzwH3a_80gLB "Search page")

**Video page:**
![Video page](https://drive.google.com/uc?export=view&id=1090KRx6LSEBPaCPghrJ5UqvpOpFhYo7q "Video page")

**Liked videos page:**
![Liked videos page](https://drive.google.com/uc?export=view&id=1BKljDhENiGWlKQoGCe5fE1MI-3e2U-wa "Liked videos page")

**Register page:**
![Register page](https://drive.google.com/uc?export=view&id=1OloSZNzEPE9XnHC11QPs0i4wMb5LkqsX "Register page")

**Login page:**
![Login page](https://drive.google.com/uc?export=view&id=1rGPDJAQN4ZFsq2r3ZQnHRJVcSfLPmUSX "Login page")

The site also has a mobile version.