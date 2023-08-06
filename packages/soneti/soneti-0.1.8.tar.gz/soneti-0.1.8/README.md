# Soneti Orchestrator

Orchestration of Soneti services (i.e. Senpy, GSICrawler, Scaner, etc.).
The orchestration is based on the luigi daemon, a set of custom luigi tasks, and some additional code to provide scheduling.

This repository contains:

* A python package with several custom luigi tasks for the main Soneti services. The package is also available through PyPI (`pip install soneti`).
* A base image with luigi and the scripts to schedule tasks.
* An **example orchestrator** in the `example` folder.
