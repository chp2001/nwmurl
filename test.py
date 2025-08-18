import os, sys, json, pickle
from pathlib import Path

import datetime

# string of format:
# https://noaa-nwm-pds.s3.amazonaws.com/nwm.20250814/forcing_medium_range/nwm.t12z.medium_range.forcing.f001.conus.nc

test_file = Path("dist/examples.txt")
test_text = test_file.read_text()
test_list = test_text.splitlines()
# print("Test list:", test_list)
# Unravel the list into dates, forecast cycles, and lead times
first_item = test_list[0]
first_item_parts = first_item.split("/")
print("First item parts:", first_item_parts)
date_part = first_item_parts[3]
var_part = first_item_parts[5]
var_part_parts = var_part.split(".")
cycle_part = var_part_parts[1]
lead_time_part = var_part_parts[4]
date = date_part[4:]
date = datetime.datetime.strptime(date, "%Y%m%d")
cycle = cycle_part[1:3]
cycle = int(cycle)
lead_time = lead_time_part[1:]
lead_time = int(lead_time)
print("Date:", date)
print("Cycle:", cycle)
print("Lead time:", lead_time)
# Set the hour of the date to the cycle hour
ref_date = date.replace(hour=cycle)
print("Updated Date:", ref_date)
target_date = ref_date + datetime.timedelta(hours=lead_time)
print("Target Date:", target_date)


def get_url_parts(url):
    """
    Extracts the date, cycle, and lead time from a URL formatted like:
    https://noaa-nwm-pds.s3.amazonaws.com/nwm.20250814/forcing_medium_range/nwm.t12z.medium_range.forcing.f001.conus.nc
    """
    parts = url.split("/")
    date_part = parts[3]
    var_part = parts[5]
    var_part_parts = var_part.split(".")
    cycle_part = var_part_parts[1]
    lead_time_part = var_part_parts[4]

    date = date_part[4:]
    date = datetime.datetime.strptime(date, "%Y%m%d")
    cycle = cycle_part[1:3]
    cycle = int(cycle)
    lead_time = lead_time_part[1:]
    lead_time = int(lead_time)

    return date, cycle, lead_time


def get_ref_and_target_date_from_string(s):
    """
    Extracts reference and target dates from a string formatted like:
    https://noaa-nwm-pds.s3.amazonaws.com/nwm.20250814/forcing_medium_range/nwm.t12z.medium_range.forcing.f001.conus.nc
    """
    # parts = s.split("/")
    # date_part = parts[3]
    # var_part = parts[5]
    # var_part_parts = var_part.split(".")
    # cycle_part = var_part_parts[1]
    # lead_time_part = var_part_parts[4]

    # date = date_part[4:]
    # date = datetime.datetime.strptime(date, "%Y%m%d")
    # cycle = cycle_part[1:3]
    # cycle = int(cycle)
    # lead_time = lead_time_part[1:]
    # lead_time = int(lead_time)

    # ref_date = date.replace(hour=cycle)
    # target_date = ref_date + datetime.timedelta(hours=lead_time)

    # return ref_date, target_date
    date, cycle, lead_time = get_url_parts(s)
    ref_date = date.replace(hour=cycle)
    target_date = ref_date + datetime.timedelta(hours=lead_time)
    return ref_date, target_date


# Example usage
ref_date, target_date = get_ref_and_target_date_from_string(first_item)
print("Reference Date:", ref_date)
print("Target Date:", target_date)

# Generate a list of dates from the test_list
date_list = []
for item in test_list:
    if len(item) < 10:
        continue
    ref_date, target_date = get_ref_and_target_date_from_string(item)
    date_list.append((ref_date, target_date))
print("Date List:")
for ref, target in date_list:
    print(f"Reference Date: {ref}, Target Date: {target}")
import matplotlib.pyplot as plt

# Plotting the reference and target dates
ref_dates = [d[0] for d in date_list]
target_dates = [d[1] for d in date_list]
plt.figure(figsize=(10, 5))
plt.plot(ref_dates, label="Reference Dates", marker="o")
plt.plot(target_dates, label="Target Dates", marker="x")
# Put a horizontal line at 202508150100
plt.axhline(
    y=datetime.datetime(2025, 8, 15, 1, 0),
    color="r",
    linestyle="--",
    label="2025-08-15 01:00",
)
plt.xlabel("Index")
plt.ylabel("Date")
plt.title("Reference and Target Dates from Test List")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("dist/date_plot.png")
# plt.show()


# Trying to interpolate between date 15 and 17
date_parts = []
for item in test_list:
    if len(item) < 10:
        continue
    date_parts.append(get_url_parts(item))
print("Date parts:")
for date_part in date_parts:
    print(date_part)

date_segment1 = date_parts[0:15]
lastpart = date_segment1[-1]
lastdate = lastpart[0]
lastcycle = lastpart[1]
lastleadtime = lastpart[2]
new_date_segment = []
for i in range(0, 204 - len(date_segment1)):
    newleadtime = lastleadtime + i + 1
    new_date_segment.append((lastdate, lastcycle, newleadtime))

date_segments_for_interpolation = date_segment1 + new_date_segment

interpolated_dates = []
for date_part in date_segments_for_interpolation:
    ref_date = date_part[0].replace(hour=date_part[1])
    target_date = ref_date + datetime.timedelta(hours=date_part[2])
    interpolated_dates.append((ref_date, target_date))

ref_dates_2 = [d[0] for d in interpolated_dates]
target_dates_2 = [d[1] for d in interpolated_dates]
plt.figure(figsize=(10, 5))
plt.plot(ref_dates_2, label="Interpolated Reference Dates", marker="o")
plt.plot(target_dates_2, label="Interpolated Target Dates", marker="x")
# Put a horizontal line at 202508150100
plt.axhline(
    y=datetime.datetime(2025, 8, 15, 1, 0),
    color="r",
    linestyle="--",
    label="2025-08-15 01:00",
)
plt.xlabel("Index")
plt.ylabel("Date")
plt.title("Interpolated Reference and Target Dates")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("dist/interpolated_date_plot.png")
# plt.show()

from typing import (
    List,
    Tuple,
    Dict,
    Set,
    Any,
    Union,
    Callable,
    Literal,
    Optional,
    TypeAlias,
    TypedDict,
)

forcing_medium_range_lead_times: List[int] = list(range(1, 241, 1))  # 1 to 240 hours
forcing_short_range_lead_times: List[int] = list(range(1, 19, 1))  # 1 to 18 hours


def fix_basic_product_args(
    ref_date: Union[str, datetime.datetime],
    forecast_cycle: Union[List[int], int] = 0,
    lead_time: Union[List[int], int] = 1,
) -> Tuple[datetime.datetime, List[int], List[int]]:
    """
    Fix the arguments for generating basic product targets.

    :param ref_date: Reference date as a string or datetime object.
    :param forecast_cycle: Forecast cycle as an integer or list of integers.
    :param lead_time: Lead time as an integer or list of integers.
    :return: Tuple containing reference date as datetime, forecast cycle as list of integers, and lead time as list of integers.
    """
    if isinstance(ref_date, str):
        # string expected to be in format 'YYYYMMDDhhmm' or 'YYYYMMDD'
        if len(ref_date) == 8:
            ref_date = datetime.datetime.strptime(ref_date, "%Y%m%d")
        elif len(ref_date) == 12:
            ref_date = datetime.datetime.strptime(ref_date, "%Y%m%d%H%M")
    elif not isinstance(ref_date, datetime.datetime):
        raise ValueError(
            "ref_date must be a string in 'YYYYMMDD' or 'YYYYMMDDhhmm' format or a datetime object."
        )

    if isinstance(forecast_cycle, int):
        forecast_cycle = [forecast_cycle]
    if isinstance(lead_time, int):
        lead_time = [lead_time]

    if not isinstance(forecast_cycle, list) or not isinstance(lead_time, list):
        raise ValueError(f"forecast_cycle and lead_time must be lists or integers. Got {type(forecast_cycle)} and {type(lead_time)}.")

    if not all(isinstance(fc, int) for fc in forecast_cycle):
        exceptions = set(type(fc) for fc in forecast_cycle if not isinstance(fc, int))
        raise ValueError(f"All elements in forecast_cycle must be integers. Found types: {exceptions}.")

    if not all(isinstance(lt, int) for lt in lead_time):
        exceptions = set(type(lt) for lt in lead_time if not isinstance(lt, int))
        raise ValueError(f"All elements in lead_time must be integers. Found types: {exceptions}.")

    return ref_date, forecast_cycle, lead_time


def gen_basic_target_product(
    ref_date: Union[str, datetime.datetime],
    forecast_cycle: Union[List[int], int] = 0,
    lead_time: Union[List[int], int] = 1,
) -> List[Tuple[datetime.datetime, int, int]]:
    """
    Generate a list of tuples containing reference date, forecast cycle, and lead time.

    :param ref_date: Reference date as a string or datetime object.
    :param forecast_cycle: Forecast cycle as an integer or list of integers.
    :param lead_time: Lead time as an integer or list of integers.
    :return: List of tuples with reference date, forecast cycle, and lead time.
    """
    ref_date, forecast_cycle, lead_time = fix_basic_product_args(
        ref_date, forecast_cycle, lead_time
    )

    target_products = []
    for fc in forecast_cycle:
        for lt in lead_time:
            # The url builder ignores the hour of the reference date:
            # hour is handled only through forecast_cycle and lead_time
            base_target_date = ref_date.replace(hour=0)
            target_products.append((base_target_date, fc, lt))

    return target_products

test_args_from_jordan = {
    "forcing_type" : "operational_archive", # Not used in this example
    "start_date"   : "202508150100",
    "end_date"     : "202508150100", # Given that function is only for a single datetime, this is not relevant
    "fcst_cycle"   : [0], # One single cycle
    "lead_time"    : forcing_medium_range_lead_times,
    "varinput"     : 5, # varinput = 5 means 'forcing'
    "geoinput"     : 1, # 'geoinput' = 1 means 'conus'
    "runinput"     : 2, # 'runinput' = 2 means 'medium_range'
    "urlbaseinput" : 7, # 'urlbaseinput' = 7 means 'https://noaa-nwm-pds.s3.amazonaws.com/'
    "meminput"     : 3, # 'meminput' = 3 means referencing 'member 3' of the ensemble
}

test_base_products = gen_basic_target_product(
    ref_date=test_args_from_jordan["start_date"],
    forecast_cycle=test_args_from_jordan["fcst_cycle"],
    lead_time=test_args_from_jordan["lead_time"],
)
print("Test Base Products:", f"({len(test_base_products)} products)")
printnum = 8
for product in test_base_products[0:printnum]:  # Print first 5 products
    print(product)
if len(test_base_products) > printnum:
    print("...", f"({len(test_base_products) - printnum} more products)")
    print(test_base_products[-1])  # Print last product
    
def refresh_fc_day(
    fc: int,
    cur_date: datetime.datetime,
    verbose: bool = False,
)-> Tuple[int, datetime.datetime]:
    """
    Ensure the forecast cycle is aligned with the day.
    Adjusts the forecast cycle and date if necessary.
    
    :param fc: Current forecast cycle.
    :param cur_date: Current date.
    :return: Tuple containing the adjusted forecast cycle and date.
    """
    def vlog(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)
    if fc < 0:
        # Adjust the date backward
        cur_date -= datetime.timedelta(days=1)
        fc = (fc + 24) % 24  # Wrap around the cycle
        vlog(f"Adjusting date backward: {cur_date}, new fc: {fc}")
    elif fc >= 24:
        # Adjust the date forward
        cur_date += datetime.timedelta(days=1)
        fc = fc % 24  # Wrap around the cycle
        vlog(f"Adjusting date forward: {cur_date}, new fc: {fc}")
    else:
        vlog(f"No date adjustment needed: {cur_date}, new fc: {fc}")
    
    return fc, cur_date
    
def refresh_fc_step(
    fc: int,
    forecast_step: int = 6,
    verbose: bool = False,
)->Tuple[int, int]:
    """
    Ensure the forecast cycle is aligned with the forecast step.
    Adjusts the forecast cycle if necessary.
    
    :param fc: Current forecast cycle.
    :param forecast_step: Valid forecast cycle step in hours.
    :return: Tuple containing the adjusted forecast cycle and potential remainder.
    """
    def vlog(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)
    if fc % forecast_step != 0:
        # Adjust the forecast cycle to align with the forecast step
        remainder = fc % forecast_step
        fc = (fc // forecast_step) * forecast_step
        vlog(f"Adjusting forecast cycle: new fc: {fc}, remainder: {remainder}")
    else:
        remainder = 0
        vlog(f"No forecast cycle adjustment needed: {fc} (forecast_step: {forecast_step})")
    return fc, remainder
    
    
    
def offset_product_tuple_forecast(
    product_tuple: Tuple[datetime.datetime, int, int],
    offset_hours: int = 0,
    # valid forecast cycle step in hours. Would result in [0, 6, 12, 18] for a 6-hour cycle
    forecast_step: int = 6, 
    verbose: bool = False
) -> Tuple[datetime.datetime, int, int]:
    """
    Offset the product tuple by a specified number of hours with the forecast cycle.
    Lead time is adjusted when the offset does not align with the forecast cycle step.
    Either forward or backward in time.

    :param product_tuple: Tuple containing (reference date, forecast cycle, lead time).
    :param offset_hours: Number of hours to offset.
    :param forecast_step: Valid forecast cycle step in hours.
    :return: New tuple with the updated values.
    
    :Example:
    
    >>> offset_product_tuple((datetime.datetime(2025, 8, 15, 0, 0), 18, 3), offset_hours=6)
    (datetime.datetime(2025, 8, 16, 7, 0), 0, 3)
    """
    def vlog(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)
    ref_date, fc, lt = product_tuple
    # ref_date's hour is irrelevant for making the url, so we can ignore it
    # and just use the date part. mostly.
    cur_date: datetime.datetime = ref_date
    vlog(f"Original product tuple: {product_tuple}, offset_hours: {offset_hours}, forecast_step: {forecast_step}")
    # Adjust the fc
    fc = fc + offset_hours
    fc, cur_date = refresh_fc_day(fc, cur_date, verbose=verbose)
    fc, remainder = refresh_fc_step(fc, forecast_step=forecast_step, verbose=verbose)
    lt = lt + remainder
    vlog(f"Adjusted product tuple: ({cur_date}, {fc}, {lt})")
    # Return the new product tuple with the updated date
    return (cur_date, fc, lt)

def offset_product_tuple_lead_time(
    product_tuple: Tuple[datetime.datetime, int, int],
    offset_hours: int = 0,
    forecast_step: int = 6,
    verbose: bool = False
) -> Tuple[datetime.datetime, int, int]:
    """
    Offset the product tuple by a specified number of hours with the lead time.
    The forecast cycle will adjust to prevent <= 0 lead time.

    :param product_tuple: Tuple containing (reference date, forecast cycle, lead time).
    :param offset_hours: Number of hours to offset.
    :return: New tuple with the updated values.
    
    :Example:
    
    >>> offset_product_tuple((datetime.datetime(2025, 8, 15, 0, 0), 18, 3), offset_hours=6)
    (datetime.datetime(2025, 8, 15, 0, 0), 18, 9)
    """
    def vlog(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)
    ref_date, fc, lt = product_tuple
    vlog(f"Original product tuple: {product_tuple}, offset_hours: {offset_hours}")
    # Adjust the lead time
    new_lt = lt + offset_hours
    if new_lt <= 0:
        num_steps_below_zero = (-new_lt + forecast_step) // forecast_step
        vlog(f"Lead time is non-positive ({new_lt}), adjusting by {num_steps_below_zero} steps of {forecast_step} hours.")
        ref_date, fc, lt = offset_product_tuple_forecast(
            product_tuple,
            offset_hours=-num_steps_below_zero * forecast_step,
            forecast_step=forecast_step,
            verbose=verbose
        )
        new_lt = new_lt + num_steps_below_zero * forecast_step
        vlog(f"Adjusted product tuple: ({ref_date}, {fc}, {new_lt})")
        # If lead time is now positive, we can return the adjusted date and cycle
        if new_lt > 0:
            return (ref_date, fc, new_lt)
    else:
        # If lead time is positive, we can just return the original date and cycle
        return (ref_date, fc, new_lt)
    
if __name__ == "__main__":
    # test the offset function
    test_product = (datetime.datetime(2025, 8, 15, 0, 0), 18, 6)
    print("Original product:", test_product)
    offset_product = offset_product_tuple_forecast(test_product, offset_hours=3)
    print("Offset product:", offset_product)
    
def get_target_date_from_product_tuple(
    product_tuple: Tuple[datetime.datetime, int, int],
) -> datetime.datetime:
    """
    Get the target date from a product tuple.
    
    :param product_tuple: Tuple containing (reference date, forecast cycle, lead time).
    :return: Target date as a datetime object.
    """
    ref_date, fc, lt = product_tuple
    # The url builder ignores the hour of the reference date:
    # hour is handled only through forecast_cycle and lead_time
    base_target_date = ref_date.replace(hour=0)
    target_date = base_target_date + datetime.timedelta(hours=fc + lt)
    return target_date
    
    
if __name__ == "__main__":
    mem3_offset = 12
    fulcrum_date = datetime.datetime(2025, 8, 15, 1, 0)
    offsetted_base_products = []
    # for product in test_base_products[5:6]:
    for product in test_base_products:
        # offsetted_product = adjust_product_tuple_backwards_around_fulcrum_date(
        #     product,
        #     fulcrum_date=fulcrum_date,
        #     adjustment_hours=mem3_offset,
        #     # verbose=True
        # )
        offsetted_product = offset_product_tuple_lead_time(
            product,
            offset_hours=-mem3_offset,
            forecast_step=6,  # Assuming a 6-hour forecast step
            # verbose=True
        )
        offsetted_base_products.append(offsetted_product)
    print("Offsetted Base Products:", f"({len(offsetted_base_products)} products)")
    printnum = 13
    for product in offsetted_base_products[0:printnum]:  # Print first 5 products
        print(product)
    if len(offsetted_base_products) > printnum:
        print("...", f"({len(offsetted_base_products) - printnum} more products)")
        print(offsetted_base_products[-1])
        
        
# Need to make simple version of the offset_product_tuple_lead_time function that has no dependencies
# so that it can be used in the url builder without circular imports
def simple_product_offsetter(
    target_date: datetime.datetime,
    fc: int,
    lt: int,
    offset_hours: int,
    forecast_step: int = 6,
) -> Tuple[datetime.datetime, int, int]:
    """
    Offset the product tuple by a specified number of hours with the lead time.
    The forecast cycle will adjust to prevent <= 0 lead time.
    :param target_date: Target date as a datetime object.
    :param fc: Forecast cycle as an integer.
    :param lt: Lead time as an integer.
    :param offset_hours: Number of hours to offset.
    :param forecast_step: Valid forecast cycle step in hours.
    :return: New tuple with the updated values.
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


if __name__ == "__main__":
    # test the simple offset function
    mem3_offset = 12
    simple_offsetted_base_products: List[Tuple[datetime.datetime, int, int]] = []
    # for product in test_base_products[5:6]:
    for product in test_base_products:
        # print("Original product:", product)
        offset_product = simple_product_offsetter(
            target_date=product[0],
            fc=product[1],
            lt=product[2],
            offset_hours=-mem3_offset,
            forecast_step=6,  # Assuming a 6-hour forecast step
        )
        # print("Simple Offset product:", offset_product)
        simple_offsetted_base_products.append(offset_product)
    print("Simple Offsetted Base Products:", f"({len(simple_offsetted_base_products)} products)")
    printnum = 13
    for product in simple_offsetted_base_products[0:printnum]:  # Print first 5 products
        print(product)
    if len(simple_offsetted_base_products) > printnum:
        print("...", f"({len(simple_offsetted_base_products) - printnum} more products)")
        print(simple_offsetted_base_products[-1])
        
    simple_dates = [] # (ref_date, target_date)
    for product in simple_offsetted_base_products:
        ref_date, fc, lt = product
        reference_date = ref_date.replace(hour=fc)
        target_date = reference_date + datetime.timedelta(hours=lt)
        simple_dates.append((reference_date, target_date))
    plt.figure(figsize=(10, 5))
    simple_ref_dates = [d[0] for d in simple_dates]
    simple_target_dates = [d[1] for d in simple_dates]
    plt.plot(simple_ref_dates, label="Simple Offset Reference Dates", marker="o")
    plt.plot(simple_target_dates, label="Simple Offset Target Dates", marker="x")
    # Put a horizontal line at 202508150100
    plt.axhline(
        y=datetime.datetime(2025, 8, 15, 1, 0),
        color="r",
        linestyle="--",
        label="2025-08-15 01:00",
    )
    plt.xlabel("Index")
    plt.ylabel("Date")
    plt.title("Simple Offset Reference and Target Dates")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("dist/simple_offsetted_date_plot.png")
    # plt.show()
        
    # Compare the two offsetted lists to find any differences
    differences = []
    for original, simple in zip(offsetted_base_products, simple_offsetted_base_products):
        if original != simple:
            differences.append((original, simple))
    if differences:
        print("Differences found between the two offset methods:")
        for orig, simp in differences:
            print(f"Original: {orig}, Simple: {simp}")
        print(f"Total differences: {len(differences)}")
    else:
        print("No differences found between the two offset methods.")
        
        
# Next step is to make a self contained function to pull the values from any(?) url

# Critical part of the url creation process that follows immediately after the prefix: 
# f"nwm.{date.strftime('%Y%m%d')}"
# So we can split off the beginning of the url by finding the date part, then use familiar patterns
# to extract the cycle and lead time from the rest of the url.
from re import search as re_search
def harvest_from_url(
    url: str,
)->Tuple[Tuple[datetime.datetime, int, int], str]:
    """
    Extract the reference date, forecast cycle, and lead time from a URL.
    
    :param url: URL string to extract information from.
    :return: Tuple containing (reference date, forecast cycle, lead time) and the URL with the values replaced with placeholders (e.g., {date}, {cycle}, {lead_time}).
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
    url_with_placeholders = url.replace(
        f"nwm.{date_str}",
        "nwm.{date:%Y%m%d}"
    ).replace(
        f".t{cycle:02d}z.",
        ".t{cycle:02d}z."
    ).replace(
        f".f{lead_time:03d}.",
        ".f{lead_time:03d}."
    )
    return (date, cycle, lead_time), url_with_placeholders

if __name__ == "__main__":
    # Test the harvest_from_url function
    test_url = "https://noaa-nwm-pds.s3.amazonaws.com/nwm.20250814/forcing_medium_range/nwm.t12z.medium_range.forcing.f001.conus.nc"
    (date, cycle, lead_time), url_with_placeholders = harvest_from_url(test_url)
    print(f"Extracted Date: {date}, Cycle: {cycle}, Lead Time: {lead_time}")
    print(f"URL with placeholders: {url_with_placeholders}")
    print("Reconstructed URL:", url_with_placeholders.format(date=date, cycle=cycle, lead_time=lead_time))