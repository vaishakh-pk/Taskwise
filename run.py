import subprocess

# Run the mailservice.py file
subprocess.Popen(['python', 'todo/mailservice.py'])

# Run the Django server
subprocess.run(['python', 'manage.py', 'runserver'])
