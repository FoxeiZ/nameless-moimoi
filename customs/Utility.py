import logging
from typing import Callable, Tuple, Type, Optional
from urllib.parse import quote_plus as qp, urlparse

import discord
from discord.ext import commands

import config

__all__ = ["Utility"]


class Utility:
    """
    List of utilities that aid the further developments of this project.
    """

    @staticmethod
    def get_db_url(
        config_cls: Optional[Type[config.Config]] = None,
    ) -> Tuple[str, str, str, str, str, str, str, str]:
        """
        Get the database connection URL based on the config and its components.
        :param config_cls: The class used to retrieve config. Defaults to config.Config.
        :return: Database connection URL
        """
        if hasattr(config_cls, "DATABASE") and (db := config_cls.DATABASE):
            dialect = db["dialect"]
            driver = qp(f"+{db['driver']}", safe="+") if db["driver"] else ""
            username = db["username"] if db["username"] else ""
            password = qp(f":{db['password']}", safe=":") if db["password"] else ""
            at = qp("@", safe="@") if username and password else ""
            host = db["host"]
            port = qp(f":{db['port']}", safe=":") if db["port"] else ""
            db_name = db["db_name"]

            return (
                f"{dialect}{driver}://{username}{password}{at}{host}{port}/{db_name}",
                dialect,
                driver,
                username,
                password,
                host,
                port,
                db_name,
            )

        logging.warning("Using SQLite database as fallback method")
        return (
            "sqlite:///nameless.db",
            "",
            "",
            "",
            "",
            "",
            "",
            "nameless.db",
        )

    @staticmethod
    def is_an_url(url: str) -> bool:
        return urlparse(url).netloc != ""

    @staticmethod
    def message_waiter(ctx: commands.Context) -> Callable[[discord.Message], bool]:
        """
        Message waiter to use with Client.wait_for("message", ...).

        Usages:
            message: discord.Message = await bot.wait_for("message", check=wait_for)

        :param ctx: Current context.
        :return: The waiter function.
        """

        def message_checker(message: discord.Message) -> bool:
            return (
                message.author.id == ctx.author.id
                and ctx.channel.id == message.channel.id
            )

        return message_checker
