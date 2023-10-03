from django.contrib.messages import get_messages


def flash_message_test(response, expected_message):
    """
    Test whether message in the response.
    Test whether message corresponds to the expected message.
    """
    number_of_messages = 1
    current_message = get_messages(response.wsgi_request)
    assert len(current_message) == number_of_messages
    assert str(*current_message) == expected_message
