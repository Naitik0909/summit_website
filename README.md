# MIT WPU Summit 2023 Website

This project has been created on MVT Architecture using Django. MySQL database has been used to store the data.
This guide will help you setup the repository on your local machine as well as deploy any changes to the college server.

## Running the app locally

### Prerequisites

1. Python installed on you machine (Version 3.9 or higher)
2. Get the `.env` file contents from one of the collaborators of the repo or the Summit team.


### Steps

1. Clone the github repository
2. Place the `.env` file (mentioned in prerequisites) in the `summit_app` folder.
3. Create and Activate a virtual environment (Optional)
4. To install the dependencies, run- `pip3 install -r requirements.txt` on linux OR `pip install -r requirements.txt` on windows.
5. Finally, to run the project locally, run- `python3 manage.py runserver` on linux OR `python manage.py runserver` on windows.

Bravo! Now you'll be able to visit the website on localhost port 8000 (http://127.0.0.1:8000)

## Deploying the app to the Azure VM

### Prerequisites

1. SSH command to access the Azure VM that includes the IP address and the superuser password. (Which college will provide)
2. Credentials of a Github account that has write access to this repository.(Or even Summit's own github account access)

### Steps

The Github app has been cloned into our college's Azure VM and has been deployed there itself. To deploy the changes to production, follow these steps-

1. SSH into the VM provided by our college. (Ask Summit team for credentials)
2. When you are connected to the VM, execute the following commands in order-

```
source myenv/bin/activate
cd summit_website
git pull origin main
pip3 install -r requirements.txt
python3 manage.py collectstatic
sudo service supervisor restart
sudo service nginx restart
```

These steps will only work if the college gives us back the same VM as 2023. If they give us a new VM, then these commands won't work. In that case, you'll have to setup the app first on the new VM and then execute the above commands.

> Note- After running the command `git pull origin main`, you'll be prompted to login to github. You can enter credentials of any github account that has the write access to this repository.
