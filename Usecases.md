
Use Cases

## Use Cases Table

| Use Case ID | Use Case Name | Actor | Requirement |
|---|---|---|---|
| UC1 | View Availability | Patient | R1 |
| UC2 | Book Appointment | Patient | R2, R4 |
| UC3 | Accept or Decline Appointment Request | Doctor | R3 |

## UC2 — Book Appointment

### Main Flow
1. The patient views the available appointment times.
2. The patient selects an available time slot.
3. The system checks whether the patient has fewer than 3 upcoming appointments.
4. The system checks whether the selected time slot is still available.
5. The system books the appointment.
6. The system confirms the booking to the patient.

### Alternative Flow
1. If the patient has already reached the maximum of 3 upcoming appointments, the system does not book the appointment and informs the patient.
2. If the selected time slot has already been taken, the system does not book the appointment and asks the patient to select another available time slot.
