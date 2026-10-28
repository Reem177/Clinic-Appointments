"""Clinic Appointments - simple console app (R1-R4).

Class and method names follow class_diagram.md and sequence_diagram.md.
Rule N = 3: a patient can have at most 3 upcoming appointments
(future Pending + Accepted only; Declined and past ones do not count).
"""
from datetime import datetime, timedelta
from enum import Enum

MAX_UPCOMING = 3  # N


class AppointmentStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"


class AvailabilitySlot:
    def __init__(self, slot_id, doctor, start_time, end_time):
        self.slot_id = slot_id
        self.doctor = doctor
        self.start_time = start_time
        self.end_time = end_time
        self.is_available = True

    def checkAvailability(self):
        return self.is_available

    def reserve(self):
        self.is_available = False

    def release(self):
        self.is_available = True

    def __str__(self):
        return (f"[{self.slot_id}] {self.start_time:%a %d %b %Y, %H:%M}"
                f" - {self.end_time:%H:%M}")


class Appointment:
    def __init__(self, appointment_id, patient, doctor, slot):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.slot = slot
        self.appointment_date_time = slot.start_time
        self.status = None

    def book(self):
        self.status = AppointmentStatus.PENDING

    def accept(self):
        self.status = AppointmentStatus.ACCEPTED

    def decline(self):
        self.status = AppointmentStatus.DECLINED
        self.slot.release()  # declined slot becomes available again

    def is_upcoming(self):
        return (self.appointment_date_time > datetime.now()
                and self.status in (AppointmentStatus.PENDING,
                                    AppointmentStatus.ACCEPTED))

    def __str__(self):
        return (f"#{self.appointment_id} {self.slot.start_time:%a %d %b %H:%M}"
                f" | Dr. {self.doctor.name} | Patient: {self.patient.name}"
                f" | {self.status.value}")


class Doctor:
    def __init__(self, doctor_id, name, specialty):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty
        self.slots = []         # AvailabilitySlot defined by the doctor
        self.appointments = []  # Appointment handled by the doctor

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"

    def viewSchedule(self):
        return [a for a in self.appointments
                if a.status == AppointmentStatus.PENDING]

    def acceptAppointment(self, appointment):
        appointment.accept()

    def declineAppointment(self, appointment):
        appointment.decline()


class Patient:
    def __init__(self, patient_id, name, contact_info):
        self.patient_id = patient_id
        self.name = name
        self.contact_info = contact_info
        self.appointments = []

    def __str__(self):
        return self.name

    def viewAvailability(self, doctor):
        """R1: list the doctor's free days and times."""
        return [s for s in doctor.slots
                if s.checkAvailability() and s.start_time > datetime.now()]

    def getUpcomingAppointments(self):
        return [a for a in self.appointments if a.is_upcoming()]

    def bookAppointment(self, doctor, slot, next_id):
        """R2 + R4: returns (appointment or None, message)."""
        if len(self.getUpcomingAppointments()) >= MAX_UPCOMING:
            return None, (f"Booking rejected: you already have "
                          f"{MAX_UPCOMING} upcoming appointments.")
        if not slot.checkAvailability():
            return None, "Booking rejected: slot already taken. Choose another."
        appointment = Appointment(next_id, self, doctor, slot)
        appointment.book()   # status = PENDING
        slot.reserve()
        self.appointments.append(appointment)
        doctor.appointments.append(appointment)
        return appointment, "Request sent. Waiting for the doctor."


# ---------------------------------------------------------------- console UI
def seed_data():
    doctors = [Doctor(1, "Ahmed", "Cardiology"), Doctor(2, "Salma", "Dermatology")]
    base = datetime.now().replace(minute=0, second=0, microsecond=0)
    slot_id = 1
    for doc in doctors:
        for day in range(1, 4):
            for hour in (9, 10, 11):
                start = (base + timedelta(days=day)).replace(hour=hour)
                doc.slots.append(AvailabilitySlot(
                    slot_id, doc, start, start + timedelta(minutes=30)))
                slot_id += 1
    patients = [Patient(1, "Reem", "reem@mail.com"),
                Patient(2, "Mariam", "mariam@mail.com")]
    return doctors, patients


def choose(prompt, items):
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    raw = input(prompt).strip()
    if raw.isdigit() and 1 <= int(raw) <= len(items):
        return items[int(raw) - 1]
    print("Invalid choice.")
    return None


def patient_menu(patient, doctors, state):
    while True:
        print(f"\n--- Patient: {patient.name} ---")
        print("1. View doctor availability\n2. Book appointment\n"
              "3. My appointments\n0. Back")
        c = input("> ").strip()
        if c == "0":
            return
        if c in ("1", "2"):
            doc = choose("Select doctor: ",
                         doctors)
            if not doc:
                continue
            slots = patient.viewAvailability(doc)
            if not slots:
                print("No available slots.")
                continue
            print(f"\nAvailable slots for Dr. {doc.name}:")
            for s in slots:
                print(" ", s)
            if c == "2":
                raw = input("Enter slot id to book: ").strip()
                slot = next((s for s in doc.slots if str(s.slot_id) == raw), None)
                if not slot:
                    print("Invalid slot id.")
                    continue
                appt, msg = patient.bookAppointment(doc, slot, state["next_id"])
                if appt:
                    state["next_id"] += 1
                print(msg)
        elif c == "3":
            if not patient.appointments:
                print("No appointments yet.")
            for a in patient.appointments:
                print(" ", a)


def doctor_menu(doctor):
    while True:
        print(f"\n--- Doctor: Dr. {doctor.name} ---")
        pending = doctor.viewSchedule()
        if not pending:
            print("No pending requests.")
            return
        print("Pending requests (0 to go back):")
        for i, a in enumerate(pending, 1):
            print(f"  {i}. {a}")
        raw = input("Select request: ").strip()
        if raw == "0" or not raw.isdigit() or not 1 <= int(raw) <= len(pending):
            return
        appt = pending[int(raw) - 1]
        act = input("(a)ccept or (d)ecline? ").strip().lower()
        if act == "a":
            doctor.acceptAppointment(appt)
            print("Appointment accepted.")
        elif act == "d":
            doctor.declineAppointment(appt)
            print("Appointment declined.")


def main():
    doctors, patients = seed_data()
    state = {"next_id": 1}
    while True:
        print("\n=== Clinic Appointments ===")
        print("1. Patient\n2. Doctor\n0. Exit")
        c = input("> ").strip()
        if c == "0":
            print("Goodbye.")
            return
        if c == "1":
            p = choose("Select patient: ", patients)
            if p:
                patient_menu(p, doctors, state)
        elif c == "2":
            d = choose("Select doctor: ", doctors)
            if d:
                doctor_menu(d)


if __name__ == "__main__":
    main()
