# darrkzero-scissor Application
darrkzero-scissor project aims to develop a user-friendly and efficient URL shortening service. This application makes URL management a breeze! With various powerful tools and features, you can easily shorten URLs, customize them to your liking, generate QR codes, and track the number of clicks for each URL. It is built with Flask  and can be accessed through https://darrkzero.pythonanywhere.com/, a PythonAnywhere-powered web app

<h1>Prerequisites</h1>
Python version: Python 3.10.10
<div></div>  
<h1>Installation</h1>
<div></div>
<ul style="font-size:18px;">
    <li>Clone the repository to your local machine.</li>
    <li>Navigate to the project directory.</li>
    <li>Create a virtual environment and activate it:</li>
    <li>Install the dependencies:</li>
    <li>Run the application:</li>
</ul>
<h1>Website Features</h1>
1. A user can shorten long URLs to make them more compact and easier to share. Additionally, the user have the option to customize the shortened URLs with their own desired keywords.
2. QR code generation for the shortened URLs, it allows the user to quickly share them in printed or digital media. Simply scan the QR code with a compatible device to access the corresponding URL
3. The website tracks the number of clicks each shortened URL receives. This helps the user monitor the popularity and effectiveness of their shared links.


```console
python -m venv venv
source venv/bin/activate
```

```console
pip install -r requirements.txt
```

```console
flask run
```

## Built with:
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
