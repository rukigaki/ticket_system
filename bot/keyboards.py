from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Create", callback_data="create"),
                                                  InlineKeyboardButton(text="Delete", callback_data="delete")],

                                                 [InlineKeyboardButton(text="Get", callback_data="get"),
                                                  InlineKeyboardButton(text="List", callback_data="list")],

                                                 [InlineKeyboardButton(text="Patch", callback_data="patch"),
                                                  InlineKeyboardButton(text="Put", callback_data="put")]])

category_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Бочок потик", callback_data="create_ticket_toilet_broke"),
                                                           InlineKeyboardButton(text="Телевизор поломался", callback_data="create_ticket_tv_broke"),
                                                           InlineKeyboardButton(text="Вернуться назад", callback_data="return_back")]])


boolean_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Yes", callback_data="pressed_yes"),
                                                          InlineKeyboardButton(text="No", callback_data="pressed_no")]])