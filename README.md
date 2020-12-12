# fampay_assignment

Here are steps to set up and run the project after cloning it to your device.

1) We set up RabbitMq which is a message broker that allows Celery to send and recieve messages. Run the following lines on
   your MacOS terminal.

   ```
   brew install rabbitmq 
   export PATH=$PATH:/usr/local/sbin
   brew services start rabbitmq
   ```
   
   For Linux , use apt-get instead.
   
2) Set up and activate your virtualenv using the following commands. 
   
   MacOS
   
   ```
   pip install virtualenv
   virtualenv <your-env>
   source <your-env>/bin/activate
   ```
  
   Windows
   
   ```
   pip install virtualenv
   virtualenv <your-env>
   <your-env>\Scripts\activate
   ```
 
3) To install the dependencies in your virtualenv , go to the the base directory of this repositry and run the following command

   ```
   pip install -r requirements.txt
   ```
   
4) Now , to get the django server running , run the following commands from your base directory.
   
   ```
   python manage.py migrate
   python manage.py runserver
   ``` 

5) The project uses celery for asynchronously and periodically fetching data from the youtube api and updating the database. 
   Run these commands in two seperate terminals from your base directory.
   
   This command begins the celery worker which executes a task. 
   
   ```
   celery -A fampay_assignment worker -l info
   ```
   
   This command uses celery beat to schedule tasks in particular intervals.
   
   ```
   celery -A fampay_assignment beat -l info
   ```
   
   After executing the above steps , the project should be running properly.
   The first celery task first populates the sqlite databse with data about videos from Youtube containing the string "Playstation 5".
   After every 30 seconds , a celery task looks for new videos and accordingly updates the db.

   A GET request to the '/api' endpoint returns a paginated json response ( 100 entries per page ) containing the stored entries from the db. These 
   are sorted in descending order of published datetime. To request for a specific page , provide the pge no to the parameter 'page'. The easiest way to do this is to append 
   ``` ?page=``` followed by the page number to the endpoint.
   
   Similary , a GET request to the '/search' endpoint returns a filtered response based on the value provided to the parameter 'search'. 
   Multiple search terms should be whitespace and/or comma separated.


  
   
  
