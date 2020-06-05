# docker-crypt-server-saml
A Docker container for Crypt Server that uses SAML

You will almost certainly need to edit `settings.py` and provide your own metadata.xml file from your SAML provider.

_The following instructions are provided as a best effort to help get started. They might require modifications to meet specific environments._

## settings.py changes you will certainly need to make
- `SAML_ATTRIBUTE_MAPPING` (These values come from OpenLDAP, Active Directory, etc)
- `SAML_CONFIG`
  - `entityid` Ex: https://crypt.example.com/saml2/metadata/
  - `assertion_consumer_service` Ex: https://crypt.example.com/saml2/acs/
  - `single_logout_service` Ex: https://crypt.example.com/saml2/ls/ and https://crypt.example.com/saml2/post
  - `required_attributes` - These should match the values from SAML_ATTRIBUTE_MAPPING
  - `idp`
    - `root url` Ex: https://app.onelogin.com/saml/metadata/1234567890
    - `single_sign_on_service` Ex: https://apps.onelogin.com/trust/saml2/http-post/sso/1234567890
    - `single_logout_service` Ex: https://apps.onelogin.com/trust/saml2/http-redirect/slo/1234567890

## Using groups in the SAML assertion to assign Crypt permissions
crypt-server-saml adds a Django signal callback to act on group membership information passed in a SAML assertion during login. If you can configure your IdP to add group information, you can use it to automate the addition and revocation of permissions.

To take advantage of this, edit the settings.py to include these preferences:
- `SAML_GROUPS_ATTRIBUTE`: Default (`memberOf`) The assertion dict's key for the group membership attribute.
- `SAML_ACTIVE_GROUPS`: Default `[]` (empty list) List of groups who should be considered active by Django's builtin auth system.
- `SAML_STAFF_GROUPS`: Default `[]` (empty list) List of groups who should be given "staff" permission. This grants access to the Django admin site. Staff-members are also granted the "active" attribute.
- `SAML_SUPERUSER_GROUPS` Default `[]` (empty list) List of groups who should be given superuser status. Superusers are also granted the "active" and "staff" attributes.

For example:
```
SAML_ACTIVE_GROUPS = ['cn=anonymous_henchmen,ou=memberOf,dc=lopan,dc=com', 'cn=cleaning_crew,ou=memberOf,dc=lopan,dc=com']
SAML_SUPERUSER_GROUPS` = ['cn=threestorms,ou=memberOf,dc=lopan,dc=com']
```

## An example Docker run

Please note that this docker run is **incomplete**, but shows where to pass the `metadata.xml` and `settings.py`

```bash
docker run -d --name="crypt" \
-p 80:8000 \
-v /yourpath/metadata.xml:/home/docker/crypt/fvserver/metadata.xml \
-v /yourpath/settings.py:/home/docker/crypt/fvserver/settings.py \
--restart="always" \
macadmins/crypt-server-saml:2.2.0
```

## Notes on OneLogin
1. In the OneLogin admin portal click on Apps > Add Apps.
1. Search for `SAML Test Connector (IdP)`. Click on this option.
1. Give the application a display name, upload a icon if you wish, and then click save.
1. Under "Configuration" tab, you will need at least the minimum settings shown below:
    * `Recipient`: https://crypt.example.com/saml2/acs/
    * `ACS (Consumer) URL Validator`: .*  (Note this is a period followed by an asterisk)
    * `ACS (Consumer) URL`: https://crypt.example.com/saml2/acs/
1. Under the "Parameters" tab, you will need to add the custom iDP Fields/Values. The process looks like:
    * Click "Add parameter"
      - `Field name`: FIELD_NAME
      - `Flags`: Check the Include in SAML assertion
    * Now click on the created field and set the appropriate FIELD_VALUE based on the table below.

    Repeat the above steps for all required fields:

    | **FIELD_NAME** | **FIELD_VALUE**   |
    |-----------|--------------|
    | urn:mace:dir:attribute-def:cn   | First Name      |
    | urn:mace:dir:attribute-def:sn   | Last Name       |
    | urn:mace:dir:attribute-def:mail | Email           |
    | urn:mace:dir:attribute-def:uid  | Email name part |

1. Under the "SSO" tab, download the "Issuer URL" metadata file. This will be mounted in your docker container [(see above)](#an-example-docker-run).
1. Under the "SSO" tab, you will find the "SAML 2.0 Endpoint" and "SLO Endpoint" which will go into the `settings.py` > `idp` section.
1. Lastly, "Save" the SAML Test Connector (IdP).


## Notes on Okta
Okta has a slightly different implementation and a few of the tools that this container uses, specifically [`pysaml2`](https://github.com/rohe/pysaml2) and [`djangosaml2`](https://github.com/knaperek/djangosaml2), do not like this implementation by default. Please follow the setup instructions, make sure to replace the example URL:
1. Create a new app from the admin portal

    Platform: Web
    Sign on method: SAML 2.0

1. Under "General Settings", give the app a name, add a logo and modify app visibility as desired.
1. Under "Configure SAML" enter the following (if no value is given after the colon leave it blank):

    #### General

    Single sign on URL: **https://crypt.example.com/saml2/acs/**
    Use this for Recipient URL and Destination URL: **Checked**
    Allow this app to request other SSO URLs: **Unchecked** (If this option is available)
    Audience URI (SP Entity ID): **https://crypt.example.com/saml2/metadata/**
    Default RelayState:
    Default RelayState: **Unspecified**
    Application username: **Okta username**

    #### Attribute Statements

    | **Name** | **Format** | **Value** |
    |-----------|-----------|-----------|
    | urn:mace:dir:attribute-def:cn   | Basic | ${user.firstName} |
    | urn:mace:dir:attribute-def:sn   | Basic | ${user.lastName}  |
    | urn:mace:dir:attribute-def:mail | Basic | ${user.email}     |
    | urn:mace:dir:attribute-def:uid  | Basic | ${user.login}     |

    #### Group Attribute Statements

    crypt does not support these at this time.

1. Under "Feedback":

    Are you a customer or partner? I'm an Okta customer adding an internal app
    App type: This is an internal app that we have created

Now that Okta is setup you will need to modify your settings.py to match. Note if you used the Attribute Statements above you should not have to modify the `SAML_ATTRIBUTE_MAPPING` variable. The metadata file can be downloaded from the Application's "Sign On" tab > Settings > SAML 2.0 > "Identity Provider metadata" link. The `idp` URLs are found under the "Sign On" > Settings > SAML 2.0 > "View Setup Instructions" button.

## Notes on Azure AD
1. Create a new Enterprise application. Choose "Non-gallery application"
1. Under "Single sign-on", choose SAML.
1. Set "Basic SAML Configuration" to:

    | **Name** | **Value** |
    |----------|-----------|
    | Identifier (Entity ID)                     | https://crypt.example.com/saml2/metadata/ |
    | Reply URL (Assertion Consumer Service URL) | https://crypt.example.com/saml2/acs/      |
    | Sign on URL                                | https://crypt.example.com/saml2/login/    |
    | Relay State                                | Optional                                  |
    | Logout Url                                 | https://crypt.example.com/saml2/ls        |

    Set the "Clain name" name identifier format to "Persistent".

1. Set "User Attributes & Claims" to:

    | **Claim name** | **Value** |
    |----------------|-----------|
    | urn:oid:2.5.4.42                  | user.givenname         |
    | urn:oid:0.9.2342.19200300.100.1.1 | user.userprincipalname |
    | urn:oid:2.5.4.4                   | user.surname           |
    | urn:oid:0.9.2342.19200300.100.1.3 | user.mail              |
    | Unique User Identifier            | user.userprincipalname |

1. Set the attribute mapping in settings.py to:

    ```
    SAML_ATTRIBUTE_MAPPING = {
        'uid': ('username', ),
        'mail': ('email', ),
        'givenName': ('first_name', ),
        'sn': ('last_name', ),
    }
    ```
 1. Set the id section in settings.py to:

    ```
           'idp': {
              'https://sts.windows.net/[tenantId]': {
                  'single_sign_on_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://login.microsoftonline.com/[tenantId]/saml2',
                      },
                  'single_logout_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://login.microsoftonline.com/[tenantId]/saml2',
                      },
                  },
              },
    ```

# Help

For more information on what to put in your settings.py, look at https://github.com/knaperek/djangosaml2
