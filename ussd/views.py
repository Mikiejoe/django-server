from rest_framework.response import Response
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from django.core.mail import EmailMessage
import re

from ussd.stkpush import stkpush

from .models import Student, Fees, Transaction
from .serializers import StudentSerializer, FeeSerializer, TransactionSerializer
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


@api_view(["POST"])
def create_student(request):
    data = request.data
    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


def checkRegNo(regno):
    pattern = r'[A-Z][A-Z][A-Z]/[A-Z]/[0-9][0-9]-\d{5}/\d{4}'
    match = (re.match(pattern, regno))
    if match:
        return True
    else:
        return False


@api_view(['POST'])
def ussd_callback(request):
    session_id = request.POST.get('sessionId')
    service_code = request.POST.get('serviceCode')
    phone_number = request.POST.get('phoneNumber')
    text = request.POST.get('text')
    print(text)
    user_input = text.split("*")
    cpin = None
    response = ""

    if user_input[0] == '1' and len(user_input) > 2:
        pin = int(user_input[1])

    if len(user_input) > 2:
        users = Student.objects.get(phone=phone_number)
        cpin = users.pin

    if user_input[0] == "2" and len(user_input) == 2:
        regno = user_input[1]
        print(regno)
        match = checkRegNo(regno)
        if match:
            try:
                student = Student.objects.get(regno=regno)
                if student.pin is None:
                    response = "CON Enter your pin"
            except Exception:
                response = "END Student with that registration number does not exist!!"

        else:
            response = "END Not a valid registration number!!"

    if text == "":
        response = start()
    elif text == "1":
        response = login()
    elif text == "2":
        response = register()

    if len(user_input) == 2 and user_input[0] == '1':
        pin = int(user_input[1])
        user = Student.objects.get(phone=phone_number)

        if user.pin != None:
            if user.pin == pin:
                response = main_menu(phone_number)
            else:
                response = "END You have entered the wrong pin"
        else:
            response = "END You need to register"
    elif cpin:
        print(cpin == pin)
        if text == f"1*{cpin}*1":
            response = pay_fee()
        elif text == f"1*{cpin}*2":
            response = fee_statement()
        elif text == f"1*{cpin}*3":
            response = showbalance(phone_number)
        elif text == f"1*{cpin}*4":
            response = fee_structure()
        elif len(user_input) >= 4 and user_input[0] == '1':
            amount = (user_input[3])
            response = get_phone()
            if len(user_input) == 5:
                stkpush(user_input[-1], amount)
                # response = f"CON Phone {user_input[-1]} amount is {amount}"
                response = "END Your request is being processed. You will receive a request to enter pin shortly."

    return HttpResponse(response)


def start():
    response = "CON WELCOME TO FEEWIZ\n"
    response += "1. Login\n"
    response += "2. Register"
    return response


def login():
    """
    This is what is served to the user if he/she has a registered phne number
    Returns:
        _type_: str
    """
    response = "CON Welcome to FeeWiz\n"
    response += "Enter your pin"
    return response


def register():
    """
    Ifthe user is not registered he is served with this menu
    Returns:
        _type_: str
    """
    response = "CON Welcome to fee faster\n"
    response += "Enter your registration number to register"
    return response


def get_pin():
    response = "CON Enter your pin"
    return response


def main_menu(phone_number):
    """
    If the authentication is successful the user is served
    with this menu which is the main menu
    Returns:
        _type_: str
    """
    user = Student.objects.get(phone=phone_number)
    response = f"CON Hey {user.name} What would you like to do?\n"
    response += "1 Pay fees\n"
    response += "2. View fee statement\n"
    response += "3. View fee balance\n"
    response += "4. View fee structure\n"
    return response


def pay_fee():
    response = "CON Enter Amount to pay"
    return response


def get_phone():
    response = "CON Enter phone number to pay"
    return response


def send_message(reg_no):
    user = Student.objects.get(regno=reg_no)
    email = user.email
    pass


def getbalance(phone):
    user = Student.objects.get(phone=phone)
    balance = user.fee_balance
    return balance


def showbalance(phone):
    response = f"END Your balance is {getbalance(phone)}"
    return response


def fee_statement(regno):
    student = Student.objects.get(regno=regno)
    email = student.email
    sendemail(email)
    return "END your fee statement has been sent to your student email"


def fee_structure():
    return "END Your fee statement has been sent to your email"


def sendemail(email):
        """
    Send an email with the given email address.

    :param email: the email address to send the email to
    :return: None
    """
    email = EmailMessage()
    email.attach('fee_statement.pdf')
    email.send(to=[email])
    


def daraja_response(request):
    pass
