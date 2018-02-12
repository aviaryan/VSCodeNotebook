<a name="docs"></a>
# Table of Contents

:one: [Requirements](#rq)  
:two: [Getting Started](#gs)  
:three: [Accessing your notes](#ac)  
:four: [Encrypting your notes](#en)  
:five: [Note taking features](#nt)  
:six: [Changing SublimeNotebook password](#cp)  
:seven: [Customizing which folders are encrypted](#custen)  
:eight: [Automatic git backups](#git)  
:nine: [Setting up better Markdown highlighting in Sublime Text](#mdext)  
:keycap_ten: [FAQ](#faq)  


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

Whenever you want to open your VSCode Notebook, you can use the switch project shortcut (Cmd-Ctrl-P or Ctrl-Alt-P) and select `notebook.sublime-project` to switch to the Notebook project.

![Project Selector](https://user-images.githubusercontent.com/4047597/35473121-4556dd7a-03a1-11e8-8c3a-6e85592d5d5f.png)

PS - To open SublimeNotebook from commandline, see [this section](#subl-cli).


<a name="en"></a>
## :four: Encrypting your notes
:point_up_2: [[back to top](#docs)]

To encrypt or decrypt notes, you use the `manager.py` file located in the notebook root. It runs in Python 3 and requires no additional dependencies.
I recommend changing the first line of the file to point to your interpreter.

```python
#!/Users/aviaryan/miniconda3/bin/python
```

To run `manager.py`, you can use the shortcut Ctrl-B (Cmd-B on OSX) to launch a terminal window in the `manager.py`'s directory.

Then use `python manager.py` or `./manager.py` to run the script.

When it runs for the first time, it will find the notes and ask you a password for encryption.
After getting the password, it will encrypt all [non-public notes](#custen) using that password.

![first time encryption](https://user-images.githubusercontent.com/4047597/35779481-b09abd92-09f3-11e8-8dee-accbf5a64581.png)

In the subsequent runs, `manager.py` will work as an un-locker where it will ask password to decrypt the notes and then pause its execution.
Now you can view and edit your notes and then later on encrypt them again by entering 'e' in the prompt.

![second run](https://user-images.githubusercontent.com/4047597/35779488-dc1046cc-09f3-11e8-8773-ae66da8325c4.png)


<a name="nt"></a>
## :five: Note taking features
:point_up_2: [[back to top](#docs)]

* To search through all your notes, use the Sublime Text’s search in project feature (Ctrl-Shift-F or Cmd-Shift-F).

* You can use the Sublime Text sidebar to view your notes in a hierarchical fashion.

* Store the folder in Dropbox, Google Drive or Box to have it on all your computers (as well as secure a backup).

* The Python 3 script uses no extra dependencies so you can run the script out-of-the-box on any system that has Python installed (popular Linux distros and Macs for example have it by default).


<a name="cp"></a>
## :six: Changing SublimeNotebook password
:point_up_2: [[back to top](#docs)]

To change password of your Sublime Notebook, decrypt your existing notes using old `manager.py`, then exit the script in decrypted state (using "d").

Then start `manager.py` again to re-encrypt your notes. This time you will be asked for a new password to encrypt your notes.

![changing password](https://user-images.githubusercontent.com/4047597/35779512-310e70a4-09f4-11e8-9298-4243ae3fe04d.png)


<a name="custen"></a>
## :seven: Customizing which folders are encrypted
:point_up_2: [[back to top](#docs)]

To customize which folders are encrypted, use the `settings.json` file in `sublime_notebook/` directory.

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

To enable git backups, enable the feature from `sublime_notebook/settings.json`.

```json
{
    "do_git_backup": true,
}
```

Once this setting is enabled, you will have to make your notebook a git repository and set `notebookbackup` branch to the git remote you want to backup to.
Start with an empty remote repository to avoid any conflicts.

```sh
# pwd is the directory with manager.py and sublime_notebook/ folder.
$ git init
$ git remote add notebookbackup <GIT_REMOTE_URL>
# ^ ssh git url preferred
```

The git backup will run when you re-encrypt after decrypting the notebook.

![git backup](https://user-images.githubusercontent.com/4047597/35779595-e2e04022-09f5-11e8-8fb6-2e808b29cdb6.png)

To change how frequently git backup happens, change the `git_push_interval_minutes` value in `settings.json`.

```js
{
    "git_push_interval_minutes": 1440,
}
```

1440 minutes means 24 hours i.e. 1 day. Set it to `0` to enable instant backups.


<a name="mdext"></a>
## :nine: Setting up better Markdown highlighting in Sublime Text
:point_up_2: [[back to top](#docs)]

* Install the packages from here.

	* [Sublime Markdown Extended](https://github.com/jonschlinkert/sublime-markdown-extended)
	* [Sublime Monokai Extended](https://github.com/jonschlinkert/sublime-monokai-extended) - companion to the first package.

* Make Sublime Markdown Extended as default language for markdown.

> Navigate through the following menus in Sublime Text: View -> Syntax -> Open all with current extension as... -> Markdown Extended

* Make Sublime Monokai Extended default theme for Markdown extended. Open `Settings - Syntax Specific` from preferences and update the file as follows.

```js
{
	"color_scheme": "Packages/Monokai Extended/Monokai Extended.tmTheme",
	"extensions":
	[
		"md"
	]
}
```

![sublime monkai](https://camo.githubusercontent.com/e5112e65510eada23f8cdc306ba46bfe1043f201/68747470733a2f2f662e636c6f75642e6769746875622e636f6d2f6173736574732f3338333939342f3732363833332f30666465306431362d653133382d313165322d386533642d3864626663393132323465372e706e67)

<a name="faq"></a>
## :keycap_ten: FAQ
:point_up_2: [[back to top](#docs)]

* Only *.txt and *.md files are detected as notes.

* You don't need to be in decrypted state to create a new note. Even when in encrypted state, you can create a note. When `manager.py` starts decrypting the notes, this new file will be ignored and will be encrypted when it's time to encrypt. 

<a name="subl-cli"></a>
* **Open SublimeNotebook from commandline:** You can open a Sublime Text project from the command line with `subl --project path/to/your/project`, provided that you set up the `subl` command on your system ([see the official Sublime Text documentation](https://www.sublimetext.com/docs/3/osx_command_line.html)). You might want to set up an alias to open your notebook project. Also check out other command line options listed in the [unofficial documentation for Sublime Text](http://docs.sublimetext.info/en/latest/command_line/command_line.html).
