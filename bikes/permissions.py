from rest_framework import permissions


class OwnsBike(permissions.BasePermission):

    def has_object_permission(self, request, view, bike):
        user = request.user
        try:
            if user.is_staff or user in bike.owners_set.all():
                return True
            else:
                return False
        except(AttributeError):
            return False
