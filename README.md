[![Actions Status](https://github.com/serVmik/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/serVmik/python-project-52/actions)
[![Python CI](https://github.com/serVmik/python-project-52/actions/workflows/pici.yml/badge.svg)](https://github.com/serVmik/python-project-52/actions/workflows/pici.yml)
<a href="https://codeclimate.com/github/serVmik/python-project-52/maintainability"><img src="https://api.codeclimate.com/v1/badges/ad45895325c9ef37b952/maintainability" /></a>
<a href="https://codeclimate.com/github/serVmik/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/ad45895325c9ef37b952/test_coverage" /></a>

# Task manager

Task manager is the webapp of managing a task through its lifecycle.
It involves planning, testing, tracking.

[WEB](https://task-manager-cecs.onrender.com/) version

## How to install the app:

For install and use the application you will need the following applications: git, poetry. You can install them:  
```
sudo apt update
```  
```
sudo apt install git-all
```  
```
sudo apt install curl
```  
```
curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
```  

Clone the application from GitHub and install the necessary:  
```
git clone git@github.com:serVmik/python-project-52.git
```    
```
cd python-project-52
```  
```
make install
```  

Create '.env' file in the root folder and add the following variables to it:  
Set the secret key.  
```  
SECRET_KEY=secret_key  
DEBUG=False
```  
Create migrations and apply them to the database:  
```
make migrate
```

Run the application local:  
```
make dev
```  

Go to the browser address http://localhost:8000/  
## How to use the app:  
### Registration
Only a registered user can create, view and change tasks, statuses and labels for tasks. 

### Tasks list

### Create task

### Update task
