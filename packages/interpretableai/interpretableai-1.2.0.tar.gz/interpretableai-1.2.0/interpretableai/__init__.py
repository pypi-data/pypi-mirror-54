import os


def install(runtime="julia", **kwargs):
    """Install Julia packages required for `interpretableai.iai`."""
    import julia
    os.environ['IAI_DISABLE_INIT'] = 'True'
    julia.install(julia=runtime, **kwargs)
    del os.environ['IAI_DISABLE_INIT']
