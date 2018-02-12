<a name="docs"></a>
# Table of Contents

:one: [Requirements](#rq)  
:two: [Getting Started](#gs)  
:three: [Accessing your notes](#ac)  
:four: [Encrypting your notes](#en)  
:five: [Note taking features](#nt)  
:six: [Changing Notebook password](#cp)  
:seven: [Customizing which folders are encrypted](#custen)  
:eight: [Automatic git backups](#git)  
:nine: [FAQ](#faq)  


<a name="rq"></a>
## :one: Requirements
:point_up_2: [[back to top](#docs)]

The requirements for using this tool are as follows. Make sure to have them installed before proceeding to the next section.

* [Visual Studio Code](https://code.visualstudio.com/)
* Python 3
* [Optional] A cloud sync application setup (Dropbox, Google Drive, OneDrive etc)


<a name="gs"></a>
## :two: Getting started
:point_up_2: [[back to top](#docs)]

The first step is downloading the release (`VSCodeNotebook_vX.Y.zip`) from https://github.com/aviaryan/VSCodeNotebook/releases/latest.

Then you extract the zip file and put the contents in a cloud synced or local folder of your choice.

Done! You can now create any number of notes in that folder. For hierarchy, you can use folders and sub-folders.

Notes can be `txt` or `md` files and they will be encrypted with your password.

By default, only `diary` folder (if it exists) is encrypted. You can learn more about changing this setting [here](#custen).

![How a VSCode Notebook looks like](https://user-images.githubusercontent.com/4047597/36103351-24210400-1035-11e8-9a33-4eeed64473fe.png)


<a name="ac"></a>
## :three: Accessing your notes
:point_up_2: [[back to top](#docs)]

To access your notes, we will use the Workspace feature of VSCode.

Open VSCode and click on "Open Workspace" in the File menu.

Browse for the `notebook.code-workspace` file in the folder you downloaded and open it. Now open the Explorer (View -> Explorer). You will see all your notes presented there with the hierarchy.

Whenever you want to open your VSCode Notebook, you can use the [Open Recent feature](https://code.visualstudio.com/docs/editor/multi-root-workspaces#_opening-workspace-files) (Ctrl-R) and select `notebook (workspace)` to switch to your VSCode notebook.

![Open Recent](https://user-images.githubusercontent.com/4047597/36104189-4f75759e-1037-11e8-9528-ae6fb841a93d.png)


<a name="en"></a>
## :four: Encrypting your notes
:point_up_2: [[back to top](#docs)]

To encrypt or decrypt notes, you use the `manager.py` file located in the notebook root. It runs in Python 3 and requires no additional dependencies.
I recommend changing the first line of the file to point to your interpreter.

```python
#!/Users/aviaryan/miniconda3/bin/python
```

> You can also change the "command" in `.vscode/tasks.json`. You might need to change it to something like "python3 manager.py" if you are a Windows user.

To run `manager.py`, you can use the shortcut Ctrl-Shift-B (Cmd-Shift-B on OSX) to show the console with `manager.py` running.

When it runs for the first time, it will find the notes and ask you a password for encryption.
After getting the password, it will encrypt all [non-public notes](#custen) using that password.

![first time encryption](https://user-images.githubusercontent.com/4047597/36105242-1e228484-103a-11e8-8739-66e735e09825.png)

In the subsequent runs, `manager.py` will work as an un-locker where it will ask password to decrypt the notes and then pause its execution.
Now you can view and edit your notes and then later on encrypt them again by entering 'e' in the prompt.

![second run](https://user-images.githubusercontent.com/4047597/36105306-48d096e4-103a-11e8-9b29-8e22f0b3dabc.png)


<a name="nt"></a>
## :five: Note taking features
:point_up_2: [[back to top](#docs)]

* To search through all your notes, use the VSCode’s find all feature (Ctrl-Shift-F or Cmd-Shift-F).

* You can use the VSCode explorer to view your notes in a hierarchical fashion.

* Store the folder in Dropbox, Google Drive or Box to have it on all your computers (as well as secure a backup).

* The Python 3 script uses no extra dependencies so you can run the script out-of-the-box on any system that has Python installed (popular Linux distros and Macs for example have it by default).


<a name="cp"></a>
## :six: Changing Notebook password
:point_up_2: [[back to top](#docs)]

To change password of your Notebook, decrypt your existing notes using old `manager.py` (Ctrl-Shift-B or Cmd-Shift-B), then exit the script in decrypted state (using "d").

Then start `manager.py` again to re-encrypt your notes. This time you will be asked for a new password to encrypt your notes.

![leave decrypted](https://user-images.githubusercontent.com/4047597/36106585-ca9d1eba-103d-11e8-9228-e9d969453c46.png)

![encrypt again](https://user-images.githubusercontent.com/4047597/36106587-cadfb9a0-103d-11e8-97ff-fefce2b8c672.png)


<a name="custen"></a>
## :seven: Customizing which folders are encrypted
:point_up_2: [[back to top](#docs)]

To customize which folders are encrypted, use the `settings.json` file in `vscode_notebook/` directory.

1. "private_folders" are the one that are encrypted.
2. "public_folders" are not encrypted.

A folder by default is public if it is not included in either of them.

You can also use the "*" symbol to select all folders. For example, in the following `settings.json` file, all folders except "web_links" are private(encrypted).

```json
{
    "private_folders": [
        "*"
    ],
    "public_folders": [
        "web_links"
    ]
}
```

**NOTE** - You should edit `settings.json` file only when the notebook is in a decrypted state. Changing it when notebook is encrypted can cause
unintentional side-effects. `"is_encrypted": false` will be present in `settings.json` when notebook is decrypted.


<a name="git"></a>
## :eight: Automatic git backups
:point_up_2: [[back to top](#docs)]

> This feature comes in handy for those who don't trust cloud data storage providers. You can even use this as a second backup for your data. I personally have auto git backups set up so that my notes are stored on both Dropbox and GitHub.

To enable git backups, enable the feature from `vscode_notebook/settings.json`.

```json
{
    "do_git_backup": true,
}
```

Once this setting is enabled, you will have to make your notebook a git repository and set `notebookbackup` branch to the git remote you want to backup to.
Start with an empty remote repository to avoid any conflicts.

```sh
# pwd is the directory with manager.py and vscode_notebook/ folder.
$ git init
$ git remote add notebookbackup <GIT_REMOTE_URL>
# ^ ssh git url preferred
```

The git backup will run when you re-encrypt after decrypting the notebook.

![git backup](https://user-images.githubusercontent.com/4047597/36108087-ec5be960-1041-11e8-9558-23b8e457134a.png)

To change how frequently git backup happens, change the `git_push_interval_minutes` value in `settings.json`.

```js
{
    "git_push_interval_minutes": 1440,
}
```

1440 minutes means 24 hours i.e. 1 day. Set it to `0` to enable instant backups.


<a name="faq"></a>
## :nine: FAQ
:point_up_2: [[back to top](#docs)]

* Only *.txt and *.md files are detected as notes.

* You don't need to be in decrypted state to create a new note. Even when in encrypted state, you can create a note. When `manager.py` starts decrypting the notes, this new file will be ignored and will be encrypted when it's time to encrypt. 
