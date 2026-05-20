## NOTE FOR DEVELOPER ##

Before you start, please make sure you have the following tools installed:
1. All modules in the readme file of the project.
2. Docker and Docker Compose.
3. Paystack API keys for payment.

Ensure you set up the environment variables as specified in the project documentation. Any variable define with ${Variable_name} in docker-compose.yml or os.getenv() in settings.py, must be defined in a .env file. This may include database credentials, API keys, and other configuration settings necessary for the application to run correctly.

The backend returns every response in the form of a json. Use insomnia to see the data format for each response from every endpoint. This will help you understand how to handle the data in the frontend.

The project used docker for containerization as well as nginx so as to fit the scalability requirement defined in the project proposal. Ensure you understand how to work with docker and nginx, as this will be crucial for the operation of the application.