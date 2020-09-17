# Auto test for Web application
Script based on page onject pattern, for web-app testing and further integration to TestRail

# How to install
Web-app should be already installed! Get app from your mentor.
Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```bash
$ pip install -r requirements.txt
```
Browser name (Chrome/Firefox), url should be in config.json
___
Run pytest test_web_app for testing module:
```bash
$ pytest test_web_app.py --browser='Chrome'
============================= test session starts ==============================
test_web_app.py .                                                    [100%]
============================== 1 passed in 34.74s ==============================
```