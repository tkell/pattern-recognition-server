# Pattern Recognition Server

This is the magic Python webserver that supports the Pattern Recognition app.

Pattern Recognition is part of my MA thesis, more of which here:  http://www.tide-pool.ca/master-of-arts-thesis/

## Deploying to AWS
`docker build -t pattern-recognition-server .`
`docker tag pattern-recognition-server:latest 721044467845.dkr.ecr.us-west-2.amazonaws.com/pattern-recognition-server:latest`
`docker push 721044467845.dkr.ecr.us-west-2.amazonaws.com/pattern-recognition-server:latest`

- The rest is from the web UI!
- Work through https://aws.amazon.com/getting-started/tutorials/deploy-docker-containers/
- Based on this doc, a Service with one Task should be in the free tier!
- You can press `Update Service` and set the number of tasks you want to 0 or 1 or more!
- We want to link to the Load Balancer for the Service in our DNS!

## DNS
- DNS is handled via Dreamhost and `pattern-rec.tide-pool.link`, e.g. `http://pattern-rec.tide-pool.link/pattern-rec/analysis`

## Local Testing with Docker
- Build the image: `docker build -t pattern-recognition-server .`
- Run container:  `docker run -d --name prs-container -p 80:80 pattern-recognition-server`
- Test things at `http://localhost/pattern-rec/hello`
- Stop container: `docker stop prs-container`
- Delete container: `docker rm prs-container`

