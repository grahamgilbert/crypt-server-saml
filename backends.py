from djangosaml2.backends import Saml2Backend

from django.conf import settings

ACTIVE_GROUPS = set(getattr(settings, "SAML_ACTIVE_GROUPS", []))
STAFF_GROUPS = set(getattr(settings, "SAML_STAFF_GROUPS", []))
SUPERUSER_GROUPS = set(getattr(settings, "SAML_SUPERUSER_GROUPS", []))
GROUPS_ATTRIBUTE = getattr(settings, "SAML_GROUPS_ATTRIBUTE", "memberOf")


class CustomAttributesBackend(Saml2Backend):
    def _update_user(
        self, user, attributes: dict, attribute_mapping: dict, force_save: bool = False
    ):
        """Update user's access level based on passed SAML attributes

        Args:
            user: The user object to update
            attributes: The SAML attributes dict found in the request
            attribute_mapping: The mapping of SAML attributes to Django user model attributes
            force_save: Whether to force save the user object

        Returns:
            The result of calling the superclass's `_update_user()` method with our updated values
        """
        assertion_groups = set(attributes.get(GROUPS_ATTRIBUTE, []))
        if SUPERUSER_GROUPS.intersection(assertion_groups):
            user.is_superuser = True
            user.is_staff = True

            force_save = True
        elif STAFF_GROUPS.intersection(assertion_groups):
            user.is_staff = True
            user.is_superuser = False

            force_save = True

        if (
            ACTIVE_GROUPS.union(STAFF_GROUPS)
            .union(SUPERUSER_GROUPS)
            .intersection(assertion_groups)
        ):
            # All of the groups referenced above should be active.
            user.is_active = True
            force_save = True

        return super()._update_user(user, attributes, attribute_mapping, force_save)
