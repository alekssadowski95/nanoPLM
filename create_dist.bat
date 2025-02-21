@set mypath=%cd%

cd %mypath%

python -m PyInstaller run_local.py --icon "nanoplm/static/nanoplm-logo.ico" --add-data="nanoplm/templates/*:nanoplm/templates" --add-data="nanoplm/static/*:nanoplm/static" --add-data="nanoplm/static/bootstrap-5.3.3-dist/css/*:nanoplm/static/bootstrap-5.3.3-dist/css" --add-data="nanoplm/static/bootstrap-5.3.3-dist/js/*:nanoplm/static/bootstrap-5.3.3-dist/js" --add-data="nanoplm/static/bootstrap-icons-1.11.3/*:nanoplm/static/bootstrap-icons-1.11.3" --add-data="nanoplm/static/bootstrap-icons-1.11.3/font/*:nanoplm/static/bootstrap-icons-1.11.3/font" --add-data="nanoplm/static/bootstrap-icons-1.11.3/font/fonts/*:nanoplm/static/bootstrap-icons-1.11.3/font/fonts" --add-data="nanoplm/site.db:nanoplm" --add-data="LICENSE:." --splash nanoplm/static/nanoplm-splash.jpg --noconfirm --noconsole

@Pause