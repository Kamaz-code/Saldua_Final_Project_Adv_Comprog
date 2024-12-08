# Saldua_Final_Project_Adv_Comprog

I. Project Overview

  The EduManga Hub is an innovative platform designed to centralize and streamline the management of manga content with an educational focus. It caters to manga enthusiasts and administrators by enabling features like personal comic collection tracking, status updates, and efficient content searches. Administrators benefit from tools for recommending and curating content, as well as overseeing user activities, all while promoting an interactive and structured ecosystem.

Key features include:

    User Management: Enables users to sign up, log in, and access personalized collections.

    Comic Management: Supports adding, updating, and searching for comics, with user-specific and admin-added entries accessible.

    Admin Tools: Allow recommendations and oversight of all user collections.

    Notification System: Alerts users about admin actions, such as removed comics.

    Search Functionality: Simplifies comic retrieval by title.

Excluded features are external database integrations and social interactions like reviews or comments. The project follows SMART objectives, aiming for deployment by Q4 2024, with measurable success tied to achieving at least 100 comic additions and searches.

-------------------------------------------------------------------------------------------------------------------------------------------------------------

II. Explanation of How Python Concepts, Libraries, etc. were Applied

1. Graphical User Interface (GUI):

The project uses the tkinter library for creating an intuitive and responsive user interface. Components like buttons, labels, entry widgets, and frames are utilized to enhance the user experience.


2. Database Management:

sqlite3 is employed to store user data, comic details, and notifications in a relational database. The database facilitates seamless data retrieval and updates for features like adding comics, viewing user information, and managing notifications.


3. Modular Programming:

The project is structured into modular functions for various operations, such as user authentication, comic addition, and status updates. This modularity improves code readability, maintenance, and scalability.


4. Error Handling and Validation:

Input validation and exception handling are implemented to ensure robustness. For example, users are prompted for confirmation before deleting comics, and notifications handle acknowledgment status efficiently.


5. Custom Functions:

Functions like center_window() ensure dynamic window placement.


6. Notifications:

A notification system was integrated using database queries and message boxes to inform users about important updates, enhancing interactivity.


7. Admin Privileges:

Separate workflows for regular users and admins are created to manage content and users, ensuring security and role-specific access.

-------------------------------------------------------------------------------------------------------------------------------------------------------------

III. Details of the Chosen SDG and Its Integration

Sustainable Development Goal (SDG) 4: Quality Education


  EduManga Hub aligns with SDG 4: Quality Education by leveraging the universal appeal of comics to promote literacy, creativity, and educational engagement. The platform provides an accessible space for users to explore stories that can inspire learning, while its admin features ensure the quality and relevance of content.

-------------------------------------------------------------------------------------------------------------------------------------------------------------

IV. Instructions for Running the Program

--- Prerequisites ---

Ensure Python 3.7+ is installed on your system.

Install the required libraries using the following command:
pip install tk sqlite3


--- Prepare the following resources ---

A valid SQLite database file (user_data.db).
An application logo image (smol_ina.png).


--- Steps to Run the Program ---

Place the project files and resources in the same directory.
Run the script using the Python interpreter


--- Upon launch ---


Login Window: Enter a valid username and password to log in or register a new account.


Main Page (User): Access features like adding comics, viewing your collection, and managing your profile.


Admin Page: Manage users and comics with additional administrative controls.


--- Note ---

To test admin functionalities, ensure the account has admin privileges set in the database.
The database schema can be initialized using the create_db() function in the code.
