Conmy Api Client for Python
===================

Installation:

    pip install conomy_api_client

Usage

    from conomy_api_client import DataClient

    token = 'lalalalalalala'
    dc = DataClient(token) 

    issuers = dc.get_issurs()    # return list of issuers
