import pandas as pd
import time
from datetime import datetime

from alerts.smart_alert_engine import (
    generate_alerts
)

from ai.institutional_ai_engine import (
    run_ai_engine
)

# =====================================================
# LIVE ENGINE
# =====================================================

class LiveMonitoringEngine:

    def __init__(
        self,
        refresh_interval=300
    ):

        self.refresh_interval = (
            refresh_interval
        )

    # =================================================
    # LOAD DATA
    # =================================================

    def load_latest_data(self):

        df = pd.read_parquet(

            "data/cache/parquet/"
            "institutional_rankings.parquet"
        )

        return df

    # =================================================
    # PROCESS LIVE DATA
    # =================================================

    def process(self):

        df = self.load_latest_data()

        df, insights = (
            run_ai_engine(df)
        )

        alerts_df = (
            generate_alerts(df)
        )

        return (
            df,
            insights,
            alerts_df
        )

    # =================================================
    # LIVE LOOP
    # =================================================

    def run(self):

        print(
            "\nLIVE INSTITUTIONAL "
            "MONITORING STARTED\n"
        )

        while True:

            try:

                print(
                    "\nRefreshing..."
                )

                df, insights, alerts = (
                    self.process()
                )

                print(
                    f"\nTimestamp: "
                    f"{datetime.now()}"
                )

                print(
                    "\nAI INSIGHTS:\n"
                )

                for insight in insights:

                    print(
                        f"• {insight}"
                    )

                print(
                    "\nALERT COUNT:"
                )

                print(len(alerts))

                time.sleep(
                    self.refresh_interval
                )

            except Exception as e:

                print(
                    f"\nLIVE ENGINE ERROR: "
                    f"{e}"
                )

                time.sleep(60)

# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":

    engine = LiveMonitoringEngine(
        refresh_interval=300
    )

    engine.run()
