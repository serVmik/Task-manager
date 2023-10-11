[![Actions Status](https://github.com/serVmik/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/serVmik/python-project-52/actions)
[![Python CI](https://github.com/serVmik/python-project-52/actions/workflows/pici.yml/badge.svg)](https://github.com/serVmik/python-project-52/actions/workflows/pici.yml)
<a href="https://codeclimate.com/github/serVmik/python-project-52/maintainability"><img src="https://api.codeclimate.com/v1/badges/ad45895325c9ef37b952/maintainability" /></a>
<a href="https://codeclimate.com/github/serVmik/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/ad45895325c9ef37b952/test_coverage" /></a>

# Task manager
[wiki](https://en.wikipedia.org/wiki/Task_management)


Task manager is the webapp of managing a task through its lifecycle.
It involves planning, testing, tracking.

[WEB](https://task-manager-cecs.onrender.com/) version

## How to install the app:
Clone the application from GitHub and install the necessary:  
```
git clone git@github.com:serVmik/python-project-52.git
```    
```
make install
```  

Create '.env' file in the root folder and add the following variables to it:
```  
SECRET_KEY=some_secret_key  
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

### Home page
![home](https://github.com/serVmik/python-project-52/assets/56305558/bbdcef86-88f4-42c0-9e87-725d98e4b979)

### Registration
Only a registered user can create, view and change tasks, statuses and labels for tasks. 
![create_user](https://github.com/serVmik/python-project-52/assets/56305558/a2cd4700-2b8e-4926-836b-758f9dd346bd)

### View the full list of users
![users_auth](https://github.com/serVmik/python-project-52/assets/56305558/c680c7ba-68a4-43df-bd2c-bc28525fb92e)

### View the complete list of tasks with the ability to apply filtering
![tasks_list](https://github.com/serVmik/python-project-52/assets/56305558/ee2ba442-4ea6-4a2e-90ba-1e59d21968d9)

### Create statuses and labels by name only
![create_label](https://github.com/serVmik/python-project-52/assets/56305558/dea27d7f-9c7f-42cc-a25f-a38e6d311b6f)

### Create tasks and view all tasks together with other users  
Implemented task filtering based on several criteria.
![create_task](https://github.com/serVmik/python-project-52/assets/56305558/1a575a91-d62e-4a90-9b77-684203f2ddfd)

### View each task in detail separately
![create_show](https://github.com/serVmik/python-project-52/assets/56305558/b4332c29-9fb8-446c-8fc7-cab5437a817d)

