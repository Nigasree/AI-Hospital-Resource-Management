def schedule_staff(predicted_patients, current_staff):

    doctors = current_staff["doctors"]
    nurses = current_staff["nurses"]

    patients_per_doctor = 10
    patients_per_nurse = 5

    required_doctors = predicted_patients // patients_per_doctor
    required_nurses = predicted_patients // patients_per_nurse

    extra_doctors = max(0, required_doctors - doctors)
    extra_nurses = max(0, required_nurses - nurses)

    return {
        "required_doctors": required_doctors,
        "extra_doctors": extra_doctors,
        "required_nurses": required_nurses,
        "extra_nurses": extra_nurses
    }