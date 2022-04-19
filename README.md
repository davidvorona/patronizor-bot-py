# patronizor-bot

**NOTE: The python version of this bot is deprecated, and will no longer be updated. Please refer to the [TypeScript rewrite](https://github.com/davidvorona/patronizor-bot) for the most up-to-date version with support for slash commands.**

A Discord bot that treats people as they should be treated.

## Setup

1. Clone the app locally

```
git clone https://github.com/davidvorona/patronizor-bot.git
```

2. Install `discord.py` package

```
pip install -U discord.py
```

*For help setting up a `venv`, refer to: https://discordpy.readthedocs.io/en/stable/intro.html#virtual-environments*

3. Add `auth.json` to the project root. It should look like this:

```
{
    "token": "YOUR_TOKEN"
}
```

4. Create an empty `data/` directory in the project root

## Usage

1. Run the bot

```
PYTHON_PATH bot.py
```
