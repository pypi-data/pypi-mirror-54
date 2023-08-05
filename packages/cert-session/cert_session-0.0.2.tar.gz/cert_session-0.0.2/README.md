# Cert Session

## Background

http://westside-consulting.blogspot.com/2019/10/certsession.html

## Summary

This package provides an object, **CertSession**,
based on [requests](https://github.com/psf/requests/blob/master/requests/sessions.py).session
that takes an alternate issuer certificate
or issuer certificates collection as its single argument.
Subsequent http requests made with this object will use both the given issuer certificate collection
as well as the certificate collection provided by **certifi**.

## Installation

    pip install cert_session

## Usage

    from certsession import Session
    session = Session('/path/to/my-root-certificates.pem')
    response = session.get('https://my-web-service/...')
    assert response.status_code == 200
