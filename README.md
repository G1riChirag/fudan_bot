# Fudan Bot

## A Discord moderation bot

Fudan is a Discord bot designed to demonstrate the implementation of a simple moderation system using Python and the Discord.py library. The bot includes features such as banning words, kicking and banning users, purging messages, and logging various server events.

### Purpose

The purpose of this project is to gain practical experience in building a moderation bot for Discord servers, focusing on best practices in terms of security such as:
* rate limiting,
* logging and auditing,
* permissions management, and
* extensive documentation.

By mastering moderation and security fundamentals within Discord servers, my personal goal is to enhance skills applicable to various server environments and broader systems security contexts.

### Usage

*Installation: Clone the repository. To install the required dependencies, using pip install discord.
*Configuration: Modify the fudan.py file to include your Discord bot token.
*Running the Bot: Execute the fudan.py file to start the bot. Ensure that the bot has the necessary permissions in your Discord server.
*Commands: Use various commands prefixed with ! to interact with the bot. See the help command for a list of available commands and their usage.

### Features

*Word Banning: Ban specific words from being used in messages.
*User Management: Kick, ban, and unban users from the server.
*Message Purging: Delete a specified number of messages from a channel.
*Voice Channel Management: Mute and unmute members in voice channels.
*Event Logging: Log message deletions, edits, role changes, channel creations, and deletions.

### Future Enhancements

* Enhanced logging: Add more detailed logging features, such as member joining, leaving, creating invite, command usuage and more.
* Customizable Configuration: Implement a configuration system to allow server administrators to customize bot behavior and settings.
* More commands: temporarily mute members from talking in the server.
* Auto moderation: Implementing a point-based warning system that automatically kicks/bans members based on how many strikes they have accumulated.
* Improved Error Handling: Enhance error handling mechanisms to provide more informative feedback to users.
* Vulnerability scanning: Develop a feature that scans messages, links, and attachments for potential vulnerabilities and malware.


### How to use this project for your own purposes

The project is a work in progress. Since this is a good starter boilerplate for a more advanced moderation bot, I'd encourage you to clone and rename this project to use for your own purposes.

### Find a bug?

Contributions to this project are welcome! If you found an issue or would like to submit an improvement to this project, feel free to fork the repository, make improvements, and submit pull requests. For major changes, please open an issue first to discuss the proposed changes.
