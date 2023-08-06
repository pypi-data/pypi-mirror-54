# Copyright (c) 2019 Microsoft Corporation
# Distributed under the MIT software license

import sys
import logging
from ..provider.visualize import AutoVisualizeProvider, PreserveProvider

log = logging.getLogger(__name__)

this = sys.modules[__name__]
this.app_runner = None
this.app_addr = None

this._preserve_provider = None
this.visualize_provider = None


def get_visualize_provider():
    return this.visualize_provider


def set_visualize_provider(provider):
    has_render_method = hasattr(provider, "render")
    if provider is None or has_render_method:
        this.visualize_provider = provider
    else:  # pragma: no cover
        raise ValueError(
            "Object of type {} is not a visualize provider.".format(type(provider))
        )


def set_show_addr(addr):
    """ Set a (ip, port) for inline visualizations and dashboard. Has side effects stated below.
    Side effect: restarts the app runner for 'show' method.

    Args:
        addr: (ip, port) tuple as address to assign show method to.
    Returns:
        None.
    """
    addr = (addr[0], int(addr[1]))
    init_show_server(addr)


def get_show_addr():
    """ Returns (ip, port) used for show method.

    Returns:
        Address tuple (ip, port).
    """
    return this.app_addr


def shutdown_show_server():
    """ This is a hard shutdown method for the show method's backing server.

    Returns:
        True if show server has stopped.
    """
    if this.app_runner is not None:
        return this.app_runner.stop()

    return True  # pragma: no cover


def status_show_server():
    """ Returns status and associated information of show method's backing server.

    Returns:
        Status and associated information as a dictionary.
    """
    status_dict = {}

    if this.app_runner is not None:
        status_dict["app_runner_exists"] = True
        status_dict.update(this.app_runner.status())
    else:
        status_dict["app_runner_exists"] = False

    return status_dict


def init_show_server(addr=None, base_url=None, use_relative_links=False):
    """ Initializes show method's backing server.

    Args:
        addr: (ip, port) tuple as address to assign show method to.
        base_url: Base url path as string. Used mostly when server is running behind a proxy.
        use_relative_links: Use relative links for what's returned to client. Otherwise have absolute links.

    Returns:
        None.
    """
    from .dashboard import AppRunner

    if this.app_runner is not None:
        log.info("Stopping previous app runner at {0}".format(this.app_addr))
        shutdown_show_server()
        this.app_runner = None

    log.info("Create app runner at {0}".format(addr))
    this.app_runner = AppRunner(
        addr, base_url=base_url, use_relative_links=use_relative_links
    )
    this.app_runner.start()
    this.app_addr = this.app_runner.ip, this.app_runner.port

    return None


def _get_integer_key(key, explanation):
    if key is not None and not isinstance(key, int):
        series = explanation.selector[explanation.selector.columns[0]]
        if key not in series.values:  # pragma: no cover
            raise ValueError("Key {} not in explanation's selector".format(key))
        key = series[series == key].index[0]

    return key


def show(explanation, key=-1, **kwargs):
    """ Provides an interactive visualization for a given explanation(s).

    The visualization provided is not preserved when the notebook exits.

    Args:
        explanation: As provided in 'show'.
        key: As provided in 'show'.

    Returns:
        None.
    """

    try:
        # Get explanation key
        key = _get_integer_key(key, explanation)

        # Set default render if needed
        if this.visualize_provider is None:
            this.visualize_provider = AutoVisualizeProvider()

        # Render
        this.visualize_provider.render(explanation, key=key, **kwargs)
    except Exception as e:  # pragma: no cover
        log.error(e, exc_info=True)
        raise e

    return None


def show_link(explanation, share_tables=None):
    """ Provides the backing URL link behind the associated 'show' call for explanation.

    Args:
        explanation: Either a scalar Explanation or list of Explanations
                     that would be provided to 'show'.
        share_tables: Boolean or dictionary that dictates if Explanations
                      should all use the same selector as provided to 'show'.
                      (table used for selecting in the Dashboard).

    Returns:
        URL as a string.
    """
    # Initialize server if needed
    if this.app_runner is None:  # pragma: no cover
        init_show_server(this.app_addr)

    # Register
    this.app_runner.register(explanation, share_tables=share_tables)

    try:
        url = this.app_runner.display_link(explanation)
        return url
    except Exception as e:  # pragma: no cover
        log.error(e, exc_info=True)
        raise e


def preserve(explanation, selector_key=None, file_name=None, **kwargs):
    """ Preserves an explanation's visualization for Jupyter cell, or file.

    If file_name is not None the following occurs:
    - For Plotly figures, saves to HTML using `plot`.
    - For dataframes, saves to HTML using `to_html`.
    - For strings (html), saves to HTML.
    - For Dash components, fails with exception. This is currently not supported.

    Args:
        explanation: An explanation.
        selector_key: If integer, treat as index for explanation. Otherwise, looks up value in first column, gets index.
        file_name: If assigned, will save the visualization to this filename.
        **kwargs: Kwargs which are passed to the underlying render/export call.

    Returns:
        None.
    """
    if this._preserve_provider is None:
        this._preserve_provider = PreserveProvider()

    try:
        # Get explanation key
        key = _get_integer_key(selector_key, explanation)

        this._preserve_provider.render(
            explanation, key=key, file_name=file_name, **kwargs
        )
        return None
    except Exception as e:  # pragma: no cover
        log.error(e, exc_info=True)
        raise e
