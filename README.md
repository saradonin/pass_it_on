# Pass it on 

Pass it on project is a donation management system that helps users connect with the causes they care about and facilitate the process of giving. 

## Features
This Django-based web application facilitates the donation process, allowing users to contribute to various institutions. Key features include:
- **Index Page**: Displays donation stats and institution categories.
- **Donation Form**: Authenticated users can donate to chosen categories and institutions.
- **Donation Confirmation**: Confirms successful submissions.
- **User Authentication**: Supports login, registration, and account activation.
- **User Settings**: Allows users to view and update their profile information.
- **Password Management**: Sends password reset emails and allows users to set new passwords.
- **Admin Panel**: Offers features for managing users and institutions. 

## Technologies
- Django: Backend web framework.
- Python, HTML, JavaScript: Backend and frontend development.
- Page layout including CSS and HTML mockups prepared by Magda - a graduate of CodesLab UX course.
- PostgreSQL: Database.

## Getting started

To set up the Pass it on for development or testing purposes, follow these steps:

1. Clone the repository to your local machine:

```
git clone https://github.com/saradonin/pass _it_on
```

2. Create .env file in root directory
```
SECRET_KEY=your_secret_key

POSTGRES_NAME=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password

EMAIL_HOST=your_smtp_email_host
EMAIL_HOST_USER=your_email_address
EMAIL_HOST_PASSWORD=your_email_access_token
EMAIL_PORT=587
```

3. Run the container:

```
docker-compose up
```

3. Access the app in your web browser at http://localhost:8000.

Ensure you have [Docker](https://www.docker.com/get-started/) installed before running these commands.


## License

The Scent Swap App is licensed under the MIT License. Please see the LICENSE file for more details.



