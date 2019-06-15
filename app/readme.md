# Pattern Recognition Server

This is the magic Python webserver that supports the Pattern Recognition app.

Pattern Recognition is part of my MA thesis, more of which here:  http://www.tide-pool.ca/master-of-arts-thesis/

## Deploying to AWS
(As a note to my future self:  the easiest way to run this on AWS is with nginx and a `proxy_pass`.)

## DNS

DNS is handled via Dreamhost and `tide-pool.link`, e.g. `http://tide-pool.link/pattern-rec/analysis`

## Local Testing
Run `python app.py`, and then call the `pattern-rec/validate/<classification>` endpoints, e.g.  `pattern-rec/validate/piano`
