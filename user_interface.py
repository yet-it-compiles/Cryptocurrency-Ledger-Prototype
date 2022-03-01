""" This module configures each page of the Cryptocurrency ledger """
from typing import Any

import tkinter as tk
from tkinter import *
import database
from database import *
import password_encryption
from password_encryption import *
import Error
from Error import *


class CryptocurrencyLedger(tk.Tk):
    """
    Configures the initial conditions for the UI, and contains the logic to switch between different canvases
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Declares the size of the canvas, and positions it on the screen
        tk.Tk.geometry(self, "")
        tk.Tk.configure(self, bg="#343333")

        canvas_setup = Canvas(self, bg="#343333", height=600, width=1000, bd=0, highlightthickness=0,
                              relief="ridge")
        canvas_setup.place(x=0, y=0)

        # Captures the background image for the canvas
        self.login_background = PhotoImage(file=f"login_background.png")
        canvas_setup.create_image(395.0, 300.0, image=self.login_background)

        # Initializing canvases to an empty dictionary
        self.collection_of_canvases = {}

        # Declaration of logic to iterate through each page layout
        for each_layout in (LoginPage, Enrollment, Dashboard, ComingSoon, Settings, AlertPopUp
                            , NotesTab, Portfolio):
            each_canvas = each_layout(canvas_setup, self)

            self.collection_of_canvases[each_layout] = each_canvas

            each_canvas.grid(row=5, column=0, sticky="nsew")

        self.show_canvas(LoginPage)  # First frame to show

    def show_canvas(self, container):
        """
        Displays the current from that is passed as a parameter, and raises it to the current stack
        :param container: The passed in window to display next
        :return: the new canvas
        """
        for each_canvas in self.collection_of_canvases.values():
            each_canvas.grid_remove()

        each_canvas = self.collection_of_canvases[container]
        each_canvas.grid()

        self.geometry(f'{each_canvas.winfo_reqwidth()}x{each_canvas.winfo_reqheight()}')  # resizes the canvases


class LoginPage(tk.Frame):
    """
    Configures, and displays the login page
    """

    def destroy_error(self):
        pop.destroy()

    def logoutbuttonClicker(self):
        pop = Toplevel(self)
        pop.geometry('537x250')
        pop.config(height=250, width=537)

        def destroy_error():
            pop.destroy()

        error_canvas = Canvas(pop, bg="#ffffff", height=273, width=537, bd=0, highlightthickness=0, relief="ridge")
        error_canvas.place(x=0, y=0)

        self.error_background_img = PhotoImage(file=f"error_background.png")
        error_canvas.create_image(0, 0, anchor='nw', image=self.error_background_img)

        self.error_message = Label(self, text=message, font='Times 12 bold').place(x=265, y=150)
        self.error_button_img = PhotoImage(file=f"error_button_img.png")
        error_button_obj = error_canvas.create_image(280, 200, image=self.error_button_img)
        error_canvas.tag_bind(error_button_obj, "<ButtonRelease-1>", lambda event: destroy_error())

    def sign_in(self, controller, usernameE, passwordE):
        global username
        username = usernameE.get()
        password = passwordE.get()

        if Database.checkUsername(username):
            if PasswordEncryption.password_comparison(username, password):
                print("made it")
                controller.show_canvas(Dashboard)
            else:

                error = "Incorrect Password"
                self.logoutbuttonClicker()
        else:
            error = "No Username"
            self.logoutbuttonClicker()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=1000, height=600)
        self.controller = controller
        username = tk.StringVar()
        password = tk.StringVar()

        login_canvas = Canvas(self, bg="#343333", height=600, width=1000, bd=0, highlightthickness=0,
                              relief="ridge")
        login_canvas.place(x=0, y=0)

        # Grabs the background image, and applies it
        self.login_background = PhotoImage(file=f"login_background.png")
        login_canvas.create_image(395.0, 300.0, image=self.login_background)

        # Logic to populate the window
        self.sign_in_button = PhotoImage(file=f"sign_in_button.png")
        sign_in_button_location = Button(self, image=self.sign_in_button, borderwidth=0, highlightthickness=0,
                                         command=lambda: self.sign_in(self.controller, username, password),
                                         relief="flat",
                                         activebackground="#343333")
        sign_in_button_location.place(x=659, y=417, width=159, height=53)

        # Creates, and displays the forgot password button
        self.forgot_password_button = PhotoImage(file=f"forgot_password_button.png")
        forgot_password_location = Button(self, image=self.forgot_password_button, borderwidth=0, highlightthickness=0,
                                          command=lambda: controller.show_canvas(Dashboard),
                                          relief="flat", activebackground="#343333")
        forgot_password_location.place(x=444, y=537, width=142, height=50)

        # Creates, and displays the sign-up button
        self.sign_up_button = PhotoImage(file=f"sign_up_button.png")
        sign_up_button_location = Button(self, image=self.sign_up_button, borderwidth=0, highlightthickness=0,
                                         relief="flat", activebackground="#343333",
                                         command=lambda: controller.show_canvas(Enrollment))

        sign_up_button_location.place(x=864, y=537, width=136, height=46)

        # Creates, and initializes the text boxes
        self.login_textbox_one = PhotoImage(file=f"login_textbox.png")
        login_canvas.create_image(738.5, 263.0, image=self.login_textbox_one)
        textbox_one_location = Entry(self, textvariable=username, bd=0, bg="#696969", highlightthickness=0)
        textbox_one_location.place(x=602.0, y=240, width=273.0, height=44)

        self.login_textbox_two = PhotoImage(file=f"login_textbox.png")
        login_canvas.create_image(738.5, 368.0, image=self.login_textbox_two)
        textbox_two_location = Entry(self, textvariable=password, bd=0, bg="#696969", highlightthickness=0, show='*')
        textbox_two_location.place(x=602.0, y=345, width=273.0, height=44)


class Enrollment(tk.Frame):
    """
    Configures, and displays the login page
    """

    def add_user(self, controller, username, password, email):
        usernameTxt = username.get()
        passwordTxt = password.get()
        emailTxt = email.get()

        if Database.checkUsername(usernameTxt):
            error = "username is taken"
            print(error)
            controller.show_canvas(LoginPage)
            return
        # possible check for password constraints
        Database.adduser(usernameTxt, emailTxt, passwordTxt)
        controller.show_canvas(LoginPage)
        username.set("")
        password.set("")
        email.set("")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=1000, height=600)
        self.controller = controller
        email = tk.StringVar()
        username = tk.StringVar()
        password = tk.StringVar()

        # Initializes the enrollment page, and configures the position of the canvas
        enrollment_canvas = Canvas(self, bg="#343333", height=600, width=1000, bd=0, highlightthickness=0,
                                   relief="ridge")
        enrollment_canvas.place(x=0, y=0)

        # Captures the background image for the canvas
        self.enrollment_background = PhotoImage(file=f"enrollment_background.png")
        enrollment_canvas.create_image(348.0, 300.0, image=self.enrollment_background)

        # Declaration of string variable which captures user entries
        self.enrollment_text_box = PhotoImage(file=f"enrollment_textBox.png")
        enrollment_canvas.create_image(722.5, 176.0, image=self.enrollment_text_box)
        email_text_box = Entry(self, textvariable=email, bd=0, bg="#696969", highlightthickness=0)
        email_text_box.place(x=586.0, y=153, width=273.0, height=44)

        self.enrollment_text_box_2 = PhotoImage(file=f"enrollment_textBox.png")
        enrollment_canvas.create_image(722.5, 293.0, image=self.enrollment_text_box_2)
        enrollment_text_box = Entry(self, textvariable=password, bd=0, bg="#696969", highlightthickness=0)
        enrollment_text_box.place(x=586.0, y=270, width=273.0, height=44)

        self.enrollment_text_box_3 = PhotoImage(file=f"enrollment_textBox.png")
        enrollment_canvas.create_image(722.5, 410.0, image=self.enrollment_text_box_3)
        user_name_text_box = Entry(self, textvariable=username, bd=0, bg="#696969", highlightthickness=0)
        user_name_text_box.place(x=586.0, y=387, width=273.0, height=44)

        self.get_started_button = PhotoImage(file=f"enrollment_get_started.png")
        get_started_background = Button(self, image=self.get_started_button, borderwidth=0, highlightthickness=0,
                                        command=lambda: self.add_user(controller, username, password, email),
                                        relief="flat",
                                        activebackground="#343333")
        get_started_background.place(x=636, y=481, width=161, height=53)

        enrollment_canvas.create_text(727.5, 71.5, text="Create Account", fill="#ffffff",
                                      font=("Rosarivo-Regular", int(36.0)))

        self.existing_account = PhotoImage(file=f"enrollment_existing_account.png")
        existing_account_background = Button(self, image=self.existing_account, borderwidth=0, highlightthickness=0,
                                             command=lambda: self.controller.show_canvas(LoginPage), relief="flat",
                                             activebackground="#343333")

        existing_account_background.place(x=618, y=530, width=212, height=51)


class Dashboard(tk.Frame):
    """
    Configures, and displays the Dashboard
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=1440, height=1024)
        flash_delay = 100  # Milliseconds.
        self.controller = controller

        canvas = tk.Canvas(self, bg="#343333", height=1024, width=1440, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Captures the background image for the canvas
        image_path = "dashboard_background.png"
        self.background_img = tk.PhotoImage(file=image_path)
        canvas.create_image(0, 0, anchor='nw', image=self.background_img)

        def logoutbuttonClicker():
            pop = Toplevel(self)
            pop.geometry('537x273')
            pop.config(height=273, width=537)

            logout_canvas = Canvas(pop, bg="#ffffff", height=273, width=537, bd=0, highlightthickness=0, relief="ridge")
            logout_canvas.place(x=0, y=0)

            self.logout_background_img = PhotoImage(file=f"logout_background.png")
            logout_canvas.create_image(0, 0, anchor='nw', image=self.logout_background_img)

            def destroy_logout():
                pop.destroy()

            # creates and adds functionality for the Yes button in the log out pop up
            self.logout_yes_img = PhotoImage(file=f"logout_yes.png")
            logout_yes_img_obj = logout_canvas.create_image(112, 135, anchor='nw', image=self.logout_yes_img)
            logout_canvas.tag_bind(logout_yes_img_obj, "<ButtonRelease-1>",
                                   lambda event: [destroy_logout(), (
                                   flash_hidden(logout_yes_img_obj), controller.show_canvas(LoginPage))])

            # creates and adds functionality for the No button in the log out pop up
            self.logout_no_img = PhotoImage(file=f"logout_no.png")
            logout_no_img_obj = logout_canvas.create_image(297, 135, anchor='nw', image=self.logout_no_img)
            logout_canvas.tag_bind(logout_no_img_obj, "<ButtonRelease-1>", lambda event: destroy_logout())

        # creates and opens up a log out pop up    
        logout_image_path = "dashboard_logout.png"
        self.logout_image = tk.PhotoImage(file=logout_image_path)
        logoutButton = canvas.create_image(45, 950, anchor='nw', image=self.logout_image)
        canvas.tag_bind(logoutButton, "<ButtonRelease-1>", lambda event: logoutbuttonClicker())

        # Creates text-fields for Searchbar, and Username
        canvas.create_text(588.0, 40.5, text="Search Bar\n", fill="#abb0c8", font=("Rosarivo-Regular", int(12.0)))
        canvas.create_text(1398.5, 68.5, text="John Doe", fill="#ffffff", font=("Rosarivo-Regular", int(12.0)))

        # Investing Portfolio
        canvas.create_text(430.0, 198.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(430.0, 248.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(430.0, 298.5, text="%", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))

        # Top Earner #1
        canvas.create_text(640.0, 147.0, text="$", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(640.0, 190.0, text="$", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(690.0, 214.0, text="%", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))

        # Top Earner #2
        canvas.create_text(865.0, 147.0, text="$", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(865.0, 190.0, text="$", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(920.0, 214.0, text="%", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))

        # Top Earner #3
        canvas.create_text(1096.0, 149.0, text="$", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(1096.0, 192.0, text="$", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(1149.0, 214.0, text="%", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))

        # Top Earner #4
        canvas.create_text(1322.0, 149.0, text="$", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(1322.0, 192.0, text="$", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(1373.0, 214.0, text="%", fill="#e5e5e5", font=("Rosarivo-Regular", int(10.0)))

        # Closest to profit #1
        canvas.create_text(640.0, 295.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(640.0, 338.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(690.0, 356.0, text="%", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))

        # Closest to profit #2
        canvas.create_text(865.0, 295.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(865.0, 338.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(920.0, 356.0, text="%", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))

        # Closest to profit #3
        canvas.create_text(1096.0, 295.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(1096.0, 338.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(1149.0, 356.0, text="%", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))

        # Closest to profit #4
        canvas.create_text(1322.0, 295.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(1322.0, 338.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(1373.0, 356.0, text="%", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))

        # Percent Increase Calculator
        canvas.create_text(968.0, 469.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(968.0, 504.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(968.0, 553.0, text="%", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(968.0, 604.0, text="$", fill="#ffffff", font=("Rosarivo-Regular", int(10.0)))
        canvas.create_text(975.0, 620.0, text="$0.00 is a 0% increase from $0.00", fill="#ffffff",
                           font=("Rosarivo-Regular", int(10.0)))

        # Retrieves the images, and configures the dashboard button
        dashboard_image_path = "dashboard_dashboard.png"
        self.dashboard_image = tk.PhotoImage(file=dashboard_image_path)
        dashboard_image_obj = canvas.create_image(0, 120, anchor='nw', image=self.dashboard_image)
        canvas.tag_bind(dashboard_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(dashboard_image_obj), controller.show_canvas(Dashboard)))

        # Retrieves the images, and configures the simulated trading button
        simulated_trading_image_path = "dashboard_simulated_trading.png"
        self.simulated_trading_image = tk.PhotoImage(file=simulated_trading_image_path)
        simulated_trading_image_obj = canvas.create_image(0, 230, anchor='nw', image=self.simulated_trading_image)
        canvas.tag_bind(simulated_trading_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(simulated_trading_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the charts button
        charts_image_path = "dashboard_charts.png"
        self.charts_image = tk.PhotoImage(file=charts_image_path)
        charts_image_obj = canvas.create_image(0, 340, anchor='nw', image=self.charts_image)
        canvas.tag_bind(charts_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(charts_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the portfolio button
        portfolio_image_path = "dashboard_portfolio.png"
        self.portfolio_image = tk.PhotoImage(file=portfolio_image_path)
        portfolio_image_obj = canvas.create_image(0, 450, anchor='nw', image=self.portfolio_image)
        canvas.tag_bind(portfolio_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(portfolio_image_obj), controller.show_canvas(Portfolio)))

        alarm_image_path = "dashboard_alarms.png"
        self.alarm_image = tk.PhotoImage(file=alarm_image_path)
        alarm_image_obj = canvas.create_image(0, 560, anchor='nw', image=self.alarm_image)
        canvas.tag_bind(alarm_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(alarm_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the news button
        news_image_path = "dashboard_news.png"
        self.news_image = tk.PhotoImage(file=news_image_path)
        news_image_obj = canvas.create_image(0, 670, anchor='nw', image=self.news_image)
        canvas.tag_bind(news_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(news_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the settings button
        settings_image_path = "dashboard_settings.png"
        self.settings_image = tk.PhotoImage(file=settings_image_path)
        settings_image_obj = canvas.create_image(0, 780, anchor='nw', image=self.settings_image)
        canvas.tag_bind(settings_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(settings_image_obj), controller.show_canvas(Settings)))

        # Retrieves the images, and configures the notifications image
        notifications_image_path = "dashboard_notifications.png"
        self.notifications_image = tk.PhotoImage(file=notifications_image_path)
        notifications_image_obj = canvas.create_image(1027, 19, anchor='nw', image=self.notifications_image)
        canvas.tag_bind(notifications_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notifications_image_obj), controller.show_canvas(AlertPopUp)))

        # Retrieves the images, and configures the support image
        support_image_path = "dashboard_support.png"
        self.support_image = tk.PhotoImage(file=support_image_path)
        support_image_obj = canvas.create_image(1155, 16, anchor='nw', image=self.support_image)
        canvas.tag_bind(support_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(support_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the profile image
        notes_image_path = "dashboard_notes.png"
        self.notes_image = tk.PhotoImage(file=notes_image_path)
        notes_image_obj = canvas.create_image(1268, 19, anchor='nw', image=self.notes_image)
        canvas.tag_bind(notes_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notes_image_obj), controller.show_canvas(NotesTab)))

        # Retrieves the images, and configures the profile image
        profile_image_path = "dashboard_profile_img.png"
        self.profile_image = tk.PhotoImage(file=profile_image_path)
        profile_image_obj = canvas.create_image(1360, 4, anchor='nw', image=self.profile_image)
        canvas.tag_bind(profile_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(profile_image_obj), controller.show_canvas(Settings)))

        canvas.create_text(1398.5, 68.5, text="John Doe", fill="#ffffff", font=("Rosarivo-Regular", int(12.0)))

        def flash_hidden(image_obj):
            """
            Method sets the state of the object, and hides the buttons when they are interacted with

            :param image_obj: is the image object to hide
            :type : int
            :return: a hidden button when pressed
            """
            set_state(tk.HIDDEN, image_obj)
            canvas.after(flash_delay, set_state, tk.NORMAL, image_obj)

        def set_state(state, image_obj):
            """
            Sets the state of the image object

            :param state: the state to apply to the buttons
            :param image_obj: is the image object to apply a state on
            :return: an image object with a state applied
            """
            canvas.itemconfigure(image_obj, state=state)

        self.background_img.width(), self.background_img.height()


class ComingSoon(tk.Frame):
    """
    Configures, and displays the Dashboard
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=1440, height=1024)
        flash_delay = 100  # Milliseconds.
        self.controller = controller

        canvas = tk.Canvas(self, bg="#343333", height=1024, width=1440, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=f"coming_soon.png")
        canvas.create_image(718.0, 512.0, image=self.background_img)

        def logoutbuttonClicker():
            pop = Toplevel(self)
            pop.geometry('537x273')
            pop.config(height=273, width=537)

            logout_canvas = Canvas(pop, bg="#ffffff", height=273, width=537, bd=0, highlightthickness=0, relief="ridge")
            logout_canvas.place(x=0, y=0)

            self.logout_background_img = PhotoImage(file=f"logout_background.png")
            logout_canvas.create_image(0, 0, anchor='nw', image=self.logout_background_img)

            def destroy_logout():
                pop.destroy()

            # creates and adds functionality for the Yes button in the log out pop up
            self.logout_yes_img = PhotoImage(file=f"logout_yes.png")
            logout_yes_img_obj = logout_canvas.create_image(112, 135, anchor='nw', image=self.logout_yes_img)
            logout_canvas.tag_bind(logout_yes_img_obj, "<ButtonRelease-1>",
                                   lambda event: [destroy_logout(), (
                                   flash_hidden(logout_yes_img_obj), controller.show_canvas(LoginPage))])

            # creates and adds functionality for the No button in the log out pop up
            self.logout_no_img = PhotoImage(file=f"logout_no.png")
            logout_no_img_obj = logout_canvas.create_image(297, 135, anchor='nw', image=self.logout_no_img)
            logout_canvas.tag_bind(logout_no_img_obj, "<ButtonRelease-1>", lambda event: destroy_logout())

        # creates and opens up a log out pop up    
        logout_image_path = "dashboard_logout.png"
        self.logout_image = tk.PhotoImage(file=logout_image_path)
        logoutButton = canvas.create_image(45, 950, anchor='nw', image=self.logout_image)
        canvas.tag_bind(logoutButton, "<ButtonRelease-1>", lambda event: logoutbuttonClicker())

        # Retrieves the images, and configures the dashboard button
        dashboard_image_path = "dashboard_dashboard.png"
        self.dashboard_image = tk.PhotoImage(file=dashboard_image_path)
        dashboard_image_obj = canvas.create_image(0, 120, anchor='nw', image=self.dashboard_image)
        canvas.tag_bind(dashboard_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(dashboard_image_obj), controller.show_canvas(Dashboard)))

        # Retrieves the images, and configures the simulated trading button
        simulated_trading_image_path = "dashboard_simulated_trading.png"
        self.simulated_trading_image = tk.PhotoImage(file=simulated_trading_image_path)
        simulated_trading_image_obj = canvas.create_image(0, 230, anchor='nw', image=self.simulated_trading_image)
        canvas.tag_bind(simulated_trading_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(simulated_trading_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the charts button
        charts_image_path = "dashboard_charts.png"
        self.charts_image = tk.PhotoImage(file=charts_image_path)
        charts_image_obj = canvas.create_image(0, 340, anchor='nw', image=self.charts_image)
        canvas.tag_bind(charts_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(charts_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the portfolio button
        portfolio_image_path = "dashboard_portfolio.png"
        self.portfolio_image = tk.PhotoImage(file=portfolio_image_path)
        portfolio_image_obj = canvas.create_image(0, 450, anchor='nw', image=self.portfolio_image)
        canvas.tag_bind(portfolio_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(portfolio_image_obj), controller.show_canvas(Portfolio)))

        alarm_image_path = "dashboard_alarms.png"
        self.alarm_image = tk.PhotoImage(file=alarm_image_path)
        alarm_image_obj = canvas.create_image(0, 560, anchor='nw', image=self.alarm_image)
        canvas.tag_bind(alarm_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(alarm_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the news button
        news_image_path = "dashboard_news.png"
        self.news_image = tk.PhotoImage(file=news_image_path)
        news_image_obj = canvas.create_image(0, 670, anchor='nw', image=self.news_image)
        canvas.tag_bind(news_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(news_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the settings button
        settings_image_path = "dashboard_settings.png"
        self.settings_image = tk.PhotoImage(file=settings_image_path)
        settings_image_obj = canvas.create_image(0, 780, anchor='nw', image=self.settings_image)
        canvas.tag_bind(settings_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(settings_image_obj), controller.show_canvas(Settings)))

        # Retrieves the images, and configures the notifications image
        notifications_image_path = "dashboard_notifications.png"
        self.notifications_image = tk.PhotoImage(file=notifications_image_path)
        notifications_image_obj = canvas.create_image(1027, 19, anchor='nw', image=self.notifications_image)
        canvas.tag_bind(notifications_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notifications_image_obj), controller.show_canvas(AlertPopUp)))

        # Retrieves the images, and configures the support image
        support_image_path = "dashboard_support.png"
        self.support_image = tk.PhotoImage(file=support_image_path)
        support_image_obj = canvas.create_image(1155, 16, anchor='nw', image=self.support_image)
        canvas.tag_bind(support_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(support_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the profile image
        notes_image_path = "dashboard_notes.png"
        self.notes_image = tk.PhotoImage(file=notes_image_path)
        notes_image_obj = canvas.create_image(1268, 19, anchor='nw', image=self.notes_image)
        canvas.tag_bind(notes_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notes_image_obj), controller.show_canvas(NotesTab)))

        # Retrieves the images, and configures the profile image
        profile_image_path = "dashboard_profile_img.png"
        self.profile_image = tk.PhotoImage(file=profile_image_path)
        profile_image_obj = canvas.create_image(1360, 4, anchor='nw', image=self.profile_image)
        canvas.tag_bind(profile_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(profile_image_obj), controller.show_canvas(Settings)))

        canvas.create_text(1398.5, 68.5, text="John Doe", fill="#ffffff", font=("Rosarivo-Regular", int(12.0)))

        def flash_hidden(image_obj):
            """
            Method sets the state of the object, and hides the buttons when they are interacted with

            :param image_obj: is the image object to hide
            :type : int
            :return: an image object that is hidden
            """
            set_state(tk.HIDDEN, image_obj)
            canvas.after(flash_delay, set_state, tk.NORMAL, image_obj)

        def set_state(state, image_obj):
            """
            Sets the state of the image object

            :param state: the state to apply to the buttons
            :param image_obj: is the image object to apply a state on
            :return: an image object with a state applied
            """
            canvas.itemconfigure(image_obj, state=state)

        self.background_img.width(), self.background_img.height()


class Settings(tk.Frame):
    """
    Configures, and displays the Settings page
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=1440, height=1024)
        self.controller = controller

        flash_delay = 100  # in milliseconds.

        canvas = tk.Canvas(self, bg="#343333", height=1024, width=1440, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Retrieves the images, and configures the dashboard button
        self.background_img = tk.PhotoImage(file=f"settings_background.png")
        canvas.create_image(722.0, 512.0, image=self.background_img)

        def logoutbuttonClicker():
            pop = Toplevel(self)
            pop.geometry('537x273')
            pop.config(height=273, width=537)

            logout_canvas = Canvas(pop, bg="#ffffff", height=273, width=537, bd=0, highlightthickness=0, relief="ridge")
            logout_canvas.place(x=0, y=0)

            self.logout_background_img = PhotoImage(file=f"logout_background.png")
            logout_canvas.create_image(0, 0, anchor='nw', image=self.logout_background_img)

            def destroy_logout():
                pop.destroy()

            # creates and adds functionality for the Yes button in the log out pop up
            self.logout_yes_img = PhotoImage(file=f"logout_yes.png")
            logout_yes_img_obj = logout_canvas.create_image(112, 135, anchor='nw', image=self.logout_yes_img)
            logout_canvas.tag_bind(logout_yes_img_obj, "<ButtonRelease-1>",
                                   lambda event: [destroy_logout(), (
                                   flash_hidden(logout_yes_img_obj), controller.show_canvas(LoginPage))])

            # creates and adds functionality for the No button in the log out pop up
            self.logout_no_img = PhotoImage(file=f"logout_no.png")
            logout_no_img_obj = logout_canvas.create_image(297, 135, anchor='nw', image=self.logout_no_img)
            logout_canvas.tag_bind(logout_no_img_obj, "<ButtonRelease-1>", lambda event: destroy_logout())

        # creates and opens up a log out pop up    
        logout_image_path = "dashboard_logout.png"
        self.logout_image = tk.PhotoImage(file=logout_image_path)
        logoutButton = canvas.create_image(45, 950, anchor='nw', image=self.logout_image)
        canvas.tag_bind(logoutButton, "<ButtonRelease-1>", lambda event: logoutbuttonClicker())

        # Retrieves the images, and configures the dashboard button
        dashboard_image_path = "dashboard_dashboard.png"
        self.dashboard_image = tk.PhotoImage(file=dashboard_image_path)
        dashboard_image_obj = canvas.create_image(0, 120, anchor='nw', image=self.dashboard_image)
        canvas.tag_bind(dashboard_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(dashboard_image_obj), controller.show_canvas(Dashboard)))

        # Retrieves the images, and configures the simulated trading button
        simulated_trading_image_path = "dashboard_simulated_trading.png"
        self.simulated_trading_image = tk.PhotoImage(file=simulated_trading_image_path)
        simulated_trading_image_obj = canvas.create_image(0, 230, anchor='nw', image=self.simulated_trading_image)
        canvas.tag_bind(simulated_trading_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(simulated_trading_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the charts button
        charts_image_path = "dashboard_charts.png"
        self.charts_image = tk.PhotoImage(file=charts_image_path)
        charts_image_obj = canvas.create_image(0, 340, anchor='nw', image=self.charts_image)
        canvas.tag_bind(charts_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(charts_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the portfolio button
        portfolio_image_path = "dashboard_portfolio.png"
        self.portfolio_image = tk.PhotoImage(file=portfolio_image_path)
        portfolio_image_obj = canvas.create_image(0, 450, anchor='nw', image=self.portfolio_image)
        canvas.tag_bind(portfolio_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(portfolio_image_obj), controller.show_canvas(Portfolio)))

        alarm_image_path = "dashboard_alarms.png"
        self.alarm_image = tk.PhotoImage(file=alarm_image_path)
        alarm_image_obj = canvas.create_image(0, 560, anchor='nw', image=self.alarm_image)
        canvas.tag_bind(alarm_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(alarm_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the news button
        news_image_path = "dashboard_news.png"
        self.news_image = tk.PhotoImage(file=news_image_path)
        news_image_obj = canvas.create_image(0, 670, anchor='nw', image=self.news_image)
        canvas.tag_bind(news_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(news_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the settings button
        settings_image_path = "dashboard_settings.png"
        self.settings_image = tk.PhotoImage(file=settings_image_path)
        settings_image_obj = canvas.create_image(0, 780, anchor='nw', image=self.settings_image)
        canvas.tag_bind(settings_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(settings_image_obj), controller.show_canvas(Settings)))

        # Retrieves the images, and configures the notifications image
        notifications_image_path = "dashboard_notifications.png"
        self.notifications_image = tk.PhotoImage(file=notifications_image_path)
        notifications_image_obj = canvas.create_image(1027, 19, anchor='nw', image=self.notifications_image)
        canvas.tag_bind(notifications_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notifications_image_obj), controller.show_canvas(AlertPopUp)))

        # Retrieves the images, and configures the support image
        support_image_path = "dashboard_support.png"
        self.support_image = tk.PhotoImage(file=support_image_path)
        support_image_obj = canvas.create_image(1155, 16, anchor='nw', image=self.support_image)
        canvas.tag_bind(support_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(support_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the profile image
        notes_image_path = "dashboard_notes.png"
        self.notes_image = tk.PhotoImage(file=notes_image_path)
        notes_image_obj = canvas.create_image(1268, 19, anchor='nw', image=self.notes_image)
        canvas.tag_bind(notes_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notes_image_obj), controller.show_canvas(NotesTab)))

        # Retrieves the images, and configures the profile image
        profile_image_path = "dashboard_profile_img.png"
        self.profile_image = tk.PhotoImage(file=profile_image_path)
        profile_image_obj = canvas.create_image(1360, 4, anchor='nw', image=self.profile_image)
        canvas.tag_bind(profile_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(profile_image_obj), controller.show_canvas(Settings)))

        canvas.create_text(1398.5, 68.5, text="John Doe", fill="#ffffff", font=("Rosarivo-Regular", int(12.0)))

        def flash_hidden(image_obj):
            """
            Method sets the state of the object, and hides the buttons when they are interacted with

            :param image_obj: is the image object to hide
            :type : int
            :return: a hidden button when pressed
            """
            set_state(tk.HIDDEN, image_obj)
            canvas.after(flash_delay, set_state, tk.NORMAL, image_obj)

        def set_state(state, image_obj):
            """
            Sets the state of the image object

            :param state: the state to apply to the buttons
            :param image_obj: is the image object to apply a state on
            :return: an image object with a state applied
            """
            canvas.itemconfigure(image_obj, state=state)

        self.settings_image.width(), self.settings_image.height()

        self.entry0_img = PhotoImage(file=f"settings_entry.png")
        canvas.create_image(731.5, 766.5, image=self.entry0_img)
        settings_email = Entry(self, bd=0, bg="#696969", highlightthickness=0)
        settings_email.place(x=597.5, y=741, width=268.0, height=49)

        self.entry1_img = PhotoImage(file=f"settings_entry.png")
        canvas.create_image(731.5, 647.5, image=self.entry1_img)

        entry1 = Entry(self, bd=0, bg="#696969", highlightthickness=0)

        entry1.place(x=597.5, y=622, width=268.0, height=49)

        self.entry2_img = PhotoImage(file=f"settings_entry.png")
        canvas.create_image(731.5, 528.5, image=self.entry2_img)

        entry2 = Entry(self, bd=0, bg="#696969", highlightthickness=0)

        entry2.place(x=597.5, y=503, width=268.0, height=49)

        canvas.create_text(731.5, 422.0, text="John Doe", fill="#ffffff", font=("Rosarivo-Regular", int(26.0)))


class NotesTab(tk.Frame):
    """
    Configures, and displays the Notes tab
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=1440, height=1024)
        self.controller = controller

        flash_delay = 100  # in milliseconds.
        canvas = Canvas(self, bg="#ffffff", height=1024, width=1440, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=f"sticky_notes_background.png")
        canvas.create_image(720.0, 512.0, image=self.background_img)

        def logoutbuttonClicker():
            pop = Toplevel(self)
            pop.geometry('537x273')
            pop.config(height=273, width=537)

            logout_canvas = Canvas(pop, bg="#ffffff", height=273, width=537, bd=0, highlightthickness=0, relief="ridge")
            logout_canvas.place(x=0, y=0)

            self.logout_background_img = PhotoImage(file=f"logout_background.png")
            logout_canvas.create_image(0, 0, anchor='nw', image=self.logout_background_img)

            def destroy_logout():
                pop.destroy()

            # creates and adds functionality for the Yes button in the log out pop up
            self.logout_yes_img = PhotoImage(file=f"logout_yes.png")
            logout_yes_img_obj = logout_canvas.create_image(112, 135, anchor='nw', image=self.logout_yes_img)
            logout_canvas.tag_bind(logout_yes_img_obj, "<ButtonRelease-1>",
                                   lambda event: [destroy_logout(), (
                                   flash_hidden(logout_yes_img_obj), controller.show_canvas(LoginPage))])

            # creates and adds functionality for the No button in the log out pop up
            self.logout_no_img = PhotoImage(file=f"logout_no.png")
            logout_no_img_obj = logout_canvas.create_image(297, 135, anchor='nw', image=self.logout_no_img)
            logout_canvas.tag_bind(logout_no_img_obj, "<ButtonRelease-1>", lambda event: destroy_logout())

        # creates and opens up a log out pop up    
        logout_image_path = "dashboard_logout.png"
        self.logout_image = tk.PhotoImage(file=logout_image_path)
        logoutButton = canvas.create_image(45, 950, anchor='nw', image=self.logout_image)
        canvas.tag_bind(logoutButton, "<ButtonRelease-1>", lambda event: logoutbuttonClicker())

        # Retrieves the images, and configures the dashboard button
        dashboard_image_path = "dashboard_dashboard.png"
        self.dashboard_image = tk.PhotoImage(file=dashboard_image_path)
        dashboard_image_obj = canvas.create_image(0, 120, anchor='nw', image=self.dashboard_image)
        canvas.tag_bind(dashboard_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(dashboard_image_obj), controller.show_canvas(Dashboard)))

        # Retrieves the images, and configures the simulated trading button
        simulated_trading_image_path = "dashboard_simulated_trading.png"
        self.simulated_trading_image = tk.PhotoImage(file=simulated_trading_image_path)
        simulated_trading_image_obj = canvas.create_image(0, 230, anchor='nw', image=self.simulated_trading_image)
        canvas.tag_bind(simulated_trading_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(simulated_trading_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the charts button
        charts_image_path = "dashboard_charts.png"
        self.charts_image = tk.PhotoImage(file=charts_image_path)
        charts_image_obj = canvas.create_image(0, 340, anchor='nw', image=self.charts_image)
        canvas.tag_bind(charts_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(charts_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the portfolio button
        portfolio_image_path = "dashboard_portfolio.png"
        self.portfolio_image = tk.PhotoImage(file=portfolio_image_path)
        portfolio_image_obj = canvas.create_image(0, 450, anchor='nw', image=self.portfolio_image)
        canvas.tag_bind(portfolio_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(portfolio_image_obj), controller.show_canvas(Portfolio)))

        alarm_image_path = "dashboard_alarms.png"
        self.alarm_image = tk.PhotoImage(file=alarm_image_path)
        alarm_image_obj = canvas.create_image(0, 560, anchor='nw', image=self.alarm_image)
        canvas.tag_bind(alarm_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(alarm_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the news button
        news_image_path = "dashboard_news.png"
        self.news_image = tk.PhotoImage(file=news_image_path)
        news_image_obj = canvas.create_image(0, 670, anchor='nw', image=self.news_image)
        canvas.tag_bind(news_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(news_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the settings button
        settings_image_path = "dashboard_settings.png"
        self.settings_image = tk.PhotoImage(file=settings_image_path)
        settings_image_obj = canvas.create_image(0, 780, anchor='nw', image=self.settings_image)
        canvas.tag_bind(settings_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(settings_image_obj), controller.show_canvas(Settings)))

        # Retrieves the images, and configures the notifications image
        notifications_image_path = "dashboard_notifications.png"
        self.notifications_image = tk.PhotoImage(file=notifications_image_path)
        notifications_image_obj = canvas.create_image(1027, 19, anchor='nw', image=self.notifications_image)
        canvas.tag_bind(notifications_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notifications_image_obj), controller.show_canvas(AlertPopUp)))

        # Retrieves the images, and configures the support image
        support_image_path = "dashboard_support.png"
        self.support_image = tk.PhotoImage(file=support_image_path)
        support_image_obj = canvas.create_image(1155, 16, anchor='nw', image=self.support_image)
        canvas.tag_bind(support_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(support_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the profile image
        notes_image_path = "dashboard_notes.png"
        self.notes_image = tk.PhotoImage(file=notes_image_path)
        notes_image_obj = canvas.create_image(1268, 19, anchor='nw', image=self.notes_image)
        canvas.tag_bind(notes_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notes_image_obj), controller.show_canvas(NotesTab)))

        # Retrieves the images, and configures the profile image
        profile_image_path = "dashboard_profile_img.png"
        self.profile_image = tk.PhotoImage(file=profile_image_path)
        profile_image_obj = canvas.create_image(1360, 4, anchor='nw', image=self.profile_image)
        canvas.tag_bind(profile_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(profile_image_obj), controller.show_canvas(Settings)))

        canvas.create_text(1398.5, 68.5, text="John Doe", fill="#ffffff", font=("Rosarivo-Regular", int(12.0)))

        def flash_hidden(image_obj):
            """
            Method sets the state of the object, and hides the buttons when they are interacted with

            :param image_obj: is the image object to hide
            :type : int
            :return: a hidden button when pressed
            """
            set_state(tk.HIDDEN, image_obj)
            canvas.after(flash_delay, set_state, tk.NORMAL, image_obj)

        def set_state(state, image_obj):
            """
            Sets the state of the image object

            :param state: the state to apply to the buttons
            :param image_obj: is the image object to apply a state on
            :return: an image object with a state applied
            """
            canvas.itemconfigure(image_obj, state=state)

        self.entry0_img = PhotoImage(file=f"sticky_notes_textBox0.png")
        canvas.create_image(1132.5, 720.5, image=self.entry0_img)
        entry0 = Entry(self, bd=0, bg="#306380", highlightthickness=0)
        entry0.place(x=975, y=611, width=315, height=217)

        self.entry1_img = PhotoImage(file=f"sticky_notes_textBox1.png")
        canvas.create_image(754.5, 720.5, image=self.entry1_img)
        entry1 = Entry(self, bd=0, bg="#2da596", highlightthickness=0)
        entry1.place(x=597, y=611, width=315, height=217)

        self.entry2_img = PhotoImage(file=f"sticky_notes_textBox2.png")
        canvas.create_image(376.5, 720.5, image=self.entry2_img)
        entry2 = Entry(self, bd=0, bg="#9d5a89", highlightthickness=0)
        entry2.place(x=219, y=611, width=315, height=217)

        self.entry3_img = PhotoImage(file=f"sticky_notes_textBox3.png")
        canvas.create_image(1132.5, 352.5, image=self.entry3_img)
        entry3 = Entry(self, bd=0, bg="#646da7", highlightthickness=0)
        entry3.place(x=975, y=243, width=315, height=217)

        self.entry4_img = PhotoImage(file=f"sticky_notes_textBox4.png")
        canvas.create_image(754.5, 352.5, image=self.entry4_img)
        entry4 = Entry(self, bd=0, bg="#417e9a", highlightthickness=0)
        entry4.place(x=597, y=243, width=315, height=217)

        self.entry5_img = PhotoImage(file=f"sticky_notes_textBox5.png")
        canvas.create_image(376.5, 352.5, image=self.entry5_img)
        entry5 = Entry(self, bd=0, bg="#826fa8", highlightthickness=0)
        entry5.place(x=219, y=243, width=315, height=217)

        self.img0 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b0 = Button(self, image=self.img0, borderwidth=0, highlightthickness=0, relief="flat")
        b0.place(x=1260, y=835, width=20, height=12)

        self.img1 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b1 = Button(self, image=self.img1, borderwidth=0, highlightthickness=0, relief="flat")
        b1.place(x=1232, y=835, width=19, height=12)

        self.img2 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b2 = Button(self, image=self.img2, borderwidth=0, highlightthickness=0, relief="flat")
        b2.place(x=1203, y=835, width=20, height=12)

        self.img3 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b3 = Button(self, image=self.img3, borderwidth=0, highlightthickness=0, relief="flat")
        b3.place(x=880, y=835, width=20, height=12)

        self.img4 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b4 = Button(self, image=self.img4, borderwidth=0, highlightthickness=0, relief="flat")
        b4.place(x=852, y=835, width=19, height=12)

        self.img5 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b5 = Button(self, image=self.img5, borderwidth=0, highlightthickness=0, relief="flat")
        b5.place(x=823, y=835, width=20, height=12)

        self.img6 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b6 = Button(self, image=self.img6, borderwidth=0, highlightthickness=0, relief="flat")
        b6.place(x=500, y=836, width=20, height=12)

        self.img7 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b7 = Button(self, image=self.img7, borderwidth=0, highlightthickness=0, relief="flat")
        b7.place(x=473, y=836, width=19, height=12)

        self.img8 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b8 = Button(self, image=self.img8, borderwidth=0, highlightthickness=0, relief="flat")
        b8.place(x=445, y=836, width=20, height=12)

        self.img9 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b9 = Button(self, image=self.img9, borderwidth=0, highlightthickness=0, relief="flat")
        b9.place(x=1260, y=466, width=20, height=12)

        self.img10 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b10 = Button(self, image=self.img10, borderwidth=0, highlightthickness=0, relief="flat")
        b10.place(x=1232, y=466, width=19, height=12)

        self.img11 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b11 = Button(self, image=self.img11, borderwidth=0, highlightthickness=0, relief="flat")
        b11.place(x=1203, y=466, width=20, height=12)

        self.img12 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b12 = Button(self, image=self.img12, borderwidth=0, highlightthickness=0, relief="flat")
        b12.place(x=880, y=466, width=20, height=12)

        self.img13 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b13 = Button(self, image=self.img13, borderwidth=0, highlightthickness=0, relief="flat")
        b13.place(x=852, y=466, width=19, height=12)

        self.img14 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b14 = Button(self, image=self.img14, borderwidth=0, highlightthickness=0, relief="flat")
        b14.place(x=823, y=466, width=20, height=12)

        self.img15 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b15 = Button(self, image=self.img15, borderwidth=0, highlightthickness=0, relief="flat")
        b15.place(x=500, y=466, width=20, height=12)

        self.img16 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b16 = Button(self, image=self.img16, borderwidth=0, highlightthickness=0, relief="flat")
        b16.place(x=473, y=466, width=19, height=12)

        self.img17 = PhotoImage(file=f"sticky_notes_color_changer.png")
        b17 = Button(self, image=self.img17, borderwidth=0, highlightthickness=0, relief="flat")
        b17.place(x=445, y=466, width=20, height=12)


class AlertPopUp(tk.Frame):
    """
    Configures, and displays the alert popup
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=684, height=426)
        self.controller = controller

        flash_delay = 100  # in milliseconds.
        canvas = Canvas(self, bg="#ffffff", height=426, width=684, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=f"alert_popup_background.png")
        canvas.create_image(342.0, 213.0, image=self.background_img)

        self.entry0_img = PhotoImage(file=f"alert_popup_textBox0.png")
        canvas.create_image(331.5, 294.5, image=self.entry0_img)

        entry0 = Entry(self, bd=0, bg="#dcdcdc", highlightthickness=0)
        entry0.place(x=264.5, y=283, width=134.0, height=21)

        self.entry1_img = PhotoImage(file=f"alert_popup_textBox1.png")
        canvas.create_image(297.5, 240.5, image=self.entry1_img)

        entry1 = Entry(self, bd=0, bg="#dcdcdc", highlightthickness=0)
        entry1.place(x=264.5, y=229, width=66.0, height=21)

        self.entry2_img = PhotoImage(file=f"alert_popup_textBox2.png")
        canvas.create_image(335.5, 132.0, image=self.entry2_img)
        entry2 = Entry(self, bd=0, bg="#dcdcdc", highlightthickness=0)
        entry2.place(x=268.0, y=121, width=135.0, height=20)

        self.img0 = PhotoImage(file=f"alert_popup_img0.png")
        b0 = Button(self, image=self.img0, borderwidth=0, highlightthickness=0, relief="flat")
        b0.place(x=342, y=178, width=98, height=22)

        self.img1 = PhotoImage(file=f"alert_popup_img1.png")
        b1 = Button(self, image=self.img1, borderwidth=0, highlightthickness=0, relief="flat")
        b1.place(x=253, y=178, width=80, height=22)


class Portfolio(tk.Frame):
    """

    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=1440, height=1024)
        self.controller = controller

        flash_delay = 100  # in milliseconds.

        canvas = Canvas(self, bg="#ffffff", height=1024, width=1440, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=f"portfolio_background.png")
        canvas.create_image(720.0, 512.0, image=self.background_img)

        def logoutbuttonClicker():
            pop = Toplevel(self)
            pop.geometry('537x273')
            pop.config(height=273, width=537)

            logout_canvas = Canvas(pop, bg="#ffffff", height=273, width=537, bd=0, highlightthickness=0, relief="ridge")
            logout_canvas.place(x=0, y=0)

            self.logout_background_img = PhotoImage(file=f"logout_background.png")
            logout_canvas.create_image(0, 0, anchor='nw', image=self.logout_background_img)

            def destroy_logout():
                pop.destroy()

            # creates and adds functionality for the Yes button in the log out pop up
            self.logout_yes_img = PhotoImage(file=f"logout_yes.png")
            logout_yes_img_obj = logout_canvas.create_image(112, 135, anchor='nw', image=self.logout_yes_img)
            logout_canvas.tag_bind(logout_yes_img_obj, "<ButtonRelease-1>",
                                   lambda event: [destroy_logout(), (
                                   flash_hidden(logout_yes_img_obj), controller.show_canvas(LoginPage))])

            # creates and adds functionality for the No button in the log out pop up
            self.logout_no_img = PhotoImage(file=f"logout_no.png")
            logout_no_img_obj = logout_canvas.create_image(297, 135, anchor='nw', image=self.logout_no_img)
            logout_canvas.tag_bind(logout_no_img_obj, "<ButtonRelease-1>", lambda event: destroy_logout())

        # creates and opens up a log out pop up    
        logout_image_path = "dashboard_logout.png"
        self.logout_image = tk.PhotoImage(file=logout_image_path)
        logoutButton = canvas.create_image(45, 950, anchor='nw', image=self.logout_image)
        canvas.tag_bind(logoutButton, "<ButtonRelease-1>", lambda event: logoutbuttonClicker())

        canvas.create_text(601.0, 904.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(763.0, 886.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 895.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 917.0, text="0.00%", fill="#ffffff", font=("RopaSans-Regular", int(13.0)))
        canvas.create_text(763.0, 912.0, text="0", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(376.0, 905.0, text="-", fill="#ffffff", font=("Rosarivo-Regular", int(13.0)))
        canvas.create_text(978.5, 191.5, text="0.00%", fill="#ffffff", font=("SourceCodePro-Regular", int(15.0)))
        canvas.create_text(717.5, 191.5, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(15.0)))
        canvas.create_text(1196.5, 191.5, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(15.0)))
        canvas.create_text(374.5, 197.5, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(25.0)))
        canvas.create_text(1398.5, 68.5, text="John Doe", fill="#ffffff", font=("Rosarivo-Regular", int(12.0)))
        canvas.create_text(601.0, 387.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(759.0, 387.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 378.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(938.0, 387.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(938.0, 463.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(938.0, 549.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(938.0, 640.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(938.0, 724.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(938.0, 818.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(938.0, 904.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1131.0, 387.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1131.0, 460.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1131.0, 546.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1131.0, 637.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1131.0, 721.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1131.0, 815.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1131.0, 901.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 399.0, text="0.00%", fill="#ffffff", font=("RopaSans-Regular", int(13.0)))
        canvas.create_text(759.0, 409.0, text="0 ", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(376.0, 384.0, text="-", fill="#ffffff", font=("Rosarivo-Regular", int(13.0)))
        canvas.create_text(601.0, 466.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(763.0, 451.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 460.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 482.0, text="0.00%", fill="#ffffff", font=("RopaSans-Regular", int(13.0)))
        canvas.create_text(763.0, 477.0, text="0", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(376.0, 470.0, text="-", fill="#ffffff", font=("Rosarivo-Regular", int(13.0)))
        canvas.create_text(601.0, 562.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(763.0, 538.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 547.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 569.0, text="0.00%", fill="#ffffff", font=("RopaSans-Regular", int(13.0)))
        canvas.create_text(763.0, 564.0, text="0", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(376.0, 557.0, text="-", fill="#ffffff", font=("Rosarivo-Regular", int(13.0)))
        canvas.create_text(601.0, 644.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(763.0, 625.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 634.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 656.0, text="0.00%", fill="#ffffff", font=("RopaSans-Regular", int(13.0)))
        canvas.create_text(763.0, 651.0, text="0", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(376.0, 644.0, text="-", fill="#ffffff", font=("Rosarivo-Regular", int(13.0)))
        canvas.create_text(601.0, 727.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(763.0, 710.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 719.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 741.0, text="0.00%", fill="#ffffff", font=("RopaSans-Regular", int(13.0)))
        canvas.create_text(763.0, 736.0, text="0", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(376.0, 729.0, text="-", fill="#ffffff", font=("Rosarivo-Regular", int(13.0)))
        canvas.create_text(601.0, 822.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(763.0, 803.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 812.0, text="$", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(1270.0, 834.0, text="0.00%", fill="#ffffff", font=("RopaSans-Regular", int(13.0)))
        canvas.create_text(763.0, 829.0, text="0", fill="#ffffff", font=("SourceCodePro-Regular", int(13.0)))
        canvas.create_text(376.0, 822.0, text="-", fill="#ffffff", font=("Rosarivo-Regular", int(13.0)))
        canvas.create_text(378.5, 237.0, text="0.00%", fill="#ffffff", font=("SourceCodePro-Regular", int(15.0)))

        # Retrieves the images, and configures the dashboard button
        dashboard_image_path = "dashboard_dashboard.png"
        self.dashboard_image = tk.PhotoImage(file=dashboard_image_path)
        dashboard_image_obj = canvas.create_image(0, 120, anchor='nw', image=self.dashboard_image)
        canvas.tag_bind(dashboard_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(dashboard_image_obj), controller.show_canvas(Dashboard)))

        # Retrieves the images, and configures the simulated trading button
        simulated_trading_image_path = "dashboard_simulated_trading.png"
        self.simulated_trading_image = tk.PhotoImage(file=simulated_trading_image_path)
        simulated_trading_image_obj = canvas.create_image(0, 230, anchor='nw', image=self.simulated_trading_image)
        canvas.tag_bind(simulated_trading_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(simulated_trading_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the charts button
        charts_image_path = "dashboard_charts.png"
        self.charts_image = tk.PhotoImage(file=charts_image_path)
        charts_image_obj = canvas.create_image(0, 340, anchor='nw', image=self.charts_image)
        canvas.tag_bind(charts_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(charts_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the portfolio button
        portfolio_image_path = "dashboard_portfolio.png"
        self.portfolio_image = tk.PhotoImage(file=portfolio_image_path)
        portfolio_image_obj = canvas.create_image(0, 450, anchor='nw', image=self.portfolio_image)
        canvas.tag_bind(portfolio_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(portfolio_image_obj), controller.show_canvas(ComingSoon)))

        alarm_image_path = "dashboard_alarms.png"
        self.alarm_image = tk.PhotoImage(file=alarm_image_path)
        alarm_image_obj = canvas.create_image(0, 560, anchor='nw', image=self.alarm_image)
        canvas.tag_bind(alarm_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(alarm_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the news button
        news_image_path = "dashboard_news.png"
        self.news_image = tk.PhotoImage(file=news_image_path)
        news_image_obj = canvas.create_image(0, 670, anchor='nw', image=self.news_image)
        canvas.tag_bind(news_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(news_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the settings button
        settings_image_path = "dashboard_settings.png"
        self.settings_image = tk.PhotoImage(file=settings_image_path)
        settings_image_obj = canvas.create_image(0, 780, anchor='nw', image=self.settings_image)
        canvas.tag_bind(settings_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(settings_image_obj), controller.show_canvas(Settings)))

        # Retrieves the images, and configures the notifications image
        notifications_image_path = "dashboard_notifications.png"
        self.notifications_image = tk.PhotoImage(file=notifications_image_path)
        notifications_image_obj = canvas.create_image(1027, 19, anchor='nw', image=self.notifications_image)
        canvas.tag_bind(notifications_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notifications_image_obj), controller.show_canvas(AlertPopUp)))

        # Retrieves the images, and configures the support image
        support_image_path = "dashboard_support.png"
        self.support_image = tk.PhotoImage(file=support_image_path)
        support_image_obj = canvas.create_image(1155, 16, anchor='nw', image=self.support_image)
        canvas.tag_bind(support_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(support_image_obj), controller.show_canvas(ComingSoon)))

        # Retrieves the images, and configures the profile image
        notes_image_path = "dashboard_notes.png"
        self.notes_image = tk.PhotoImage(file=notes_image_path)
        notes_image_obj = canvas.create_image(1268, 19, anchor='nw', image=self.notes_image)
        canvas.tag_bind(notes_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(notes_image_obj), controller.show_canvas(NotesTab)))

        # Retrieves the images, and configures the profile image
        profile_image_path = "dashboard_profile_img.png"
        self.profile_image = tk.PhotoImage(file=profile_image_path)
        profile_image_obj = canvas.create_image(1360, 4, anchor='nw', image=self.profile_image)
        canvas.tag_bind(profile_image_obj, "<ButtonRelease-1>",
                        lambda event: (flash_hidden(profile_image_obj), controller.show_canvas(Settings)))

        canvas.create_text(1398.5, 68.5, text="John Doe", fill="#ffffff", font=("Rosarivo-Regular", int(12.0)))

        def flash_hidden(image_obj):
            """
            Method sets the state of the object, and hides the buttons when they are interacted with

            :param image_obj: is the image object to hide
            :type : int
            :return: a hidden button when pressed
            """
            set_state(tk.HIDDEN, image_obj)
            canvas.after(flash_delay, set_state, tk.NORMAL, image_obj)

        def set_state(state, image_obj):
            """
            Sets the state of the image object

            :param state: the state to apply to the buttons
            :param image_obj: is the image object to apply a state on
            :return: an image object with a state applied
            """
            canvas.itemconfigure(image_obj, state=state)

        self.entry0_img = PhotoImage(file=f"portfolio_textBox0.png")
        canvas.create_image(977.0, 251.0, image=self.entry0_img)

        entry0 = Entry(self, bd=0, bg="#053f53", highlightthickness=0)
        entry0.place(x=856.0, y=235, width=242.0, height=30)

        self.img12 = PhotoImage(file=f"portfolio_img12.png")
        b12 = Button(self, image=self.img12, borderwidth=0, highlightthickness=0, relief="flat")
        b12.place(x=1140, y=226, width=190, height=50)

        self.img13 = PhotoImage(file=f"portfolio_img13.png")
        b13 = Button(self, image=self.img13, borderwidth=0, highlightthickness=0, relief="flat")
        b13.place(x=883, y=97, width=43, height=25)

        self.img14 = PhotoImage(file=f"portfolio_img14.png")
        b14 = Button(self, image=self.img14, borderwidth=0, highlightthickness=0, relief="flat")
        b14.place(x=829, y=97, width=32, height=23)

        self.img15 = PhotoImage(file=f"portfolio_img15.png")
        b15 = Button(self, image=self.img15, borderwidth=0, highlightthickness=0, relief="flat")
        b15.place(x=772, y=96, width=30, height=30)

        self.img16 = PhotoImage(file=f"portfolio_img16.png")
        b16 = Button(self, image=self.img16, borderwidth=0, highlightthickness=0, relief="flat")
        b16.place(x=722, y=97, width=29, height=25)

        self.img17 = PhotoImage(file=f"portfolio_img17.png")
        b17 = Button(self, image=self.img17, borderwidth=0, highlightthickness=0, relief="flat")
        b17.place(x=670, y=98, width=30, height=28)

        self.img18 = PhotoImage(file=f"portfolio_img18.png")
        b18 = Button(self, image=self.img18, borderwidth=0, highlightthickness=0, relief="flat")
        b18.place(x=614, y=96, width=32, height=26)

        self.img19 = PhotoImage(file=f"portfolio_img19.png")
        b19 = Button(self, image=self.img19, borderwidth=0, highlightthickness=0, relief="flat")
        b19.place(x=1074, y=238, width=30, height=27)


def main():
    """
    Launchpad method to compile, and run this module

    :return: runs the program
    """
    app = CryptocurrencyLedger()
    app.mainloop()


if __name__ == '__main__':
    main()
