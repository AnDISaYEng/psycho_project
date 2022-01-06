from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from rest_framework import serializers


User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(max_length=30)
    password = serializers.CharField(min_length=6, required=True)
    password_confirmation = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким почтовым адрессом уже существует. Выберите другую '
                                              'почту')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self):
        attrs = self.validated_data
        user = User.objects.create_user(**attrs)
        code = user.generate_activation_code()
        user.send_activation_mail(user.email, code)
        return user


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6, required=True)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def activate(self):
        code = self.validated_data.get('code')
        user = User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password, request=request)
            if not user:
                raise serializers.ValidationError('Неверные почта или пароль')
        else:
            raise serializers.ValidationError('Почта и пароль обязательны')
        attrs['user'] = user
        return attrs



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6, required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirmation = serializers.CharField(min_length=6, required=True)

    def validate_old_password(self, old_password):
        if not User.objects.filter(password=old_password).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return old_password

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        code = user.generate_activation_code()
        message = f'Ваш код подтверждения: {code}'
        send_mail('Восстановление пароля', message, 'test@gmail.com', [email])


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6, required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirmation = serializers.CharField(min_length=6, required=True)

    def validate_code(self, code):
        if not User.objects.get(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        code = self.validated_data.get('code')
        password = self.validated_data.get('password')
        user = User.objects.filter(activation_code=code)
        user.set_password(password)
        user.activation_code = ''
        user.save()
