# Python-Sharepoint-API
Download, upload, delete and list SharePoint files

Easy to use.

Tested on Windows and Linux.

# Required libreries:
- django-environ
- Office365
- Office365-REST-Python-Client
- Shareplum
- Sharepoint


# Install

**Required Python3**

- `pip install django-environ`
- `pip install Office365`
- `pip install Office365-REST-Python-Client`
- `pip install Shareplum`
- `pip install Sharepoint`

**Edit Shareplum file `folder.py`**
- path in Debian: /var/local/lib/python3.x/dist-package/shareplum/folder.py
- path in Windows: C:\...\Python3x\lib\site-packages\shareplum\folder.py
- In `__init__` method change `timeout = 3` to `timeout = None`

# Set config file

In `.env` file add SharePoint identity.

**Example**
- sharepoint_email="sharepoint-user@example-domain.com
- sharepoint_password="SharepointUserPassword"
- sharepoint_url="https://**tenant**.sharepoint.com"
- sharepoint_url_site="https://<tenant>.sharepoint.com/sites/**site-name**"
- sharepoint_site_name="**site-name**"
- sharepoint_doc_library="Shared Folder/"
  
 # Upload
  
  `python3 upload.py "<path_to_file>" "<sharepoint_folder>"`
   
  For more detail use `upload.py help`.
  
  # Download
  
  `python3 download.py "<path_to_local_file>" "<sharepoint_path>" <option>`
  
  For more detail use `download.py help`.
  
  # Delete
  
  `python3 delete.py "<sharepoint_path>"`
  
  For more detail use `delete.py help`.
  
  # List
  
  `python3 list.py "<sharepoint_path>" <option>`
  
  For more detail use `list.py help`.
  
