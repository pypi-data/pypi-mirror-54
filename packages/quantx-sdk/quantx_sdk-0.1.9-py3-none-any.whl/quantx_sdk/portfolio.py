import pandas as pd
from quantx_sdk.util import Util


class Portfolio:
    """
    ポートフォリオを管理します。
    """
    def __init__(self, engineVersion, portfolio):
        self._engineVersion = engineVersion
        self.portfolio = portfolio

    def summary(self):
        """サマリーを取得します。

        Returns
        -------
        dict
        """
        latest = self.portfolio["latest"].copy()
        del latest["positions"]
        del latest["open_order_list"]
        del latest["complete_order_list"]
        return latest

    def positions(self):
        """ポジションを取得します。

        Returns
        -------
        pandas.DataFrame
        """
        latest = self.portfolio["latest"]
        columns = [
            # "symbol",
            "total_entry_price",
            "value",
            "amount",
            "position_ratio",
            "entry_price",
            "exit_price",
            "max_returns",
            "returns",
            "portfolio_ratio",
            "total_exit_price",
            "pnl",
        ]
        df = pd.DataFrame.from_dict(latest["positions"], orient="index")

        # for backward compatibility
        df = df.rename(columns={"total_buy_price": "total_entry_price",
                                "total_sell_price": "total_exit_price",
                                "buy_price": "entry_price",
                                "sell_price": "exit_price"})
        df = df.ix[:,columns]
        df = Util.convert_df(df, date_columns=[], number_columns=df.columns)
        return df

    def orders(self):
        """取引履歴を取得します。

        Returns
        -------
        pandas.DataFrame
        """
        latest = self.portfolio["latest"]
        if self._engineVersion == "maron-0.0.1b":
            data = [o for o in reversed(latest["open_order_list"])]
            data.extend([o for o in reversed(latest["complete_order_list"])])
            for row in data:
                row.append({})

            columns = [
                "symbol", "ordered_at", "completed_at", "completed_price",
                "amount", "comission", "comment", "order_params"
            ]

            df = pd.DataFrame(data, columns=columns)
            df = Util.convert_df(
                df,
                date_columns=["ordered_at", "completed_at"],
                number_columns=["completed_price", "amount", "comission"])
            df["status"] = "close"
            df["order_type"] = "market_close"
            df.loc[df["completed_price"].isnull(), "status"] = "open"
            return df
        else:
            data = [o for o in reversed(latest["open_order_list"])]
            data.extend([o for o in reversed(latest["complete_order_list"])])
            # maron-0.0.5 or later
            columns = [
                "symbol",
                "order_type",
                "ordered_at",  # "signal_date",
                "completed_at",  # "trade_date",
                "completed_price",
                "amount",
                "comission",
                "comment",
                "order_params"
            ]

            df = pd.DataFrame(data, columns=columns)
            df = Util.convert_df(
                df,
                date_columns=["ordered_at", "completed_at"],
                number_columns=["completed_price", "amount", "comission"],
            )
            df["status"] = "close"
            df.loc[df["completed_price"].isnull(), "status"] = "open"
            df.loc[df["order_type"] == 1, "order_type"] = "market_close"
            df.loc[df["order_type"] == 2, "order_type"] = "market_open"
            df.loc[df["order_type"] == 3, "order_type"] = "limit"
            return df

    def trends(self):
        """トレンドを取得します。

        Returns
        -------
        pandas.DataFrame
        """
        dates = self.portfolio["dates"]
        columns = [
            "date", "portfolio_cumulative_return",
            "benchmark_cumulative_return"
        ]
        data = []
        for i, v in enumerate(dates):
            data.append([
                v,
                self.portfolio["portfolio_cumulative_returns"][i],
                self.portfolio["benchmark_cumulative_returns"][i],
            ])
        df = pd.DataFrame(data, columns=columns)
        df = Util.convert_df(
            df,
            date_columns=["date"],
            number_columns=[
                "portfolio_cumulative_return",
                "benchmark_cumulative_return",
            ],
        )
        df = df.set_index("date")
        return df
