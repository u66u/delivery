from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
import logging

from app.services.client.backend_client import get_me, register_or_get_user_in_backend
from app.services.client.middleware import ClientMiddleware
from app.services.client.user import UserClient
from app.keyboards import PaginatedKeyboard

logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(ClientMiddleware([UserClient]))

def get_location_keyboard():
    """Create a keyboard with a button to share location."""
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(text="Share my location", request_location=True)
        ]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

@router.message(Command("start"))
async def handle_start(message: types.Message, user: UserClient):
    """
    Handle the /start command from users.
    Extract user data from the message and register the user with the backend.
    """
    # Log the start command
    logger.info(f"User {message.from_user.id} ({message.from_user.username}) started the bot")
    
    user_info = {
        "tg_id": message.from_user.id,
        "username": message.from_user.username or "",
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name or "",
    }
    
    # Send user data to backend and receive the response
    backend_user = await user.register_or_get_user(user_info)
    
    if backend_user:
        # User successfully registered/retrieved from backend
        await message.answer(
            f"Welcome, {message.from_user.username}! \n"
            f'Your data: {backend_user}',
            reply_markup=get_location_keyboard()
        )
        
        # You can store user info in a local cache/state if needed
        # For example: user_state.set_user(message.from_user.id, backend_user)
    else:
        # Failed to register/retrieve user from backend
        await message.answer(
            "Sorry, I couldn't authenticate you with our service at the moment. "
            "Please try again later or contact support."
        ) 

@router.message(Command("me"))
async def handle_me(message: types.Message, user: UserClient):
    """
    Handle the /me command from users.
    Get user data from the backend and send it to the user.
    """
    user_info = {
        "tg_id": message.from_user.id,
        "username": message.from_user.username or "",
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name or "",
    }
    me_data = await user.get_me()
    if me_data:
        await message.answer(
            f'Your data: {me_data}'
        )
    else:
        await message.answer(
            "Sorry, I couldn't get your data from the backend. "
            "Please try again later or contact support."
        )

@router.message(Command("location"))
async def handle_location(message: types.Message):
    """
    Handle the /location command.
    Prompts the user to share their location.
    """
    await message.answer(
        "Please share your location by clicking the button below:",
        reply_markup=get_location_keyboard()
    )

@router.message(Command("paginaton"))
async def keyboard_pagination_with_additional_buttons(message: Message):
    buttons = [
        InlineKeyboardButton(text=f"Button {i}", callback_data=f"button_{i}")
        for i in range(1, 31) # 30 items
    ]
    additional_buttons = [
        [ # First row of additional buttons
            InlineKeyboardButton(text="Info ℹ️", callback_data="info"),
            {"text": "Help ❓", "callback_data": "help"} # Can mix types
        ],
        [ # Second row
            InlineKeyboardButton(text="Go back 🔙", callback_data="go_back"),
        ]
    ]

    paginator = PaginatedKeyboard(
        data=buttons,
        router=router,
        additional_buttons=additional_buttons,
        per_page=10,
        per_row=1,
    )

    await message.answer(
        text="Pagination with additional buttons:",
        reply_markup=paginator.as_markup(),
    )

@router.callback_query(F.data.startswith("item_") | F.data.startswith("button_"))
async def handle_item_click(call: CallbackQuery):
    item_id = call.data.split("_")[-1]
    await call.answer(f"You clicked Item {item_id}")

@router.callback_query(F.data.in_({"info", "help", "go_back"}))
async def handle_additional_button_click(call: CallbackQuery):
    action = call.data
    await call.answer(f"You clicked: {action.capitalize()}")

# @router.message()
# async def handle_location_received(message: types.Message):
#     """
#     Handle location data when a user shares their location.
#     """
#     location = message.location
#     logger.info(
#         f"Received location from user {message.from_user.id}: "
#         f"Latitude: {location.latitude}, Longitude: {location.longitude}"
#     )
    
#     # Here you can send this data to your backend if needed
#     # For now, just acknowledge receipt
#     await message.answer(
#         f"Thank you for sharing your location!\n"
#         f"Latitude: {location.latitude}\n"
#         f"Longitude: {location.longitude}",
#         reply_markup=types.ReplyKeyboardRemove()
#     )