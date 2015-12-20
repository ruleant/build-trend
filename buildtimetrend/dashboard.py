# vim: set expandtab sw=4 ts=4:
"""
Dashboard related functions.

Copyright (C) 2014-2015 Dieter Adriaenssens <ruleant@users.sourceforge.net>

This file is part of buildtimetrend/python-lib
<https://github.com/buildtimetrend/python-lib/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import division
from builtins import str
from buildtimetrend import keenio
from buildtimetrend import logger
from buildtimetrend.settings import Settings
from buildtimetrend.tools import check_file
from buildtimetrend.tools import check_dict


def get_dashboard_config_dict(repo, extra=None):
    """
    Generate the configuration settings for the dashboard.

    The dashboard is Javascript powered HTML file that contains the
    graphs generated by Keen.io.

    Parameters:
    - repo : repo name (fe. buildtimetrend/service)
    - extra : dictionary of extra config settings, format : {"name" : "value"}
    """
    # initialise config settings dictionaries
    config = {}

    # add repo and project name
    if repo is not None and not repo == "":
        # merge extra settings into existing config dictionary
        config.update({
            'projectName': str(repo),
            'repoName': str(repo)
        })

    # add extra config parameters
    if extra is not None and check_dict(extra, "extra"):
        config.update(extra)

    return config


def get_dashboard_config(repo, extra=None):
    """
    Generate the configuration settings for the dashboard.

    The dashboard is Javascript powered HTML file that contains the
    graphs generated by Keen.io.

    Parameters:
    - repo : repo name (fe. buildtimetrend/service)
    - extra : dictionary of extra config settings, format : {"name" : "value"}
    """
    # initialise config settings dictionaries
    config = get_dashboard_config_dict(repo, extra)
    keen_config = keenio.get_dashboard_keen_config(repo)

    # create configuration as a string
    return "var config = {};\nvar keenConfig = {};".format(config, keen_config)


def generate_dashboard_config_file(repo):
    """
    Generate the configuration file for the dashboard.

    The dashboard is Javascript powered HTML file that contains the
    graphs generated by Keen.io.

    Parameters:
    - repo : repo name (fe. buildtimetrend/service)
    """
    # get config settings
    config_string = get_dashboard_config(repo)

    # write config file
    config_file = Settings().get_setting("dashboard_configfile")
    with open(config_file, 'w') as outfile:
        outfile.write(config_string)

    if check_file(config_file):
        logger.info("Created trends dashboard config file %s", config_file)
        return True
    else:
        logger.warning("The dashboard config file was not created")
        return False
