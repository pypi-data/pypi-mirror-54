"""Test yarn registry replacement"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import os
from os.path import join as pjoin
import subprocess
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from jupyter_core import paths

from jupyterlab import commands

from .test_jupyterlab import AppHandlerTest


class TestAppHandlerRegistry(AppHandlerTest):

    def test_yarn_config(self):
        with patch("subprocess.check_output") as check_output:
            yarn_registry = "https://private.yarn/manager"
            check_output.return_value = b'\n'.join([
                b'{"type":"info","data":"yarn config"}',
                b'{"type":"inspect","data":{"registry":"' + bytes(yarn_registry, 'utf-8') + b'"}}',
                b'{"type":"info","data":"npm config"}',
                b'{"type":"inspect","data":{"registry":"' + bytes(yarn_registry, 'utf-8') + b'"}}'
            ])
            logger = logging.getLogger('jupyterlab')
            config = commands._yarn_config(logger)
            
            self.assertDictEqual(config, 
                {"yarn config": {"registry": yarn_registry}, 
                "npm config": {"registry": yarn_registry}}
            )

    def test_yarn_config_failure(self):
        with patch("subprocess.check_output") as check_output:
            check_output.side_effect = subprocess.CalledProcessError(1, ['yarn', 'config', 'list'], stderr=b"yarn config failed.")

            logger = logging.getLogger('jupyterlab')
            config = commands._yarn_config(logger)
            
            self.assertDictEqual(config, 
                {"yarn config": {}, 
                "npm config": {}}
            )

    def test_get_registry(self):
        with patch("subprocess.check_output") as check_output:
            yarn_registry = "https://private.yarn/manager"
            check_output.return_value = b'\n'.join([
                b'{"type":"info","data":"yarn config"}',
                b'{"type":"inspect","data":{"registry":"' + bytes(yarn_registry, 'utf-8') + b'"}}',
                b'{"type":"info","data":"npm config"}',
                b'{"type":"inspect","data":{"registry":"' + bytes(yarn_registry, 'utf-8') + b'"}}'
            ])
            
            handler = commands.AppOptions()

            self.assertEqual(handler.registry, yarn_registry)

    def test_populate_staging(self):
        with patch("subprocess.check_output") as check_output:
            yarn_registry = "https://private.yarn/manager"
            check_output.return_value = b'\n'.join([
                b'{"type":"info","data":"yarn config"}',
                b'{"type":"inspect","data":{"registry":"' + bytes(yarn_registry, 'utf-8') + b'"}}',
                b'{"type":"info","data":"npm config"}',
                b'{"type":"inspect","data":{"registry":"' + bytes(yarn_registry, 'utf-8') + b'"}}'
            ])

            staging = pjoin(self.app_dir, 'staging')
            handler = commands._AppHandler(commands.AppOptions())
            handler._populate_staging()

            lock_path = pjoin(staging, 'yarn.lock')
            with open(lock_path) as f:
                lock = f.read()

            self.assertNotIn(commands.YARN_DEFAULT_REGISTRY, lock)
            self.assertIn(yarn_registry, lock)
