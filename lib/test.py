def assert_status_with_message(status_code=200, response=None, message=None):
    """ Check to see if a message is contained within a response. """
    assert response.status_code == status_code
    assert message in str(response.data)
