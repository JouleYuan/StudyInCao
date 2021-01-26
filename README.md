# StudyInCao - Back End

This is a flask-restful back end of the StudyInCao project for ZJU RE&SME courses.

## Build

Install the required dependencies.

```shell
pip install -r requirements.txt
```

Create database studyincao and execute the database.sql file in mysql.

```
CREAT DATABASE studyincao;
SOURCE studyincao.sql;
```

Create your own directory to store uploaded files. The file directory is shown as followed.

```
file
├── avatar
│   ├── course
│   ├── student
│   └── teacher
├── homework
└── resource
```

## Run

If you are to run this on Linux Server, input the following in the shell.

```shell
gunicorn app:app -c gunicorn.conf.py --daemon
```

If you are to run this on Windows, you can run this back end by running app.py.