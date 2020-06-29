from django.dispatch import receiver

from djangosaml2.signals import pre_user_save

from django.conf import settings


ACTIVE_GROUPS = set(getattr(settings, 'SAML_ACTIVE_GROUPS', []))
STAFF_GROUPS = set(getattr(settings, 'SAML_STAFF_GROUPS', []))
SUPERUSER_GROUPS = set(getattr(settings, 'SAML_SUPERUSER_GROUPS', []))
GROUPS_ATTRIBUTE = getattr(settings, 'SAML_GROUPS_ATTRIBUTE', 'memberOf')


@receiver(pre_user_save)
def update_group_membership(
        sender, instance, attributes: dict, user_modified: bool, **kwargs) -> bool:
    """Update user's group membership based on passed SAML groups

    Args:
        sender: The class of the user that just logged in.
        instance: User instance
        attributes: SAML attributes dict.
        user_modified: Bool whether the user has been modified
        kwargs:
            signal: The signal instance

    Returns:
        Whether or not the user has been modified. This allows the user
        instance to be saved once at the conclusion of the auth process
        to keep the writes to a minimum.
    """
    assertion_groups = set(attributes.get(GROUPS_ATTRIBUTE, []))
    if SUPERUSER_GROUPS.intersection(assertion_groups):
        instance.is_superuser = True
        user_modified = True
    if STAFF_GROUPS.intersection(assertion_groups):
        instance.is_staff = True
        user_modified = True
    if ACTIVE_GROUPS.union(STAFF_GROUPS).union(SUPERUSER_GROUPS).intersection(assertion_groups):
        # All of the groups referenced above should be active.
        instance.is_active = True
        user_modified = True
    return user_modified
