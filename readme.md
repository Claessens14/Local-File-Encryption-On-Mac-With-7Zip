
# Local File Encryption On Mac With 7-zip 

Encrypt files locally on the mac with 7-zip. The following is a python wrapper around the 7-zip encryptor/decryptor which provides the following.   
  
  - Using 'random character overwrite deletion' to automatically remove the original unencrypted file/folder after the encryption is completed. 
  - Upon successful decryption, remove the .7z file. 
  - Verify the password is entered in properly during encryption using multiple entries.
  - Clearly denote encrypted files with `ENCRYPTED` being added to the file name. Also increment the file names incase of duplicates.   
  - Password entry is in python programs stdin (not in command line which has history), and is visibly hidden during entry. 
  - Unlike other tools, everything is open source! 7-zip, the packages, this code!

### Setup 
1) Go to the official 7-zip website, download the execuatable. Or use homebrew to install 7-zip.  
2) Determine the path to the execuatabe and paste it in the `.env` file.  
```
SEVEN_ZIP_PATH=""
```
3) Install the following python packages
```
pip install getpass python-dotenv
```

### Runtime
Encryption:  
```
python encrypt.py {optional file/folder name}
```
  
Decryption:  
```
python decrypt.py {optional file/folder name}

```
### Recommendation
Test out the functionality on test files prior to running on important files.   

### Optional 
Add the encryption functionality to your `~/.zshrc` file so you can access it it anytime. 
```
encrypt() {
    python {GLOBAL PATH TO DIRECTORY}/7zip_method/encrypt.py "$@"
}
decrypt() {
    python {GLOBAL PATH TO DIRECTORY}/7zip_method/decrypt.py "$@"
}
```
Then run:  
```
source ~/.zshrc
```
Now you can type the following in your shell to access the encryption functionality
```
encrypt
  OR 
decrypt
```

### Notes
Several functions were written by chatGPT.   

In general if you see an issue or area improvement, email me (found on profile page)
