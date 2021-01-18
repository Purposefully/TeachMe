
<h1 align="center">
    TeachMe
</h1>

<p align="center">
    <a href="" alt="Video Tour">Take a Video Tour</a>
</p>

[![Video Tour](/Screenshots/Login.png?raw=true)](https://youtu.be/LCcyI3A38RM)

### *A Learning Management System (LMS)*  
___

## Table of Contents
* [Background](#Background)
* [Features](#Features)
* [Technologies Used](#Technologies-Used)
* [Screenshots](#More-Screenshots)
* [Functionality](#Functionality)
* [Design](#Design)
* [Running Locally](#Running-Locally)
* [Image Credits](#Image-Credits)

___

## Background


[Return to Table of Contents](#Table-of-Contents)

___

## Features
* General Features
    * Login/Registration with validations  

    <img src="https://github.com/Purposefully/TeachMe/blob/main/Screenshots/Login.png?raw=true" alt="Login/Register" width="300">  

    * User Profile Page

    <img src="https://github.com/Purposefully/TeachMe/blob/main/Screenshots/Login.png?raw=true" alt="Login/Register" width="300">

    * Course Library

    <img src="https://github.com/Purposefully/TeachMe/blob/main/Screenshots/Login.png?raw=true" alt="Login/Register" width="300">

    * Individual Course Page

    <img src="https://github.com/Purposefully/TeachMe/blob/main/Screenshots/Login.png?raw=true" alt="Login/Register" width="300">

    * Multiple Choice Quiz

    <img src="https://github.com/Purposefully/TeachMe/blob/main/Screenshots/Login.png?raw=true" alt="Login/Register" width="300">

* Admin Features
    * Create a Course

    <img src="https://github.com/Purposefully/TeachMe/blob/main/Screenshots/Login.png?raw=true" alt="Login/Register" width="300">

    * Create or Edit a Quiz Menu

    <img src="https://github.com/Purposefully/TeachMe/blob/main/Screenshots/Login.png?raw=true" alt="Login/Register" width="300">

    * Edit a Quiz

    <img src="https://github.com/Purposefully/TeachMe/blob/main/Screenshots/Login.png?raw=true" alt="Login/Register" width="300">


[Return to Table of Contents](#Table-of-Contents)
___

## Technologies Used
* Python Django 
* HTML, CSS, and Bootstrap
* AJAX, jQuery, and RESTful routing
* SQLite3
* HTML and Bootstrap validations as well as server-side validations and Bcrypt for secure login
* YouTube API


[Return to Table of Contents](#Table-of-Contents)
___

## More Screenshots
* Menu screens  
    * Single or Double Image Lesson  
    <img src="https://github.com/Purposefully/Connections/blob/master/Screenshots/4SingleOrDouble.png?raw=true" alt="Choose single or double lesson" width="300">  

    * Options for Single Image Lessons  

    <img src="https://github.com/Purposefully/Connections/blob/master/Screenshots/12LessonOptions.png?raw=true" alt="Single Image Lesson Options" width="300">  

    * Options for Double Image Lessons  

    <img src="https://github.com/Purposefully/Connections/blob/master/Screenshots/14DoubleImageOptions.png?raw=true" alt="Double Image Lesson Options" width="300">  

* Thank you screen when student is finished  

<img src="https://github.com/Purposefully/Connections/blob/master/Screenshots/10ThankYouMsg.png?raw=true" alt="Thank You Screen" width="300">  


[Return to Table of Contents](#Table-of-Contents)

___

## Functionality
Upon logging in, the user is taken to their profile page.  It lists any playlists the user has created.  When a playlist is selected, the related courses are displayed in two categories:  courses already taken and courses that could be taken.  If a course has already been taken, the user's quiz score for it is displayed.  Selecting a course takes the user to that course's page.

On an individual course's page, the user can read the description imported through YouTube's API.  In case the user arrived on the course page from the course library, there is an option for adding the course to one of their playlists.  They may attempt the quiz before and/or after watching the video.  When a video ends, a modal provides the option to add the course to one of the user's existing playlists or for a new list to be created with this course, and then the user is taken to the quiz page for that course.

The quizzes are five multiple choice questions.  The questions and answer choices are shuffled each time the quiz is displayed.  Each quiz is immediately scored and results are displayed for the user.

The course library lists all the courses with quizzes that have been entered into the TeachMe app by an administrator.  There is a search feature to faciliate locating desired courses.  Selecting a course takes the user to the individual course's page.

Users who have administrative permission may create a course by pasting in the YouTube url for that video on the create a course page.  The course will not appear in the course library, however, until a quiz has been created for it.

Users who have administrative permission may create or edit a quiz for a course.  For development and demo purposes, one option is a lorem ipsum quiz which automatically fills in random text for the questions and answers.  For real use purposes, another option is to actually create an appropriate quiz.  An administrator may write 5 questions and supply three incorrect and one correct answer for each question.  The edit quiz option populates with the current questions and answers and allows an administrator to modify them.


[Return to Table of Contents](#Table-of-Contents)

___

## Design
I do not have experience with Learning Management Systems (LMS), but a teammate had reported frequent frustration with them because they often force users to start over at the beginning instead of returning to the previous location on the learning path.  We designed this LMS to have playlists making it easy for the user to find the next course they had wanted to watch whenever they finished a course.

The navbar remains the same throughout the site, allowing easy navigation.  Users with administrative permission see two additional links on their navbar for creating courses and quizzes.


[Return to Table of Contents](#Table-of-Contents)

___

## Running Locally

These steps work on Windows and assume you have Python
1. Create virtual environment
    ```
    python -m venv name
    ```
    where name is whatever you want to call the environment 
2. Activate the virtual environment
    ```
    call name\Scripts\activate
    ```
    where name is the name of the virtual environment you created
3. Clone this repository
    ```
    git clone https://github.com/Purposefully/TeachMe.git
    ```
4. Move into the repository
    ```
    cd TeachMe
    ```
5. Install the dependencies
    ```
    pip install -r requirements.txt
    ```
6.  Move into the TeachMe app
    ```
    cd TeachMe
    ```
7.  Get a random secret key.  Using https://miniwebtool.com/django-secret-key-generator/ is one option.

8.  Create a secrets.py file and include a secret key
    ```
    notepad secrets.py
    ```
    Choose yes to create the file.
    Then type the following into the file.  Save and close.
    ```
    secret='paste secret key here'
    ```
9.  Get a YouTube API key
    https://developers.google.com/youtube/v3/getting-started






10.  Move out of the app
    ``` 
    cd..
    ```
11. Migrate
    ```
    python manage.py migrate
    ```
12. Run a local server
    ```
    python manage.py runserver
    ```
13.  Open browser  
        ```
        localhost8000:
        ```

[Return to Table of Contents](#Table-of-Contents)
