# dailytaskmanager

<h5>Requirements:</h5>
- Have Docker installed. To install Docker, use this guide: https://docs.docker.com/get-docker/ or, for linux, try this one: https://www.linux.com/topic/desktop/how-install-and-use-docker-linux/ <br/>
- Have Docker Compose installed: https://docs.docker.com/compose/install/ <br />
- Web browser <br />

<h5>Installation:</h5>
1.	In the folder where the project lives, execute the following:
<pre>docker-compose build</pre>
2.	Once it's built, start up the containers (warning: it'll fail the first time! Read the next section to set it up correctly):
<pre>docker-compose up</pre>

<p></p>
<h5>Configuration of database:</h5>
4.	Wait for db service to announce that it's ready to accept connections and then, in a different terminal:
<pre>docker-compose exec db mysql -u root -p</pre>
5.	Enter the password defined in both the docker-compose.yml file and the django settings file. If not changed, the password is:
<pre>secret123</pre>
6.	Within the mysql client that is opened, we can check that the django_app database exists by typing this (if it doesn't show up, see 6a):
<pre>show databases;</pre>
6a.
<pre>create database django_app;</pre>
7.	We have to give the right privileges to the user to access the database, which we do like this (if it says you don't have permission to create a user this way, see 7a):
<pre>grant all privileges on django_app.* to 'django_app'@'%';</pre>
7a.
<pre>create user django_app@localhost identified by ‘secret123’;</pre>
8.	Within the terminal where the db container is still running, stop it with CTRL + C or, from a different terminal:
<pre>docker-compose down</pre>
9. Restart the containers:
<pre>docker-compose up</pre>
10.	The application will run now! Congratulations! But we still have to apply the right migrations, which we do, from a different terminal, like this:
<pre>docker-compose exec web python manage.py migrate</pre>
11.	The last step we have to do is create a superuser and fill in the information that is asked:
<pre>docker-compose exec web python manage.py createsuperuser</pre>
12.	Now we can access the application from here: http://localhost:8000/

<p></p>
<h5>Troubleshooting</h5>
If the web container starts working and says it can't make a connection to the database, try restarting the containers.

<p></p>
<h5>Where to see your data?</h5>
You can access the Django Admin panel like this: http://localhost:8000/admin, where we can log in using our superuser credentials. You can also access mysql from the terminal like we did in step 4.
Once you're in the mysql terminal client, you can use this handy guide to find the right sql commands: http://g2pc1.bu.edu/~qzpeng/manual/MySQL%20Commands.htm 
