# Sale-Nice-Device-Bot

This is a Telegram bot designed to facilitate buying and selling transactions within Telegram groups. Users can browse listings, post their own items for sale, and communicate directly with sellers.

## Features

- **User Interface**: The bot provides a user-friendly interface for browsing categories, viewing listings, and posting items for sale.
- **Category Filtering**: Users can filter listings by category to find relevant items more easily.
- **Image Support**: Users can upload images of items they want to sell, making listings more visually appealing.
- **Contact Integration**: The bot integrates with Telegram's contact feature, allowing users to easily share their contact information when posting listings.
- **Statistics**: Administrators have access to statistical data on user activity, sales, and more.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up your Telegram bot token, group ID, admin IDs, session name, API hash, API ID, and other configurations in the `config.py` file.

```python
TOKEN = 'your_telegram_bot_token'
GROUP_ID = 'your_telegram_group_id'
ADMIN_IDS = ['admin_user_id1', 'admin_user_id2']
SESSION_NAME = 'your_telegram_session_name'
API_HASH = 'your_api_hash'
API_ID = 'your_api_id'
channels = ['channel_name1', 'channel_name2']


5. Run the bot using `python main.py`.

## Usage

- Start the bot by sending the `/start` command.
- Navigate through the menu to browse categories or post items for sale.
- Follow the prompts to provide necessary information when posting a listing.
- Administrators can access additional functionalities by using the `/admin` command.


## Configuration

The bot requires certain configuration parameters to be set up before running. These parameters are stored in the `config.py` file:

- **TOKEN**: The API token generated when you create a new bot using the BotFather on Telegram.
- **GROUP_ID**: The ID of the Telegram group where the bot will operate. Make sure the bot is added as an administrator to this group.
- **ADMIN_IDS**: A list of user IDs who have administrative privileges for the bot. These users will have access to additional functionalities.
- **API_ID** and **API_HASH**: These are the API credentials required for using the Telethon library, which allows the bot to interact with Telegram's API.
- **SESSION_NAME**: The name of the session file where Telethon will store session data. This file is used to maintain the bot's authorization state.
- **channels**: A list of Telegram channel names where the bot will search for listings.

Make sure to set up these parameters correctly in the `config.py` file before running the bot.

## Telethon API

This bot utilizes the Telethon library, a Python implementation of the Telegram API. Telethon provides a convenient way to interact with Telegram's API, allowing the bot to send and receive messages, manage contacts, and perform various other actions.

To use Telethon, you need to obtain your API credentials (API ID and API hash) from the Telegram website. These credentials are required to authenticate your bot and establish a connection with Telegram's servers.

For more information on setting up Telethon and obtaining API credentials, refer to the Telethon documentation: [Telethon Documentation](https://docs.telethon.dev/en/latest/)

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For any questions or issues, please open an issue in the [issue tracker](https://github.com/your-username/telegram-marketplace-bot/issues).

## Roadmap

Future improvements and features planned for this project are listed in the [roadmap](ROADMAP.md) file.

## Acknowledgements

- Thanks to the developers of the [aiogram](https://github.com/aiogram/aiogram) library for making it easy to build Telegram bots.
- Special thanks to [Your Name] for their valuable contributions to this project.

## Contact

For any inquiries or feedback, please contact [Your Name](mailto:your.email@example.com).

