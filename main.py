import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from app.Controllers.Main.Main.MainController import main_router
from app.Controllers.Auth.Register.RegisterController import register_router
from app.Controllers.Auth.Login.LoginController import login_router
from app.Controllers.Auth.Logout.LogoutController import logout_router
from app.Controllers.Coins.CoinController import coin_router
from app.Controllers.Balance.BalanceController import balance_router
from app.Controllers.Bids.Index.IndexBidController import bid_router
from app.Controllers.Bids.CRUD.StoreBidController import store_bid_router
from app.Controllers.Bids.Index.IndexUserBidController import user_bid_router
from app.Controllers.Bids.CRUD.DeleteBidController import delete_bid_router
from app.Controllers.Bids.Payment.AskBidController import ask_bid_router
from app.Controllers.Bids.Payment.ResponseBidController import response_bid_route
from app.Controllers.Bids.Payment.PayBidController import pay_bid_router
from app.Controllers.Bids.Payment.CompleteBidController import complete_bid_router
from app.Controllers.Bids.Payment.CancelBidController import cancel_bid_router
from app.Controllers.Balance.SecretController import secret_router
from app.Controllers.Main.Help.HelpController import help_router

load_dotenv()

token = os.getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher()


async def main():
    dp.include_router(main_router)
    dp.include_router(register_router)
    dp.include_router(login_router)
    dp.include_router(logout_router)
    dp.include_router(coin_router)
    dp.include_router(balance_router)
    dp.include_router(bid_router)
    dp.include_router(store_bid_router)
    dp.include_router(user_bid_router)
    dp.include_router(delete_bid_router)
    dp.include_router(ask_bid_router)
    dp.include_router(response_bid_route)
    dp.include_router(pay_bid_router)
    dp.include_router(complete_bid_router)
    dp.include_router(cancel_bid_router)
    dp.include_router(secret_router)
    dp.include_router(help_router)

    await bot.delete_webhook()
    await dp.start_polling(bot)


async def bot_send_message(chat_id, text):
    await bot.send_message(chat_id, text)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())