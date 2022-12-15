<h2>Description</h2>
<p>The IoTGoat Project is a deliberately insecure firmware based on OpenWrt and maintained by OWASP as a platform to educate software developers and security professionals with testing commonly found vulnerabilities in IoT devices.</p>
<p></p>
<p>An IoTGoat machine is currently being emulated in a machine deployed on the network. The ssh port of IoTGoat is open and has been forwarded to the port 8022 of its host machine through NAT.</p>
<p>You have access to the firmware image of the IoTGoat machine.</p>

<h2>Goal</h2>
<p>Access to the IoTGoat machine using a ssh connection.</p>

<h2>Solution</h2>
<details>
    <summary>Spoilers! (click to expand)</summary>
    <p>1. Extract the files system using binwalk</p>
    <p>2. Find a user that can use /bin/ash</p>
    <p>3. Crack his password with a wordlist of common IoT passwords</p>
    <p>4. Connect to IotGoat using ssh through the port 8022 with the user hacked credentials</p>
    <p></p>
    <p>(reminder: ssh {user}@{ip} -p {port} -oHostKeyAlgorithms=+ssh-rsa)</p>
</details>
