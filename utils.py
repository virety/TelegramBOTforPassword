def calculate_password_reliability(password):
    common_passwords = ['123456', 'password', 'qwerty', '123456789', '12345678']
    if len(password) < 12:
        return "Ненадежный - используйте как минимум 12 символов"
    elif password.lower() in common_passwords:
        return "Ненадежный - избегайте распространенных паролей"
    elif password.isalpha() or password.isdigit() or password.islower() or password.isupper():
        return "Ненадежный - используйте буквы разных регистров, цифры и специальные символы"
    else:
        return "Надежный"
       