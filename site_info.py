import site

if site.ENABLE_USER_SITE:
    print(f"Install profall.py and profall.pth into either {site.getusersitepackages()} or any of {site.getsitepackages()}")
else:
    print(f"Install profall.py and profall.pth into any of {site.getsitepackages()}")