import site

if getattr(site, "ENABLE_USER_SITE", False):
    print(
        f"Install profall.py and profall.pth into either {site.getusersitepackages()} "
        f"or any of {site.getsitepackages()}"
    )
else:
    print(f"Install profall.py and profall.pth into any of {site.getsitepackages()}")
