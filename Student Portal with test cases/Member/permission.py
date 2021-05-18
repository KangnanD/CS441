from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import user_passes_test


def group_required(group_name):
    """
    Checks if a user is in the specified  group.
    """
    return user_passes_test(
        lambda u: u.groups.filter(name=group_name).count() != 0,
        login_url='/login?next=no_permission'
    )