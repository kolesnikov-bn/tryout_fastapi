# tryout_fastapi
Pet project for tryout new framework FastAPI


## How to use


* Собрать образ 
```docker
docker build -t tryout-fast-image .
```
* Запустить контейнер
```docker
docker run -d --name tryout-fast-container -p 5000:5000 tryout-fast-image
```
* При запуске запустится скрипт первичной загрузки данных, а так же создаст нового пользователя 
с параметрами для авторизации `username=admin`, `password=secret`
* Перейти в документацию проекта  http://127.0.0.1:5000/docs
* Все действия без значка `замок`, можно выполнять без авторизации. При наличии значка, 
необходимо ввести в форму авторизации данные `username=admin`, `password=secret`. 
После этого все методы в примерах будут доступны для выполнения 



