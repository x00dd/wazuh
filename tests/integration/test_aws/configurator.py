# Copyright (C) 2015-2023, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

"""
    This file contain the Test Configurator class that will manage all resources and configurations for each test
    module.
"""
from os.path import join
from uuid import uuid4

# qa-integration-framework imports
from wazuh_testing.utils.configuration import (
    get_test_cases_data,
    load_configuration_template,
)
from wazuh_testing.logger import logger


# Local imports
from .utils import TEST_DATA_PATH, TEMPLATE_DIR, TEST_CASES_DIR


# Classes
class TestConfigurator:
    """
    TestConfigurator class is responsible for configuring test data and parameters for a specific test module.

    Attributes:
    - module (str): The name of the test module.
    - configuration_path (str): The path to the configuration directory for the test module.
    - test_cases_path (str): The path to the test cases directory for the test module.
    - metadata (list): Test metadata retrieved from the test cases.
    - parameters (list): Test parameters retrieved from the test cases.
    - cases_ids (list): Identifiers for the test cases.
    - test_configuration_template (list): The loaded configuration template for the test module.

    """

    def __init__(self):
        self.module = None
        self._metadata: list = []
        self._cases_ids: list = []
        self._test_configuration_template = None
        self._set_session_id()

    @property
    def module(self):
        return self.module

    @module.setter
    def module(self, test_module: str):
        self.module = test_module

    @property
    def metadata(self):
        return self._metadata

    @property
    def cases_ids(self):
        return self._cases_ids

    def _set_session_id(self) -> None:
        """Create and set the test session id."""
        self._session_id = str(uuid4())[:8]
        logger.info(f"This test session id is: {self._session_id}")

    def configure_test(self, configuration_file="", cases_file="") -> None:
        """
        Configure and manage the resources for the test.

        Params
        ------
        - configuration_file (str): The name of the configuration file.
        - cases_file (str): The name of the test cases file.
        """
        # Set test cases yaml path
        cases_yaml_path = join(TEST_DATA_PATH, TEST_CASES_DIR, self.module, cases_file)

        # Set test cases data
        parameters, self._metadata, self._cases_ids = get_test_cases_data(cases_yaml_path)

        # Modify original data to include session information
        self._modify_raw_data(parameters=parameters)

        # Set test configuration template for tests with config files
        self._load_configuration_template(configuration_file=configuration_file,
                                          parameters=parameters)

    def _load_configuration_template(self, configuration_file: str, parameters: str) -> None:
        """Set the configuration template of the test

        Params
        ------
        - configuration_file (str): The name of the configuration file.
        - parameters (str): The test parameters.

        """
        if configuration_file != "":
            # Set config path
            configuration_path = join(TEST_DATA_PATH, TEMPLATE_DIR, self.module, configuration_file)

            # load configuration template
            self._test_configuration_template = load_configuration_template(
                configuration_path,
                parameters,
                self._metadata
            )

    def _modify_raw_data(self, parameters: list) -> None:
        """Modify raw data to add test session information

        Params
        ------
        - parameters (list): The parameters of the test.
        - metadata (list): The metadata of the test.
        """
        # Add Suffix (_todelete) to alert a safe deletion of resource in case of errors.
        suffix = self._session_id + '_todelete'
        for param, data in zip(parameters, self._metadata):
            if param["RESOURCE_TYPE"] is "bucket":
                param["BUCKET_NAME"] += suffix
                data["bucket_name"] += suffix

            elif param["RESOURCE_TYPE"] is "log_stream":
                param["LOG_STREAM_NAME"] += suffix
                data["LOG_STREAM_NAME"] += suffix


# Instantiate configurator
configurator = TestConfigurator()
