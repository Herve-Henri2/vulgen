<h2>Description</h2>
<p>The Format String exploit occurs when the submitted data of an input string is evaluated as a command by the application. In this way, the attacker could execute code, read the stack, or cause a segmentation fault in the running application, causing new behaviors that could compromise the security or the stability of the system.</p>

<h2>Goal</h2>
<p>You need to read flag.txt with the binary.</p>

<h2>Solution</h2>
<details>
    <summary>Spoilers! (click to expand)</summary>
    <p>* Test what is possible to do with %s and %x</p>
    <p>* Idea for a python script that can read the flag from the binary results when you input several %x : b"".join([ pwn.p32(int(x,16)) for x in "".split(" ") ])	(separate each "%x" with a space</p>
    <p></p>
</details>
