# docker-crypt-server-saml
A Docker container for Crypt Server that uses SAML

You will almost certainly need to edit `settings.py` and provide your own metadata.xml file from your SAML provider.

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

## An example Docker run

Please note that this docker run is **incomplete**, but shows where to pass the `metadata.xml` and `settings.py`

```bash
docker run -d --name="crypt" \
-p 80:8000 \
-v /yourpath/metadata.xml:/home/docker/crypt/fvserver/metadata.xml \
-v /yourpath/settings.py:/home/docker/crypt/fvserver//settings.py \
--restart="always" \
macadmins/crypt-server-saml:2.2.0
```

## Notes on OneLogin
Your Onelogin `Configuration` should have the minimum settings
- `Recipient` Ex: https://crypt.example.com/saml2/acs/
- `ACS (Consumer) URL Validator` Ex: .*
- `ACS (Consumer) URL`Ex: https://crypt.example.com/saml/acs/

You will also need to configure your `Parameters` section with the custom iDP Fields/Values.
- Ensure these fields are passed in the SAML Assertion


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
    Allow this app to request other SSO URLs: **Unchecked**
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

# Help

For more information on what to put in your settings.py, look at https://github.com/knaperek/djangosaml2
