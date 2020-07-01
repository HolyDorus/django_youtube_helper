# YouTube Helper
A YouTube Helper application allows users to search videos from YouTube and add them to favorite video list.
## Installation
All dependencies locate in `pyproject.toml`, so you can use [poetry](https://github.com/python-poetry/poetry)
1. You need to download all files from this repository
`git clone https://github.com/HolyDorus/youtube_helper`

2. Use this command to install all dependencies
```
cd youtube_helper
poetry install
```

3. You need to create file `.env`  with filled values (see `.env.example`) or manually add values in your enviroment variables

4. Next, you need to make migrations and migrate
```
cd YouTubeHelper
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

5. Use this command to create a super user
`poetry run python manage.py createsuperuser`

6. Next, run application
`poetry run python manage.py runserver`

7. Visit [localhost:8000](http://localhost:8000) (by default)

## Screenshots
The site also has a mobile version.

**Index page:**
![Index page](https://github.com/HolyDorus/youtube_helper/raw/master/screenshots/index_page.png "Index page")

**Search page:**
![Search page](https://github.com/HolyDorus/youtube_helper/raw/master/screenshots/search_page.png "Search page")

**Video page:**
![Video page](https://github.com/HolyDorus/youtube_helper/raw/master/screenshots/video_page.png "Video page")

**Liked videos page:**
![Liked videos page](https://github.com/HolyDorus/youtube_helper/raw/master/screenshots/liked_videos_page.png "Liked videos page")

**Register page:**
![Register page](https://github.com/HolyDorus/youtube_helper/raw/master/screenshots/register_page.png "Register page")

**Login page:**
![Login page](https://github.com/HolyDorus/youtube_helper/raw/master/screenshots/login_page.png "Login page")
