<h1 align="center">Welcome to Movie Link 👋</h1>

> Scrapes movie links from different websites using `beautifulsoup` and `Selenium`.<br /> This project is only for educational purpose.

## ✨ Demo

If you are not getting the required result, try to be more specific by providing more details. Sometimes you might be required to use VPN.

<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208126172-a623d21e-5d0a-4ca9-8e1b-85af675be7ae.png" alt="demo"/>
</p>
<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208126179-bfc94ae4-8102-4e4f-8a5e-afa610c398f1.png" alt="demo"/>
</p>
<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208126200-2b28c5c9-35b8-43ec-9452-65ecef0f7942.png" alt="demo"/>
</p>
<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208126247-9664916f-8caf-4be8-b01b-d4bb74c3405c.png" alt="demo"/>
</p>
<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208126278-6c89ae03-feea-4b1d-a96d-0a4e3e85abde.png" alt="demo"/>
</p>
<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208126286-3f861a0d-249f-4d1e-951f-571bc9a2e9a9.png" alt="demo"/>
</p>
<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208126318-4540c42a-af93-4ab5-bd16-351ffaf9f646.png" alt="demo"/>
</p>

## 🚀 Usage

Either you can use <a href="https://movie-link.up.railway.app/">this</a> website or run the project locally.
Remember that the website from which the data is scraped can change its tags and attributes anytime, leading to the `non-functioning` of the project.

<b>To run the project locally, follow the steps:</b>

Download the project from <a href="https://github.com/4d4r5h/movielink/archive/refs/heads/main.zip">here</a>. Extract it.

Create a `virtual environment`.
```sh
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate
```
If unable to activate, run the below command in the powershell as an administrator and enter `Y`.
```sh
Set-ExecutionPolicy RemoteSigned
```

Install all the required libraries.
```sh
pip install -r requirements.txt
```
<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208132310-f4b2d94e-5851-4f7b-9fec-b77495044773.png" alt="usage"/>
</p>

Run the server and visit the website.
```sh
python manage.py runserver
```
<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208132353-b916ecb1-72d8-448b-b50f-c5f4e10190aa.png" alt="usage"/>
</p>

Do not forget to create a `.env` file and put all the keys inside it.
<p align="center">
  <img width="800" align="center" src="https://user-images.githubusercontent.com/46349391/208132397-f66b02c6-661e-42be-b117-0d728a018291.png" alt="usage"/>
</p>

Read [this](https://mixedanalytics.com/blog/seo-data-google-custom-search-json-api/) to know how to get the keys.
<br>
OR
<br>
Contact me on [LinkedIn](https://www.linkedin.com/in/adarsh-kumar-958277212/) and I'll provide you a temporary key.

## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](https://github.com/4d4r5h/movielink/issues) if you want to contribute.
