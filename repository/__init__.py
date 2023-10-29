"""
Repositories are responsible for data access and storage.
They provide a clean and consistent API for the rest
of the application to interact with data.

They hide the implementation details of how data is stored and retrieved.
This means the core application code for example use_cases
doesn't need to know if the data is coming from a database,
a web service, or some other source.

The repository layer implements the interfaces defined in the interface layer.
"""
