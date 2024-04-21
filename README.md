# Authentication / Authorization

## Flask Feedback

This project involves creating an application that allows users to sign up and log in to their own accounts. Once logged in, users can add, edit, and delete feedback, as well as view a list of all feedback they've given. Many of these routes are protected, ensuring that only authenticated users can access certain features.

## Part 0: Set up your environment

Set up a virtual environment, install necessary packages with pip, and host your code on GitHub.

## Part 1: Create User Model

Create a `User` model for SQLAlchemy with the following columns:
- `username`: a unique primary key, up to 20 characters
- `password`: a non-nullable text column
- `email`: a non-nullable unique column, up to 50 characters
- `first_name`: a non-nullable column, up to 30 characters
- `last_name`: a non-nullable column, up to 30 characters

## Part 2: Make a Base Template

Create a base template with placeholders for the page title and content. Other templates will extend this base template.

## Part 3: Make Routes For Users

- **GET /:** Redirect to /register.
- **GET /register:** Show a form to register a new user.
- **POST /register:** Process the registration form and redirect to /secret upon successful registration.
- **GET /login:** Show a form to log in.
- **POST /login:** Process the login form and redirect to /secret if authenticated.
- **GET /secret:** Display "You made it!" (to be updated later).

## Part 4: Protect the /secret Route

Store the username in the session upon successful registration or login to restrict access to /secret to authenticated users only.

## Part 5: Log out users

- **GET /logout:** Clear session information and redirect to /.

## Part 6: Change /secret to /users/<username>

- **GET /users/<username>:** Display user information (excluding password) and restrict access to logged-in users.

## Part 7: Add Feedback Model

Create a `Feedback` model for SQLAlchemy with the following columns:
- `id`: a unique primary key, auto-incrementing integer
- `title`: a non-nullable column, up to 100 characters
- `content`: a non-nullable text column
- `username`: a foreign key referencing the `username` column in the `users` table

## Part 8: Modify Routes For Users and Feedback

- **GET /users/<username>:** Show user information and feedback. Allow only the logged-in user to access.
- **POST /users/<username>/delete:** Delete user and associated feedback. Restrict access to the user who is logged in.
- **GET /users/<username>/feedback/add:** Display form to add feedback. Restrict access to the logged-in user.
- **POST /users/<username>/feedback/add:** Add new feedback. Allow only the logged-in user to add feedback.
- **GET /feedback/<feedback-id>/update:** Display form to edit feedback. Allow only the user who wrote the feedback.
- **POST /feedback/<feedback-id>/update:** Update feedback. Restrict access to the user who wrote the feedback.
- **POST /feedback/<feedback-id>/delete:** Delete feedback. Allow only the user who wrote the feedback to delete it.

## Further Study

- Handle registration and authentication logic in models.py.
- Prevent users from accessing register or login forms if already logged in.
- Add a 404 page for not found users or feedback and a 401 page for unauthorized users.
- Implement an `is_admin` column in the users table to designate admin users with additional privileges.
- Display helpful error messages for form submission failures.
- Write tests for authentication and authorization logic.
- Challenge: Implement functionality to reset passwords using email verification.
