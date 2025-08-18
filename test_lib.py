from typing import (
    Tuple,
    TypeAlias,
)
import datetime
from re import search as re_search

product_tuple_type: TypeAlias = Tuple[datetime.datetime, int, int]


def harvest_from_url(
    url: str,
) -> Tuple[product_tuple_type, str]:
    """Extract the reference date, forecast cycle, and lead time from a URL.
    Args:
        url (str): URL string to extract information from.
    Returns:
        Tuple[Tuple[datetime.datetime, int, int], str]: A tuple containing:
            - A tuple with the reference date as a datetime object, forecast cycle as an integer,
              and lead time as an integer.
            - The URL with the date, cycle, and lead time replaced with placeholders.
    """
    url_match = re_search(r"nwm\.(\d{8})", url)
    if not url_match:
        raise ValueError(f"URL does not contain a valid date: {url}")
    date_str = url_match.group(1)
    date = datetime.datetime.strptime(date_str, "%Y%m%d")
    cycle_match = re_search(r"\.t(\d{2})z.", url)
    if not cycle_match:
        raise ValueError(f"URL does not contain a valid cycle: {url}")
    cycle = int(cycle_match.group(1))
    lead_time_match = re_search(r"\.f(\d{3})\.", url)
    if not lead_time_match:
        raise ValueError(f"URL does not contain a valid lead time: {url}")
    lead_time = int(lead_time_match.group(1))
    # Create a new URL with placeholders
    url_with_placeholders = (
        url.replace(f"nwm.{date_str}", "nwm.{date:%Y%m%d}")
        .replace(f".t{cycle:02d}z.", ".t{cycle:02d}z.")
        .replace(f".f{lead_time:03d}.", ".f{lead_time:03d}.")
    )
    return (date, cycle, lead_time), url_with_placeholders

# harvest_from_url should be able to parse all of the source URLs produced by
# the urlgennwm.py script
# To rebuild the URL from the tuple and the template, use:
# url = url_template.format(date=ref_date, cycle=fc, lead_time=lt)

def simple_product_offsetter(
    target_date: datetime.datetime,
    fc: int,
    lt: int,
    offset_hours: int,
    forecast_step: int = 6,
) -> product_tuple_type:
    """Offset the product tuple by a specified number of hours with the lead time.
    The forecast cycle will adjust to prevent <= 0 lead time.
    Args:
        target_date (datetime.datetime): Target date as a datetime object.
        fc (int): Forecast cycle as an integer.
        lt (int): Lead time as an integer.
        offset_hours (int): Number of hours to offset.
        forecast_step (int): Valid forecast cycle step in hours.
    Returns:
        result (Tuple[datetime.datetime, int, int]): New tuple with the updated values.
    """
    # No external functions used here
    new_lt = lt + offset_hours
    if new_lt <= 0:
        num_steps_below_zero = (-new_lt + forecast_step) // forecast_step
        # Adjust the target date and forecast cycle backward
        total_offset = num_steps_below_zero * forecast_step
        # target_date -= datetime.timedelta(hours=total_offset)
        fc -= total_offset
        # Wrap around the forecast cycle and adjust the date if necessary
        if fc < 0:
            days_back = (-fc + 23) // 24
            days_delta = datetime.timedelta(days=days_back)
            target_date -= days_delta
            fc = (fc + days_back * 24) % 24
        new_lt = new_lt + total_offset
    return target_date, fc, new_lt

# simple_product_offsetter is the primary function for the time lagging
# functionality. To apply a time lag like an ensemble member >1, run it
# with offset_hours = -lag_hours (e.g. -12 for member 3).
# Just ensure that the forecast_step matches the model's forecast cycle step.

def get_target_date_from_product_tuple(
    product_tuple: product_tuple_type,
) -> datetime.datetime:
    """Extract the target date from a product tuple.
    Args:
        product_tuple (Tuple[datetime.datetime, int, int]): A tuple containing the reference date,
            forecast cycle, and lead time.
    Returns:
        result (datetime.datetime): The target date calculated from the reference date,
            forecast cycle, and lead time.
    """
    ref_date, fc, lt = product_tuple
    # The url builder ignores the hour of the reference date:
    # hour is handled only through forecast_cycle and lead_time
    base_target_date = ref_date.replace(hour=0)
    target_date = base_target_date + datetime.timedelta(hours=fc + lt)
    return target_date

# get_target_date_from_product_tuple is more of an example than anything else.
# It shows how to get the target date from the product tuple.
# The 'reference date' shown in the graphs is the 'base_target_date' here, before
# the timedelta is applied.