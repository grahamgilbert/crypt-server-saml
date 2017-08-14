# docker-crypt-server-saml
A Docker container for Crypt Server that uses SAML

You will almost certainly need to edit `settings.py` and provide your own metadata.xml file from your SAML provider.

### settings.py changes you will certainly need to make
- `SAML_ATTRIBUTE_MAPPING` (These values come from OpenLDAP, Active Directory, etc)
- `SAML_CONFIG`
  - `entityid` Ex: https://crypt.domain.tld/saml2/metadata/
  - `assertion_consumer_service` Ex: https://crypt.domain.tld/saml2/acs/
  - `single_logout_service` Ex: https://crypt.domain.tld/saml2/ls/ and https://crypt.domain.tld/saml2/post
  - `required_attributes` - These should match the values from SAML_ATTRIBUTE_MAPPING
  - `idp`
    - `root url` Ex: https://app.onelogin.com/saml/metadata/1234567890
    - `single_sign_on_service` Ex: https://apps.onelogin.com/trust/saml2/http-post/sso/1234567890
    - `single_logout_service` Ex: https://apps.onelogin.com/trust/saml2/http-redirect/slo/1234567890

### An example Docker run

Please note that this docker run is **incomplete**, but shows where to pass the `metadata.xml` and `settings.py`

```bash
docker run -d --name="crypt" \
-p 80:8000 \
-v /yourpath/metadata.xml:/home/docker/crypt/fvserver/metadata.xml \
-v /yourpath/settings.py:/home/docker/crypt/fvserver//settings.py \
--restart="always" \
macadmins/crypt-server-saml:2.2.0
```

### Notes on OneLogin
Your Onelogin `Configuration` should have the minimum settings
- `Recipient` Ex: https://crypt.domain.tld/saml2/acs/
- `ACS (Consumer) URL Validator` Ex: .*
- `ACS (Consumer) URL`Ex: https://crypt.domain.tld/saml/acs/

You will also need to configure your `Parameters` section with the custom iDP Fields/Values.
- Ensure these fields are passed in the SAML Assertion

For more information on what to put in your settings.py, look at https://github.com/knaperek/djangosaml2
