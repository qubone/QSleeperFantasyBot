try:
    import os
    from importlib.metadata import version as _version

    def get_version() -> str:
        base = _version("qsleeperfantasybot")
        env = os.getenv("QSFB_VERSION_SUFFIX")
        if env:
            return f"{base}.dev+{env}"
        return base

    __version__ = get_version()

except Exception:
    __version__ = "0.0.0"  # fallback
