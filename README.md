
# Bot Telegram

This is a Python-based Telegram bot. Follow the instructions below to set up the environment and run the bot.

## Prerequisites

- Python 3.x installed on your machine
- `virtualenv` installed (you can install it using `pip install virtualenv` if you haven't already)

## Setup

1. **Clone the Repository**

   First, clone this repository to your local machine using Git:

   ```bash
   git clone https://github.com/ashkhfi/bot-telegram.git
   ```

2. **Create a Virtual Environment**

   Navigate to the project directory and create a virtual environment:

   ```bash
   cd bot-telegram
   virtualenv venv
   ```

3. **Activate the Virtual Environment**

   - On **Windows**, run:

     ```bash
venv/Scripts/activate.bat
     ```

   - On **Linux/macOS**, run:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   Install the required dependencies from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Program**

   Once all dependencies are installed, you can run the bot:

   ```bash
   python main.py
   ```

## Notes

- Make sure to add your bot token and other configuration details in the appropriate files (e.g., `.env` file or configuration script).
- To deactivate the virtual environment when you're done, simply run:

   ```bash
   deactivate
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
