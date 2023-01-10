<h2>Description</h2>
<p>The Jakarta Multipart parser in Apache Struts 2 2.3.x before 2.3.32 and 2.5.x before 2.5.10.1 has incorrect exception handling and error-message generation during file-upload attempts, which allows remote attackers to execute arbitrary commands via a crafted Content-Type, Content-Disposition, or Content-Length HTTP header, as exploited in the wild in March 2017 with a Content-Type header containing a #cmd= string.</p>

<h2>Goal</h2>
<p>Find/create a python script allowing the remote attacker to execute arbitrary commands via a Content-Type HTTP header</p>
<p>try to get "ls -l" for example</p>

<h2>Solution</h2>
<details>
    <summary>Spoilers! (click to expand)</summary>
    <p>1 - </p>
    <p>Download the exploit script on the attacker machine here :</p>
    <p>cve-2017-5638/exploit.py at master · jrrdev/cve-2017-5638 (github.com)</p>
    <p></p>
    <p>2-</p>
    <p>Run the python exploit script from the attacker machine :</p>
    <p>python exploit.py http://<DOCKER_HOST>:8080/hello "ls -l"</p>
    <p></p>
</details>
