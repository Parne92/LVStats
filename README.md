<img src="https://github.com/Parne92/LVStats/blob/main/static/Dark%20Logo.png" width="100" />

# Los Vaqueros Stats             

## What is this?

  This is an "open source" version of my web app, Los Vaqueros Stats. It is used as a stat tracker for me and my friends to compete against eachother in soccer games, even if we're not all in the same geographic area. 

  It's important to note that for the ease of setting up this repo, it is **NOT** production safe. The `SECRET_KEY` variable will have to be changed if you want to deploy this on your own. It also does not include a database, but if you have your environment set up correctly, an empty one will be created on `flask run`. 


## What's it built with?

  This project was my first foray into building a web app with Flask. So I tried to keep the other aspects as simple as I could, because that's not what I was focusing on in terms of development and learning. Because it's also built primairly for use with my friends, the sign up process is very simple, in that it's only a username and password that's required.

## Photos of the app:

First, the user will be prompted to log in, or create an account, on a mobile interface, this looks like this: 
<img src="https://github.com/Parne92/LVStats/blob/main/PicturesForTheReadMe/Login%20.png" width="50%" />

Once the user is logged in, they will be greeted by their account dashboard: 
<img src="https://github.com/Parne92/LVStats/blob/main/PicturesForTheReadMe/Player%20Dashboard.png" width="50%" />

And they are free to add (globally viewable) games, so other users can see their activity and know what they need to beat to claim top spot! 
<img src="https://github.com/Parne92/LVStats/blob/main/PicturesForTheReadMe/GameDashboard.png" width="50%" />

<img src="https://github.com/Parne92/LVStats/blob/main/PicturesForTheReadMe/Main%20Dashboard.png" width="50%" />
