from report.symbolhistory.symboldatapackage import SymbolDataPackage
from report.symbolhistory.symbolhistory import SymbolHistory
from robinhood.lib.marketplace.equity import Equity
from robinhood.lib.marketplace.optionchain import OptionChain


def test_symbol_data_package(
    symbol: str,
    equity: Equity,
    option_chain: OptionChain,
    symbol_history: SymbolHistory,
) -> None:
    print()
    data = SymbolDataPackage(
        symbol=symbol,
        equity=equity,
        option_chain=option_chain,
        events=symbol_history.get_events(symbol=symbol),
    )
    data.update()
