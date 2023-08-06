# Fyle Database Connector
Connects Fyle to a database to transfer information to and fro. [Fyle](https://www.fylehq.com/) is an expense management system.

## Installation

This project requires [Python 3+](https://www.python.org/downloads/).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

        $ pip install fyle-db-connector

## Usage

To use this connector you'll need these Fyle credentials used for OAuth2 authentication: **client ID**, **client secret** and **refresh token**.

This connector is very easy to use.
1. First you'll need to create a connection using the main class FyleSDK.
```python
from fyle_db_connector import FyleExtractConnector

config = {
    'fyle_base_url': '<YOUR BASE URL>',
    'fyle_client_id': '<YOUR CLIENT ID>',
    'fyle_client_secret': '<YOUR CLIENT SECRET>',
    'fyle_refresh_token': '<YOUR REFRESH TOKEN>' 
}

extract_connector = FyleExtractConnector(
    config, database_connector
)
```
2. After that you'll be able to extract data from fyle and store it in the db
```python
# Extract Expenses
extract_connector.extract_expenses()

#Extract Employees
extract_connector.extract_employees()
```

## Contribute

To contribute to this project follow the steps

* Fork and clone the repository.
* Run `pip install -r requirements.txt`
* Setup pylint precommit hook
    * Create a file `.git/hooks/pre-commit`
    * Copy and paste the following lines in the file - 
        ```bash
        #!/usr/bin/env bash 
        git-pylint-commit-hook
        ```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
