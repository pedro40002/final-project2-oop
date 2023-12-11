# appt_manager.py

from appointment import Appointment

def create_weekly_calendar():
    calendar = []
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    for day in days_of_week:
        for start_hour in range(9, 17):  # Adjusted end time to 17 for 4-5 PM
            appointment = Appointment(day, start_hour)
            calendar.append(appointment)

    return calendar

# Modify the load_scheduled_appointments function
def load_scheduled_appointments(appointment_list):
    file_name = input("Enter the filename to load scheduled appointments: ")

    try:
        with open(file_name, 'r') as file:
            for line in file:
                values = line.strip().split(',')
                day, start_hour = values[-2], int(values[-1])
                appointment = find_appointment_by_time(appointment_list, day, start_hour)
                if appointment:
                    appointment.schedule(values[0], values[1], int(values[2]))
        print(f"{len(values)} previously scheduled appointments have been loaded.")
    except FileNotFoundError:
        create_new_file = input("File not found. Do you want to create a new file? (yes/no): ").lower()
        if create_new_file == 'yes':
            with open(file_name, 'w') as new_file:
                print(f"New file '{file_name}' created.")
        else:
            print("Exiting the program.")
            exit()
def save_scheduled_appointments(appointment_list):
    file_name = input("Enter the filename to save scheduled appointments: ")

    try:
        with open(file_name, 'w') as file:
            for appointment in appointment_list:
                if appointment.get_appt_type() != 0:
                    file.write(appointment.format_record() + '\n')
        print(f"{len(appointment_list)} scheduled appointments have been saved.")
    except FileNotFoundError:
        print("File not found.")

def print_menu():
    print("Jojo's Hair Salon Appointment Manager")
    print("1) Schedule an appointment")
    print("2) Find appointment by name")
    print("3) Print calendar for a specific day")
    print("4) Cancel an appointment")
    print("9) Exit the system")

    try:
        choice = int(input("Enter your selection: "))
        return choice
    except ValueError:
        print("Invalid input. Please enter a number.")
        return print_menu()

# Modify the schedule_appointment function
# Modify the schedule_appointment function
def schedule_appointment(appointment_list):
    print("** Schedule an appointment **")

    # Get user input
    day = input("What day: ")
    start_hour = int(input("Enter start hour (24-hour clock): "))

    # Check if the chosen time is already booked
    existing_appointment = find_appointment_by_time(appointment_list, day, start_hour)
    if existing_appointment and existing_appointment.get_appt_type() != 0:
        print("The chosen time has already been booked by another client.")
        print("Please choose another time.")
        return

    # Get client details
    client_name = input("Client Name: ")
    client_phone = input("Client Phone: ")

    # Display appointment types
    print("Appointment types")
    print("1: Mens Cut $50, 2: Ladies Cut $86, 3: Mens Colouring $50, 4: Ladies Colouring $120")

    # Get appointment type
    appt_type = None
    while appt_type not in [1, 2, 3, 4]:
        try:
            appt_type = int(input("Select the type of appointment (1-4): "))
            if appt_type not in [1, 2, 3, 4]:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Schedule the appointment
    appointment = find_appointment_by_time(appointment_list, day, start_hour)
    if appointment:
        appointment.schedule(client_name, client_phone, appt_type)
        print(f"OK, {client_name}'s appointment is scheduled!")

        # Save the appointment to the file
        save_scheduled_appointments(appointment_list)
    else:
        print("Your file couldn't save. Please check your input.")
def find_appointment_by_name(appointment_list):
    print("Find Appointment by Name")

    # Get user input
    client_name = input("Enter the client's name: ")

    # Search for appointments by client name (case-insensitive)
    matching_appointments = [appointment for appointment in appointment_list
                             if client_name.lower() in appointment.get_client_name().lower()]

    # Display the matching appointments
    if matching_appointments:
        print("Matching Appointments:")
        for matching_appointment in matching_appointments:
            print(matching_appointment)
    else:
        print(f"No appointments found for the given client name: {client_name}")

def print_calendar_for_day(appointment_list):
    print("Print Calendar for a Specific Day")

    # Get user input
    day = input("Enter the day to print the calendar: ")

    # Filter appointments for the specified day
    day_appointments = [appointment for appointment in appointment_list
                        if appointment.get_day_of_week().lower() == day.lower()]

    # Display the calendar for the specified day
    if day_appointments:
        print(f"Appointments for {day.capitalize()}:")
        for day_appointment in day_appointments:
            print(day_appointment)
    else:
        print(f"No appointments found for the specified day: {day}")

def cancel_appointment(appointment_list):
    print("Cancel an Appointment")

    # Get user input
    day = input("Enter the day of the appointment to cancel: ")
    start_hour = int(input("Enter start_hour of the appointment to cancel: "))

    # Find the appointment to cancel
    appointment = find_appointment_by_time(appointment_list, day, start_hour)

    if appointment:
        # Display appointment details before cancellation
        print("Appointment Details:")
        print(appointment)

        # Confirm cancellation
        confirmation = input("Do you want to cancel this appointment? (yes/no): ")

        if confirmation.lower() == "yes":
            # Cancel the appointment
            appointment.cancel()
            print("Appointment canceled successfully.")
        else:
            print("Appointment not canceled.")
    else:
        print("Appointment not found.")

def find_appointment_by_time(appointment_list, day, start_hour):
    for appointment in appointment_list:
        if appointment.get_day_of_week() == day and appointment.get_start_time_hour() == start_hour:
            return appointment
    return None

def main():
    appointment_list = create_weekly_calendar()
    load_scheduled_appointments(appointment_list)

    while True:
        choice = print_menu()

        if choice == 1:
            schedule_appointment(appointment_list)
        elif choice == 2:
            find_appointment_by_name(appointment_list)
        elif choice == 3:
            print_calendar_for_day(appointment_list)
        elif choice == 4:
            cancel_appointment(appointment_list)
        elif choice == 9:
            save_scheduled_appointments(appointment_list)
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()