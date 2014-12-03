WealthManagementTool
====================

##Run the Server
- `cd WealthManagementTool/Django/metissoftware`
- `python manage.py runserver`
-  Navigate to localhost:8000 and have fun 

##HTML Templates
- Located in `WealthManagementTool/Django/metissoftware/wms/templates/wms/`
- base.html holds the style used in each webpage, other webpages simply inherit from it and override the content block
- The CSS/JS is located in `WealthManagementTool/Django/metissoftware/wms/static/wms` standard location for Django to search (logo.png is also in here)

##Database
- Current database is sqlite3 located at `WealthManagementTool/Django/metissoftware/db.sqlite3`

##Models
- `WealthManagementTool/Django/metissoftware/wms/models.py` holds the models
-  models take in data to store in the database 
-  abstract model 'User' is an abstract class which Client and FA inherit from (attributes they both share)

##Views
- Views 'link' the HTML to the python 
- Located in same directory as models.py
