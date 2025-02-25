from pathlib import Path
import tkinter as tk
from tkinter import Canvas, PhotoImage, ttk, messagebox, Button
import mysql.connector
import os


# Function to create database connection
def create_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "emp")
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
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
        self.root.title("Employee Management System - Welcome")
        self.root.iconphoto(False, tk.PhotoImage(file="c.png"))
        self.root.geometry("1440x1024")
        self.root.configure(bg="#C4D9FF")
        self.root.resizable(False, False)

        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"F:\CODE\assets\frame0")

        self.canvas = tk.Canvas(
            self.root,
            bg="#C4D9FF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)

        self.add_images()
        self.add_button()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def add_images(self):
        try:
            # Load and place background images
            image_image_1 = tk.PhotoImage(file=self.relative_to_assets("image_1.png"))
            self.canvas.create_image(829.0, 532.0, image=image_image_1)
            self.image_1 = image_image_1  # Prevent garbage collection

            image_image_2 = tk.PhotoImage(file=self.relative_to_assets("image_2.png"))
            self.canvas.create_image(720.0, 379.0, image=image_image_2)
            self.image_2 = image_image_2  # Prevent garbage collection

            # Add text
            self.canvas.create_text(
                127.0,
                483.0,
                anchor="nw",
                text="“Transform Potential into Performance.”",
                fill="#FFFFFF",
                font=("CabinSketch Regular", 64 * -1)
            )
        except Exception as e:
            messagebox.showerror("Asset Loading Error", f"Could not load assets: {e}")

    def add_button(self):
        try:
            # Load and place the button
            button_image = tk.PhotoImage(file=self.relative_to_assets("button_1.png"))
            button = tk.Button(
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=self.proceed_to_login,
                relief="flat"
            )
            button.place(x=308.0, y=628.0, width=825.0, height=98.0)
            self.button_image = button_image  # Prevent garbage collection
        except Exception as e:
            messagebox.showerror("Asset Loading Error", f"Could not load button asset: {e}")

    def proceed_to_login(self):
        self.canvas.destroy()
        LoginPage(self.root)


# Login Page
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System - Login")
        self.root.iconphoto(False, tk.PhotoImage(file="c.png"))
        self.root.geometry("1440x1024")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        # Setup paths
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"F:\CODE\assets\frame1")

        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            bg="#FFFFFF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Add background images
        self.image_image_1 = tk.PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(720.0, 512.0, image=self.image_image_1)

        # Create login button
        self.button_image_1 = tk.PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.authenticate_user,
            relief="flat"
        )
        self.button_1.place(x=595.0, y=676.0, width=250.0, height=40.0)

        # Add text elements
        self.canvas.create_text(
            595.0, 432.0,
            anchor="nw",
            text="Login",
            fill="#FFFFFF",
            font=("Gilroy Bold", 24 * -1)
        )

        self.canvas.create_text(
            595.0, 486.0,
            anchor="nw",
            text="Username",
            fill="#FFFFFF",
            font=("Roboto", 13 * -1)
        )

        # Username entry
        self.entry_image_1 = tk.PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(720.0, 541.0, image=self.entry_image_1)
        self.username_entry = tk.Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.username_entry.place(x=600.0, y=525.0, width=240.0, height=30.0)

        # Password label
        self.canvas.create_text(
            595.0, 581.0,
            anchor="nw",
            text="Password",
            fill="#FFFFFF",
            font=("Roboto", 13 * -1)
        )

        # Password entry
        self.entry_image_2 = tk.PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(720.0, 636.0, image=self.entry_image_2)
        self.password_entry = tk.Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            show="*"
        )
        self.password_entry.place(x=600.0, y=620.0, width=240.0, height=30.0)

        # Add logo
        self.image_image_2 = tk.PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(714.0, 358.0, image=self.image_image_2)

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin123":
            messagebox.showinfo("Login Successful", "Welcome to the Employee Management System!")
            self.canvas.destroy()
            EmployeeManagementApp(self.root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Employee Management Application
class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.iconphoto(False, tk.PhotoImage(file="c.png"))
        self.root.geometry("1440x1024")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        # Database connection
        self.con = create_connection()
        if self.con is None:
            self.root.destroy()
            return
        self.cursor = self.con.cursor()
        self.db = DatabaseOperations(self.cursor, self.con)

        # Setup paths
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"F:\CODE\assets\frame3")

        # Create canvas
        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Load and create background image
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(720.0, 512.0, image=self.image_image_1)

        # Initialize buttons
        self.create_buttons()
        
        # Create treeview
        self.create_treeview()
        
        # Display initial data
        self.display_employees()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def create_buttons(self):
        # Add Employee Button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_add_employee_frame,
            relief="flat"
        )
        self.button_1.place(x=157, y=194, width=223, height=102)

        # Remove Employee Button
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.remove_employee,
            relief="flat"
        )
        self.button_2.place(x=462, y=194, width=225, height=105.0)

        # Promote Employee Button
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_6.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.promote_employee,
            relief="flat"
        )
        self.button_3.place(x=809, y=194, width=225, height=100)

        # Search Employee Button
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_7.png"))
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_search_employee_frame,
            relief="flat"
        )
        self.button_4.place(x=1103, y=194, width=241, height=105)

        # Filter Button
        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.apply_filter_sort,
            relief="flat"
        )
        self.button_5.place(x=1090, y=93, width=303, height=54)

    def create_treeview(self):
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            background="#FFFFFF",
            foreground="#000000",
            rowheight=25,
            fieldbackground="#FFFFFF"
        )

        self.tree = ttk.Treeview(
            self.root,
            style="Custom.Treeview",
            columns=("emp_id", "name", "post", "salary"),
            show="headings",
            height=15
        )

        columns = {
            "emp_id": "ID",
            "name": "Name",
            "post": "Post",
            "salary": "Salary"
        }
        
        for col, heading in columns.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, anchor="center", width=200)

        self.tree.place(x=140.0, y=350.0, width=1160.0, height=400.0)

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
        add_window.geometry("400x300")

        frame = ttk.Frame(add_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Add employee form fields
        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Post:").grid(row=1, column=0, padx=5, pady=5)
        post_entry = ttk.Entry(frame)
        post_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Salary:").grid(row=2, column=0, padx=5, pady=5)
        salary_entry = ttk.Entry(frame)
        salary_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_employee():
            name = name_entry.get().strip()
            post = post_entry.get().strip()
            salary = salary_entry.get().strip()

            if not all([name, post, salary]):
                messagebox.showwarning("Input Error", "All fields are required")
                return

            try:
                salary = float(salary)
                self.db.execute_query(
                    "INSERT INTO employees (name, post, salary) VALUES (%s, %s, %s)",
                    (name, post, salary)
                )
                messagebox.showinfo("Success", "Employee added successfully")
                self.display_employees()
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Salary must be a number")

        ttk.Button(frame, text="Save", command=save_employee).grid(
            row=3, column=0, columnspan=2, pady=10)

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
        promote_window.geometry("400x200")

        frame = ttk.Frame(promote_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="New Post:").grid(row=0, column=0, padx=5, pady=5)
        post_entry = ttk.Entry(frame)
        post_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="New Salary:").grid(row=1, column=0, padx=5, pady=5)
        salary_entry = ttk.Entry(frame)
        salary_entry.grid(row=1, column=1, padx=5, pady=5)

        def save_promotion():
            new_post = post_entry.get().strip()
            new_salary = salary_entry.get().strip()

            if not all([new_post, new_salary]):
                messagebox.showwarning("Input Error", "All fields are required")
                return

            try:
                new_salary = float(new_salary)
                self.db.execute_query(
                    "UPDATE employees SET post = %s, salary = %s WHERE emp_id = %s",
                    (new_post, new_salary, emp_id)
                )
                messagebox.showinfo("Success", "Employee promoted successfully")
                self.display_employees()
                promote_window.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Salary must be a number")

        ttk.Button(frame, text="Save", command=save_promotion).grid(
            row=2, column=0, columnspan=2, pady=10)

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
        filter_window.geometry("400x250")

        frame = ttk.Frame(filter_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Filter by Post:").grid(row=0, column=0, padx=5, pady=5)
        post_var = tk.StringVar(value="All")
        post_combo = ttk.Combobox(frame, textvariable=post_var, 
                                 values=["All", "Manager", "Developer", "HR", "Intern"])
        post_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Sort by:").grid(row=1, column=0, padx=5, pady=5)
        sort_var = tk.StringVar(value="emp_id")
        sort_combo = ttk.Combobox(frame, textvariable=sort_var,
                                 values=["emp_id", "name", "post", "salary"])
        sort_combo.grid(row=1, column=1, padx=5, pady=5)

        def apply():
            post = post_var.get()
            sort_by = sort_var.get()

            query = "SELECT * FROM employees"
            params = []

            if post != "All":
                query += " WHERE post = %s"
                params.append(post)

            query += f" ORDER BY {sort_by}"

            employees = self.db.fetchall(query, params)

            for row in self.tree.get_children():
                self.tree.delete(row)

            for emp in employees:
                self.tree.insert("", tk.END, values=emp)

            filter_window.destroy()

        ttk.Button(frame, text="Apply", command=apply).grid(
            row=2, column=0, columnspan=2, pady=10)

# Main function to run the application
def main():
    root = tk.Tk()
    WelcomePage(root)
    #EmployeeManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


