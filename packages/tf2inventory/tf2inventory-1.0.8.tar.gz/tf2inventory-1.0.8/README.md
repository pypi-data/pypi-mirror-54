# Terraform 2 Ansible Inventory

## Usage
```
pip install tf2inventory
tf2inventory -i <inventory_path>
```

## Development
```
pip install --editable .
```

And then run the command as the usage part explains

## Deployment
1. Update the version number in the setup.py
2. 
```
pip install -U twine setuptools wheel
./setup.py sdist bdist_wheel
twine upload dist/*
```