# Tasks-0: Application Factory & Configuration

In this task, the project structure was updated to follow the **Application Factory Pattern** for better scalability and environment management.

## Key Changes

- **Dynamic Configuration**: Updated the `create_app()` function in `app/__init__.py` to accept a `config_class` parameter.

- **Config Loading**: Integrated `app.config.from_object(config_class)` to automatically load settings (like `DEBUG`, `SECRET_KEY`) from the `config.py` file.

- **Default Behavior**: Set `config.DevelopmentConfig` as the default setting to ensure the app runs in development mode by default.

- **Clean Startup**: Refactored `run.py` to use the factory instance, removing the need to manually pass `debug=True`.
