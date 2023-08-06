# Google Sheets Connector
Connects Google sheets to a database to transfer information to and fro. [Fyle](https://www.fylehq.com/) is an expense management system.

## Installation

This project requires [Python 3+](https://www.python.org/downloads/).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

        $ pip install gsheets-db-connector

## Usage

This connector is very easy to use.

First you'll need to create a connection using the main class FyleSDK.
```python
from gsheets_db_connector import GoogleSheetsConnector

config = {
    'gsheets_credentials': '<Credentials>',
    'sheet_name': '<Sheet Name>'
}
gsheets_connector = GoogleSheetsConnector(config, database_connection)
```
After that you'll be able to extract/load data
```python
gsheets_connector.extract_data()
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
     * Run `chmod +x .git/hooks/pre-commit`
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
