from robinhood.lib.marketplace.equity import Equity


class CurrentPosition(object):

    def __init__(
        self,
        symbol: str,
        equity: Equity,
        events: List[SymbolHistoryEvent],
    ) -> None:
        self._symbol = symbol
        self._equity = equity
        self._events = events

    def get_report(self) -> str:
        if len(self._events) == 0:
            return f'No event for {self._symbol}...'

        last_event = self._events[-1]
        