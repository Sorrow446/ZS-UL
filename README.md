# ZS-UL
CLI Zippyshare uploader written in Python.   
**People have been seen selling my tools. DO NOT buy them. My tools are free and always will be.**   
[Windows binaries](https://github.com/Sorrow446/ZS-UL/releases)    
Download from Zippyshare with [ZS-DL](https://github.com/Sorrow446/ZS-DL).
![](https://i.imgur.com/r1t2wpe.png)

```
 _____ _____     _____ __
|__   |   __|___|  |  |  |
|   __|__   |___|  |  |  |__
|_____|_____|   |_____|_____|

usage: zs-ul.py [-h] -p PATHS [PATHS ...] [--private] [--proxy PROXY]
                [-o OUTPUT] [-w] [-t TEMPLATE] [-r {0,1,2,3,4,5}]

optional arguments:
  -h, --help            show this help message and exit
  -p PATHS [PATHS ...], --paths PATHS [PATHS ...]
                        Paths to look in for files to upload. Files in
                        subfolders will also be included.
  --private             Set uploaded files to private.
  --proxy PROXY         HTTPS only. <IP>:<port>.
  -o OUTPUT, --output OUTPUT
                        Path of text file to write URLs to. Customizable with
                        the template arg.
  -w, --wipe            Wipe output text file before writing to it.
  -t TEMPLATE, --template TEMPLATE
                        Output text file template. Vars: file_url, filename,
                        file_path.
  -r {0,1,2,3,4,5}, --retries {0,1,2,3,4,5}
                        How many times to re-attempt failed uploads. Default =
                        0.
  ```
# Usage
Upload all of the files in `E:\Linux ISOs` and `F:\More Linux ISOs`, then write the output to `G:\out.txt` with the default template.   
`zs-ul_x64.exe/zs-ul.py -p "E:\Linux ISOs" "F:\More Linux ISOs" -o G:\out.txt`

G:\out.txt:
```
E:\Linux ISOs\test_upload.zip.001
https://www18.zippyshare.com/v/HQcMt6r3/file.html
E:\Linux ISOs\test_upload.zip.002
https://www21.zippyshare.com/v/LXqPz2r9/file.html
E:\Linux ISOs\New folder\test_upload.zip
https://www21.zippyshare.com/v/EKoSe0p2/file.html
F:\More Linux ISOs\test_upload.zip.001
https://www15.zippyshare.com/v/IZcXt63m/file.html
F:\More Linux ISOs\test_upload.zip.002
https://www15.zippyshare.com/v/PPaKt72i/file.html
```
You can configure the output with the `-t` arg. `{file_path}\n{file_url}\n` was used here.   
ZS-UL will also include all files inside of subfolders (see the third path above).
