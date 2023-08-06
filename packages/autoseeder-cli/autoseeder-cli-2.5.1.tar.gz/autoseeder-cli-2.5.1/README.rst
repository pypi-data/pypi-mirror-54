The autoseeder-cli tools allow you to interact easily with the
Autoseeder API to submit new URLs and check the status of existing URLs.

Installation
============

::

    pip install autoseeder_cli

Usage
=====

**Please Note:** *Only Python 3.6+ are officially supported by
autoseeder-cli. Python 2.7 will reach EOL as of the 1st of January 2020
and will not be supported.*

For each of these tools, before use you should configure the following
as environment variables:

::

      AUTOSEEDER_BASE_URL  The URL that the Autoseeder service resides at [e.g.: https://your.instance.hostname/autoseeder/]
      AUTOSEEDER_TOKEN     Token to authenticate with - recommended method

Linux/MacOS:

::

    export AUTOSEEDER_BASE_URL=https://your.instance.hostname/autoseeder/
    export AUTOSEEDER_TOKEN='35999b9065…'

Windows Powershell:

::

    $env:AUTOSEEDER_BASE_URL = "https://your.instance.hostname/autoseeder/"
    $env:AUTOSEEDER_TOKEN = "35999b9065…"

Windows Command Prompt:

::

    set AUTOSEEDER_BASE_URL=https://your.instance.hostname/autoseeder/
    set AUTOSEEDER_TOKEN=35999b9065…

Commands available:
===================

autoseeder-cli get\_token
-------------------------

Required Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  AUTOSEEDER\_USER
-  AUTOSEEDER\_PASS
-  AUTOSEEDER\_BASE\_URL

via CLI
~~~~~~~

Log in to autoseeder and obtain an API token. Note that if you've been
supplied with a token string to use already, you do not need to do this.

Linux/MacOS Command line:

::

    AUTOSEEDER_USER=josephpilgrim
    AUTOSEEDER_PASS=onthetrail
    AUTOSEEDER_BASE_URL=https://oregon.usa/autoseeder/

    export AUTOSEEDER_TOKEN=$(autoseeder-cli get_token)

via Python lib
~~~~~~~~~~~~~~

::

    import os
    import autoseeder_cli

    username = os.environ.get('AUTOSEEDER_USER')
    password = os.environ.get('AUTOSEEDER_PASS')
    base_url = os.environ.get('AUTOSEEDER_BASE_URL')

    api = autoseeder_cli.AutoseederTokenGetter(user=username, password=password, base_url=base_url) 
    print('API token: {}'.format(api.get_token()))

autoseeder-cli submit
---------------------

Required Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  AUTOSEEDER\_TOKEN
-  AUTOSEEDER\_BASE\_URL

via CLI
~~~~~~~

Submit a single URL to Autoseeder for seeding. You can optionally select
a geographic region to limit seeding activity to.

Command line:

::

    autoseeder-cli submit https://example.com/ --seed-region=AU

via Python lib
~~~~~~~~~~~~~~

::

    import os
    import autoseeder_cli

    token = os.environ.get('AUTOSEEDER_TOKEN')
    base_url = os.environ.get('AUTOSEEDER_BASE_URL')

    submitter = autoseeder_cli.AutoseederSubmitter(token=token, base_url=base_url) 
    response = submitter.submit_url('http://example.com', seed_region='AU')
    uuid = response.get('uuid')

    print('URL trackable via {}'.format(uuid))

autoseeder-cli list
-------------------

Required Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  AUTOSEEDER\_TOKEN
-  AUTOSEEDER\_BASE\_URL

via CLI
~~~~~~~

Presents a report of URLs you've submitted and their status.

You may find it helpful to filter and format the output with the `jq
tool <https://stedolan.github.io/jq/>`__.

Linux/MacOS command line:

::

    # show last 100
    autoseeder-cli list --limit 100

    # filter down with jq
    autoseeder-cli list --limit 100 | \
        jq '.[] | \
            select(.statistics != null) | \
           [ .statistics[].canoncical_url, .statistics[].status ]'

Windows command line:

.. code:: shell

    REM show last 100
    autoseeder-cli list --limit 100

    REM filter down with jq
    autoseeder-cli list --limit 100 | jq ".[]| select(.statistics != null)| [.statistics[].canonical_url, .statistics[].status]"

via Python lib
~~~~~~~~~~~~~~

::

    import os
    import autoseeder_cli

    token = os.environ.get('AUTOSEEDER_TOKEN')
    base_url = os.environ.get('AUTOSEEDER_BASE_URL')

    lister = autoseeder_cli.AutoseederLister(token=token, base_url=base_url) 
    urls = lister.get_url_list()

    for url in urls:
        print(url['url'])

autoseeder-cli find_urls
------------------------

Required Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  AUTOSEEDER\_TOKEN
-  AUTOSEEDER\_BASE\_URL

via CLI
~~~~~~~

Finds URLs matching a search term, and provides their Universally Unique
Identifiers (UUIDs) for further actions (e.g. ``view``).

Command line:

::

    autoseeder-cli find_urls 'example.com'

via Python lib
~~~~~~~~~~~~~~

::

    import os
    import autoseeder_cli

    token = os.environ.get('AUTOSEEDER_TOKEN')
    base_url = os.environ.get('AUTOSEEDER_BASE_URL')

    searcher = autoseeder_cli.AutoseederSearcher(token=token, base_url=base_url) 
    uuids = searcher.find_urls('example.com')

    for uuid in uuids:
        print(uuid)

autoseeder-cli view
-------------------

Required Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  AUTOSEEDER\_TOKEN
-  AUTOSEEDER\_BASE\_URL

via CLI
~~~~~~~

Presents a report of a single URL via its associated Universally unique
identifier (UUID) or specific URL.

Command line:

::

    # view by URL UUID
    autoseeder-cli view 2118f16a-3270-4e63-88dc-24b6097739ab  # UUID is sample only
    # partial URL string which must match only one registered URL
    autoseeder-cli view example.com/myurl

via Python lib
~~~~~~~~~~~~~~

::

    import os
    import autoseeder_cli

    # 2118f16a-3270-4e63-88dc-24b6097739ab is a SAMPLE ONLY, would map to a seeded URL you previously submitted
    viewer = autoseeder_cli.AutoseederURLView(token=token, base_url=myinstance_url)
    url_data = viewer.view('2118f16a-3270-4e63-88dc-24b6097739ab')

    for url in url_data:
        print(url['url'])

