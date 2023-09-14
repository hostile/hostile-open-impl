# GHunt / Holehe API

An individual Flask webserver written in Python, separated from our core API service to facilitate the use of [GHunt](https://github.com/mxrch/GHunt) and [Holehe](https://github.com/megadose/holehe).

### Purpose

Due to the licenses used for the GHunt and Holehe projects (both of which are very
powerful OSINT frameworks, and the authors deserve a lot of respect and full credit
for their work), any project that implements their code within their own project
must be opensource.

For this reason, we've created an opensource Flask instance to provide GHunt
and Holehe's content to the rest of our services.

### Usage

1) Clone the repository
2) Execute `docker build -t hostile-open-impl .`
3) Execute `docker run hostile-open-impl`
