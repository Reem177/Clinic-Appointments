# Clinic Appointments — Candidate Classes

| Class | Evidence | Classification |
|---|---|---|
| Patient | R1 and R2,UC1 (View Availability) and UC2 (Book Appointment). The patient views available times and books appointments. | Explicit |
| Doctor | R3, UC3(Accept or Decline Appointment Request). The doctor responds to appointment requests. | Explicit |
| Appointment | R2, R3,and R4, UC2 and UC3, The system needs to represent bookings, appointment times, and decisions on appointment requests. | Inferred |
| AvailabilitySlot | R1 and R2, UC1 and UC2, The system needs to represent available days and times and check whether a selected slot is still available. | Inferred |
| AppointmentStatus | R3, UC3. Accepted and Declined represent the outcome of a doctor's decision. These values can be represented as an attribute or enumeration within Appointment, so a separate domain class is not essential. | Rejected |
| MedicalRecord | R5, The requirement refers to patient medical data that must be accessible only to authorized staff. A separate class can represent this data. | Inferred |
| Staff | R5, The requirement identifies authorized staff as the people permitted to access patient medical data. | Inferred |
| AvailabilityDisplay | R6, Displaying available times within two seconds is a performance requirement, not a domain entity. | Rejected |
| MobileScreen | R7, Mobile compatibility is a user-interface concern, not a domain entity. | Rejected |


