# Welcome to Daily 👋

![Version](https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000) ![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> Simple CLI tool to write on the #daily slack channel and its corresponding timesheet.

## Features

- Write on Slack channel and Google Sheets simultaneously.
- Multiples projects support.
- Auto generated suggestions based on commits. 

## Install

```sh
pip3 install --user daily
```

## Usage


### Initializing

```sh
daily init
```

This is the first step. It will ask for Google Drive and Google Sheets permissions and 
your name on StriveLabs timesheet (if it's suitable).


### Creating a project

We can add a new project just by executing the following:

```sh
daily create-project <project name>
```

It will ask for a Slack API token. To get it, you need to create and Slack app and 
add it to your workspace. For more information check [this](https://api.slack.com/apps?new_app=1).

### Writing

To upload your working hours and the description just run the following:

```sh
daily write <project name>
```

It will opens your default editor with a template and some suggestions for your #daily-scrum channel.
After saving and closing the editor, a message will be send to Slack and the working hours will be written
on the corresponding timesheet. If you belongs to StriveLabs, that timesheet will be updated too.

## Author

👤 **Antonio Molner Domenech**

* Github: [@antoniomdk](https://github.com/antoniomdk)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/antoniomdk/daily-celtiberian/issues).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [Antonio Molner Domenech](https://github.com/antoniomdk).<br />
This project is [MIT](https://github.com/antoniomdk/daily-celtiberian/blob/master/LICENSE) licensed.
