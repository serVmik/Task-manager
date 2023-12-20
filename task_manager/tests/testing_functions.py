from django.contrib.messages import get_messages


def flash_message_test(response, expected_message, number_of_messages=1):
    """Test flash message in the response.

    Raises AssertionError if the number of messages and the message text in the
    response not correspond to the specified in function parameters.

    Parameters
    ----------
    response : `HttpResponse`
        Contains a message text (`str`) for the user.
    expected_message : `str`
        The message text which must be sent to user in response.
    number_of_messages : `int`, optional
        The number of messages which must be sent to user in response
        (default 1).

    Raises
    -------
    AssertionError:
        Raised if the message text in the response not correspond with
        expected_message.
    AssertionError:
        Raised if the number of messages in the response not correspond with
        number_of_messages.
    """
    # Get message from response.
    current_message = get_messages(response.wsgi_request)
    # Comparison number of messages.
    assert len(current_message) == number_of_messages
    # Comparison of message contents.
    assert str(*current_message) == expected_message
