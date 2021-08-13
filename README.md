The following documentation describes how the cashier app works.
1.	The app’s main idea is each person in the building to register and pay their taxes through the app.
2.	First the admin is registered and after this, each user can register and start paying their taxes.
3.	The app also features 3 user roles:
  -	Default user
  -	Household admin
  -	Admin

3.1 The default user can pay their own taxes and comment news in the “News” section.

3.2 The household admin user inherits the default user functionality and has the following advantages:
  - Can approve/ reject users to their household
  - Can add other default users to the household admin group
  - Can remove default users
  - Can pay taxes for other members in the household
  - Can edit the household ideal parts
  
3.3 The admin user inherits the household admin functionality and has the following advantages:
  - Is a household admin for each household
  - Can remove household admins
  - Can update the taxes that each default user pays each month
  - Can pay salaries
  - Can add news
 
The idea of having 2 levels of administration is to split the responsibilities, so the main admin (superuser) doesn’t have to deal with every single operation for default users.
The app includes a news section, where the admin adds important information. In the “News” section there are automatic messages to show if a tax or salary has changed. All users can comment on it.
The admin has a view for all households and for all users and has full CRUD permissions.
