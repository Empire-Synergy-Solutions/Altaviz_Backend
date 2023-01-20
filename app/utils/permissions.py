from users.models.administrator import Administrator
from users.models.moderator import Moderator
from users.models.customers import Customers
from users.models.managers import Managers
from users.models.vendors import Vendors
from users.models.attendants import Attendants

def is_administrator(user):
    """
    Return true if user is administrator
    """

    if Administrator.objects.filter(user=user):
        return True
    return False


def is_moderator(user):
    """
    Return true if user is moderator or higher
    """

    if Moderator.objects.filter(user=user):
        return True
    return is_administrator(user)

def is_customers(user):
    """
    Return true if user is a customer or higher
    """

    if Customers.objects.filter(user=user):
        return True
    return is_administrator(user)

def is_managers(user):
    """
    Return true if user is a manager or higher
    """

    if Managers.objects.filter(user=user):
        return True
    return is_administrator(user)

def is_vendors(user):
    """
    Return true if user is a vendor or higher
    """

    if Vendors.objects.filter(user=user):
        return True
    return is_administrator(user)

def is_attendants(user):
    """
    Return true if user is an Attendant or higher
    """

    if Attendants.objects.filter(user=user):
        return True
    return is_administrator(user)
