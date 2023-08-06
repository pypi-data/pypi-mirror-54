=====
Usage
=====

There are two different ways to use this module

* Using class Shipfunk:
    * Search pickup points
    * Create package cards and tracking codes
* Using class ShipfunkUser:
    * Handle user accounts

Using Shipfunk class
--------------------

.. code-block:: python

    from shipfunk_python.shipfunk import Shipfunk

    # create object
    shipfunk_client = Shipfunk('your_apikey', 'order_number')

    # Define parameters in dictionary
    params = {
        'postal_code': 30100,
        'country': 'fi',
        'products': [{
            "amount": 1,
            "code": "product123",
            "name": "Test product",
            "weight": {
                "amount": 1,
                "unit": "kg"
            },
            "dimensions": {
                "unit": "cm",
                "width": "25",
                "depth": "15",
                "height": "3"
            },
        }]
    }

    # Call method with parameters
    prices = shipfunk_client.get_price(params)

Using ShipfunkUser class
--------------------

.. code-block:: python

    from shipfunk_python.shipfunk import ShipfunkUser

    # create object
    shipfunk_client = ShipfunkUser('your_apikey')

    # Define parameters in dictionary
    params = {
        "user": {
            "email": email@email.email,
            "locale": "FI",
            "eshop_name": "Example Store",
            "business_id": "12312345",
            "customs_id": "6543210",
            "contact_person_name": "Test Tester",
            "contact_person_phone": "040 1231234",
            "contact_person_email": email@email.email,
            "web_address": "real_deal.example.com",
            "customer_contact_info": "<b>Contact us:</b> service@example.com"
        }
    }

    # Call method with parameters
    result = shipfunk_client.create_user(params)