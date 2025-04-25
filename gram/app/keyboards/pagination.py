import math
from typing import Any, Dict, List, Optional
from uuid import uuid4

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

class PaginatedKeyboard:
    """Minimalistic paginator class."""

    def __init__(
        self,
        data: List[InlineKeyboardButton | Dict[str, Any]],
        router: Router,
        per_page: int = 10,
        per_row: int = 8,
        pagination_buttons: List[Optional[str]] = ["⏪", "⬅️", "➡️", "⏩"], 
        additional_buttons: List[List[InlineKeyboardButton | Dict[str, Any]]] = None,
    ):
        if not isinstance(data, list):
            raise TypeError("Data must be a list.")
        if not data:
            raise ValueError("Data must not be empty.")
        if not all(isinstance(i, (InlineKeyboardButton, dict)) for i in data):
             raise TypeError("All items in data must be InlineKeyboardButton or dict.")
        if per_page <= 0:
            raise ValueError("Items per page must be positive.")
        if per_row <= 0:
            raise ValueError("Items per row must be positive.")
        if len(pagination_buttons) != 4:
             raise ValueError("Pagination buttons list must contain exactly 4 elements (str or None).")

        self.data = data
        self.router = router
        self.per_page = per_page
        self.per_row = per_row
        self.pagination_buttons_text = pagination_buttons
        self.additional_buttons_list = additional_buttons or []
        self.pagination_key = uuid4().hex
        self.total_pages = math.ceil(len(self.data) / self.per_page)
        self.paginator_exists = self.total_pages > 1

        if self.paginator_exists:
            self._register_handler()

    def _build_keyboard(self, current_page: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        start_index = (current_page - 1) * self.per_page
        end_index = start_index + self.per_page
        page_data = self.data[start_index:end_index]

        buttons_to_add = []
        for item in page_data:
            if isinstance(item, InlineKeyboardButton):
                buttons_to_add.append(item)
            else:
                buttons_to_add.append(InlineKeyboardButton(**item))
        builder.row(*buttons_to_add, width=self.per_row)

        if self.paginator_exists:
            pagination_row = []
            if current_page > 1 and self.pagination_buttons_text[0]:
                pagination_row.append(
                    InlineKeyboardButton(text=self.pagination_buttons_text[0], callback_data=f"{self.pagination_key}:1")
                )
            if current_page > 1 and self.pagination_buttons_text[1]:
                pagination_row.append(
                    InlineKeyboardButton(text=self.pagination_buttons_text[1], callback_data=f"{self.pagination_key}:{current_page - 1}")
                )
            pagination_row.append(
                InlineKeyboardButton(text=f"{current_page}/{self.total_pages}", callback_data="pass")
            )
            if current_page < self.total_pages and self.pagination_buttons_text[2]:
                pagination_row.append(
                    InlineKeyboardButton(text=self.pagination_buttons_text[2], callback_data=f"{self.pagination_key}:{current_page + 1}")
                )
            if current_page < self.total_pages and self.pagination_buttons_text[3]:
                pagination_row.append(
                    InlineKeyboardButton(text=self.pagination_buttons_text[3], callback_data=f"{self.pagination_key}:{self.total_pages}")
                )
            if pagination_row:
                 builder.row(*pagination_row)

        if self.additional_buttons_list:
            for row in self.additional_buttons_list:
                buttons_in_row = []
                for button_data in row:
                    if isinstance(button_data, InlineKeyboardButton):
                         buttons_in_row.append(button_data)
                    else:
                         buttons_in_row.append(InlineKeyboardButton(**button_data))
                if buttons_in_row:
                    builder.row(*buttons_in_row)

        return builder.as_markup()

    async def _callback_handler(self, call: CallbackQuery):
        try:
            _, page_str = call.data.split(":")
            if page_str == "pass": 
                await call.answer()
                return
            target_page = int(page_str)
        except (ValueError, TypeError):
            await call.answer("Invalid page data!")
            return

        if 0 < target_page <= self.total_pages:
            markup = self._build_keyboard(target_page)
            try:
                await call.message.edit_reply_markup(reply_markup=markup)
            except TelegramBadRequest as e:
                
                if "message is not modified" not in str(e).lower():
                    print(f"Error editing markup: {e}") 
            await call.answer()
        else:
             await call.answer("Invalid page number.")


    def _register_handler(self):
        self.router.callback_query.register(
            self._callback_handler,
            F.data.startswith(self.pagination_key + ":"),
        )

    def as_markup(self, start_page: int = 1) -> InlineKeyboardMarkup:
        if not (0 < start_page <= self.total_pages):
             start_page = 1
        return self._build_keyboard(start_page)
