`🗂️ Project Structure:`

- `appAuth`: Contains models, serializers, views and urls of user authentication.



`How to run the project`
- Run  : `pip install -r requirements.txt`
- Run : `py manage.py migrate`
- Run : `python manage.py createsuperuser`
- Run : `python manage.py runserver`


Free backend deployment link : `https://crud-u6f8.onrender.com/`

Postman testing screenshot link : `https://docs.google.com/document/d/15Cd1pikH2KJA0I7cogsT6RMi8Qj91_9blsq4UQvz0W8/edit?usp=sharing` 


`Registration:`
To register, provide a phone number, username, password, and confirm_password.

`Registration will fail if:`
A user with the given phone number already exists.
The password is shorter than 6 characters.
The password and confirm_password do not match.
Make sure to use a unique phone number and set a password with at least 6 characters.

`Login:`
To log in, provide a phone number and password.
Login will fail if:
The phone number, password, or both are incorrect.


`Logout:`
To log out, the user must be authorized and provide a refresh_token.


`Update Membership:`
Only an admin user can update a user's membership.
When an admin updates the member_status, the member_start_date and member_expire_date are automatically set in the User model.
