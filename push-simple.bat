@echo off
echo Pushing EchoGuard to GitHub...

echo Initializing Git repository...
"C:\Program Files\Git\bin\git.exe" init

echo Configuring Git user...
"C:\Program Files\Git\bin\git.exe" config user.name "JosephHonpah"
"C:\Program Files\Git\bin\git.exe" config user.email "honpahj@gmail.com"

echo Adding files to Git...
"C:\Program Files\Git\bin\git.exe" add .

echo Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "Initial EchoGuard deployment - Now Live!"

echo Adding remote repository...
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/JosephHonpah/Echo-Guard.git

echo Pushing to GitHub...
echo You will be prompted for your GitHub username (JosephHonpah) and personal access token.
"C:\Program Files\Git\bin\git.exe" push -u origin main

echo Done! EchoGuard has been pushed to GitHub.
pause