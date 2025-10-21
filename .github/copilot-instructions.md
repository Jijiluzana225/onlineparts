This repository is a Django 5.1 application for an online spare-parts marketplace. The goal of this file is to give AI coding agents focused, actionable context so they can make safe, correct edits quickly.

Key facts (read before editing):
- Project root: the Django project package is `Onlinespareparts` and the main app is `orders`.
- Custom user model: `orders.models.Customer` is used (see `Onlinespareparts/settings.py` -> `AUTH_USER_MODEL`). Any auth-related changes must import or reference this model.
- Storage: media files (part and bid images) are stored via Cloudinary. Configuration lives in `Onlinespareparts/settings.py` and forms/models use `cloudinary_storage.storage.MediaCloudinaryStorage()` for ImageFields. Don't hardcode local MEDIA paths.
- Static files: Whitenoise is used for static serving in production. `STATICFILES_DIRS` and `STATIC_ROOT` are configured in `settings.py`.
- Database: default shown is PostgreSQL (settings include credentials likely intended for a hosted env). Development may use `db.sqlite3` present in the repo. Be careful not to leak secrets when committing.

Architecture and flows:
- Entry points: `manage.py` for local tasks; Procfile uses `gunicorn Onlinespareparts.wsgi` for production.
- URL routing: main urls are in `Onlinespareparts/urls.py` which includes `orders.urls`. Most views and templates live under the `orders` app.
- Core models: `PartRequest` and `Bid` are the domain models. `PartRequest` owns images and has a related_name `bids` for Bid objects. Many views rely on `prefetch_related('bids')` in list views (see `views.MyPartRequestsView`).
- Auth & roles: `Customer.is_store` boolean distinguishes store accounts from regular customers. Many views require login via `@login_required` and `LoginView`/`LogoutView` are used with templates under `orders/templates/orders/`.

Conventions and patterns to follow when editing:
- Use the custom user model via `get_user_model()` or `settings.AUTH_USER_MODEL` rather than importing django.contrib.auth.models.User.
- Media uploads: ImageField definitions and forms use Cloudinary storage explicitly; preserve `storage=MediaCloudinaryStorage()` on model ImageFields unless intentionally switching storage.
- Views: prefer small function-based views consistent with existing style. Class-based generic views are used for Bid detail/update/delete; follow the same template naming and reverse URL names.
- Templates: templates are under `orders/templates/orders/`. Use existing template names when returning views (e.g., `orders/part_request_detail.html`). Template tags follow standard Django templating.
- URLs: add named routes in `orders/urls.py` and reference them with `{% url 'name' %}` in templates.

Developer workflows and commands:
- Local dev: use the project's virtual environment with the packages in `requirements.txt`. Common commands:
  - Install dependencies: pip install -r requirements.txt
  - Run locally: `python manage.py runserver` (or use `py manage.py runserver` on Windows/Powershell)
  - Migrations: `python manage.py makemigrations` and `python manage.py migrate`
  - Create superuser: `python manage.py createsuperuser`
  - Collect static for production: `python manage.py collectstatic` (whitenoise expects collected static files)
- Tests: there are no explicit test files beyond `orders/tests.py` placeholder — run `python manage.py test` to execute tests.
- Production: Procfile + gunicorn are configured. Do not attempt to run `gunicorn` on Windows without a proper WSL/Unix environment.

Safety and secrets:
- The repository already contains Cloudinary API keys and a Postgres password in `settings.py`. Treat these as secrets: avoid echoing or moving them into public commits. If you add code that reads secrets, prefer using environment variables (`os.environ`) and document the expected env var names.

Where to look for examples (most important files):
- `Onlinespareparts/settings.py` — static, media, database, AUTH_USER_MODEL, Cloudinary
- `orders/models.py` — Customer, PartRequest, Bid models (image fields configured for Cloudinary)
- `orders/forms.py` — model forms for PartRequest and Bid show how file inputs are handled
- `orders/views.py` — canonical view patterns (mix of function views and class-based generic views)
- `orders/urls.py` — named routes used across templates
- `Procfile` and `requirements.txt` — production runtime hints

If you change behavior that affects data shape (models or form fields):
- Add a migration via `makemigrations` and keep migrations in `orders/migrations/`.
- Update any templates that render or post the changed fields (search for template filenames in `orders/templates/orders/`).

Edge cases found in the codebase to watch for:
- Some ImageFields are required in forms/models; changing them can break uploads and views that assume images exist.
- `PartRequest.qty` is a PositiveIntegerField with default string "1" — prefer numeric defaults when adjusting models.

When in doubt, update small, test, and run `python manage.py runserver` locally. If a change may affect deployment (static/media/config), include a short note in the commit message explaining the change and any required env vars.

If any part of this document is unclear, tell me which area (auth, storage, URLs, templates, deployment) and I will expand with concrete examples.
