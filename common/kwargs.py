def background_thread(**kwargs):
    """Example of how to send server generated events to clients."""

    import remote
    remote.check_remote_log(handle_one_log, **kwargs)
