def register_routes(api, app, root="api"):
    from app.short_link import register_routes as attach_event

    # Add routes
    attach_event(api, app)
