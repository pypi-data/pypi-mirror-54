#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2018
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains an object that represents a Telegram SuccessfulPayment."""

from telegram import TelegramObject, OrderInfo


class SuccessfulPayment(TelegramObject):
    """This object contains basic information about a successful payment.

    Attributes:
        currency (:obj:`str`): Three-letter ISO 4217 currency code.
        total_amount (:obj:`int`): Total price in the smallest units of the currency.
        invoice_payload (:obj:`str`): Bot specified invoice payload.
        shipping_option_id (:obj:`str`): Optional. Identifier of the shipping option chosen by the
            user.
        order_info (:class:`telegram.OrderInfo`): Optional. Order info provided by the user.
        telegram_payment_charge_id (:obj:`str`): Telegram payment identifier.
        provider_payment_charge_id (:obj:`str`): Provider payment identifier.

    Args:
        currency (:obj:`str`): Three-letter ISO 4217 currency code.
        total_amount (:obj:`int`): Total price in the smallest units of the currency (integer, not
            float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp
            parameter in currencies.json, it shows the number of digits past the decimal point for
            each currency (2 for the majority of currencies).
        invoice_payload (:obj:`str`): Bot specified invoice payload.
        shipping_option_id (:obj:`str`, optional): Identifier of the shipping option chosen by the
            user.
        order_info (:class:`telegram.OrderInfo`, optional): Order info provided by the user
        telegram_payment_charge_id (:obj:`str`): Telegram payment identifier.
        provider_payment_charge_id (:obj:`str`): Provider payment identifier.
        **kwargs (:obj:`dict`): Arbitrary keyword arguments.

    """

    def __init__(self,
                 currency,
                 total_amount,
                 invoice_payload,
                 telegram_payment_charge_id,
                 provider_payment_charge_id,
                 shipping_option_id=None,
                 order_info=None,
                 **kwargs):
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id

        self._id_attrs = (self.telegram_payment_charge_id, self.provider_payment_charge_id)

    @classmethod
    def de_json(cls, data, bot):
        if not data:
            return None

        data = super(SuccessfulPayment, cls).de_json(data, bot)
        data['order_info'] = OrderInfo.de_json(data.get('order_info'), bot)

        return cls(**data)
