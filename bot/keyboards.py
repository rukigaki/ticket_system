from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Create", callback_data="create"),
                                                  InlineKeyboardButton(text="Delete", callback_data="delete")],

                                                 [InlineKeyboardButton(text="Get", callback_data="get"),
                                                  InlineKeyboardButton(text="List", callback_data="list")],

                                                 [InlineKeyboardButton(text="Patch", callback_data="patch"),
                                                  InlineKeyboardButton(text="Put", callback_data="put")]])