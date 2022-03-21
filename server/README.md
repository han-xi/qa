
## 1. Installing mongodb

Install mongodb ([Link](https://www.mongodb.com/))
change the name of the server in run.py (now: YAMI)

## 2. Installing Packages

```bash
pip install -r requirements.txt
```

## 3. Run the application locally

```bash
set FLASK_APP=run.py 

python -m flask run # at: http://127.0.0.1:5000/

# to change port add: "--port=1337"
```
