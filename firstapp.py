from pywebio import start_server 
from pywebio.input import *
from pywebio.output import * 
from pywebio.session import *
from pywebio.pin import *
import sqlite3

def App():
    # Database setup
    conn = sqlite3.connect('batcave.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    # Insert Batman if not exists
    cursor.execute('INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)', ("batman@gotham.com", "darkknight"))
    conn.commit()
    
    def check_credentials(email, password):
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        return cursor.fetchone() is not None
    
    put_html('<center><h3>Hello Hero</h3><img src="https://purepng.com/public/uploads/large/purepng.com-batman-logobatmansuperherocomicdc-comicsbob-kanebat-manbruce-wayne-1701528523391e9t65.png" width=150></center>')
    
    data = input_group("Connectez-Vouz",
            [
    input("Enter your email:", name="email"),
    input("Enter your password :", name="password", type=PASSWORD)
            ]
    )
    
    email = data["email"]
    password = data["password"]
    if check_credentials(email, password): 
        put_success("login successful ! welcome back Batman") 
        
        # Post-login dashboard
        put_markdown("## Batcave Dashboard")
        put_text("Welcome to the Batcave, Dark Knight! Here are some quick facts:")
        put_text("- Real name: Bruce Wayne")
        put_text("- City: Gotham")
        put_text("- Mission: Protect the innocent and fight crime.")
        
        # Interactive buttons
        action = actions("What would you like to do?", [
            {"label": "Fight Crime", "value": "fight"},
            {"label": "View Gadgets", "value": "gadgets"},
            {"label": "Logout", "value": "logout"}
        ])
        
        if action == "fight":
            put_text("You head out to patrol Gotham. Stay vigilant!")
        elif action == "gadgets":
            put_text("Your utility belt includes: Batarang, Grapple Gun, Smoke Pellets.")
        elif action == "logout":
            put_text("Logging out... Session ended.")
            return  # Ends the session
    else: 
        put_error("Login failed ! incorrect email or password") 
    
    # Close DB at end (optional, but good practice)
    conn.close()
        

start_server(App, port=8080, debug=True)
