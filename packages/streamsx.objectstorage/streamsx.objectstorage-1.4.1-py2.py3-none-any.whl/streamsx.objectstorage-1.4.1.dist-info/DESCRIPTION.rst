Overview
========

Provides functions to read objects from Cloud Object Storage as a stream
and submit tuples to create objects in Cloud Object Storage (COS).

This package exposes the `com.ibm.streamsx.objectstorage <https://ibmstreams.github.io/streamsx.objectstorage/>`_ toolkit as Python methods for use with Streaming Analytics service on
IBM Cloud and IBM Streams including IBM Cloud Pak for Data.

* `Streaming Analytics service <https://console.ng.bluemix.net/catalog/services/streaming-analytics>`_
* `IBM Streams developer community <https://developer.ibm.com/streamsdev/>`_

Sample
======

A simple hello world example of a Streams application writing string messages to
an object. Scan for created object on COS and read the content::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema
    from streamsx.topology.context import submit
    import streamsx.objectstorage as cos

    topo = Topology('ObjectStorageHelloWorld')

    to_cos = topo.source(['Hello', 'World!'])
    to_cos = to_cos.as_string()

    # sample bucket with resiliency "regional" and location "us-south"
    bucket = 'streamsx-py-sample'
    # US-South region private endpoint
    endpoint='s3.private.us-south.cloud-object-storage.appdomain.cloud'

    # Write a stream to COS
    cos.write(to_cos, bucket, endpoint, '/sample/hw%OBJECTNUM.txt')

    scanned = cos.scan(topo, bucket=bucket, endpoint=endpoint, directory='/sample')

    # read text file line by line
    r = cos.read(scanned, bucket=bucket, endpoint=endpoint)

    # print each line (tuple)
    r.print()

    submit('STREAMING_ANALYTICS_SERVICE', topo)
    # Use for IBM Streams including IBM Cloud Pak for Data
    # submit ('DISTRIBUTED', topo)

Documentation
=============

* `streamsx.objectstorage package documentation <http://streamsxobjectstorage.readthedocs.io/>`_


