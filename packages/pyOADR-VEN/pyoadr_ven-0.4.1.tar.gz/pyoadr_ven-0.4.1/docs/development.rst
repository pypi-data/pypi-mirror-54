Development
===========

The development of this VEN client is still in progress.

Test Driven Development
-----------------------
There are a number of tests written.

Tests should be written in a way where they don't need to contact an external VTN to run.
The ``test_responses.py`` tests use mocking and the ``responses`` package.

To run the test suite run:

.. code-block:: bash

    pytest

The tests are named in such a way to attempt to explain the specifications being tested.
To run the tests in a way they output a nice "rspec" style spec, run:

.. code-block:: bash

    pytest --spec

When writing tests, please use a similar style.


Testing with a local VTN server
-------------------------------

#. Start your VTN server
    * note the url it comes up on

#. Create a certificate authority called ``default``
    * save the CA certificate somewhere
#. Create a certificate
    * save the certificate and private key somewhere as a PEM bundle

.. code-block:: bash

    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqFiHgHccwrsrs
    ...
    lTwad+cbPVyQMzCsxEl7e7A=
    -----END PRIVATE KEY-----
    -----BEGIN CERTIFICATE-----
    MIIESzCCAzOgAwIBAgIRAOY4YtDbjUM4gek4QkBib6cwDQYJKoZIhvcNAQELBQAw
    ...
    -----END CERTIFICATE-----


#. Create a VEN on the VTN - you may need to create a Customer and Site to do this.
    * Note the VEN ID
    * Note the VTN ID used

#. Create a DRProgram on the VEN
    * Add your VEN/site to this program

#. Start a python or ipython shell
    * Import the pyoadr library
    * create an agent with the appropriate parameters

.. code-block:: python

    from pyoadr_ven import OpenADRVenAgent
    agent = OpenADRVenAgent(
            ven_id=AS_NOTED_ABOVE,
            vtn_id=AS_NOTED_ABOVE,
            vtn_address=AS_NOTED_ABOVE,
            client_pem_bundle=LOCATION_OF_SAVED_PEM_BUNDLE,
            vtn_ca_cert=LOCATION_OF_SAVED_CA_CERT
        )


Follow the instructions as on the Usage page.
