"""Version information for the qsleeperfantasybot package.
This module provides the version of the bot, which can be used for logging or display purposes.
The version is determined from the package metadata or environment variables.
"""
try:
    import os
    from importlib.metadata import version as _version

    def get_version() -> str:
        """Get the version of the qsleeperfantasybot package.
        Returns:
            str: The version string, formatted as 'X.Y.Z' or 'X.Y.dev+<env>'."""
        base = _version("qsleeperfantasybot")
        env = os.getenv("QSFB_VERSION_SUFFIX")
        if env:
            return f"{base}.dev+{env}"
        return base

    __version__ = get_version()

except Exception:
    __version__ = "0.0.0"  # fallback
