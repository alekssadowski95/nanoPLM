@set mypath=%cd%

cd %mypath%

python -m PyInstaller run_local.py --icon "nanoplm/static/nanoplm-logo.png" --add-data="nanoplm/templates/*:nanoplm/templates" --add-data="nanoplm/static/*:nanoplm/static" --add-data="nanoplm/site.db:nanoplm/site.db" --add-data="LICENSE:." --splash nanoplm/static/nanoplm-splash.jpg --noconfirm

@Pause