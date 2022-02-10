# Chromedriver-Updater
Just add to your project, in the same folder that you have the chromedriver and use:

```py
try:
    browser = webdriver.Chrome(executable_path='./chromedriver')
except Exception as error:
    update_chromedriver.start(error)
    browser = webdriver.Chrome(executable_path='./chromedriver')
```
