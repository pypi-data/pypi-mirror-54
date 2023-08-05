# GDrive Python

![License](https://img.shields.io/pypi/l/pygdrive3fixed.svg?style=flat)
![PyPI](https://img.shields.io/pypi/v/pygdrive3fixed.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pygdrive3fixed.svg)

## Installing

```sh
$ pip install pygdrive3fixed
```

## Usage

```py
from pygdrive3fixed import service

drive_service = service.DriveService('./client_secret.json')
drive_service.auth()

folder = drive_service.create_folder('Xesque')
file = drive_service.upload_file('Arquivo Teste', './files/test.pdf', folder)
link = drive_service.anyone_permission(file)

folders = drive_service.list_folders_by_name('Xesque')
files = drive_service.list_files_by_name('Arquivo Teste')

files_from_folder = drive_service.list_files_from_folder_id(folder)
```

## by [Matheus Almeida](https://twitter.com/mat_almeida)

Use Google Drive API v3 with a python interface

# MIT License
