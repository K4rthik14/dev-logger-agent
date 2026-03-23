[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "dev-logger"
version = "0.1.0"
dependencies = []

[tool.setuptools.packages.find]
include = ["dev_logger*"]

[tool.setuptools.py-modules]
modules = ["main"]

[project.scripts]
dev-log = "main:app"