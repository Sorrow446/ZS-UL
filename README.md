# ZS-UL
CLI Zippyshare uploader written in Python. JS execution and BSoup-**FREE**.   

**People have been seen selling my tools. DO NOT buy them. My tools are free and always will be.**

![](https://orion.feralhosting.com/sorrow/share/ZS-UL.png)

# Usage
Upload a single file with a HTTPS proxy and print URL to the console:    
`ZS-UL.py -f G:\text_upload.webm -p 0.0.0.0:8080`

Upload two files and write URLs to <script path>\out.txt:    
`ZS-UL.py -f G:\text_upload.webm G:\text_upload_2.webm -o out.txt`

```
 _____ _____     _____ __
|__   |   __|___|  |  |  |
|   __|__   |___|  |  |  |__
|_____|_____|   |_____|_____|

usage: ZS-UL.py [-h] -f FILES [FILES ...] [-pv] [-p PROXY] [-o OUTPUT] [-n]

optional arguments:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
                        Paths of files to upload separated by a space.
  -pv, --private        Set uploaded files to private.
  -p PROXY, --proxy PROXY
                        HTTPS only. <IP>:<port>.
  -o OUTPUT, --output OUTPUT
                        Path of text file to write URLs to.
  -n, --no-wipe         Don't wipe output text file before writing to it.
  ```
  
