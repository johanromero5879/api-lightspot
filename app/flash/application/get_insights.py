from app.flash.domain import FlashRepository, FlashQuery, TimeInsight, MostActivity, Year, Insight, MostPeriodOfDay
from app.flash.application import FlashesNotFoundError

MONTHS = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}


class GetInsights:
    def __init__(self, flash_repository: FlashRepository):
        self.__flash_repository = flash_repository

    async def __call__(self, query: FlashQuery, utc_offset: str) -> Insight:
        if query.date_range.start_date > query.date_range.end_date:
            raise ValueError("Start date must be before end date")

        # Query cities
        cities = await self.__flash_repository.count_by_cities(query)

        if len(cities) == 0:
            raise FlashesNotFoundError()

        insights = Insight()
        insights.total = 0

        # Query time
        insights.time = await self.get_time_insights(query, utc_offset)

        # set locations
        insights.location = dict()
        for city in cities:
            insights.total += city["total"]
            name = city["city"]

            if name:
                insights.location[name] = city["total"]

        return insights

    async def get_time_insights(self, query: FlashQuery, utc_offset: str) -> TimeInsight:

        items = await self.__flash_repository.count_yearly(query, utc_offset)

        years: dict[str, Year] = dict()
        year = None
        most_activity = MostActivity()

        for item in items:
            month = MONTHS[item["month"]]

            if str(item["year"]) != year:
                year = str(item["year"])
                years[year] = Year(months=self.get_months_dict())

            years[year].total += item["total"]
            years[year].months[month] = item["total"]

            if item["total"] > most_activity.total:
                most_activity.year = int(year)
                most_activity.month = month
                most_activity.total = item["total"]

        hours = await self.__flash_repository.count_hourly(query, utc_offset)
        periods_of_day = self.get_periods_of_day(hours)
        most_period_of_day = self.get_most_period_of_day(periods_of_day)
        hours_dict = self.get_hours(hours)

        return TimeInsight(
            most_activity=most_activity,
            years=years,
            periods_of_day=periods_of_day,
            hours=hours_dict,
            most_period_of_day=most_period_of_day
        )

    def get_months_dict(self):
        months = dict()
        for month in MONTHS.values():
            months[month] = 0

        return months

    def get_hours(self, hours: list[dict[str, int]]):
        hours_dict = dict()

        for hour in range(0, 24):
            name = self.get_normal_hour(hour)
            hours_dict[name] = 0

        for item in hours:
            name = self.get_normal_hour(item["hour"])
            hours_dict[name] = item["total"]

        return hours_dict

    def get_normal_hour(self, military_hour: int) -> str:
        if military_hour > 12 or military_hour == 0:
            hour = f"{abs(military_hour - 12)} {'am' if military_hour == 0 else 'pm'}"
        else:
            hour = f"{military_hour} am"

        return hour

    def get_periods_of_day(self, hours: list[dict[str, int]]):
        periods_of_day = {
            "Early morning": 0,
            "Morning": 0,
            "Afternoon": 0,
            "Evening": 0
        }

        for item in hours:
            if 0 <= item["hour"] < 6:
                periods_of_day["Early morning"] += item["total"]
                continue

            if 6 <= item["hour"] < 12:
                periods_of_day["Morning"] += item["total"]
                continue

            if 12 <= item["hour"] < 19:
                periods_of_day["Afternoon"] += item["total"]
                continue

            if 19 <= item["hour"] <= 23:
                periods_of_day["Evening"] += item["total"]
                continue

        return periods_of_day

    def get_most_period_of_day(self, periods_of_day: dict[str, int]) -> MostPeriodOfDay:
        times = [{"name": key, "total": value} for key, value in periods_of_day.items()]
        most_period = max(times, key=lambda time: time["total"])

        return MostPeriodOfDay(name=most_period["name"], total=most_period["total"])
