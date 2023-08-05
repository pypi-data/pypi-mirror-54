# Social Auth PressPass

`Social Auth PressPass` provides backend and pipeline implementations for using [PressPass](https://presspass.it) with [Python Social Auth](https://github.com/python-social-auth/social-core). It is available on PyPI as `social-auth-presspass`, and the primary module import is `social_auth_presspass`.

When a user logs into your application with PressPass, you will receive a list of the organizations that allow the user to access your app on their behalf.

## General Installation

Regardless of your web framework (or lack thereof), there are a few key steps you need to take to start using Social Auth PressPass.

#### Create a PressPass app

Create a PressPass app using the developer dashboard. The name, price, and access controls are all up to you. Then, make sure of the following in the OpenID Connect section:

* **Response types** must include `Authorization Code Flow` (`code`), as this is how Social Auth PressPass with authenticate with PressPass itself.

* **Client type** must be set to `Public`. (No, this doesn't mean that anyone will be able to log in; it means that client authentication tokens are cryptographically signed by PressPass itself.)

* **Redirect URIs** must include both the development URL and production URL of your application login callback. If you installed Social Auth under the `auth/` path in Django, this might look like `http://localhost:8000/auth/complete/presspass/`. You can add additional paths on each line. Wildcards are not supported, so be exact!

#### Link your application

In your settings (in Django, this is your `settings.py` file), set `SOCIAL_AUTH_PRESSPASS_KEY` to your application's **client ID** from the PressPass developer dashboard.

> From here, you're ready to go! Now you can integrate the PressPass backend into your app just as you would any other Python Social Auth backend. That being said, this can sometimes be tricky, so we've included a Django quickstart below.

## Django Installation

1. Install `social-auth-presspass` and `django-social-auth` from PyPI, and follow all the instructions above (in <a href="#general-installation">General Installation</a>). You should also follow `django-social-auth`'s setup instructions, though you can augment them to fit your use case with the following steps.

2. Add the PressPass auth backend to your `SOCIAL_AUTH_AUTHENTICATION_BACKENDS` setting in `settings.py`. This will probably look like the following:

```python
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_auth_presspass.backends.PressPassBackend',
)
```

3. Add the PressPass backend as a Django Authentication Backend. To do this, change the following setting:

```python
AUTHENTICATION_BACKENDS = (
    'social_auth_presspass.backends.PressPassBackend',
    ...
)
```

If you still want to allow some users to log in with a username and password (or if you want to use the Admin Panel login system), be sure to keep Django's built-in `ModelBackend` in `AUTHENTICATION_BACKENDS`:

```python
AUTHENTICATION_BACKENDS = (
    'social_auth_presspass.backends.PressPassBackend',
    'django.contrib.auth.backends.ModelBackend',
)
```

4. If you want information about a user's organizations, add the PressPass pipelines to your social auth pipelines:

```python
SOCIAL_AUTH_PIPELINE = (
    ...
    'social_auth_presspass.pipelines.extract_organizations',
    'social_auth_presspass.pipelines.link_organizations_to_session',
    ...
)
```

Note that you should probably put these pipelines _after_ the `social_details`, `social_uid`, and `auth_allowed` built-in pipelines. Note also that you don't _need_ to include `link_organizations_to_session` unless you would like to access a user's PressPass organizations from inside their session without using their `user_information` (that is, if you're even keeping track of users).

## Backends

This package provides only one backend, `social_auth_presspass.backends.PressPassBackend`. It inherits from the Python Social Auth OpenID Connect backend, and can be used like any other social auth backend.

#### User Details

This backend provides the `presspass_organizations` user detail automatically, which is a list containing information about the organizations that the user is both 1) a member of and 2) has access to the app on behalf of. The key fields in each organization are `uuid` and `name`.

## Pipelines

This package provides one pipeline, `social_auth_presspass.pipelines.link_organizations_to_session`, which is intended to help apps leverage the PressPass authentication system _in lieu_ of their own. This pipeline creates two **session variables** for the PressPass-authenticated visitor:

* `presspass_authenticated`: `True` if the visitor has been authenticated with PressPass (we recommend you use this as `session.get('presspass_authenticated', False))`, as there is no guarantee that this value is defined and non-null.

* `presspass_organizations`: a list of organizations the visitor is authorized to access your app as a member of (each organization is a dict serialized from data returned from PressPass itself). If a visitor hasn't authenticated with PressPass, this value will not be set. All authenticated visitors will be a member of at least one organization (even if that organization is just an auto-generated personal one).

## Examples

For an example app that uses this package for authentication (in lieu of its own user-management system), check out [OpenAlerts](https://github.com/news-catalyst/openalerts).

## License

This package is licensed under the MIT License (see `LICENSE`).