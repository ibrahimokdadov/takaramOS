      __          __                                        
    _/  |______  |  | ______________    _____   ____  ______
    \   __\__  \ |  |/ /\_  __ \__  \  /     \ /  _ \/  ___/
     |  |  / __ \|    <  |  | \// __ \|  Y Y  (  <_> )___ \ 
     |__| (____  /__|_ \ |__|  (____  /__|_|  /\____/____  >
               \/     \/            \/      \/           \/ 

# takaramOS
Scalable donations platform using python and mongodb
This is a platform for donations. Say you have things laying around and you do not need. What many would tell you to do is to sell them. What happens if you could not sell it? or simply you do not want to sell it?  This platform is intended to help people give to others. Simply take a picture of the item upload it and let the world make use of it. 

Here is the moto here: Something you may not need may be very useful to someone else.
Do not hold back and start giving.

This version is still in the alpha stage. Hopefully I will be adding more features to it as time goes. Feel free to tune in and help the way you want.

Here is how it looks so far:

![alt tag](https://github.com/ibininja/takaramOS/blob/master/src/static/assets/takaramOS_small.png?raw=true) | ![alt tag](https://github.com/ibininja/takaramOS/blob/master/src/static/assets/takaram_dashboard_small.png?raw=true) 

###version
0.2

###technicalilites
This project is made using:
* python 3
* mongoDB 3
* bootstrap 3
* x-editable
* d3.js
* dc.js
* crossfilter.js

###running on local
To run this project. simply install all requirements in requirements.txt and then in <b>config.py</b> set the <b>APP_PATH</b> to where the folder project is. Example
If project is in (windows) <code>C:\\\takramOS\src</code> set the path as: 
<code>APP_PATH 'C:\\\takaramos'</code>

###current features
* register and signup
* user can add profile
* user can edit profile
* if user does not have profile will automatically be prompted to create one.
* add item [inc. uploading images]
* each users edits their own items
* delete item
* view items without loggin in
* displays item details on click [shows multiple images]
* displays badge for multiple images uploaded
* add items does not show to unlogged in users
* basic approval center for new items
* logged in users can edit posts
* added Admin access (admin automatically detected)
 * ability to edit items
 * view basic statistics (number of items, number of user)
 * view list of users
 * delete specific user
* ability to search for items
* messaging system to communicate with item owner from within the app.
 * send and recieve message about posted items
 * notifications for new unread messages.
 * notifications in navbar

###todos
* add encryption to registration and logging in* 
* add profile image to accounts and navbar
* add graphs showing new items each day 
* add email handling

###done
* ~~add edit items~~
* ~~add approval center for new items~~
* ~~add admin page~~
  * ~~ability to edit items~~
  * ~~view basic statistics (number of items, number of user)~~* 
* ~~verify each users edits their own items~~
* ~~ability to search for items and in description~~
* ~~add Multiple image gallery on detail view~~
* ~~messaging system~~
* ~~add graphs showing previous registrations~~
* ~~add graphs showing items posted per given period~~
* ~~add graphs showing new registrations~~
* ~~add profiles to accounts~~
* ~~editing profile details~~

###license
MIT?
