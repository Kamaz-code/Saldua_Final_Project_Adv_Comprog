# Saldua_Final_Project_Adv_Comprog

I. A Brief Project Overview

  EduManga Hub is an innovative platform designed to provide a centralized hub for comic enthusiasts and educators to interact with manga in a digital environment. Users can add, view, search, and manage their comics while maintaining personal profiles and receiving relevant notifications. The application also supports admin functionalities to ensure smooth operation and content moderation.

  The project's goal is to provide a seamless, engaging user experience, bridging entertainment and education through manga. It emphasizes accessibility, user-centric design, and efficient data management, aligning with global goals of quality education and reduced inequalities.


II. Explanation of How Python Concepts, Libraries, etc. were Applied

1. Graphical User Interface (GUI):

The project uses the tkinter library for creating an intuitive and responsive user interface. Components like buttons, labels, entry widgets, and frames are utilized to enhance the user experience.


2.Database Management:

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



