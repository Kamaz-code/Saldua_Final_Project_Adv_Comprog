import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a SQLite database with 'users', 'comics', and 'notifications'
def create_db():
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (users_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      username TEXT UNIQUE, 
                      password TEXT, 
                      is_admin INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS comics
                     (comics_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      title TEXT, 
                      genre TEXT, 
                      author TEXT, 
                      status TEXT, 
                      users_id INTEGER DEFAULT NULL,
                      added_by_admin INT DEFAULT 0,
                      FOREIGN KEY (users_id) REFERENCES users (users_id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS notifications
                     (notifications_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      users_id INTEGER, 
                      message TEXT, 
                      status TEXT,
                      acknowledged INTEGER DEFAULT 0,
                      FOREIGN KEY (users_id) REFERENCES users (users_id))''')
        # Create an admin account if not already created
        c.execute("SELECT * FROM users WHERE username='admin'")
        admin = c.fetchone()
        if not admin:
            c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
                      ('admin', 'admin@123', 1))  # Admin credentials (username: admin, password: admin@123)

# Add comic as admin
def admin_add_comic(title, genre, author):
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()
        # Fetch admin's users_id dynamically
        c.execute("SELECT users_id FROM users WHERE username = 'admin'")
        admin_id = c.fetchone()[0]
        # Add the comic with admin's users_id
        c.execute(
            '''INSERT INTO comics (title, genre, author, status ,users_id, added_by_admin) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (title, genre, author, "Try this", admin_id, 1)
        )

# Get the user ID for a given username
def get_user_id(username):
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()
        c.execute("SELECT users_id FROM users WHERE username=?", (username,))
        user = c.fetchone()
        return user[0] if user else None

# Check if user exists in the database and return whether it's admin
def check_user(username, password):
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
    return user

# Add user to the database (regular user)
def add_user(username, password):
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, 0))  # 0 for regular user

# Add comic to the database
def add_comic(title, genre, author, users_id, added_by_admin=0):
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()

        c.execute("INSERT INTO comics (title, genre, author, status, users_id, added_by_admin) VALUES (?, ?, ?, ?, ?, ?)", 
                   (title, genre, author, 'Currently reading', users_id, added_by_admin))
        conn.commit()

# Get all comics from the database
def get_user_comics(users_id):
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM comics WHERE users_id=? OR added_by_admin = 1", (users_id,))
        comics = c.fetchall()
    return comics

# Update comic status
def update_comic_status(title, new_status, users_id):
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()
        c.execute("UPDATE comics SET status=? WHERE title=? AND users_id=?", 
                  (new_status, title, users_id))

# Search comics by title
def search_comics_by_title(search_term):
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM comics WHERE title LIKE ?", ('%' + search_term + '%',))
        results = c.fetchall()
    return results

# Center window function
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

# Login window
def login_window():
    login_win = tk.Tk()
    login_win.title('EduManga Hub')
    login_win.config(bg='#031716')
    
    icon = tk.PhotoImage(file='smol_ina.png')
    login_win.iconphoto(False, icon)
    
    # Set the window size and position
    center_window(login_win, 1080, 500)

    # Contains both frame
    container_login = tk.Frame(login_win, bg="#031716")
    container_login.pack(fill=tk.BOTH, expand=True)

    # Left Frame
    left_frame_login = tk.Frame(container_login, bg="#031716")
    left_frame_login.pack(side=tk.LEFT, expand=True)

    # Logo Image
    logo_image = tk.PhotoImage(file='smol_ina.png')
    logo_label = tk.Label(left_frame_login ,image=logo_image, bg="#031716")
    logo_label.pack(pady=10)
    
    # Welcome text
    welcome_label = tk.Label(left_frame_login, text="WELCOME TO EDUMANGA HUB", font=("Helvetica", 24, 'bold'), bg='#031716', fg='#6BA3BE')
    welcome_label.pack(padx=5)

    # Right Frame
    right_frame_login = tk.Frame(container_login, bg="#031716")
    right_frame_login.pack(side=tk.RIGHT, expand=True)

    # Username and Password entry
    username_label = tk.Label(right_frame_login, text="Username:", font=("Helvetica", 14), bg='#031716', fg='#6BA3BE')
    username_label.pack(pady=10)
    username_entry = tk.Entry(right_frame_login, font=("Helvetica", 14))
    username_entry.pack(pady=10)

    password_label = tk.Label(right_frame_login, text="Password:", font=("Helvetica", 14), bg='#031716', fg='#6BA3BE')
    password_label.pack(pady=10)
    password_entry = tk.Entry(right_frame_login, show='*', font=("Helvetica", 14))
    password_entry.pack(pady=10)

    # Login button
    def login():
        username = username_entry.get()
        password = password_entry.get()
        user = check_user(username, password)
        if user:
            if user[3] == 1:  # Check if the user is an admin
                login_win.destroy()
                admin_page()  # Redirect to admin page
            else:
                login_win.destroy()
                main_page(username)  # Pass the username to main page for regular users
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_button = tk.Button(right_frame_login, text="Login", font=("Helvetica", 14), borderwidth=0, bg='#032F30', fg='#6BA3BE', activebackground='#6BA3BE', activeforeground='#032F30', command=login)
    login_button.pack(pady=20)

    # Sign Up redirect
    def go_to_signup():
        login_win.destroy()
        signup_window()

    signup_button = tk.Button(right_frame_login, text="Don't have an account? Sign Up", font=("Helvetica", 14, "bold"), borderwidth=0, bg='#032F30', fg='#6BA3BE', activebackground='#6BA3BE', activeforeground='#032F30', command=go_to_signup)
    signup_button.pack(pady=20)

    login_win.mainloop()

# Sign Up window
def signup_window():
    signup_win = tk.Tk()
    signup_win.title('EduManga Hub')
    signup_win.config(bg='#031716')

    icon = tk.PhotoImage(file='smol_ina.png')
    signup_win.iconphoto(False, icon)

    # Set the window size and position
    center_window(signup_win, 1080, 500)

    # Container for both frames
    container_signup = tk.Frame(signup_win, bg="#031716")
    container_signup.pack(fill=tk.BOTH, expand=True)

    # Left Frame
    left_frame_signup = tk.Frame(container_signup, bg="#031716")
    left_frame_signup.pack(side=tk.LEFT, expand=True)

    # Logo Image
    logo_image = tk.PhotoImage(file='smol_ina.png')
    logo_label = tk.Label(left_frame_signup ,image=logo_image, bg="#031716")
    logo_label.pack(pady=10)

    # Welcome text
    welcome_label = tk.Label(left_frame_signup, text="CREATE A NEW ACCOUNT", font=("Helvetica", 24, "bold"), bg='#031716', fg='#6BA3BE')
    welcome_label.pack(pady=5)

    # Right Frame
    right_frame_signup = tk.Frame(container_signup, bg="#031716")
    right_frame_signup.pack(side=tk.RIGHT, expand=True)

    # Username and Password entry
    username_label = tk.Label(right_frame_signup, text="Username:", font=("Helvetica", 14), bg='#031716', fg='#6BA3BE')
    username_label.pack(pady=10)
    username_entry = tk.Entry(right_frame_signup, font=("Helvetica", 14))
    username_entry.pack(pady=10)

    password_label = tk.Label(right_frame_signup, text="Password:", font=("Helvetica", 14), bg='#031716', fg='#6BA3BE')
    password_label.pack(pady=10)
    password_entry = tk.Entry(right_frame_signup, show='*', font=("Helvetica", 14))
    password_entry.pack(pady=10)

    # Sign Up button
    def signup():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            add_user(username, password)
            messagebox.showinfo("Success", "Account created successfully!")
            signup_win.destroy()
            login_window()
        else:
            messagebox.showerror("Error", "Please fill out all fields")

    signup_button = tk.Button(right_frame_signup, text="Sign Up", font=("Helvetica", 14), borderwidth=0,  bg='#032F30', fg='#6BA3BE', activebackground='#6BA3BE', activeforeground='#032F30', command=signup)
    signup_button.pack(pady=20)

    # Back to login
    def go_to_login():
        signup_win.destroy()
        login_window()

    back_button = tk.Button(right_frame_signup, text="Back to Login", font=("Helvetica", 14), borderwidth=0,  bg='#032F30', fg='#6BA3BE', activebackground='#6BA3BE', activeforeground='#032F30', command=go_to_login)
    back_button.pack(pady=20)

    signup_win.mainloop()

# Main page for regular users
def main_page(username):
    users_id = get_user_id(username)
    main_win = tk.Tk()
    main_win.title('EduManga Hub')
    main_win.config(bg='#031716')

    icon = tk.PhotoImage(file='smol_ina.png')
    main_win.iconphoto(False, icon)

    # Set the window size and position
    center_window(main_win, 1080, 500)

    # Header Section
    header_frame = tk.Frame(main_win, bg="#031716")
    header_frame.pack(fill=tk.X, pady=10, padx=10)

    # Logo Image
    logo_image = tk.PhotoImage(file='smol_ina.png')
    logo_label = tk.Label(header_frame, image=logo_image, bg="#031716")
    logo_label.pack(side=tk.LEFT, padx=5)

    # App Name
    app_name_label = tk.Label(header_frame, text="EduManga Hub", font=("Helvetica", 24, "bold"), bg="#031716", fg="#6BA3BE")
    app_name_label.pack(side=tk.LEFT, padx=10)

    #Fetching if the notification is acknowledged or not
    conn = sqlite3.connect('user_data.db')
    with conn:
        c = conn.cursor()
        c.execute("SELECT message FROM notifications WHERE users_id=? AND status=? AND acknowledged=?", 
                  (users_id, 'unread', 0))
        notifications = c.fetchall()

    if notifications:
        notification_messages = "\n".join([notif[0] for notif in notifications])
        messagebox.showinfo("Notifications", notification_messages)
        
        # After showing the notification, mark it as acknowledged
        with conn:
            c = conn.cursor()
            c.execute("UPDATE notifications SET acknowledged=1 WHERE users_id=? AND status='unread'", 
                      (users_id,))

    # Top menu buttons
    button_frame = tk.Frame(main_win, bg="#031716")
    button_frame.pack(pady=10)

    # Add Comic Button
    def add_comic_window():
        def add_comic_action():
            title = title_entry.get()
            genre = genre_entry.get()
            author = author_entry.get()
            add_comic(title, genre, author, users_id)
            messagebox.showinfo("Success", "Comic added successfully!")
            add_comic_win.destroy()

        add_comic_win = tk.Toplevel(main_win, bg="#031716")
        add_comic_win.title("Add Comic")
        center_window(add_comic_win, 400, 300)

        icon = tk.PhotoImage(file='smol_ina.png')
        add_comic_win.iconphoto(False, icon)
        
        title_label = tk.Label(add_comic_win, text="Comic Title:", bg='#031716', fg='#6BA3BE')
        title_label.pack(pady=10)
        title_entry = tk.Entry(add_comic_win)
        title_entry.pack()
        
        genre_label = tk.Label(add_comic_win, text="Genre:", bg='#031716', fg='#6BA3BE')
        genre_label.pack(pady=10)
        genre_entry = tk.Entry(add_comic_win)
        genre_entry.pack()
        
        author_label = tk.Label(add_comic_win, text="Author:", bg='#031716', fg='#6BA3BE')
        author_label.pack(pady=10)
        author_entry = tk.Entry(add_comic_win)
        author_entry.pack()
        
        add_button = tk.Button(add_comic_win, font=("Helvetica", 16), text="ADD", borderwidth=0, bg='#032F30', fg='#6BA3BE', command=add_comic_action)
        add_button.pack(pady=15)

    add_comic_button = tk.Button(button_frame, text="Add Comic", font=("Helvetica", 14), borderwidth=0,  bg='#032F30', fg='#6BA3BE', command=add_comic_window)
    add_comic_button.pack(side=tk.LEFT, padx=20)

    # View All Comics Button
    def view_comics_window():
        comics = get_user_comics(users_id)
        view_comics_win = tk.Toplevel(main_win)
        view_comics_win.title("My Comics")
        center_window(view_comics_win, 600, 400)
        view_comics_win.config(bg='#031716')
        
        icon = tk.PhotoImage(file='smol_ina.png')
        view_comics_win.iconphoto(False, icon)

        for comic in comics:
            title_label = tk.Label(view_comics_win, text=f"Title: {comic[1]} | Status: {comic[4]}", bg='#031716',fg='#6BA3BE')
            title_label.pack(pady=5)

    view_comics_button = tk.Button(button_frame, text="View Comics", font=("Helvetica", 14), borderwidth=0,  bg='#032F30', fg='#6BA3BE', command=view_comics_window)
    view_comics_button.pack(side=tk.LEFT, padx=20)

    # Search Comics Button
    def search_comic_window():
        def search_action():
            search_term = search_entry.get()
            results = search_comics_by_title(search_term)
            results_win = tk.Toplevel(main_win)
            results_win.title("Search Results")
            center_window(results_win, 600, 400)
            results_win.config(bg='#031716')
            icon = tk.PhotoImage(file='smol_ina.png')
            results_win.iconphoto(False, icon)
            
            if results:
                for comic in results:
                    result_label = tk.Label(results_win, text=f"Title: {comic[1]} | Status: {comic[4]}", bg='#031716',fg='#6BA3BE')
                    result_label.pack(pady=5)
            else:
                no_results_label = tk.Label(results_win, text="No comics found", font=("Helvetica", 14), bg='#031716',fg='#6BA3BE')
                no_results_label.pack(pady=20)

        search_win = tk.Toplevel(main_win)
        search_win.title("Search Comics")
        center_window(search_win, 400, 150)
        search_win.config ( bg='#031716')

        icon = tk.PhotoImage(file='smol_ina.png')
        search_win.iconphoto(False, icon)

        search_label = tk.Label(search_win, text="Enter Search Term:",  bg='#031716', fg='#6BA3BE')
        search_label.pack(pady=10)
        search_entry = tk.Entry(search_win)
        search_entry.pack(pady=10)

        search_button = tk.Button(search_win, text="Search",  borderwidth=0, bg='#032F30', fg='#6BA3BE', activebackground='#6BA3BE', activeforeground='#032F30', command=search_action)
        search_button.pack(pady=10)

    search_comic_button = tk.Button(button_frame, text="Search Comics", font=("Helvetica", 14), borderwidth=0,  bg='#032F30', fg='#6BA3BE', command=search_comic_window)
    search_comic_button.pack(side=tk.LEFT, padx=20)

    # Change Status Button
    def change_comic_status_window():
        def update_status():
            title = title_entry.get()
            new_status = status_entry.get()
            update_comic_status(title, new_status, users_id)
            messagebox.showinfo("Success", "Comic status updated successfully!")
            change_status_win.destroy()

        change_status_win = tk.Toplevel(main_win)
        change_status_win.title("Change Comic Status")
        center_window(change_status_win, 400, 300)
        change_status_win.config(bg='#031716')
        
        icon = tk.PhotoImage(file='smol_ina.png')
        change_status_win.iconphoto(False, icon)
        
        title_label = tk.Label(change_status_win, text="Comic Title:", bg='#031716',fg='#6BA3BE')
        title_label.pack(pady=5)
        title_entry = tk.Entry(change_status_win)
        title_entry.pack(pady=5)

        status_label = tk.Label(change_status_win, text="New Status:", bg='#031716',fg='#6BA3BE')
        status_label.pack(pady=5)
        status_entry = tk.Entry(change_status_win)
        status_entry.pack(pady=5)

        update_button = tk.Button(change_status_win, text="Update Status", borderwidth=0, bg='#032F30',fg='#6BA3BE', activebackground='#6BA3BE', activeforeground='#032F30', command=update_status)
        update_button.pack(pady=15)

    change_status_button = tk.Button(button_frame, text="Change Status", font=("Helvetica", 14), borderwidth=0,  bg='#032F30', fg='#6BA3BE', command=change_comic_status_window)
    change_status_button.pack(side=tk.LEFT, padx=20)

    # Profile Button
    def profile_window():
        profile_win = tk.Toplevel(main_win)
        profile_win.title("Profile")
        center_window(profile_win, 400, 300)
        profile_win.config(bg='#031716')
        
        icon = tk.PhotoImage(file='smol_ina.png')
        profile_win.iconphoto(False, icon)
        
        profile_label = tk.Label(profile_win, text=f"Username: {username}", font=("Helvetica", 14), bg='#031716',fg='#6BA3BE')
        profile_label.pack(pady=20)

        conn = sqlite3.connect('user_data.db')
        with conn:
            c = conn.cursor()
            c.execute("SELECT password FROM users where username=?", (username,))
            password = c.fetchone()[0]

        password_visible = tk.BooleanVar(value=False)

        def toggle_password():
            if password_visible.get():
                password_entry.config(show="")
            else:
                password_entry.config(show="*")
        
        # Label for password
        password_label = tk.Label(profile_win, text="Password:", font=("Helvetica", 14), bg='#031716', fg='#6BA3BE')
        password_label.pack(pady=5)

        # Entry widget to display password (initially hidden)
        password_entry = tk.Entry(profile_win, show="*", font=("Helvetica", 14), fg='black')
        password_entry.insert(0, password)  # Set the password value
        password_entry.pack(pady=5)

        # Checkbox to toggle password visibility
        show_password_check = tk.Checkbutton(profile_win, text="Show Password", bg='#031716', fg='#6BA3BE', variable=password_visible, borderwidth=0, border=0, command=toggle_password)
        show_password_check.pack(pady=10)

    profile_button = tk.Button(button_frame, text="Profile", font=("Helvetica", 14), borderwidth=0,  bg='#032F30', fg='#6BA3BE', command=profile_window)
    profile_button.pack(side=tk.LEFT, padx=20)

    # Log out button
    def logout():
        main_win.destroy()
        login_window()

    logout_button = tk.Button(main_win, text="Log Out", font=("Helvetica", 14), borderwidth=0, bg='#032F30', fg='#6BA3BE', command=logout)
    logout_button.place(relx=1.0, rely=1.0, anchor='se')

    main_win.mainloop()

# Admin page
def admin_page():
    admin_win = tk.Tk()
    admin_win.title('EduManga Hub')
    admin_win.config(bg='black')

    icon = tk.PhotoImage(file='smol_ina.png')
    admin_win.iconphoto(False, icon)

    # Set the window size and position
    center_window(admin_win, 1080, 500)

    # Header frame with image and text
    header_frame = tk.Frame(admin_win, bg='black')
    header_frame.pack(pady=10, anchor='w')

    # Load and display the image
    try:
        logo = tk.PhotoImage(file='smol_ina.png')  # Replace with the path to your image
        logo_label = tk.Label(header_frame, image=logo, bg='black')
        logo_label.image = logo
        logo_label.pack(side=tk.LEFT, padx=10)
    except Exception as e:
        print(f"Error loading image: {e}")

    header_text = tk.Label(header_frame, text="EduManga Hub", font=("Helvetica", 28, "bold"), bg='black', fg='white')
    header_text.pack(side=tk.LEFT, padx=10)

    # Create a Frame for the buttons
    button_frame = tk.Frame(admin_win, bg='black')
    button_frame.pack(pady=50)

    # Add comics as admin
    def admin_add_comic_window():
        def add_comic_action():
            title = title_entry.get()
            genre = genre_entry.get()
            author = author_entry.get()
            admin_add_comic(title, genre, author)
            messagebox.showinfo("Success", "Comic added successfully!")
            add_comic_win.destroy()
        
        add_comic_win = tk.Toplevel(admin_win, bg='black')
        add_comic_win.title("Add comics")
        center_window(add_comic_win, 600, 400)

        title_label = tk.Label(add_comic_win, text="Comic Title:", bg='black', fg='white')
        title_label.pack(pady=10)
        title_entry = tk.Entry(add_comic_win)
        title_entry.pack()

        genre_label = tk.Label(add_comic_win, text="Genre:", bg='black', fg='white')
        genre_label.pack(pady=10)
        genre_entry = tk.Entry(add_comic_win)
        genre_entry.pack()

        author_label = tk.Label(add_comic_win, text="Author:", bg='black', fg='white')
        author_label.pack(pady=10)
        author_entry = tk.Entry(add_comic_win)
        author_entry.pack()

        add_button = tk.Button(add_comic_win, text="ADD", font=("Helvetica",16), bg='gray', fg='white', borderwidth=0, command=add_comic_action)
        add_button.pack(pady=25)

    admin_add_comic_button = tk.Button(button_frame, text="Add Comic", font=("Helvetica", 14), bg="gray", fg="white", borderwidth=0, command=admin_add_comic_window)
    admin_add_comic_button.pack(side=tk.LEFT, padx=20)

    # View All Users
    def view_users():
        users = []
        conn = sqlite3.connect('user_data.db')
        with conn:
            c = conn.cursor()
            c.execute("SELECT users_id, username, is_admin FROM users")
            users = c.fetchall()

        users_win = tk.Toplevel(admin_win)
        users_win.title("Manage Users")
        users_win.config(bg='black')
        center_window(users_win, 600, 400)

        icon = tk.PhotoImage(file='smol_ina.png')
        users_win.iconphoto(False, icon)

        # Container for deleting user
        container_delete_user = tk.Frame(users_win, bg="#031716")
        container_delete_user.pack(fill=tk.BOTH, expand=True)

        # Left Frame
        left_frame_delete_user = tk.Frame(container_delete_user, bg="#031716")
        left_frame_delete_user.pack(side=tk.LEFT, expand=True)
        
        # Right Frame
        right_frame_delete_user = tk.Frame(container_delete_user, bg="#031716")
        right_frame_delete_user.pack(side=tk.RIGHT, expand=True)

        for user in users:
            user_label = tk.Label(left_frame_delete_user, bg="black", fg="white", text=f"ID: {user[0]} | Username: {user[1]} | Admin: {'Yes' if user[2] else 'No'}")
            user_label.pack()

            def delete_user(users_id):
                with sqlite3.connect('user_data.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM users WHERE users_id=?", (users_id,))
                    messagebox.showinfo("Success", f"User ID {users_id} deleted!")
                    users_win.destroy()
                    view_users()  # Refresh list

            delete_button = tk.Button(right_frame_delete_user, text="Delete", bg="gray", fg="white", borderwidth=0, command=lambda uid=user[0]: delete_user(uid))
            delete_button.pack(pady=5)

    view_users_button = tk.Button(button_frame, text="View Users", font=("Helvetica", 14), bg="gray", fg="white", borderwidth=0, command=view_users)
    view_users_button.pack(side=tk.LEFT, padx=20)

    # View All Comics
    def view_comics():
        comics = []
        conn = sqlite3.connect('user_data.db')
        with conn:
            c = conn.cursor()
            c.execute("SELECT comics.comics_id, comics.title, comics.genre, comics.status, CASE WHEN comics.added_by_admin = 1 THEN 'Admin' ELSE users.username END AS added_by FROM comics LEFT JOIN users ON comics.users_id = users.users_id")
            comics = c.fetchall()

        comics_win = tk.Toplevel(admin_win)
        comics_win.title("Manage Comics")
        comics_win.config(bg='black')
        center_window(comics_win, 500, 300)

        icon = tk.PhotoImage(file='smol_ina.png')
        comics_win.iconphoto(False, icon)

        for comic in comics:
            comic_label = tk.Label(comics_win, bg="black", fg="white", borderwidth=0,text=f"Comic ID: {comic[0]} | Title: {comic[1]} | Genre: {comic[2]} | Status: {comic[3]} | Added By: {comic[4]}")
            comic_label.pack()

    view_comics_button = tk.Button(button_frame, text="View Comics", font=("Helvetica", 14), bg="gray", fg="white", borderwidth=0, command=view_comics)
    view_comics_button.pack(side=tk.LEFT, padx=20)

    # Delete Comics
    def delete_comic():
        delete_win = tk.Toplevel(admin_win)
        delete_win.title("Delete Comic")
        delete_win.config(bg='black')
        center_window(delete_win, 400, 200)

        icon = tk.PhotoImage(file='smol_ina.png')
        delete_win.iconphoto(False, icon)

        title_label = tk.Label(delete_win, text="Enter Comic Title to Delete:", bg='black', fg='white')
        title_label.pack(pady=10)

        title_entry = tk.Entry(delete_win)
        title_entry.pack(pady=10)

        def delete_action():
            title = title_entry.get()
            if not title.strip():
                messagebox.showerror("Error", "Please enter a comic title.")
                return

            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the comic '{title}'?")
            if not confirm:
                return

            with sqlite3.connect('user_data.db') as conn:
                c = conn.cursor()
                c.execute("SELECT users_id FROM comics WHERE title=?", (title,))
                comic = c.fetchone()
            
            if comic:
                users_id = comic[0]
                c = conn.cursor()
                # Delete the comic
                c.execute("DELETE FROM comics WHERE title=?", (title,))
                conn.commit()
                # Add a notification for the user
                c.execute("INSERT INTO notifications (users_id, message, status) VALUES (?, ?, ?)", 
                          (users_id, f"Your comic '{title}' has been deleted by the admin.", 'unread'))
                conn.commit()
                messagebox.showinfo("Success", f"Comic '{title}' deleted successfully!")
                delete_win.destroy()
            else:
                messagebox.showerror("Error", f"No comic found with title '{title}'.")

        delete_button = tk.Button(delete_win, text="Delete", bg='gray', fg='white', borderwidth=0, command=delete_action)
        delete_button.pack(pady=10)

    delete_comics_button = tk.Button(button_frame, text="Delete Comic", font=("Helvetica", 14), bg="gray", fg="white", borderwidth=0, command=delete_comic)
    delete_comics_button.pack(side=tk.LEFT, padx=20)

    # Log out button
    def logout():
        admin_win.destroy()
        login_window()

    logout_button = tk.Button(admin_win, text="Log Out", font=("Helvetica", 14), bg="gray", fg="white", borderwidth=0, command=logout)
    logout_button.place(relx=1.0, rely=1.0, anchor='se')

# Run the program
create_db()
login_window()