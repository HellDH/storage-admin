def _get_change_message(obj):
    """Сообщение о изменении в человекочитаемом виде"""
    change_message = obj.get_change_message()
    
    print(change_message)

    if not change_message:
        return ''

    parts = []
    for entry in change_message:
        if len(entry) < 3:
            continue

        field, old_value, new_value = entry

        if old_value == new_value:
            continue

        if isinstance(old_value, str) and len(old_value) > 100:
            old_value = f"{old_value[:97]}"

        if isinstance(new_value, str) and len(new_value) > 100:
            new_value = f"{new_value[:97]}"

        parts.append(f'{field}: {old_value} -> {new_value}')

    return ', '.join(parts)

