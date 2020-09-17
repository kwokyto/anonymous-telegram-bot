## THIS IS ANONYMOUS HANDLER

import json
import telegram
import os
import logging

from dynamo_call import *

# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}


def configure_telegram():
    """
    Configures the bot with a Telegram Token.

    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)

def webhook(event, context):
    """
    Runs the Telegram webhook.
    """

    bot = configure_telegram()
    logger.info('Event: {}'.format(event))

    if event.get('httpMethod') == 'POST' and event.get('body'): 
        logger.info('Message received')
        update = telegram.Update.de_json(json.loads(event.get('body')), bot)
        chat_id = update.message.chat.id
        text = update.message.text

        lst = get_response(text, chat_id)
        for dic in lst:
            chat_id = dic["receiver_id"]
            text = dic["message"]
            bot.sendMessage(chat_id=chat_id, text=text)
        #bot.sendMessage(chat_id=chat_id, text="hello there")
        logger.info('Message sent')

        return OK_RESPONSE

    return ERROR_RESPONSE

def set_webhook(event, context):
    """
    Sets the Telegram bot webhook.
    """

    logger.info('Event: {}'.format(event))
    bot = configure_telegram()
    url = 'https://{}/{}/'.format(
        event.get('headers').get('Host'),
        event.get('requestContext').get('stage'),
    )
    webhook = bot.set_webhook(url)

    if webhook:
        return OK_RESPONSE

    return ERROR_RESPONSE

def get_response(text, chat_id):
    """
    Process a message from Telegram
    """

    # Command Responses
    unregistered_message = \
        "You are not yet registered, please contact Love, USP for further details."
    already_registered_message = \
        "You are already registered!"
    to_register_message = \
        "To register, please use the following format:\n/register <matric number> <password>"
    registration_success_message = \
        "Registration success! Your username is "
    registration_failed_message = \
        "Registration failed, please try again or contact Love, USP."
    wrong_password_message = \
        "Wrong password! Please try again."
    start_message = \
        "Welcome to Love, USP anonymous group chat! Enter /register to register."
    invalid_command_message = \
        "Invalid command."
    non_text_message = \
        "Non-text detected. Sorry, we still do not support non-text messages."
    delete_success_message = \
        "User deleted successfully"
    delete_error_message = \
        "Error in deleting user, please contact admin."

    # Setting main objects
    first_response = {"message": unregistered_message, "receiver_id": chat_id}
    responses_list = [first_response] # to be returned

    # Validity checking
    if text == None:
        first_response["message"] = non_text_message
        return responses_list # COMPLETED AND WORKS

    # Command Handlers
    if text == "/start":
        first_response["message"] = start_message
        return responses_list # COMPLETED AND WORKS

    if text[:9] == "/register":
        # check if user is already registered
        if is_registered(chat_id):
            first_response["message"] = already_registered_message
            return responses_list
        
        # if user just puts /register
        if text == "/register":
            first_response["message"] = to_register_message
            return responses_list

        # if user is not registered
        matric_number = text[10:19]
        hash = text[20:]

        # if password is wrong
        # use https://www.md5hashgenerator.com/
        if not check_password(matric_number, hash):
            first_response["message"] = wrong_password_message
            return responses_list

        #if password is correct
        if add_id(chat_id, matric_number):
            first_response["message"] = registration_success_message + get_username(chat_id) + "."
        else:
            first_response["message"] = registration_failed_message
        return responses_list # COMPLETED AND WORKS
    
    # if user is not registered, do NOT continue
    # check if user is already registered
    if not is_registered(chat_id):
        first_response["message"] = unregistered_message
        return responses_list # COMPLETED AND WORKS

    if text == "/username":
        first_response["message"] = "Your username is: " + get_username(chat_id)
        return responses_list # COMPLETED AND WORKS

    if text[0:6] == "/leave":
        matric_number = text[7:]
        success = delete_user(matric_number)
        if success:
            first_response["message"] = "You have left the chat."
        else:
            first_response["message"] = "Command to leave failed. Remember to use /leave <matric number>"
        return responses_list # COMPLETED AND WORKS

    if text[:7] == "/delete":
        matric_number = text[8:17]
        password = text[18:]
        if password != "IAMTHELOVEUSPADMIN":
            first_response["message"] = delete_error_message
            return responses_list
        if delete_user(matric_number):
            first_response["message"] = delete_success_message
        else:
            first_response["message"] = delete_error_message
        return responses_list # COMPLETED AND WORKS


    if text[0] == "/":
        first_response["message"] = invalid_command_message
        return responses_list # COMPLETED AND WORKS

    responses_list = get_responses_list(chat_id, text)
    return responses_list # COMPLETED AND WORKS