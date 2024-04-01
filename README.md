# Immunization Tracking System

## Description
The Immunization Tracking System is a software application designed to track and manage immunization records for individuals. It provides a centralized platform for healthcare providers to record and monitor immunization data, ensuring accurate and up-to-date information.

## Features
- User-friendly interface for easy navigation and data entry
- Secure authentication and access control to protect sensitive information
- Ability to add, edit, and delete immunization records
- Automated reminders for upcoming immunizations and overdue doses
- Comprehensive reporting and analytics to track immunization coverage rates
- Integration with external systems for data exchange and interoperability

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/immunization-tracking-system.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure the database connection in the `.env` file:
    ```bash
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=immunization_db
    DB_USER=your-username
    DB_PASSWORD=your-password
    ```

4. Set up the email and SMS notification system:
    - Email: Update the `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` variables in the `.env` file with your email provider's details.
    - SMS (Africa's Talking): Update the `AFRICASTALKING_USERNAME` and `AFRICASTALKING_API_KEY` variables in the `.env` file with your Africa's Talking account details.


## Usage
1. Access the application through your web browser at `http://localhost:3000`.
2. Sign up for a new account or log in with your existing credentials.
3. Navigate through the different sections to manage immunization records, view reports, and configure settings.

## Notification System
The Immunization Tracking System includes a notification system that utilizes both email and SMS (Africa's Talking) to send automated reminders for upcoming immunizations and overdue doses. To set up the notification system, follow these steps:

1. Make sure you have the necessary environment variables set by running the following command:
    ```bash
    mysql -u root -p < immunization_DB.sql
    ```

2. Add the following command to your cron job:
    ```bash
    0 11 * * * /<path to the dir>/cron.sh
    ```

## Contributing
Contributions are welcome! If you would like to contribute to the Immunization Tracking System, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.