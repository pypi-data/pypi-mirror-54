from typing import DefaultDict
from typing import List

from robinhood.lib.marketplace.equity import Equity
from robinhood.lib.marketplace.optionchain import OptionChain
from robinhood.lib.marketplace.optioninstrument import OptionInstrument
from report.symbolhistory.symbolhistoryevent import SymbolHistoryEvent


class SymbolDataPackage(object):
    
    def __init__(
        self,
        symbol: str,
        equity: Equity,
        option_chain: OptionChain,
        events: List[SymbolHistoryEvent],
    ) -> None:
        self._symbol = symbol
        self._equity = equity
        self._option_chain = option_chain
        self._events = events

    def get_option_instruments(self) -> DefaultDict[str, List[OptionInstrument]]:
        return self._option_chain.get_option_instruments_multiple_exp_dates(
            expiration_dates=self._option_chain.expiration_dates,
        )

    def update(self) -> None:
        for option_type in {'call', 'put'}:
            option_instruments = self._option_chain.get_option_instruments_multiple_exp_dates(
                expiration_dates=self._option_chain.expiration_dates,
                option_type=option_type,
            )

            for exp_date, option_instruments in option_instruments.items():
                for option_instrument in option_instruments:
                    market_data = option_instrument.market_data
                    if market_data is None:
                        continue

                    epc = market_data.get_expected_price_change(
                        underlying_price=self._equity.last_price,
                        days=3,
                    )

                    print(exp_date, option_instrument.symbol, epc)
