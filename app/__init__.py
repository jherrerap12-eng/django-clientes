import pymysql

pymysql.install_as_MySQLdb()

# XAMPP trae MariaDB 10.4 y Django 6 pide 10.11 o superior.
# Para poder trabajar en local se omite la verificación de versión y se
# desactiva INSERT ... RETURNING, que MariaDB solo soporta desde 10.5.
# Con MySQL 8 (PythonAnywhere) esto no cambia nada.
from django.db.backends.mysql.base import DatabaseWrapper  # noqa: E402
from django.db.backends.mysql.features import DatabaseFeatures  # noqa: E402

DatabaseWrapper.check_database_version_supported = lambda self: None
DatabaseFeatures.can_return_columns_from_insert = property(
    lambda self: self.connection.mysql_is_mariadb and self.connection.mysql_version >= (10, 5)
)
