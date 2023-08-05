======
PyRAII
======

.. image:: https://img.shields.io/travis/sasha-tkachev/pyraii.svg
        :target: https://travis-ci.org/sasha-tkachev/pyraii

Declerative resource management library for python (Under construction)


Examples
--------


Closing Resources only on exception::


    from pyraii.context import closing_on_exception

    def wait_for_authenticated_client_connection():
        my_socket = wait_for_client_connection(*args)
        with closing_on_exception(my_socket):
            username = authenticate_connection(my_socket)
            return my_socket, username


Nothrow closing::


    from pyraii.context import closing_nothrow

    # If the file fails to close no exception will be thrown
    with closing_nothrow(my_file):
        my_file.write(data)

Resource owning classes::


    from pyraii.resource_owner import ResourceOwner

    class Server(ResourceOwner):
        def __init__():
            self.socket_a = get_socket()
            self.socket_b = get_other_socket()
            self._log_file = open_log_file()
            self._data = "asdasd"
    my_server = Server()
    my_server.close() # will close all sockets and files which are members of the server


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.


* Free software: MIT license

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
