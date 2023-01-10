<h2>Description</h2>
<p>MultipartStream.java in Apache Commons FileUpload before 1.3.1, as used in Apache Tomcat, JBoss Web, and other products, allows remote attackers to cause a denial of service (infinite loop and CPU consumption) via a crafted Content-Type header that bypasses a loop's intended exit conditions.</p>

<h2>Goal</h2>
<p>DOS the apache website http://Dockerhost:8080/hello</p>

<h2>Solution</h2>
<details>
    <summary>Spoilers! (click to expand)</summary>
    <p>Start the docker container :</p>
    <p>docker run -d -p 8080:8080 jrrdev/cve-2014-0050:latest</p>
    <p></p>
    <p>Download the exploit script on the attacker machine here</p>
    <p></p>
    <p>Run the python exploit script from the attacker machine :</p>
    <p></p>
    <p>python exploit.py http://<DOCKER_HOST>:8080/hello</p>
    <p></p>
    <p>Monitor CPU usage :-)</p>
</details>
