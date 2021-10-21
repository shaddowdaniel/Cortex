# Reporter

A Cortex Responder for TheHive Project that creates a Markdown report for a given case.  This is a Work in Progress.

# Installation

See `requirements.txt` for dependencies.

# Configuration

Within the Responder configuration the following configuration is required:

| Item | Description | example |
|------|-------------|---------|
|tmp_file_location | a temporary path that is used to store the markdown file before it is attached to TheHive case then removed | `/opt/Cortex-Analyzers/github-aacgood/Responders/Reporter/tmp/` |
|thehive_instance | the instance of TheHive you are integrating with | `http://server:9000` |
|thehive_api | This is the API key from a user account that has been generated from TheHive | `random 32 character string`

# ToDo

- Automatically close the task that is generated for the report
- Include the Observable description (just has the tag)
