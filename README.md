# Saldua_Final_Project_Adv_Comprog

I. A Brief Project Overview

    EduManga Hub is an innovative platform designed to provide a centralized hub for comic enthusiasts and educators to interact with manga in a digital environment. Users can add, view, search, and manage their comics while maintaining personal profiles and receiving relevant notifications. The application also supports admin functionalities to ensure smooth operation and content moderation.

    The project's goal is to provide a seamless, engaging user experience, bridging entertainment and education through manga. It emphasizes accessibility, user-centric design, and efficient data management, aligning with global goals of quality education and reduced inequalities.

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

Functions like center_window() ensure dynamic window placement, enhancing cross-device usability.


6. Notifications:

A notification system was integrated using database queries and message boxes to inform users about important updates, enhancing interactivity.


7. Admin Privileges:

Separate workflows for regular users and admins are created to manage content and users, ensuring security and role-specific access.

-------------------------------------------------------------------------------------------------------------------------------------------------------------

III. Details of the Chosen SDG and Its Integration

Sustainable Development Goal (SDG) 4: Quality Education


  EduManga Hub aligns with SDG 4: Quality Education by leveraging the universal appeal of comics to promote literacy, creativity, and educational engagement. The platform provides an accessible space for users to explore stories that can inspire learning, while its admin features ensure the quality and relevance of content.

* Users can contribute and access a wide variety of comics, encouraging the sharing of culturally diverse stories and educational themes.

* Comics provide a medium for storytelling that enhances reading skills and fosters imagination, especially for young users.

* The notification system and user interaction features promote collaboration and knowledge sharing within the community.

* Admins can curate content, ensuring the inclusion of comics with educational themes and reducing exposure to inappropriate material.

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
