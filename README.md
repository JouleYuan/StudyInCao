## StudyInCao - Back End

This is a flask-restful back end of the StudyInCao project for ZJU RE&SME courses.

### Quick Start

Install the required dependencies.

```python
pip install -r requirements.txt
```

Create your own directory to store uploaded files. The file directory is shown as followed.

```
file
└── avatar
    ├── student
    └── teacher
```

If you are to run this on Linux Server, input the following in the shell.

```
gunicorn app:app -c gunicorn.conf.py --daemon
```

If you are to run this on Windows, you can run this back end by running app.py.