from pathlib import Path
import tkinter as tk
from tkinter import Canvas, PhotoImage, ttk, messagebox, Button
import mysql.connector 
import os
from PIL import Image, ImageTk  # Add PIL for better image handling
import webbrowser  # Add this at the top with other imports


# Function to create database connection
def create_connection():
    try:
        # First try environment variables
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="emp"
        )
        # Test the connection
        conn.ping(reconnect=True, attempts=3, delay=5)
        return conn
    except mysql.connector.Error as e:
        # More specific error handling
        if e.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            messagebox.showerror("Database Error", "Invalid username or password")
        elif e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            messagebox.showerror("Database Error", "Database 'emp' does not exist")
        else:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None


class DatabaseOperations:
    def __init__(self, cursor, con):
        self.cursor = cursor
        self.con = con

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.con.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    def fetchall(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return []
    
    def check_employee_exists(self, emp_id):
        """Check if an employee exists in the database by ID."""
        try:
            query = "SELECT COUNT(*) FROM employees WHERE emp_id = %s"
            self.cursor.execute(query, (emp_id,))
            result = self.cursor.fetchone()
            return result[0] > 0  # Return True if count > 0, else False
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return False
     
    def reset_auto_increment(self):
        """Reset auto-increment to match the highest emp_id."""
        try:
            # Find the max emp_id
            self.cursor.execute("SELECT MAX(emp_id) FROM employees")
            max_id = self.cursor.fetchone()[0]
            
            # If table is empty, reset to 1, otherwise to max_id + 1
            next_id = 1 if max_id is None else max_id + 1
            
            # Reset auto-increment
            self.cursor.execute(f"ALTER TABLE employees AUTO_INCREMENT = {next_id}")
            self.con.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error resetting auto-increment: {e}")


# Welcome Page
class WelcomePage:
    def __init__(self, root):
        self.root = root
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth() 
        self.screen_height = self.root.winfo_screenheight()
        
        # Configure window for full screen
        self.root.title("Employee Management System - Welcome")
        self.root.iconphoto(False, tk.PhotoImage(file="c.png"))
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.configure(bg="#C4D9FF")
        self.root.state('zoomed')  # For Windows, maximizes the window
        
        # Setup paths
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"D:\CODE\assets\frame0")

        # Create canvas to fill screen
        self.canvas = tk.Canvas(
            self.root,
            bg="#C4D9FF",
            height=self.screen_height,
            width=self.screen_width,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Add PIL import at top of file
        try:
            from PIL import Image, ImageTk
            self.using_pil = True
        except ImportError:
            self.using_pil = False

        self.add_images()
        self.add_button()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def add_images(self):
        try:
            if hasattr(self, 'using_pil') and self.using_pil:
                # Use PIL for better image scaling
                from PIL import Image, ImageTk
                
                # Background image
                bg_img = Image.open(self.relative_to_assets("image_1.png"))
                bg_resized = bg_img.resize((self.screen_width, self.screen_height), Image.LANCZOS)
                image_image_1 = ImageTk.PhotoImage(bg_resized)
                self.canvas.create_image(self.screen_width/2, self.screen_height/2, image=image_image_1)
                self.image_1 = image_image_1  # Prevent garbage collection
                
                # Logo image
                logo_img = Image.open(self.relative_to_assets("image_2.png"))
                logo_width = int(self.screen_width * 0.4)
                logo_height = int(logo_width * (logo_img.height / logo_img.width))
                logo_resized = logo_img.resize((logo_width, logo_height), Image.LANCZOS)
                image_image_2 = ImageTk.PhotoImage(logo_resized)
                self.canvas.create_image(self.screen_width/2, self.screen_height*0.37, image=image_image_2)
                self.image_2 = image_image_2  # Prevent garbage collection
            else:
                # Fallback to original code
                image_image_1 = tk.PhotoImage(file=self.relative_to_assets("image_1.png"))
                self.canvas.create_image(self.screen_width/2, self.screen_height/2, image=image_image_1)
                self.image_1 = image_image_1
                
                image_image_2 = tk.PhotoImage(file=self.relative_to_assets("image_2.png"))
                self.canvas.create_image(self.screen_width/2, self.screen_height*0.37, image=image_image_2)
                self.image_2 = image_image_2

            # Scale text size based on screen width
            font_size = int(-1 * self.screen_width * 0.044)
            
            # Add text with position relative to screen size
            self.canvas.create_text(
                self.screen_width * 0.088,
                self.screen_height * 0.47,
                anchor="nw",
                text="“Transform Potential into Performance.”",
                fill="#FFFFFF",
                font=("CabinSketch Regular", font_size)
            )
        except Exception as e:
            messagebox.showerror("Asset Loading Error", f"Could not load assets: {e}")

    def add_button(self):
        try:
            # Size button based on screen dimensions
            button_width = int(self.screen_width * 0.57)
            button_height = int(self.screen_height * 0.096)
            
            if hasattr(self, 'using_pil') and self.using_pil:
                from PIL import Image, ImageTk
                
                # Load and resize button image
                button_img = Image.open(self.relative_to_assets("button_1.png"))
                button_resized = button_img.resize((button_width, button_height), Image.LANCZOS)
                button_image = ImageTk.PhotoImage(button_resized)
            else:
                # Fallback to regular PhotoImage
                button_image = tk.PhotoImage(file=self.relative_to_assets("button_1.png"))
            
            # Create and place button
            button = tk.Button(
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=self.proceed_to_login,
                relief="flat"
            )
            # Center button horizontally, position vertically
            button.place(
                x=(self.screen_width - button_width)/2,
                y=self.screen_height * 0.61,
                width=button_width,
                height=button_height
            )
            self.button_image = button_image  # Prevent garbage collection
        except Exception as e:
            # Fallback to text button
            button = tk.Button(
                text="CONTINUE",
                borderwidth=1,
                highlightthickness=0,
                command=self.proceed_to_login,
                relief="solid",
                bg="#4B5EAA",
                fg="white",
                font=("Arial", 16, "bold")
            )
            button.place(
                x=(self.screen_width - 400)/2,
                y=self.screen_height * 0.61,
                width=400,
                height=80
            )
            messagebox.showwarning("Asset Loading", f"Using text button as fallback: {e}")

    def proceed_to_login(self):
        self.canvas.destroy()
        LoginPage(self.root)


# Login Page
class LoginPage:
    def __init__(self, root):
        self.root = root
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Configure window for full screen
        self.root.title("Employee Management System - Login")
        self.root.iconphoto(False, tk.PhotoImage(file="c.png"))
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.configure(bg="#FFFFFF")
        self.root.state('zoomed')  # For Windows, maximizes the window
        
        # Setup paths
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"D:\CODE\assets\frame1")

        # Create canvas to fill screen
        self.canvas = tk.Canvas(
            self.root,
            bg="#FFFFFF",
            height=self.screen_height,
            width=self.screen_width,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Try to use PIL for better image scaling
        try:
            from PIL import Image, ImageTk
            self.using_pil = True
        except ImportError:
            self.using_pil = False

        self.setup_ui_elements()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_ui_elements(self):
        try:
            # Background image with scaling
            if hasattr(self, 'using_pil') and self.using_pil:
                from PIL import Image, ImageTk
                
                # Load and scale background image
                bg_img = Image.open(self.relative_to_assets("image_1.png"))
                bg_resized = bg_img.resize((self.screen_width, self.screen_height), Image.LANCZOS)
                self.image_image_1 = ImageTk.PhotoImage(bg_resized)
            else:
                # Fallback to original PhotoImage
                self.image_image_1 = tk.PhotoImage(file=self.relative_to_assets("image_1.png"))
                
            self.image_1 = self.canvas.create_image(
                self.screen_width/2, 
                self.screen_height/2, 
                image=self.image_image_1
            )

            # Calculate positions based on screen size
            center_x = self.screen_width / 2
            form_width = int(self.screen_width * 0.2)  # Form width as 20% of screen width
            
            # Login button with scaling
            button_width = int(self.screen_width * 0.17)
            button_height = int(self.screen_height * 0.04)
            
            if hasattr(self, 'using_pil') and self.using_pil:
                # Scale login button
                btn_img = Image.open(self.relative_to_assets("button_1.png"))
                btn_resized = btn_img.resize((button_width, button_height), Image.LANCZOS)
                self.button_image_1 = ImageTk.PhotoImage(btn_resized)
            else:
                # Fallback to original button
                self.button_image_1 = tk.PhotoImage(file=self.relative_to_assets("button_1.png"))
                
            self.button_1 = tk.Button(
                image=self.button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=self.authenticate_user,
                relief="flat"
            )
            
            # Position login button - centered horizontally, appropriate vertical position
            self.button_1.place(
                x=center_x - button_width/2,
                y=self.screen_height * 0.66,
                width=button_width,
                height=button_height
            )

            # Close button
            close_btn_width = button_width
            close_btn_height = button_height
            self.button_close = tk.Button(
                text="Close Application",
                borderwidth=1,
                highlightthickness=0,
                command=self.close_application,
                relief="solid",
                bg="#FF5252",
                fg="white",
                font=("Arial", 12, "bold")
            )
            self.button_close.place(
                x=center_x - close_btn_width/2,
                y=self.screen_height * 0.71,
                width=close_btn_width,
                height=close_btn_height
            )

            # Scale the font size based on screen dimensions
            title_font_size = int(self.screen_height * 0.023)
            label_font_size = int(self.screen_height * 0.013)

            # Login text
            self.canvas.create_text(
                center_x - form_width/2,
                self.screen_height * 0.42,
                anchor="nw",
                text="Login",
                fill="#FFFFFF",
                font=("Gilroy Bold", title_font_size)
            )

            # Setup username and password fields with scaled positions
            self.setup_username_field(center_x, form_width, label_font_size)
            self.setup_password_field(center_x, form_width, label_font_size)

            # Logo image with scaling
            if hasattr(self, 'using_pil') and self.using_pil:
                # Scale logo image
                logo_img = Image.open(self.relative_to_assets("image_2.png"))
                logo_width = int(self.screen_width * 0.3)
                logo_height = int(logo_width * (logo_img.height / logo_img.width))
                logo_resized = logo_img.resize((logo_width, logo_height), Image.LANCZOS)
                self.image_image_2 = ImageTk.PhotoImage(logo_resized)
            else:
                # Fallback to original logo
                self.image_image_2 = tk.PhotoImage(file=self.relative_to_assets("image_2.png"))
                
            self.image_2 = self.canvas.create_image(
                center_x,
                self.screen_height * 0.35,
                image=self.image_image_2
            )
        
        except Exception as e:
            messagebox.showerror("UI Setup Error", f"Failed to setup UI elements: {e}")
            # Fallback to minimal UI if images fail
            self.setup_fallback_ui()

    def setup_username_field(self, center_x, form_width, font_size):
        # Username label
        self.canvas.create_text(
            center_x - form_width/2,
            self.screen_height * 0.48,
            anchor="nw",
            text="Username",
            fill="#FFFFFF",
            font=("Roboto", font_size)
        )
        
        # Calculate entry dimensions based on screen size
        entry_width = int(self.screen_width * 0.17)
        entry_height = int(self.screen_height * 0.03)
        
        # Entry background
        if hasattr(self, 'using_pil') and self.using_pil:
            # Scale entry background
            entry_bg = Image.open(self.relative_to_assets("entry_1.png"))
            entry_bg_resized = entry_bg.resize((entry_width, entry_height), Image.LANCZOS)
            self.entry_image_1 = ImageTk.PhotoImage(entry_bg_resized)
        else:
            # Fallback to original entry background
            self.entry_image_1 = tk.PhotoImage(file=self.relative_to_assets("entry_1.png"))
            
        self.entry_bg_1 = self.canvas.create_image(
            center_x, 
            self.screen_height * 0.53,
            image=self.entry_image_1
        )
        
        # Username entry - adjust size and position based on screen dimensions
        # Increased font size for better visibility
        input_font_size = max(12, int(self.screen_height * 0.016))
        self.username_entry = tk.Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Arial", input_font_size)  # Added font setting with larger size
        )
        self.username_entry.place(
            x=center_x - entry_width/2 + 5,  # Small margin for better appearance
            y=self.screen_height * 0.53 - entry_height/2,
            width=entry_width - 10,  # Smaller than the background for better appearance
            height=entry_height - 6  # Slightly adjusted height for the larger font
        )

    def setup_password_field(self, center_x, form_width, font_size):
        # Password label
        self.canvas.create_text(
            center_x - form_width/2,
            self.screen_height * 0.57,
            anchor="nw",
            text="Password",
            fill="#FFFFFF",
            font=("Roboto", font_size)
        )
        
        # Calculate entry dimensions based on screen size
        entry_width = int(self.screen_width * 0.17)
        entry_height = int(self.screen_height * 0.03)
        
        # Entry background
        if hasattr(self, 'using_pil') and self.using_pil:
            # Scale entry background
            entry_bg = Image.open(self.relative_to_assets("entry_2.png"))
            entry_bg_resized = entry_bg.resize((entry_width, entry_height), Image.LANCZOS)
            self.entry_image_2 = ImageTk.PhotoImage(entry_bg_resized)
        else:
            # Fallback to original entry background
            self.entry_image_2 = tk.PhotoImage(file=self.relative_to_assets("entry_2.png"))
            
        self.entry_bg_2 = self.canvas.create_image(
            center_x,
            self.screen_height * 0.62,
            image=self.entry_image_2
        )
        
        # Password entry - adjust size and position based on screen dimensions
        # Increased font size for better visibility
        input_font_size = max(12, int(self.screen_height * 0.016))
        self.password_entry = tk.Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            show="*",
            font=("Arial", input_font_size)  # Added font setting with larger size
        )
        self.password_entry.place(
            x=center_x - entry_width/2 + 5,  # Small margin for better appearance
            y=self.screen_height * 0.62 - entry_height/2,
            width=entry_width - 10,  # Smaller than the background for better appearance
            height=entry_height - 6  # Slightly adjusted height for the larger font
        )

    def setup_fallback_ui(self):
        """Create a simple fallback UI if images fail to load"""
        # Clear canvas
        self.canvas.delete("all")
        self.canvas.configure(bg="#3A7FF6")  # Set a blue background
        
        # Add title
        self.canvas.create_text(
            self.screen_width/2,
            self.screen_height * 0.2,
            text="Employee Management System",
            fill="#FFFFFF",
            font=("Arial", 28, "bold"),
            anchor="center"
        )
        
        # Add login frame
        frame = tk.Frame(
            self.root,
            bg="#FFFFFF",
            highlightbackground="#000000",
            highlightthickness=1
        )
        frame.place(
            x=self.screen_width/2 - 150,
            y=self.screen_height * 0.4,
            width=300,
            height=200
        )
        
        # Add login elements to frame
        tk.Label(
            frame, 
            text="Login", 
            font=("Arial", 16, "bold"),
            bg="#FFFFFF"
        ).pack(pady=10)
        
        tk.Label(
            frame, 
            text="Username:", 
            anchor="w",
            bg="#FFFFFF",
            font=("Arial", 12)  # Adjusted font size
        ).pack(fill="x", padx=20)
        
        # Increased font size for better visibility in fallback UI too
        self.username_entry = tk.Entry(frame, width=30, font=("Arial", 14))
        self.username_entry.pack(padx=20, pady=5)
        
        tk.Label(
            frame, 
            text="Password:", 
            anchor="w",
            bg="#FFFFFF",
            font=("Arial", 12)  # Adjusted font size
        ).pack(fill="x", padx=20)
        
        # Increased font size for better visibility in fallback UI too
        self.password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 14))
        self.password_entry.pack(padx=20, pady=5)
        
        button_frame = tk.Frame(frame, bg="#FFFFFF")
        button_frame.pack(pady=10, fill="x")
        
        tk.Button(
            button_frame,
            text="Login",
            command=self.authenticate_user,
            bg="#3A7FF6",
            fg="#FFFFFF",
            font=("Arial", 12),  # Added font size
            width=10
        ).pack(side="left", padx=20)
        
        tk.Button(
            button_frame,
            text="Exit",
            command=self.close_application,
            bg="#FF5252",
            fg="#FFFFFF",
            font=("Arial", 12),  # Added font size
            width=10
        ).pack(side="right", padx=20)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin123":
            messagebox.showinfo("Login Successful", "Welcome Administrator!")
            self.canvas.destroy()
            EmployeeManagementApp(self.root, role="admin")
        elif username == "hr" and password == "hr123":
            messagebox.showinfo("Login Successful", "Welcome HR!")
            self.canvas.destroy()
            EmployeeManagementApp(self.root, role="hr")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def close_application(self):
        """Close the entire application after confirmation"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.root.quit()
            self.root.destroy()
            
    def update_layout(self, event=None):
        """Update UI elements when window is resized"""
        if event:
            # Only update if significant change in size
            if abs(event.width - self.screen_width) > 10 or abs(event.height - self.screen_height) > 10:
                self.screen_width = event.width
                self.screen_height = event.height
                
                # Clean up and redraw UI
                self.canvas.delete("all")
                self.setup_ui_elements()

# Employee Management Application
class EmployeeManagementApp:
    def __init__(self, root, role="admin"):
        self.root = root
        self.role = role  # Store user role
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Configure window to use full screen
        self.root.title("Employee Management System")
        self.root.iconphoto(False, tk.PhotoImage(file="c.png"))
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.configure(bg="#FFFFFF")
        self.root.state('zoomed')  # For Windows, maximizes the window
        
        # Database connection - Exit if failed
        self.con = create_connection()
        if self.con is None:
            self.root.quit()  # Properly terminate the mainloop
            return

        self.cursor = self.con.cursor()
        self.db = DatabaseOperations(self.cursor, self.con)

        # Setup paths
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"D:\CODE\assets\frame3")

        # Create canvas that fills the screen
        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=self.screen_height,
            width=self.screen_width,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Load and create background image with proper scaling
        self.load_background_image()

        # Add user role label
        user_label = tk.Label(
            self.root,
            text=f"Logged in as: {role.upper()}",
            bg="#808080", 
            fg="#FFFFFF",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5
        )
        # Position label relative to screen size
        user_label.place(x=int(0.035*self.screen_width), y=int(0.05*self.screen_height))

        # Initialize buttons
        self.create_buttons()
        
        # Create treeview
        self.create_treeview()
        
        # Display initial data
        self.display_employees()

    def load_background_image(self):
        """Load and scale background image to fit the screen"""
        try:
            # Load the image using PIL for better scaling
            original_img = Image.open(self.relative_to_assets("image_1.png"))
            # Resize to fit the screen
            resized_img = original_img.resize((self.screen_width, self.screen_height), Image.LANCZOS)
            # Convert to PhotoImage
            self.image_image_1 = ImageTk.PhotoImage(resized_img)
            # Place on canvas
            self.image_1 = self.canvas.create_image(
                self.screen_width/2, self.screen_height/2, 
                image=self.image_image_1
            )
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading background image: {e}")
            # Fallback to solid color if image fails
            self.canvas.configure(bg="#C4D9FF")

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def create_buttons(self):
        # Common button configuration with rounded corners
        button_style = {
            "borderwidth": 1,
            "highlightthickness": 0,
            "relief": "solid",
            "bg": "#4B5EAA",
            "fg": "white",
            "font": ("Arial", 14, "bold"),
            "padx": 10,
            "pady": 5
        }

        # Calculate button positions based on screen dimensions
        button_y = int(0.19 * self.screen_height)
        button_width = int(0.18 * self.screen_width)
        button_height = int(0.08 * self.screen_height)
        
        # Buttons configuration based on role
        if self.role == "admin":
            # Calculate button spacing to distribute evenly
            btn_margin = (self.screen_width - 4 * button_width) / 5
            
            # Create modern text buttons instead of image buttons
            button_texts = ["Add Employee", "Remove Employee", "Promote Employee", "Search Employee"]
            button_commands = [
                self.show_add_employee_frame,
                self.remove_employee,
                self.promote_employee,
                self.show_search_employee_frame
            ]
            
            for i, (text, command) in enumerate(zip(button_texts, button_commands)):
                btn = tk.Button(
                    self.root,
                    text=text,
                    command=command,
                    **button_style
                )
                # Use rounded corners for buttons
                x_position = btn_margin + i * (button_width + btn_margin)
                btn.place(
                    x=x_position,
                    y=button_y,
                    width=button_width,
                    height=button_height
                )
            
            # Add more compact Filter and Sort button
            filter_btn_width = int(0.15 * self.screen_width)  # Reduced width
            filter_btn = tk.Button(
                self.root,
                text="Filter and Sort",
                command=self.apply_filter_sort,
                bg="#4B5EAA",
                fg="white",
                font=("Arial", 12, "bold"),
                relief="raised",
                bd=2
            )
            filter_btn.place(
                x=int(0.81 * self.screen_width),
                y=int(0.085 * self.screen_height),
                width=filter_btn_width,
                height=int(0.05 * self.screen_height)
            )
            
        else:
            # Single centered button for HR
            search_btn = tk.Button(
                self.root,
                text="Search Employee",
                command=self.show_search_employee_frame,
                **button_style
            )
            search_btn.place(
                x=(self.screen_width - button_width)/2,
                y=button_y,
                width=button_width,
                height=button_height
            )

        # Logout Button (always visible) with rounded corners
        logout_btn_width = int(0.09 * self.screen_width)
        logout_btn_height = int(0.05 * self.screen_height)
        
        # Create a frame for the logout button to achieve rounded corners
        logout_frame = tk.Frame(self.root, bg="#FF5252", bd=0, highlightthickness=0)
        logout_frame.place(
            x=self.screen_width - logout_btn_width - 20,
            y=20,
            width=logout_btn_width,
            height=logout_btn_height
        )
        
        # Give the frame rounded corners
        self.button_logout = tk.Button(
            logout_frame,
            text="Logout",
            command=self.logout,
            bg="#FF5252",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            bd=0,
            padx=10,
            pady=5,
            highlightthickness=0
        )
        self.button_logout.pack(fill="both", expand=True)

        # Close application button (if needed)
        if hasattr(self, 'button_close'):
            close_btn_width = int(0.174 * self.screen_width)
            close_btn_height = int(0.05 * self.screen_height)
            
            close_frame = tk.Frame(self.root, bg="#FF5252", bd=0, highlightthickness=0)
            close_frame.place(
                x=(self.screen_width - close_btn_width)/2,
                y=int(0.713 * self.screen_height),
                width=close_btn_width,
                height=close_btn_height
            )
            
            self.button_close = tk.Button(
                close_frame,
                text="Close Application",
                command=self.close_application,
                bg="#FF5252",
                fg="white",
                font=("Arial", 12, "bold"),
                relief="flat",
                highlightthickness=0
            )
            self.button_close.pack(fill="both", expand=True)

    def create_treeview(self):
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            background="#FFFFFF",
            foreground="#000000",
            rowheight=25,
            fieldbackground="#FFFFFF"
        )

        # Size treeview based on screen dimensions
        tree_width = int(0.806 * self.screen_width)
        tree_height = int(0.391 * self.screen_height)
        
        self.tree = ttk.Treeview(
            self.root,
            style="Custom.Treeview",
            columns=("emp_id", "name", "post", "salary", "email"),
            show="headings",
            height=15
        )

        columns = {
            "emp_id": "ID",
            "name": "Name",
            "post": "Post",
            "salary": "Salary",
            "email": "Email"
        }
        
        # Set column widths proportionally
        col_width = tree_width // len(columns)
        for col, heading in columns.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, anchor="center", width=col_width)

        # Position treeview centered horizontally
        self.tree.place(
            x=(self.screen_width - tree_width)/2,
            y=int(0.342 * self.screen_height),
            width=tree_width,
            height=tree_height
        )
        
        # Add binding for clicking on email addresses
        self.tree.bind('<ButtonRelease-1>', self.on_tree_click)

    def on_tree_click(self, event):
        """Handle clicks on the treeview, especially for email addresses"""
        # Get the row and column that was clicked
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":  # Only process if a cell was clicked
            return
            
        # Get column ID and item (row) ID
        column_id = self.tree.identify_column(event.x)
        item_id = self.tree.identify_row(event.y)
        
        # Convert column ID (like #5) to column index (0-based)
        column_index = int(column_id[1:]) - 1
        
        # Check if the email column (index 4) was clicked
        if column_index == 4 and item_id:
            # Get values of the clicked row
            values = self.tree.item(item_id, 'values')
            if values and len(values) > 4:
                email = values[4]
                if email and '@' in email:  # Simple validation to check if it looks like an email
                    # Open default mail client with the email address
                    self.send_email(email)
    
    def send_email(self, email):
        """Open the default email client with the recipient address"""
        try:
            # Create a mailto URL and open it with the default browser/email client
            webbrowser.open(f'mailto:{email}')
        except Exception as e:
            messagebox.showerror("Email Error", f"Could not open email client: {e}")

    def display_employees(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = "SELECT * FROM employees ORDER BY emp_id"
        employees = self.db.fetchall(query)

        for emp in employees:
            self.tree.insert("", tk.END, values=emp)

    def show_add_employee_frame(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Employee")
        add_window.geometry("400x350")  # Increased height for email field

        frame = ttk.Frame(add_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Add employee form fields
        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="Post:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        post_entry = ttk.Entry(frame)
        post_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="Salary:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        salary_entry = ttk.Entry(frame)
        salary_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Added email field
        ttk.Label(frame, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        email_entry = ttk.Entry(frame, width=30)
        email_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        def save_employee():
            name = name_entry.get().strip()
            post = post_entry.get().strip()
            salary = salary_entry.get().strip()
            email = email_entry.get().strip()  # Get email value

            if not all([name, post, salary]):  # Email can be optional
                messagebox.showwarning("Input Error", "Name, Post and Salary fields are required")
                return

            try:
                salary = float(salary)
                self.db.execute_query(
                    "INSERT INTO employees (name, post, salary, email) VALUES (%s, %s, %s, %s)",
                    (name, post, salary, email)
                )
                messagebox.showinfo("Success", "Employee added successfully")
                self.display_employees()
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Salary must be a number")

        ttk.Button(frame, text="Save", command=save_employee).grid(
            row=4, column=0, columnspan=2, pady=10)  # Updated row position

    def remove_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an employee to remove")
            return

        emp_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this employee?"):
            self.db.execute_query("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
            self.db.reset_auto_increment()
            messagebox.showinfo("Success", "Employee removed successfully")
            self.display_employees()

    def promote_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an employee to promote")
            return

        emp_id = self.tree.item(selected[0])['values'][0]
        promote_window = tk.Toplevel(self.root)
        promote_window.title("Promote Employee")
        promote_window.geometry("400x250")  # Increased height for email field

        frame = ttk.Frame(promote_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="New Post:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        post_entry = ttk.Entry(frame)
        post_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="New Salary:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        salary_entry = ttk.Entry(frame)
        salary_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Added email update field
        ttk.Label(frame, text="New Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        email_entry = ttk.Entry(frame)
        email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        def save_promotion():
            new_post = post_entry.get().strip()
            new_salary = salary_entry.get().strip()
            new_email = email_entry.get().strip()  # Get new email

            if not new_post and not new_salary and not new_email:
                messagebox.showwarning("Input Error", "At least one field is required")
                return

            try:
                # Build dynamic query based on provided fields
                query = "UPDATE employees SET "
                params = []
                updates = []

                if new_post:
                    updates.append("post = %s")
                    params.append(new_post)

                if new_salary:
                    try:
                        salary = float(new_salary)
                        updates.append("salary = %s")
                        params.append(salary)
                    except ValueError:
                        messagebox.showerror("Input Error", "Salary must be a number")
                        return
                
                # Add email update if provided
                if new_email:
                    updates.append("email = %s")
                    params.append(new_email)

                # Add WHERE clause and emp_id
                query += ", ".join(updates) + " WHERE emp_id = %s"
                params.append(emp_id)

                # Execute update
                self.db.execute_query(query, params)
                messagebox.showinfo("Success", "Employee updated successfully")
                self.display_employees()
                promote_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update employee: {e}")

        ttk.Button(frame, text="Save", command=save_promotion).grid(
            row=3, column=0, columnspan=2, pady=10)  # Updated row position

    def show_search_employee_frame(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Employee")
        search_window.geometry("400x200")

        frame = ttk.Frame(search_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Search by ID:").grid(row=0, column=0, padx=5, pady=5)
        id_entry = ttk.Entry(frame)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        def search_employee():
            emp_id = id_entry.get().strip()
            if not emp_id:
                messagebox.showwarning("Input Error", "Employee ID is required")
                return

            try:
                emp_id = int(emp_id)
                query = "SELECT * FROM employees WHERE emp_id = %s"
                employees = self.db.fetchall(query, (emp_id,))

                for row in self.tree.get_children():
                    self.tree.delete(row)

                if not employees:
                    messagebox.showinfo("Not Found", f"No employee found with ID: {emp_id}")
                else:
                    for emp in employees:
                        self.tree.insert("", tk.END, values=emp)

                search_window.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Employee ID must be a number")

        ttk.Button(frame, text="Search", command=search_employee).grid(
            row=1, column=0, columnspan=2, pady=10)

    def apply_filter_sort(self):
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter and Sort")
        filter_window.geometry("450x400")  # Reduced height
        filter_window.configure(bg="#F5F5F5")  # Light background for the popup

        # Add a title to the filter window
        title_frame = tk.Frame(filter_window, bg="#4B5EAA", height=50)
        title_frame.pack(fill="x", pady=0)
        
        title_label = tk.Label(
            title_frame, 
            text="Filter and Sort Employees",
            bg="#4B5EAA",
            fg="white",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()

        # Main content frame with padding
        frame = ttk.Frame(filter_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Apply custom styles to comboboxes and buttons
        style = ttk.Style()
        style.configure("TCombobox", padding=5)
        style.configure("TButton", font=("Arial", 12), padding=5)

        # Filter by Post dropdown with better styling
        ttk.Label(frame, text="Filter by Post:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=10, sticky="w")
        post_var = tk.StringVar(value="All")
        post_combo = ttk.Combobox(frame, textvariable=post_var, 
                                 values=["All", "Manager", "Developer", "HR", "Intern", "Analyst", "Designer"],
                                 state="readonly",
                                 width=20)
        post_combo.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Filter by Salary Range with better styling
        ttk.Label(frame, text="Salary Range:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=10, sticky="w")
        salary_var = tk.StringVar(value="All")
        salary_ranges = [
            "All",
            "Below 20000",
            "20000-40000",
            "40001-60000",
            "60001-80000",
            "Above 80000"
        ]
        salary_combo = ttk.Combobox(frame, textvariable=salary_var,
                                   values=salary_ranges,
                                   state="readonly",
                                   width=20)
        salary_combo.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        # Sort by field with better styling
        ttk.Label(frame, text="Sort by:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=10, sticky="w")
        sort_var = tk.StringVar(value="Employee ID")
        sort_fields = [
            ("Employee ID", "emp_id"),
            ("Name", "name"),
            ("Post", "post"),
            ("Salary", "salary"),
            ("Email", "email")  # Added email as a sortable field
        ]
        sort_combo = ttk.Combobox(frame, textvariable=sort_var,
                                 values=[field[0] for field in sort_fields],
                                 state="readonly",
                                 width=20)
        sort_combo.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        # Sort order with better styling
        ttk.Label(frame, text="Sort Order:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=10, sticky="w")
        order_var = tk.StringVar(value="Ascending")
        order_combo = ttk.Combobox(frame, textvariable=order_var,
                                  values=["Ascending", "Descending"],
                                  state="readonly",
                                  width=20)
        order_combo.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

        # Create a styled button frame with better spacing
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # Apply filter function
        def apply():
            try:
                post = post_var.get()
                salary_range = salary_var.get()
                sort_field = next(field[1] for field in sort_fields if field[0] == sort_var.get())
                order = "ASC" if order_var.get() == "Ascending" else "DESC"

                query = "SELECT * FROM employees WHERE 1=1"
                params = []

                # Add post filter
                if post != "All":
                    query += " AND post = %s"
                    params.append(post)

                # Add salary range filter
                if salary_range != "All":
                    if salary_range.startswith("Below"):
                        query += " AND salary < %s"
                        params.append(20000)
                    elif salary_range.startswith("Above"):
                        query += " AND salary > %s"
                        params.append(80000)
                    else:
                        min_salary, max_salary = map(int, salary_range.split("-"))
                        query += " AND salary BETWEEN %s AND %s"
                        params.extend([min_salary, max_salary])

                # Add sorting
                query += f" ORDER BY {sort_field} {order}"

                # Execute query and update treeview
                employees = self.db.fetchall(query, params)
                
                for row in self.tree.get_children():
                    self.tree.delete(row)

                for emp in employees:
                    self.tree.insert("", tk.END, values=emp)

                filter_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply filters: {e}")

        # Improved button designs - unified style
        button_style = {
            "padx": 10,
            "pady": 5,
            "font": ("Arial", 12),
            "width": 10
        }

        # Apply button
        apply_btn = tk.Button(
            button_frame,
            text="Apply",
            command=apply,
            bg="#4B5EAA",
            fg="white",
            **button_style
        )
        apply_btn.grid(row=0, column=0, padx=5)

        # Reset button
        def reset():
            self.display_employees()
            filter_window.destroy()

        reset_btn = tk.Button(
            button_frame,
            text="Reset",
            command=reset,
            bg="#6B7ECA",
            fg="white",
            **button_style
        )
        reset_btn.grid(row=0, column=1, padx=5)

        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=filter_window.destroy,
            bg="#CCCCCC",
            fg="black",
            **button_style
        )
        cancel_btn.grid(row=0, column=2, padx=5)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Clean up resources
            if self.con:
                self.cursor.close()
                self.con.close()
            
            # Clear the window
            for widget in self.root.winfo_children():
                widget.destroy()
                
            # Return to login page
            LoginPage(self.root)

    def close_application(self):
        if messagebox.askyesno("Close Application", "Are you sure you want to close the application?"):
            self.root.quit()

# Main function to run the application
def main():
    root = tk.Tk()
    
    # Set up window to track resize events
    def on_resize(event):
        # Pass the resize event to active page
        for widget in root.winfo_children():
            if hasattr(widget, 'update_layout'):
                widget.update_layout(event)
    
    # Bind resize event
    root.bind('<Configure>', on_resize)
    
    WelcomePage(root)
    root.mainloop()

if __name__ == "__main__":
    main()