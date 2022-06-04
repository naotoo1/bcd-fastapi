# bcd-fastapi
Breast Cancer detection using prosemble ML package within fastapi framework with deployment on Heroku cloud platform
## How to use
To diagnose breast cancer disease and return the confidence of the diagnosis,
1. click on the bcd-fastapi on the environments section and then click on view deployment or simply use the link https://bcd-fastapi.herokuapp.com/docs
3. After opening the link click on ```GET``` ---> ```Try it out``` ---> ```Execute```
4. click on ```POST``` ---> ```Try it out``` enter the values for Radius_mean and Radius_texture and choose the method either as soft or hard. Below is an example
```
"Radius_mean": 10,
"Radius_texture": 9.8,
"Method": "soft"
  ```
 4. click on ```Execute```
