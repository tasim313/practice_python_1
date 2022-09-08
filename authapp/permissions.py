from rest_framework import permissions


class ServiceProviderPermission(permissions.BasePermission):
    """
    Service Provider Permission Class.
    """

    def has_permission(self, request, view):

        if request.user.role == 3:
            return True
        else:
            return False


class CustomerPermission(permissions.BasePermission):
    """
    Customer Permission Class.
    """

    def has_permission(self, request, view):

        if request.user.role == 2:
            return True
        else:
            return False


class CustomerSupportPermission(permissions.BasePermission):
    """
    Customer Support Permission Class.
    """

    def has_permission(self, request, view):

        if request.user.role == 4:
            return True
        else:
            return False
