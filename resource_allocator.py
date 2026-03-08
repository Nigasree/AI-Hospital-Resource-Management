def allocate_resources(predicted_patients, available_resources):

    beds_available = available_resources["beds"]
    icu_available = available_resources["icu"]
    ventilators_available = available_resources["ventilators"]

    extra_beds_needed = max(0, predicted_patients - beds_available)

    icu_needed = predicted_patients * 0.1
    extra_icu_needed = max(0, int(icu_needed - icu_available))

    ventilator_needed = predicted_patients * 0.05
    extra_ventilators = max(0, int(ventilator_needed - ventilators_available))

    return {
        "extra_beds": extra_beds_needed,
        "extra_icu": extra_icu_needed,
        "extra_ventilators": extra_ventilators
    }