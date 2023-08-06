

# Mock Base

`support for python >3.5`

> the philosophy of this package is to have no dependencies and to do everything with the standard library

Mock base is an implementation with utils for mocktest
of the google `firebase-admin-python` package.

is useful for creating Mock for Firebase admin fake tests and verifying proper functioning of cloud-functions in python

---

#### install it

normal installation:

```bash
pip3 install mock_base
```

installation in a folder:

```bash
pip3 install --no-dependencies --upgrade -t lib git+https://github.com/SpinaNico/python-mock-base.git@master
```

# Structure

* **mock_base**
    * **mock_messaging**
      a fake messaging implementation notifies the fake devices
    * **mock_store**
      This is a firestore implementation, you can create collections generate queries, even create sub-collections all with the same identical API as the signatures.
    * **mock_storage**
      *not yet implemented*
    * **mock_auth**
      It helps you verify a user of a specific app, to generate fake_token you need to use a fake_device.
    * **fake_device**
      Fake devices help you manage notifications and authentication, you can create fake devices with a specific UID and then generate fake tokens and fake device tokens, which you can check to see if they are correct through mock_auth
    